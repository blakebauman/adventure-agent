# API Deployment Guide

This guide explains how to deploy the Adventure Agent as a REST API following LangChain best practices.

## Overview

The Adventure Agent uses **LangGraph CLI** to expose a complete REST API. This is the recommended approach for LangGraph applications as it provides:

- Automatic API endpoint generation
- Built-in checkpointing and state management
- Thread-based conversation persistence
- Human-in-the-loop support via interrupts
- Streaming support
- OpenAPI documentation

## Quick Start

### Development Server

For local development and testing:

```bash
# Install LangGraph CLI (if not already installed)
uv pip install "langgraph-cli[inmem]"

# Start the development server
langgraph dev
```

The server will start on `http://localhost:2024` by default. You can access:
- API endpoints: `http://localhost:2024`
- OpenAPI docs: `http://localhost:2024/docs`
- Studio UI: URL provided in console output

### Production Server

For production deployment with Docker:

```bash
# Build Docker image
langgraph build

# Start with Docker (requires Docker and LangSmith API key)
langgraph up
```

## API Endpoints

The LangGraph CLI automatically exposes the following endpoints:

### Threads

- `POST /threads` - Create a new thread
- `GET /threads/{thread_id}` - Get thread details
- `GET /threads/{thread_id}/history` - Get thread execution history

### Runs

- `POST /threads/{thread_id}/runs` - Create and execute a run
- `GET /threads/{thread_id}/runs/{run_id}` - Get run status
- `GET /threads/{thread_id}/runs/{run_id}/state` - Get run state
- `POST /threads/{thread_id}/runs/{run_id}/resume` - Resume interrupted run

### Assistants

- `GET /assistants` - List assistants
- `GET /assistants/{assistant_id}` - Get assistant details

## Usage Examples

### Python Client

```python
import requests
from typing import Optional, Dict, Any

class AdventureAgentClient:
    """Client for interacting with the Adventure Agent API."""
    
    def __init__(self, base_url: str = "http://localhost:2024", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["X-Api-Key"] = api_key
    
    def create_thread(self, user_id: Optional[str] = None, session_id: Optional[str] = None) -> str:
        """Create a new conversation thread."""
        config = {"configurable": {}}
        if user_id:
            config["configurable"]["user_id"] = user_id
        if session_id:
            config["configurable"]["session_id"] = session_id
        
        response = requests.post(
            f"{self.base_url}/threads",
            json={"config": config},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()["thread_id"]
    
    def create_adventure_plan(
        self,
        thread_id: str,
        user_input: str,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create an adventure plan from natural language input."""
        input_data = {"user_input": user_input}
        if user_preferences:
            input_data["user_preferences"] = user_preferences
        
        response = requests.post(
            f"{self.base_url}/threads/{thread_id}/runs",
            json={
                "assistant_id": "agent",
                "input": input_data
            },
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_run_state(self, thread_id: str, run_id: str) -> Dict[str, Any]:
        """Get the current state of a run."""
        response = requests.get(
            f"{self.base_url}/threads/{thread_id}/runs/{run_id}/state",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def wait_for_completion(self, thread_id: str, run_id: str, timeout: int = 300) -> Dict[str, Any]:
        """Wait for a run to complete and return the final state."""
        import time
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            state = self.get_run_state(thread_id, run_id)
            status = state.get("status")
            
            if status == "success":
                return state["values"]
            elif status == "error":
                raise RuntimeError(f"Run failed: {state.get('error')}")
            
            time.sleep(1)
        
        raise TimeoutError(f"Run did not complete within {timeout} seconds")
    
    def resume_interrupted_run(
        self,
        thread_id: str,
        run_id: str,
        status: str = "approved",
        feedback: str = ""
    ) -> Dict[str, Any]:
        """Resume an interrupted run (e.g., after human review)."""
        response = requests.post(
            f"{self.base_url}/threads/{thread_id}/runs/{run_id}/resume",
            json={
                "command": {
                    "resume": {
                        "status": status,  # "approved", "rejected", "needs_revision"
                        "feedback": feedback
                    }
                }
            },
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    client = AdventureAgentClient()
    
    # Create a thread
    thread_id = client.create_thread(user_id="user123", session_id="session456")
    print(f"Created thread: {thread_id}")
    
    # Create an adventure plan
    run = client.create_adventure_plan(
        thread_id,
        user_input="I want to plan a 3-day mountain bike trip in Colorado for intermediate riders. I prefer camping and want to explore some challenging trails with great views."
    )
    run_id = run["run_id"]
    print(f"Started run: {run_id}")
    
    # Wait for completion
    try:
        final_state = client.wait_for_completion(thread_id, run_id)
        adventure_plan = final_state.get("adventure_plan")
        print(f"Adventure plan: {adventure_plan.get('title') if adventure_plan else 'None'}")
    except RuntimeError as e:
        print(f"Error: {e}")
```

### JavaScript/TypeScript Client

