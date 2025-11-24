import { useState, useCallback, useRef } from 'react';
import { AdventureAgentClient } from '@/services/api-client';
import type { Message, UserPreferences, AdventurePlan, StreamEvent } from '@/types/adventure';
import { useToast } from '@/components/ui/use-toast';

// Use proxy in development, direct URL in production
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.DEV ? '/api' : 'http://localhost:2024');

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentThreadId, setCurrentThreadId] = useState<string | null>(null);
  const [currentRunId, setCurrentRunId] = useState<string | null>(null);
  const [needsReview, setNeedsReview] = useState(false);
  const clientRef = useRef(new AdventureAgentClient(API_BASE_URL));
  const { toast } = useToast();

  const sendMessage = useCallback(
    async (userInput: string, userPreferences?: UserPreferences) => {
      if (!userInput.trim()) return;

      setIsLoading(true);

      // Add user message
      const userMessage: Message = {
        id: `user-${Date.now()}`,
        role: 'user',
        content: userInput,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMessage]);

      try {
        // Create or get thread
        let threadId = currentThreadId;
        if (!threadId) {
          threadId = await clientRef.current.createThread();
          setCurrentThreadId(threadId);
        }

        // Create run
        const run = await clientRef.current.createAdventurePlan(
          threadId,
          userInput,
          userPreferences
        );
        setCurrentRunId(run.run_id);

        // Add placeholder for assistant response
        const assistantMessageId = `assistant-${Date.now()}`;
        let assistantMessage: Message = {
          id: assistantMessageId,
          role: 'assistant',
          content: '',
          timestamp: new Date(),
          isStreaming: true,
        };
        setMessages((prev) => [...prev, assistantMessage]);

        // Stream updates
        let fullContent = '';
        let adventurePlan: AdventurePlan | undefined;
        let currentAgent = '';
        let streamStartTime = Date.now();
        const slowWarningThreshold = 30000; // 30 seconds
        let slowWarningShown = false;

        try {
          console.log('Starting stream for run:', run.run_id);
          let eventCount = 0;
          for await (const event of clientRef.current.streamRun(threadId, run.run_id)) {
            eventCount++;
            // Show warning if streaming is taking a long time
            const elapsed = Date.now() - streamStartTime;
            if (elapsed > slowWarningThreshold && !slowWarningShown) {
              slowWarningShown = true;
              toast({
                title: 'Processing...',
                description: 'This may take a while due to external API calls. Please wait...',
              });
            }
            console.log(`Stream event ${eventCount}:`, event.event, event.name || '');
            // Handle different event types
            if (event.event === 'on_chain_start') {
              currentAgent = event.name || 'agent';
              fullContent += `\n\n**${currentAgent} is working...**\n`;
            } else if (event.event === 'on_chain_end' && event.data?.output) {
              const output = event.data.output;
              console.log('on_chain_end event output:', output);
              
              // Helper to recursively find adventure plan
              const findPlanInOutput = (obj: any): AdventurePlan | null => {
                if (!obj || typeof obj !== 'object') return null;
                if (obj.title || obj.description || obj.itinerary || obj.trails) {
                  return obj as AdventurePlan;
                }
                if (obj.adventure_plan) return obj.adventure_plan as AdventurePlan;
                if (obj.adventurePlan) return obj.adventurePlan as AdventurePlan;
                if (obj.plan) return obj.plan as AdventurePlan;
                // Recursively search
                for (const key in obj) {
                  if (obj.hasOwnProperty(key) && typeof obj[key] === 'object') {
                    const found = findPlanInOutput(obj[key]);
                    if (found) return found;
                  }
                }
                return null;
              };
              
              const plan = findPlanInOutput(output);
              
              if (plan) {
                console.log('Found adventure plan in stream event!', plan);
                adventurePlan = plan;
                fullContent = `# ${adventurePlan.title || 'Adventure Plan'}\n\n${adventurePlan.description || ''}`;
              } else if (typeof output === 'string') {
                fullContent += output;
              } else if (typeof output === 'object') {
                // Format object output
                fullContent += `\n\n**${currentAgent} completed:**\n${JSON.stringify(output, null, 2)}`;
              }
            } else if (event.event === 'on_chain_error') {
              const errorMsg = event.data?.error || event.error || 'Unknown error';
              fullContent += `\n\n⚠️ Error in ${currentAgent}: ${errorMsg}`;
            } else if (event.event === 'on_tool_start' || event.event === 'on_tool_end') {
              // Show tool usage
              const toolName = event.name || 'tool';
              if (event.event === 'on_tool_start') {
                fullContent += `\n\n🔧 Using ${toolName}...\n`;
              }
            } else if (event.event === 'on_run_end' || event.event === 'on_chain_stream_end') {
              console.log('Run end event received:', event.event);
              // Run or chain completed - ensure we capture any final data
              // Use the same recursive search as on_chain_end
              const findPlanInEvent = (obj: any): AdventurePlan | null => {
                if (!obj || typeof obj !== 'object') return null;
                if (obj.title || obj.description || obj.itinerary || obj.trails) {
                  return obj as AdventurePlan;
                }
                if (obj.adventure_plan) return obj.adventure_plan as AdventurePlan;
                if (obj.adventurePlan) return obj.adventurePlan as AdventurePlan;
                if (obj.plan) return obj.plan as AdventurePlan;
                // Recursively search
                for (const key in obj) {
                  if (obj.hasOwnProperty(key) && typeof obj[key] === 'object') {
                    const found = findPlanInEvent(obj[key]);
                    if (found) return found;
                  }
                }
                return null;
              };
              
              // Check in multiple places: event.data.output, event.data, event itself
              const plan = 
                (event.data?.output && findPlanInEvent(event.data.output)) ||
                (event.data && findPlanInEvent(event.data)) ||
                findPlanInEvent(event);
              
              if (plan) {
                console.log('Found adventure plan in run_end event!', plan);
                adventurePlan = plan;
                fullContent = `# ${adventurePlan.title || 'Adventure Plan'}\n\n${adventurePlan.description || ''}`;
              }
              
              // ALWAYS mark as complete when run ends, regardless of content
              // The UI will show a helpful message if there's no content/plan
              console.log('Marking message as complete (run_end received)');
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === assistantMessageId
                    ? {
                        ...msg,
                        content: fullContent || msg.content, // Preserve existing content if fullContent is empty
                        isStreaming: false,
                        adventurePlan: adventurePlan || msg.adventurePlan, // Preserve existing plan
                      }
                    : msg
                )
              );
              // Continue to update in real-time for other events
              continue;
            }

            // Update message in real-time
            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === assistantMessageId
                  ? {
                      ...msg,
                      content: fullContent,
                      isStreaming: true,
                      adventurePlan: adventurePlan,
                    }
                  : msg
              )
            );
          }
          console.log(`Stream loop completed after ${eventCount} events`);
        } catch (streamError) {
          console.error('Streaming error:', streamError);
          fullContent += `\n\n⚠️ Streaming error: ${streamError instanceof Error ? streamError.message : 'Connection lost'}`;
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantMessageId
                ? {
                    ...msg,
                    content: fullContent,
                    isStreaming: false,
                  }
                : msg
            )
          );
        }

        // Mark streaming as complete (if not already marked by on_run_end)
        console.log('Stream loop ended, checking if message needs completion');
        setMessages((prev) =>
          prev.map((msg) => {
            if (msg.id === assistantMessageId) {
              // Only update if still streaming (on_run_end might have already set it to false)
              if (msg.isStreaming !== false) {
                console.log('Stream ended but message still marked as streaming - marking complete');
                // Always mark as complete when stream ends, even if no content
                // The UI will show a helpful message if there's no content/plan
                return { 
                  ...msg, 
                  content: fullContent || msg.content, // Preserve existing content
                  isStreaming: false, 
                  adventurePlan: adventurePlan || msg.adventurePlan 
                };
              } else {
                console.log('Message already marked as complete');
              }
              // Otherwise just ensure adventurePlan is set
              return { ...msg, adventurePlan: adventurePlan || msg.adventurePlan };
            }
            return msg;
          })
        );

        // Check for final state immediately after stream ends
        // Don't wait - the run might be cleaned up quickly by the backend
        // If we already have a plan from streaming, we can skip this check
        let shouldCheckState = true;
        if (adventurePlan && (adventurePlan.title || adventurePlan.description || adventurePlan.itinerary || adventurePlan.trails)) {
          console.log('Already have plan from streaming, checking state for any additional data...');
          // Still check, but don't wait - do it immediately
        } else {
          console.log('No plan from streaming, checking state for final plan...');
          // Small delay only if we don't have a plan yet
          await new Promise(resolve => setTimeout(resolve, 500));
        }

        // Check for final state and human review (handle 404 gracefully - run might be cleaned up)
        try {
          const state = await clientRef.current.getRunState(threadId, run.run_id);
          console.log('Final run state:', state);
          
          if (state.status === 'pending') {
            setNeedsReview(true);
            toast({
              title: 'Review Required',
              description: 'Your adventure plan is ready for review.',
            });
          } else if (state.status === 'error') {
            const errorMsg = state.error || 'An error occurred while planning your adventure';
            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === assistantMessageId
                  ? {
                      ...msg,
                      isStreaming: false,
                      content: msg.content + `\n\n⚠️ Error: ${errorMsg}`,
                    }
                  : msg
              )
            );
            toast({
              title: 'Error',
              description: errorMsg,
              variant: 'destructive',
            });
          } else if (state.status === 'success') {
            // Log the full state structure for debugging
            console.log('Final run state structure:', JSON.stringify(state, null, 2));
            console.log('State values keys:', state.values ? Object.keys(state.values) : 'no values');
            
            // Helper function to recursively search for adventure plan
            const findAdventurePlan = (obj: any): AdventurePlan | null => {
              if (!obj || typeof obj !== 'object') return null;
              
              // Check if this object itself is an adventure plan
              if (obj.title || obj.description || obj.itinerary || obj.trails) {
                return obj as AdventurePlan;
              }
              
              // Check common property names
              if (obj.adventure_plan) return obj.adventure_plan as AdventurePlan;
              if (obj.adventurePlan) return obj.adventurePlan as AdventurePlan;
              if (obj.plan) return obj.plan as AdventurePlan;
              
              // Recursively search nested objects
              for (const key in obj) {
                if (obj.hasOwnProperty(key) && typeof obj[key] === 'object') {
                  const found = findAdventurePlan(obj[key]);
                  if (found) return found;
                }
              }
              
              return null;
            };
            
            // Always update with final state if available, even if we have a plan from streaming
            const finalPlan = findAdventurePlan(state.values) || adventurePlan;
            
            // Check if state.values is empty (might be 404 response)
            const isStateEmpty = !state.values || Object.keys(state.values).length === 0;
            
            if (finalPlan && (finalPlan.title || finalPlan.description || finalPlan.itinerary || finalPlan.trails)) {
              console.log('Found adventure plan! Updating message:', finalPlan);
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === assistantMessageId
                    ? {
                        ...msg,
                        isStreaming: false,
                        adventurePlan: finalPlan,
                        content: finalPlan.title 
                          ? `# ${finalPlan.title}\n\n${finalPlan.description || ''}`
                          : msg.content,
                      }
                    : msg
                )
              );
              
              // Show completion toast
              toast({
                title: 'Adventure Plan Complete!',
                description: 'Your adventure plan is ready.',
              });
            } else if (isStateEmpty && adventurePlan && (adventurePlan.title || adventurePlan.description || adventurePlan.itinerary || adventurePlan.trails)) {
              // State check returned empty (likely 404 - run cleaned up), but we have plan from streaming
              console.log('State check returned empty (run may be cleaned up), using plan from streaming');
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === assistantMessageId
                    ? {
                        ...msg,
                        isStreaming: false,
                        adventurePlan: adventurePlan,
                      }
                    : msg
                )
              );
              toast({
                title: 'Adventure Plan Complete!',
                description: 'Your adventure plan is ready.',
              });
            } else {
              console.warn('Run completed successfully but no adventure plan found. State:', state);
              console.warn('Adventure plan from streaming:', adventurePlan);
              
              // If we have a plan from streaming, still show it
              if (adventurePlan && (adventurePlan.title || adventurePlan.description || adventurePlan.itinerary || adventurePlan.trails)) {
                console.log('Using adventure plan from streaming');
                setMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === assistantMessageId
                      ? {
                          ...msg,
                          isStreaming: false,
                          adventurePlan: adventurePlan,
                        }
                      : msg
                  )
                );
                toast({
                  title: 'Adventure Plan Complete!',
                  description: 'Your adventure plan is ready.',
                });
              } else {
                // No plan found, but run completed - show completion anyway
                console.log('Run completed but no plan found - showing completion message');
                setMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === assistantMessageId
                      ? {
                          ...msg,
                          isStreaming: false,
                        }
                      : msg
                  )
                );
              }
            }
          }
        } catch (error) {
          // 404 is OK - run might be cleaned up or doesn't exist yet
          // Only log if it's not a 404
          if (error instanceof Error && !error.message.includes('404')) {
            console.warn('Failed to get run state for review check:', error);
          } else {
            console.log('State check returned 404 (run cleaned up) - using plan from streaming if available');
          }
          
          // Even if we can't get state, if we have an adventure plan from streaming, show it
          if (adventurePlan && (adventurePlan.title || adventurePlan.description || adventurePlan.itinerary || adventurePlan.trails)) {
            console.log('Using adventure plan from streaming (state check failed/404)');
            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === assistantMessageId
                  ? {
                      ...msg,
                      isStreaming: false,
                      adventurePlan: adventurePlan,
                    }
                  : msg
              )
            );
            toast({
              title: 'Adventure Plan Complete!',
              description: 'Your adventure plan is ready.',
            });
          } else {
            // No plan from streaming either, but run completed - ensure we're marked complete
            console.log('No plan found from streaming, but ensuring message is marked complete');
            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === assistantMessageId
                  ? {
                      ...msg,
                      isStreaming: false,
                    }
                  : msg
              )
            );
          }
        }
      } catch (error) {
        console.error('Error sending message:', error);
        const errorMessage: Message = {
          id: `error-${Date.now()}`,
          role: 'system',
          content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);
        toast({
          title: 'Error',
          description: error instanceof Error ? error.message : 'Failed to send message',
          variant: 'destructive',
        });
      } finally {
        setIsLoading(false);
      }
    },
    [currentThreadId, toast]
  );

  const handleReview = useCallback(
    async (
      status: 'approved' | 'rejected' | 'needs_revision',
      feedback: string = ''
    ) => {
      if (!currentThreadId || !currentRunId) return;

      try {
        await clientRef.current.resumeInterruptedRun(
          currentThreadId,
          currentRunId,
          status,
          feedback
        );

        // Continue streaming if needed
        if (status === 'approved' || status === 'needs_revision') {
          // Stream the resumed run
          const assistantMessageId = `assistant-${Date.now()}`;
          let assistantMessage: Message = {
            id: assistantMessageId,
            role: 'assistant',
            content: '',
            timestamp: new Date(),
            isStreaming: true,
          };
          setMessages((prev) => [...prev, assistantMessage]);

          let fullContent = '';
          for await (const event of clientRef.current.streamRun(
            currentThreadId,
            currentRunId
          )) {
            if (event.event === 'on_chain_end' && event.data?.output) {
              const output = event.data.output;
              if (output.adventure_plan) {
                fullContent = `# ${output.adventure_plan.title || 'Adventure Plan'}\n\n${output.adventure_plan.description || ''}`;
              }
            }

            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === assistantMessageId
                  ? { ...msg, content: fullContent, isStreaming: true }
                  : msg
              )
            );
          }

          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantMessageId
                ? { ...msg, isStreaming: false }
                : msg
            )
          );
        }

        setNeedsReview(false);
      } catch (error) {
        console.error('Error handling review:', error);
        toast({
          title: 'Error',
          description: 'Failed to submit review',
          variant: 'destructive',
        });
      }
    },
    [currentThreadId, currentRunId, toast]
  );

  const clearChat = useCallback(() => {
    setMessages([]);
    setCurrentThreadId(null);
    setCurrentRunId(null);
    setNeedsReview(false);
  }, []);

  return {
    messages,
    sendMessage,
    isLoading,
    currentThreadId,
    currentRunId,
    needsReview,
    handleReview,
    clearChat,
  };
}

