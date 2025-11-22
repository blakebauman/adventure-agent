"""Python client for the Adventure Agent API.

This module provides a convenient client for interacting with the Adventure Agent
REST API exposed by LangGraph CLI.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional

import httpx


class AdventureAgentClient:
    """Client for interacting with the Adventure Agent API.
    
    This client provides methods to interact with the LangGraph API server,
    including creating threads, running adventure planning requests, and
    handling human-in-the-loop interrupts.
    
    Example:
        ```python
        client = AdventureAgentClient(base_url="http://localhost:2024")
        
        # Create a thread
        thread_id = client.create_thread(user_id="user123")
        
        # Create an adventure plan
        run = client.create_adventure_plan(
            thread_id,
            "Plan a 3-day mountain bike trip in Colorado"
        )
        
        # Wait for completion
        state = client.wait_for_completion(thread_id, run["run_id"])
        ```
    """

    def __init__(
        self,
        base_url: str = "http://localhost:2024",
        api_key: Optional[str] = None,
        timeout: float = 300.0,
    ) -> None:
        """Initialize the Adventure Agent API client.
        
        Args:
            base_url: Base URL of the LangGraph API server
            api_key: Optional API key for authentication
            timeout: Default timeout for requests in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["X-Api-Key"] = api_key

    def create_thread(
        self,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> str:
        """Create a new conversation thread.
        
        Args:
            user_id: Optional user ID for tracking
            session_id: Optional session ID for grouping related requests
            
        Returns:
            The thread ID for the created thread
            
        Raises:
            httpx.HTTPStatusError: If the request fails
        """
        config: Dict[str, Any] = {"configurable": {}}
        if user_id:
            config["configurable"]["user_id"] = user_id
        if session_id:
            config["configurable"]["session_id"] = session_id

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/threads",
                json={"config": config},
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()["thread_id"]

    def create_adventure_plan(
        self,
        thread_id: str,
        user_input: str,
        user_preferences: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create an adventure plan from natural language input.
        
        Args:
            thread_id: The thread ID to use for this request
            user_input: Natural language description of the desired adventure
            user_preferences: Optional structured preferences
            
        Returns:
            Dictionary containing run_id and other run metadata
            
        Raises:
            httpx.HTTPStatusError: If the request fails
        """
        input_data: Dict[str, Any] = {"user_input": user_input}
        if user_preferences:
            input_data["user_preferences"] = user_preferences

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/threads/{thread_id}/runs",
                json={
                    "assistant_id": "agent",
                    "input": input_data,
                },
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    def get_run_state(self, thread_id: str, run_id: str) -> Dict[str, Any]:
        """Get the current state of a run.
        
        Args:
            thread_id: The thread ID
            run_id: The run ID
            
        Returns:
            Dictionary containing the run state and status
            
        Raises:
            httpx.HTTPStatusError: If the request fails
        """
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(
                f"{self.base_url}/threads/{thread_id}/runs/{run_id}/state",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    def wait_for_completion(
        self,
        thread_id: str,
        run_id: str,
        timeout: Optional[float] = None,
        poll_interval: float = 1.0,
    ) -> Dict[str, Any]:
        """Wait for a run to complete and return the final state.
        
        Args:
            thread_id: The thread ID
            run_id: The run ID
            timeout: Maximum time to wait in seconds (defaults to client timeout)
            poll_interval: Time between status checks in seconds
            
        Returns:
            The final state values from the completed run
            
        Raises:
            TimeoutError: If the run doesn't complete within the timeout
            RuntimeError: If the run fails with an error
        """
        timeout = timeout or self.timeout
        start_time = time.time()

        while time.time() - start_time < timeout:
            state = self.get_run_state(thread_id, run_id)
            status = state.get("status")

            if status == "success":
                return state.get("values", {})
            elif status == "error":
                error_msg = state.get("error", "Unknown error")
                raise RuntimeError(f"Run failed: {error_msg}")
            elif status == "pending":
                # Run is interrupted (e.g., waiting for human review)
                raise RuntimeError(
                    "Run is interrupted and requires human review. "
                    "Use resume_interrupted_run() to continue."
                )

            time.sleep(poll_interval)

        raise TimeoutError(
            f"Run did not complete within {timeout} seconds"
        )

    def resume_interrupted_run(
        self,
        thread_id: str,
        run_id: str,
        status: str = "approved",
        feedback: str = "",
    ) -> Dict[str, Any]:
        """Resume an interrupted run (e.g., after human review).
        
        Args:
            thread_id: The thread ID
            run_id: The run ID
            status: Approval status - "approved", "rejected", or "needs_revision"
            feedback: Optional feedback to incorporate into the plan
            
        Returns:
            Dictionary containing the resumed run information
            
        Raises:
            httpx.HTTPStatusError: If the request fails
        """
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/threads/{thread_id}/runs/{run_id}/resume",
                json={
                    "command": {
                        "resume": {
                            "status": status,
                            "feedback": feedback,
                        }
                    }
                },
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    def stream_run(
        self,
        thread_id: str,
        run_id: str,
    ) -> Any:  # Generator[Dict[str, Any], None, None]
        """Stream events from a run.
        
        Args:
            thread_id: The thread ID
            run_id: The run ID
            
        Yields:
            Event dictionaries as they arrive from the server
        """
        with httpx.Client(timeout=None) as client:
            with client.stream(
                "GET",
                f"{self.base_url}/threads/{thread_id}/runs/{run_id}/stream",
                headers=self.headers,
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        yield json.loads(line)

    def get_thread_history(self, thread_id: str) -> Dict[str, Any]:
        """Get the execution history for a thread.
        
        Args:
            thread_id: The thread ID
            
        Returns:
            Dictionary containing the thread history
            
        Raises:
            httpx.HTTPStatusError: If the request fails
        """
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(
                f"{self.base_url}/threads/{thread_id}/history",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()


# Convenience function for simple usage
def create_adventure_plan_simple(
    user_input: str,
    user_preferences: Optional[Dict[str, Any]] = None,
    base_url: str = "http://localhost:2024",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Create an adventure plan with a single function call.
    
    This is a convenience function that creates a thread, runs the adventure
    planning, and waits for completion in one call.
    
    Args:
        user_input: Natural language description of the desired adventure
        user_preferences: Optional structured preferences
        base_url: Base URL of the LangGraph API server
        api_key: Optional API key for authentication
        
    Returns:
        The final adventure plan from the completed run
        
    Example:
        ```python
        plan = create_adventure_plan_simple(
            "Plan a 3-day mountain bike trip in Colorado"
        )
        print(plan["adventure_plan"]["title"])
        ```
    """
    client = AdventureAgentClient(base_url=base_url, api_key=api_key)
    thread_id = client.create_thread()
    run = client.create_adventure_plan(thread_id, user_input, user_preferences)
    return client.wait_for_completion(thread_id, run["run_id"])