```typescript
import { Client } from "@langchain/langgraph-sdk";

const client = new Client({
  apiUrl: "http://localhost:2024",
  apiKey: process.env.LANGSMITH_API_KEY, // Optional
});

// Create a thread
const thread = await client.threads.create({
  config: {
    configurable: {
      user_id: "user123",
      session_id: "session456",
    },
  },
});

// Create and stream a run
const stream = await client.runs.stream(
  thread.thread_id,
  "agent", // assistant_id
  {
    input: {
      user_input: "Plan a 3-day mountain bike trip in Colorado",
      user_preferences: {
        activity_type: "mountain_biking",
        skill_level: "intermediate",
        region: "Colorado",
      },
    },
  }
);

// Process streamed events
for await (const event of stream) {
  console.log(`Event: ${event.event}`, event.data);
}
```

### cURL Examples

```bash
# Create a thread
curl -X POST http://localhost:2024/threads \
  -H "Content-Type: application/json" \
  -d '{
    "config": {
      "configurable": {
        "user_id": "user123",
        "session_id": "session456"
      }
    }
  }'

# Create a run
curl -X POST http://localhost:2024/threads/{thread_id}/runs \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent",
    "input": {
      "user_input": "Plan a 3-day mountain bike trip in Colorado"
    }
  }'

# Get run state
curl http://localhost:2024/threads/{thread_id}/runs/{run_id}/state

# Resume interrupted run (human-in-the-loop)
curl -X POST http://localhost:2024/threads/{thread_id}/runs/{run_id}/resume \
  -H "Content-Type: application/json" \
  -d '{
    "command": {
      "resume": {
        "status": "approved",
        "feedback": ""
      }
    }
  }'
```

## Streaming

The API supports streaming for real-time updates:

```python
import requests

def stream_run(thread_id: str, run_id: str):
    """Stream events from a run."""
    response = requests.get(
        f"{self.base_url}/threads/{thread_id}/runs/{run_id}/stream",
        headers=self.headers,
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            event = json.loads(line)
            yield event
```

## Human-in-the-Loop

When the graph hits an interrupt (e.g., in `human_review_node`), the run will be in a "pending" state. To resume:

```python
# Check if run is interrupted
state = client.get_run_state(thread_id, run_id)
if state.get("status") == "pending":
    # Resume with approval
    client.resume_interrupted_run(
        thread_id,
        run_id,
        status="approved",
        feedback="Looks good!"
    )
```

## Configuration

The `langgraph.json` file configures the API server:

```json
{
  "$schema": "https://langgra.ph/schema.json",
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent/graph.py:graph"
  },
  "env": ".env",
  "image_distro": "wolfi"
}
```

- `graphs`: Maps graph names to Python module paths
- `env`: Environment file to load
- `image_distro`: Base image for Docker builds

## Custom Routes

You can add custom API routes by creating a `webapp.py` file:

```python
# src/agent/webapp.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/custom-endpoint")
async def custom_endpoint():
    return {"message": "Custom route"}
```

Then update `langgraph.json`:

```json
{
  "graphs": {
    "agent": "./src/agent/graph.py:graph"
  },
  "webapp": "./src/agent/webapp.py:app"
}
```

## Authentication

For production deployments, configure authentication in `langgraph.json` or via environment variables. See the [LangGraph authentication documentation](https://docs.langchain.com/langsmith/auth) for details.

## Deployment Options

1. **LangGraph CLI (`langgraph dev`)**: Local development
2. **LangGraph CLI (`langgraph up`)**: Local Docker deployment
3. **LangSmith Cloud**: Managed hosting via LangSmith
4. **Self-hosted**: Deploy the Docker image to your infrastructure

## Best Practices

1. **Use threads for conversation persistence**: Each user session should have its own thread
2. **Handle interrupts gracefully**: Check for pending status and resume appropriately
3. **Implement retry logic**: Network calls can fail, implement exponential backoff
4. **Monitor run status**: Use streaming or polling to track long-running operations
5. **Set appropriate timeouts**: Adventure planning can take time, set reasonable timeouts
6. **Use structured logging**: Log thread_id and run_id for debugging

## Troubleshooting

### Server won't start
- Check that all dependencies are installed: `uv pip install -e ".[dev]"`
- Verify `langgraph.json` syntax is correct
- Check that the graph module path is correct

### Runs timing out
- Increase timeout values in your client
- Check for interrupts that need human review
- Verify external API keys are configured

### State not persisting
- Ensure checkpointing is configured in your graph
- For `langgraph dev`, state is stored in `.langgraph_api/`
- For `langgraph up`, ensure PostgreSQL is running

## Additional Resources

- [LangGraph CLI Documentation](https://docs.langchain.com/langsmith/cli)
- [Agent Server API Reference](https://docs.langchain.com/langsmith/server-api-ref)
- [LangGraph SDK Documentation](https://docs.langchain.com/langsmith/use-remote-graph)

