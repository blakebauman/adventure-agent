import type { UserPreferences, RunState, StreamEvent } from '@/types/adventure';

// Use proxy in development, direct URL in production
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.DEV ? '/api' : 'http://localhost:2024');

export class AdventureAgentClient {
  private baseUrl: string;
  private headers: Record<string, string>;

  constructor(baseUrl: string = API_BASE_URL, apiKey?: string) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.headers = { 'Content-Type': 'application/json' };
    if (apiKey) {
      this.headers['X-Api-Key'] = apiKey;
    }
  }

  async createThread(userId?: string, sessionId?: string): Promise<string> {
    const config: Record<string, any> = { configurable: {} };
    if (userId) config.configurable.user_id = userId;
    if (sessionId) config.configurable.session_id = sessionId;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

    try {
      const response = await fetch(`${this.baseUrl}/threads`, {
        method: 'POST',
        headers: this.headers,
        body: JSON.stringify({ config }),
        signal: controller.signal,
      });
      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage = `Failed to create thread: ${response.statusText}`;
        try {
          const errorJson = JSON.parse(errorText);
          errorMessage = errorJson.detail || errorJson.message || errorMessage;
        } catch {
          errorMessage = errorText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      return data.thread_id;
    } catch (error) {
      clearTimeout(timeoutId);
      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Request timed out. The server may be slow due to blocking operations.');
      }
      throw error;
    }
  }

  async createAdventurePlan(
    threadId: string,
    userInput: string,
    userPreferences?: UserPreferences
  ): Promise<{ run_id: string }> {
    const inputData: Record<string, any> = { user_input: userInput };
    if (userPreferences) {
      inputData.user_preferences = userPreferences;
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout for run creation

    try {
      const response = await fetch(
        `${this.baseUrl}/threads/${threadId}/runs`,
        {
          method: 'POST',
          headers: this.headers,
          body: JSON.stringify({
            assistant_id: 'agent',
            input: inputData,
          }),
          signal: controller.signal,
        }
      );
      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage = `Failed to create adventure plan: ${response.statusText}`;
        try {
          const errorJson = JSON.parse(errorText);
          errorMessage = errorJson.detail || errorJson.message || errorMessage;
        } catch {
          errorMessage = errorText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      return response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Request timed out. The server may be slow due to blocking operations. Please try again.');
      }
      throw error;
    }
  }

  async *streamRun(
    threadId: string,
    runId: string
  ): AsyncGenerator<StreamEvent> {
    // No timeout for streaming - let it run as long as needed
    // But add a heartbeat to detect if connection is dead
    let lastEventTime = Date.now();
    const heartbeatInterval = 60000; // 60 seconds
    
    const response = await fetch(
      `${this.baseUrl}/threads/${threadId}/runs/${runId}/stream`,
      {
        headers: this.headers,
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      let errorMessage = `Failed to stream run: ${response.statusText}`;
      try {
        const errorJson = JSON.parse(errorText);
        errorMessage = errorJson.detail || errorJson.message || errorMessage;
      } catch {
        errorMessage = errorText || errorMessage;
      }
      throw new Error(errorMessage);
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) {
      throw new Error('Response body is not readable');
    }

    let buffer = '';
    let currentEvent: { event?: string; data?: string; id?: string } = {};
    
    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        // Update heartbeat on any data
        lastEventTime = Date.now();

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmed = line.trim();
          
          // Empty line indicates end of SSE event
          if (!trimmed) {
            if (currentEvent.data) {
              try {
                const parsedData = JSON.parse(currentEvent.data);
                
                // Check if the parsed data is already in StreamEvent format
                // (has an 'event' field that matches LangChain event types)
                if (parsedData && typeof parsedData === 'object' && 'event' in parsedData) {
                  // Already a StreamEvent, use as-is
                  lastEventTime = Date.now();
                  const eventType = parsedData.event;
                  if (eventType === 'on_run_end' || eventType === 'on_chain_stream_end') {
                    console.log('Stream: Run end event detected:', eventType);
                  }
                  yield parsedData as StreamEvent;
                } else {
                  // Construct StreamEvent from SSE format
                  // Map SSE event types to StreamEvent structure
                  const event: StreamEvent = {
                    event: currentEvent.event || 'message',
                    data: parsedData,
                  };
                  lastEventTime = Date.now();
                  if (event.event === 'on_run_end' || event.event === 'on_chain_stream_end') {
                    console.log('Stream: Run end event detected (SSE format):', event.event);
                  }
                  yield event;
                }
              } catch (e) {
                // If parsing fails, skip this event but don't crash
                console.warn('Failed to parse SSE data:', e, currentEvent.data?.substring(0, 100));
              }
            }
            currentEvent = {};
            continue;
          }

          // Parse SSE field format: "field: value"
          const colonIndex = trimmed.indexOf(':');
          if (colonIndex === -1) continue;

          const field = trimmed.substring(0, colonIndex).trim();
          const value = trimmed.substring(colonIndex + 1).trim();

          if (field === 'event') {
            currentEvent.event = value;
          } else if (field === 'data') {
            // SSE data can span multiple lines - accumulate it
            if (currentEvent.data) {
              currentEvent.data += '\n' + value;
            } else {
              currentEvent.data = value;
            }
          } else if (field === 'id') {
            currentEvent.id = value;
          }
          // Ignore other fields like 'retry'
        }

        // Check for heartbeat timeout (connection might be dead)
        if (Date.now() - lastEventTime > heartbeatInterval) {
          console.warn('Stream heartbeat timeout - connection may be dead');
          // Don't break, let it try to continue
        }
      }

      // Process any remaining event in buffer
      if (currentEvent.data) {
        try {
          const parsedData = JSON.parse(currentEvent.data);
          
          // Check if the parsed data is already in StreamEvent format
          if (parsedData && typeof parsedData === 'object' && 'event' in parsedData) {
            console.log('Stream: Processing final buffered event:', parsedData.event);
            yield parsedData as StreamEvent;
          } else {
            const event: StreamEvent = {
              event: currentEvent.event || 'message',
              data: parsedData,
            };
            console.log('Stream: Processing final buffered event (SSE format):', event.event);
            yield event;
          }
        } catch (e) {
          console.warn('Failed to parse final SSE event:', e);
        }
      }
      
      console.log('Stream: Reader done, stream ended');
    } finally {
      reader.releaseLock();
    }
  }

  async getRunState(threadId: string, runId: string): Promise<RunState> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

    try {
      const response = await fetch(
        `${this.baseUrl}/threads/${threadId}/runs/${runId}/state`,
        { 
          headers: this.headers,
          signal: controller.signal,
        }
      );
      clearTimeout(timeoutId);

      if (!response.ok) {
        // 404 is acceptable - run might not exist yet or was cleaned up
        // This is normal when the backend cleans up completed runs quickly
        if (response.status === 404) {
          console.log('Run state 404 (run cleaned up) - this is normal for completed runs');
          return {
            status: 'success' as const,
            values: {},
          };
        }
        const errorText = await response.text();
        let errorMessage = `Failed to get run state: ${response.statusText}`;
        try {
          const errorJson = JSON.parse(errorText);
          errorMessage = errorJson.detail || errorJson.message || errorMessage;
        } catch {
          errorMessage = errorText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      return response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Request timed out. The server may be slow.');
      }
      throw error;
    }
  }

  async resumeInterruptedRun(
    threadId: string,
    runId: string,
    status: 'approved' | 'rejected' | 'needs_revision',
    feedback: string = ''
  ): Promise<Record<string, any>> {
    const response = await fetch(
      `${this.baseUrl}/threads/${threadId}/runs/${runId}/resume`,
      {
        method: 'POST',
        headers: this.headers,
        body: JSON.stringify({
          command: {
            resume: { status, feedback },
          },
        }),
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to resume run: ${response.statusText}`);
    }

    return response.json();
  }

  async getThreadHistory(threadId: string): Promise<Record<string, any>> {
    const response = await fetch(
      `${this.baseUrl}/threads/${threadId}/history`,
      { headers: this.headers }
    );

    if (!response.ok) {
      throw new Error(`Failed to get thread history: ${response.statusText}`);
    }

    return response.json();
  }
}

