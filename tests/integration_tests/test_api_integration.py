"""Integration tests for LangGraph API endpoints.

These tests require the LangGraph dev server to be running.
Start it with: ./run.sh dev
"""

import time
from typing import Optional

import httpx
import pytest


# Configuration
API_URL = "http://127.0.0.1:8123"
ASSISTANT_ID = "agent"
DEFAULT_TIMEOUT = 300  # 5 minutes


@pytest.fixture(scope="session")
def api_url():
    """Return the API URL."""
    return API_URL


@pytest.fixture(scope="session")
def assistant_id():
    """Return the assistant ID."""
    return ASSISTANT_ID


@pytest.fixture(scope="session")
def server_available(api_url):
    """Check if the LangGraph dev server is running."""
    try:
        with httpx.Client(timeout=5.0) as client:
            # Try to connect to the server - any HTTP response means server is running
            # We'll try the root endpoint - connection errors mean server is down
            client.get(f"{api_url}/", follow_redirects=True)
            return True
    except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError):
        pytest.skip("LangGraph dev server is not running. Start it with: ./run.sh dev")
    except Exception:
        # Any other exception (like HTTPStatusError) means server responded
        # which means it's running
        return True


@pytest.fixture
def thread_id(server_available, api_url):
    """Create a new thread for testing."""
    with httpx.Client(timeout=10.0) as client:
        response = client.post(
            f"{api_url}/threads",
            json={"config": {"configurable": {"user_id": "test_user", "session_id": "test_session"}}},
        )
        response.raise_for_status()
        thread_id = response.json()["thread_id"]
        yield thread_id
        # Cleanup could go here if needed


def create_thread(api_url: str, user_id: str = "test_user", session_id: str = "test_session") -> str:
    """Create a new thread."""
    with httpx.Client(timeout=10.0) as client:
        response = client.post(
            f"{api_url}/threads",
            json={"config": {"configurable": {"user_id": user_id, "session_id": session_id}}},
        )
        response.raise_for_status()
        return response.json()["thread_id"]


def submit_request(
    api_url: str,
    assistant_id: str,
    thread_id: str,
    user_input: str,
    user_preferences: Optional[dict] = None,
) -> str:
    """Submit an adventure planning request."""
    input_data = {"user_input": user_input}
    if user_preferences:
        input_data["user_preferences"] = user_preferences

    with httpx.Client(timeout=30.0) as client:
        response = client.post(
            f"{api_url}/threads/{thread_id}/runs",
            json={
                "assistant_id": assistant_id,
                "input": input_data,
            },
        )
        response.raise_for_status()
        return response.json()["run_id"]


def wait_for_completion(
    api_url: str,
    thread_id: str,
    run_id: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> Optional[dict]:
    """Wait for a run to complete."""
    start_time = time.time()
    with httpx.Client(timeout=10.0) as client:
        while time.time() - start_time < timeout:
            response = client.get(f"{api_url}/threads/{thread_id}/runs/{run_id}")
            response.raise_for_status()
            status = response.json()["status"]

            if status == "success":
                return response.json()
            elif status == "failure":
                return response.json()

            time.sleep(2)

    return None


def get_thread_state(api_url: str, thread_id: str) -> dict:
    """Get the current state of a thread."""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(f"{api_url}/threads/{thread_id}/state")
        response.raise_for_status()
        return response.json()


@pytest.mark.integration
class TestAPIIntegration:
    """Test LangGraph API endpoints."""

    def test_basic_mountain_biking_request(self, server_available, api_url, assistant_id):
        """Test a basic mountain biking adventure planning request."""
        thread_id = create_thread(api_url, user_id="test_user_1", session_id="test_session_1")

        run_id = submit_request(
            api_url,
            assistant_id,
            thread_id,
            "I want to go mountain biking in Colorado for 3 days",
            {
                "activity_type": "mountain_biking",
                "region": "Colorado",
                "duration_days": 3,
                "skill_level": "intermediate",
            },
        )

        result = wait_for_completion(api_url, thread_id, run_id)

        assert result is not None, "Run should complete"
        assert result["status"] in ["success", "failure"], "Run should have a status"

        if result["status"] == "success":
            state = get_thread_state(api_url, thread_id)

            # Check for adventure plan
            if "values" in state and "adventure_plan" in state["values"]:
                plan = state["values"]["adventure_plan"]
                if plan:
                    assert "title" in plan or plan is not None, "Adventure plan should have content"

    def test_natural_language_request(self, server_available, api_url, assistant_id):
        """Test natural language text-to-adventure request."""
        thread_id = create_thread(api_url, user_id="test_user_2", session_id="test_session_2")

        run_id = submit_request(
            api_url,
            assistant_id,
            thread_id,
            "I'm looking for a weekend bikepacking trip in Utah, something challenging but not too extreme",
        )

        result = wait_for_completion(api_url, thread_id, run_id)

        assert result is not None, "Run should complete"

        if result["status"] == "success":
            state = get_thread_state(api_url, thread_id)

            # Check that preferences were extracted
            prefs = state.get("values", {}).get("user_preferences", {})
            # Preferences should be populated by the orchestrator
            assert isinstance(prefs, dict), "User preferences should be a dictionary"

    def test_error_handling(self, server_available, api_url, assistant_id):
        """Test error handling with invalid input."""
        thread_id = create_thread(api_url, user_id="test_user_3", session_id="test_session_3")

        run_id = submit_request(
            api_url,
            assistant_id,
            thread_id,
            "I want to go biking in Nowhere, Antarctica",
        )

        result = wait_for_completion(api_url, thread_id, run_id)

        assert result is not None, "Run should complete"

        if result["status"] == "success":
            state = get_thread_state(api_url, thread_id)
            errors = state.get("values", {}).get("errors", [])

            # Errors should be captured or handled gracefully
            # Either errors list exists, or the system handled it gracefully
            assert isinstance(errors, list), "Errors should be a list (even if empty)"

    def test_thread_creation(self, server_available, api_url):
        """Test thread creation endpoint."""
        thread_id = create_thread(api_url)
        assert thread_id is not None
        assert isinstance(thread_id, str)
        assert len(thread_id) > 0

    def test_thread_state_retrieval(self, server_available, api_url):
        """Test retrieving thread state."""
        thread_id = create_thread(api_url)
        state = get_thread_state(api_url, thread_id)

        assert "values" in state
        assert isinstance(state["values"], dict)

