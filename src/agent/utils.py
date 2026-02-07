"""Utility functions for the adventure agent."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Literal

from langgraph.types import Command

if TYPE_CHECKING:
    from agent.state import AdventureState, UserPreferences

logger = logging.getLogger(__name__)


def extract_activity_type(
    user_prefs: UserPreferences | None,
    default: str = "mountain_biking",
) -> str:
    """Extract activity type from user preferences with backward compatibility.

    Handles both activity_type (current) and adventure_type (deprecated) fields.

    Args:
        user_prefs: User preferences dict or None
        default: Default activity type if not found

    Returns:
        Activity type string (mountain_biking, hiking, trail_running, bikepacking)
    """
    if not user_prefs:
        return default

    # Primary field
    if activity := user_prefs.get("activity_type"):
        return activity

    # Fallback for deprecated field
    if adventure := user_prefs.get("adventure_type"):
        return adventure

    return default


def extract_location(state: AdventureState, default: str = "") -> str:
    """Extract location from state with cascading fallbacks.

    Priority order:
    1. geo_info.location (from geo_agent output)
    2. user_preferences.region
    3. First word of user_input (last resort)
    4. Default value

    Args:
        state: Current adventure state
        default: Default value if no location found

    Returns:
        Location string
    """
    # Try geo_info first (most accurate, from geo_agent)
    if geo_info := state.get("geo_info"):
        if location := geo_info.get("location"):
            return location

    # Try user preferences
    if user_prefs := state.get("user_preferences"):
        if region := user_prefs.get("region"):
            return region

    # Last resort: extract from user input
    if user_input := state.get("user_input"):
        if user_input.strip():
            return user_input.split()[0]

    return default


def extract_context(state: AdventureState, agent_name: str) -> str:
    """Extract agent-specific context from state.

    Falls back to user_input if no specific context is set.

    Args:
        state: Current adventure state
        agent_name: Name of the agent (e.g., "geo_agent")

    Returns:
        Context string for the agent
    """
    agent_context = state.get("agent_context", {})
    return agent_context.get(agent_name, state.get("user_input", ""))


async def invoke_tool_async(tool: Any, args: dict[str, Any]) -> Any:
    """Invoke a LangChain tool asynchronously to avoid blocking the event loop.

    Args:
        tool: The LangChain tool to invoke
        args: Arguments to pass to the tool

    Returns:
        Tool result
    """
    return await asyncio.to_thread(tool.invoke, args)


def extract_route_info(state: AdventureState) -> dict[str, Any]:
    """Extract route info dict from trail_info in state.

    Used by agents that need trail information (safety, food, photography, historical).

    Args:
        state: Current adventure state

    Returns:
        Dict with trails list
    """
    trail_info = state.get("trail_info", [])
    return {
        "trails": [dict(t) for t in trail_info] if trail_info else [],
    }


def create_agent_node(
    agent_name: str,
    output_field: str,
    invoke_fn: Callable[[AdventureState, str], Awaitable[Any]],
    fallback_value: Any = None,
) -> Callable[[AdventureState], Awaitable[dict[str, Any] | Command[Literal["orchestrator"]]]]:
    """Create an agent node with standardized error handling.

    This factory reduces boilerplate by handling:
    - Context extraction
    - Error handling with handle_agent_error
    - Command-based error recovery routing
    - Consistent return format with completed_agents

    Args:
        agent_name: Name of the agent (e.g., "blm_agent")
        output_field: State field to store result (e.g., "blm_info")
        invoke_fn: Async function(state, context) that calls the agent and returns result.
                   Should extract any needed params from state and call the agent method.
        fallback_value: Value to use on error (None, [], {}, etc.)

    Returns:
        Async node function for use in LangGraph

    Example:
        ```python
        async def invoke_blm(state, context):
            location = extract_location(state)
            activity_type = extract_activity_type(state.get("user_preferences"))
            return await blm_agent.get_blm_information(location, activity_type, context)

        blm_agent_node = create_agent_node(
            "blm_agent", "blm_info", invoke_blm, fallback_value=[]
        )
        ```
    """
    # Import here to avoid circular imports
    from agent.graph import handle_agent_error

    async def node(
        state: AdventureState,
    ) -> dict[str, Any] | Command[Literal["orchestrator"]]:
        try:
            context = extract_context(state, agent_name)
            result = await invoke_fn(state, context)

            return {
                output_field: result,
                "completed_agents": [agent_name],
            }
        except Exception as e:
            error_result = handle_agent_error(e, agent_name, state, fallback_value)
            # Check if it's a Command (for LLM-recoverable errors)
            if hasattr(error_result, "goto"):
                return error_result
            # Add output field to error result
            error_result[output_field] = fallback_value
            return error_result

    # Set function name for debugging
    node.__name__ = f"{agent_name}_node"
    node.__doc__ = f"{agent_name.replace('_', ' ').title()} node - auto-generated."

    return node

