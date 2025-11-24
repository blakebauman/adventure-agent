"""Main LangGraph for adventure agent system."""

from __future__ import annotations

import asyncio
import warnings
from typing import Any, Dict, List, Literal

from langgraph.graph import END, StateGraph
from langgraph.types import Command, RetryPolicy, interrupt
from typing_extensions import TypedDict

from agent.archive import archive_plan
from agent.config import Config

# Suppress known non-critical warnings
# LangSmith UUID v7 warning: This is a deprecation warning from LangChain's internal
# processing. It doesn't affect functionality and will be resolved when LangChain updates.
warnings.filterwarnings(
    "ignore",
    message="LangSmith now uses UUID v7.*",
    category=UserWarning,
    module="pydantic.v1.main",
)
from agent.error_handling import (
    ErrorCategory,
    ErrorType,
    is_llm_recoverable_error,
    is_user_fixable_error,
)

# Checkpointing configuration
# LangGraph API handles persistence automatically when deployed via API.
# For local development or standalone deployment, configure a checkpointer.
_checkpointer = None
if Config.CHECKPOINTER_TYPE == "memory":
    from langgraph.checkpoint.memory import MemorySaver
    _checkpointer = MemorySaver()
elif Config.CHECKPOINTER_TYPE == "sqlite" and Config.CHECKPOINTER_DB_URL:
    from langgraph.checkpoint.sqlite import SqliteSaver
    _checkpointer = SqliteSaver.from_conn_string(Config.CHECKPOINTER_DB_URL)
elif Config.CHECKPOINTER_TYPE == "postgres" and Config.CHECKPOINTER_DB_URL:
    from langgraph.checkpoint.postgres import PostgresSaver
    _checkpointer = PostgresSaver.from_conn_string(Config.CHECKPOINTER_DB_URL)
# If CHECKPOINTER_TYPE is "none" or unset, no checkpointer (for LangGraph API)

# Validate checkpointer for human-in-the-loop
# Human-in-the-loop features require a checkpointer to persist state between interrupts
if Config.ENABLE_HUMAN_REVIEW and _checkpointer is None and Config.CHECKPOINTER_TYPE == "none":
    warnings.warn(
        "Human-in-the-loop is enabled but no checkpointer is configured. "
        "Set CHECKPOINTER_TYPE to 'memory', 'sqlite', or 'postgres' for human-in-the-loop to work properly. "
        "Note: LangGraph API (langgraph dev) handles checkpointing automatically.",
        UserWarning
    )

from agent.agents import (
    AccommodationAgent,
    AdvocacyAgent,
    AjoAgent,
    BikepackingAgent,
    BisbeeAgent,
    BLMAgent,
    CampVerdeAgent,
    CommunityAgent,
    CottonwoodAgent,
    FlagstaffAgent,
    FoodAgent,
    GearAgent,
    GeoAgent,
    GlobeMiamiAgent,
    GrandCanyonAgent,
    HistoricalAgent,
    JeromeAgent,
    KingmanAgent,
    LakeHavasuAgent,
    LocationAgentBase,
    OrchestratorAgent,
    PageAgent,
    ParkerAgent,
    PatagoniaAgent,
    PaysonAgent,
    PermitsAgent,
    PhoenixAgent,
    PhotographyAgent,
    PineAgent,
    PinetopAgent,
    PlanningAgent,
    PrescottAgent,
    RoutePlanningAgent,
    SafetyAgent,
    SedonaAgent,
    ShowLowAgent,
    SierraVistaAgent,
    SonoitaAgent,
    SpringervilleEagarAgent,
    StrawberryAgent,
    TombstoneAgent,
    TrailAgent,
    TransportationAgent,
    TucsonAgent,
    WeatherAgent,
    WilliamsAgent,
    YumaAgent,
    get_all_location_agents,
    register_location_agent,
)
from agent.state import AdventureState


class Context(TypedDict):
    """Context parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    """

    user_id: str
    session_id: str


# Initialize agents
orchestrator = OrchestratorAgent()
blm_agent = BLMAgent()
trail_agent = TrailAgent()
geo_agent = GeoAgent()
accommodation_agent = AccommodationAgent()
planning_agent = PlanningAgent()
gear_agent = GearAgent()
weather_agent = WeatherAgent()
permits_agent = PermitsAgent()
safety_agent = SafetyAgent()
transportation_agent = TransportationAgent()
food_agent = FoodAgent()
community_agent = CommunityAgent()
photography_agent = PhotographyAgent()
historical_agent = HistoricalAgent()
route_planning_agent = RoutePlanningAgent()
bikepacking_agent = BikepackingAgent()
advocacy_agent = AdvocacyAgent()

# Initialize location agents
jerome_agent = JeromeAgent()
sedona_agent = SedonaAgent()
prescott_agent = PrescottAgent()
flagstaff_agent = FlagstaffAgent()
grand_canyon_agent = GrandCanyonAgent()
payson_agent = PaysonAgent()
pine_agent = PineAgent()
strawberry_agent = StrawberryAgent()
pinetop_agent = PinetopAgent()
williams_agent = WilliamsAgent()
phoenix_agent = PhoenixAgent()
tucson_agent = TucsonAgent()
cottonwood_agent = CottonwoodAgent()
camp_verde_agent = CampVerdeAgent()
show_low_agent = ShowLowAgent()
bisbee_agent = BisbeeAgent()
tombstone_agent = TombstoneAgent()
sierra_vista_agent = SierraVistaAgent()
patagonia_agent = PatagoniaAgent()
page_agent = PageAgent()
kingman_agent = KingmanAgent()
lake_havasu_agent = LakeHavasuAgent()
globe_miami_agent = GlobeMiamiAgent()
springerville_eagar_agent = SpringervilleEagarAgent()
ajo_agent = AjoAgent()
sonoita_agent = SonoitaAgent()
yuma_agent = YumaAgent()
parker_agent = ParkerAgent()

# Register all location agents
register_location_agent(jerome_agent)
register_location_agent(sedona_agent)
register_location_agent(prescott_agent)
register_location_agent(flagstaff_agent)
register_location_agent(grand_canyon_agent)
register_location_agent(payson_agent)
register_location_agent(pine_agent)
register_location_agent(strawberry_agent)
register_location_agent(pinetop_agent)
register_location_agent(williams_agent)
register_location_agent(phoenix_agent)
register_location_agent(tucson_agent)
register_location_agent(cottonwood_agent)
register_location_agent(camp_verde_agent)
register_location_agent(show_low_agent)
register_location_agent(bisbee_agent)
register_location_agent(tombstone_agent)
register_location_agent(sierra_vista_agent)
register_location_agent(patagonia_agent)
register_location_agent(page_agent)
register_location_agent(kingman_agent)
register_location_agent(lake_havasu_agent)
register_location_agent(globe_miami_agent)
register_location_agent(springerville_eagar_agent)
register_location_agent(ajo_agent)
register_location_agent(sonoita_agent)
register_location_agent(yuma_agent)
register_location_agent(parker_agent)


def handle_agent_error(
    error: Exception,
    agent_name: str,
    state: AdventureState,
    fallback_value: Any = None,
) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Handle errors in agent nodes with appropriate strategy.
    
    Args:
        error: The exception that was raised
        agent_name: Name of the agent that raised the error
        state: Current graph state
        fallback_value: Value to return for the agent's output field (None, [], etc.)
    
    Returns:
        Either a state update dict or a Command to route back to orchestrator
        for LLM-recoverable errors.
    """
    error_detail = ErrorCategory.create_error_dict(error, agent_name)
    error_type = ErrorType(error_detail["type"])
    
    # Get existing error details
    existing_error_details = state.get("error_details", [])
    
    # For LLM-recoverable errors, route back to orchestrator
    if error_type == ErrorType.LLM_RECOVERABLE:
        # Store error in state and route to orchestrator for recovery
        return Command(
            update={
                "error_details": existing_error_details + [error_detail],
                # Don't mark as completed - let orchestrator decide if we should retry
            },
            goto="orchestrator",
        )
    
    # For user-fixable errors, we could use interrupt, but for now just store error
    # (Could be enhanced to use interrupt() for user input)
    if error_type == ErrorType.USER_FIXABLE:
        return {
            "error_details": existing_error_details + [error_detail],
            "completed_agents": [agent_name],  # Mark as completed to avoid infinite loops
        }
    
    # For transient and permanent errors, store error and continue
    # Transient errors should be handled by retry policies
    # Permanent errors should be logged and execution should continue
    return {
        "error_details": existing_error_details + [error_detail],
        "completed_agents": [agent_name],
    }


def create_error_detail(error: Exception, agent_name: str) -> Dict[str, Any]:
    """Create an error detail dict for state updates.
    
    Helper function to create error details consistently across nodes.
    """
    return ErrorCategory.create_error_dict(error, agent_name)


def normalize_agent_name(agent_name: str) -> str:
    """Normalize human-readable agent names to node names.
    
    Converts names like "Route Planning Agent" to "route_planning_agent".
    Also handles invalid names like "location-specific_agents" by removing them.
    """
    # Invalid agent names that should be filtered out
    invalid_names = {
        "location-specific_agents",
        "location-specific agent",
        "location_specific_agents",
        "location_specific_agent",
        "location agents",
        "location_agents",
    }
    
    if agent_name.lower() in invalid_names:
        # Return empty string or None - caller should handle this
        # For now, return a safe default that will be filtered
        return ""
    
    # Mapping of common variations to node names
    name_mapping = {
        "route planning agent": "route_planning_agent",
        "route_planning_agent": "route_planning_agent",
        "blm agent": "blm_agent",
        "blm_agent": "blm_agent",
        "trail agent": "trail_agent",
        "trail_agent": "trail_agent",
        "geo agent": "geo_agent",
        "geo_agent": "geo_agent",
        "accommodation agent": "accommodation_agent",
        "accommodation_agent": "accommodation_agent",
        "planning agent": "planning_agent",
        "planning_agent": "planning_agent",
        "gear agent": "gear_agent",
        "gear_agent": "gear_agent",
        "weather agent": "weather_agent",
        "weather_agent": "weather_agent",
        "permits agent": "permits_agent",
        "permits_agent": "permits_agent",
        "safety agent": "safety_agent",
        "safety_agent": "safety_agent",
        "transportation agent": "transportation_agent",
        "transportation_agent": "transportation_agent",
        "food agent": "food_agent",
        "food_agent": "food_agent",
        "community agent": "community_agent",
        "community_agent": "community_agent",
        "photography agent": "photography_agent",
        "photography_agent": "photography_agent",
        "historical agent": "historical_agent",
        "historical_agent": "historical_agent",
        "bikepacking agent": "bikepacking_agent",
        "bikepacking_agent": "bikepacking_agent",
        "advocacy agent": "advocacy_agent",
        "advocacy_agent": "advocacy_agent",
        "jerome agent": "jerome_agent",
        "jerome_agent": "jerome_agent",
    }
    
    # Try exact match first (case-insensitive)
    normalized = name_mapping.get(agent_name.lower())
    if normalized:
        return normalized
    
    # Fallback: convert to lowercase, replace spaces with underscores, remove "agent" suffix
    normalized = agent_name.lower().strip()
    normalized = normalized.replace(" ", "_")
    if normalized.endswith("_agent"):
        return normalized
    if normalized.endswith("agent"):
        normalized = normalized[:-5].strip("_") + "_agent"
    return normalized


async def orchestrator_node(state: AdventureState) -> Dict[str, Any]:
    """Orchestrator node - analyzes request and determines routing.
    
    Uses structured output to extract intent from natural language,
    including location, duration, and skill level if mentioned.
    
    Can also handle recovery from LLM-recoverable errors by adjusting strategy
    based on error_details in state.
    """
    try:
        # Check for LLM-recoverable errors from previous agent executions
        error_details = state.get("error_details", [])
        llm_recoverable_errors = [
            err for err in error_details
            if err.get("type") == ErrorType.LLM_RECOVERABLE.value
        ]
        
        # If there are recoverable errors, include them in context for the orchestrator
        # to potentially adjust the strategy
        analysis = await orchestrator.analyze_request(
            state.get("user_input", ""),
            state.get("user_preferences"),
            error_context=llm_recoverable_errors if llm_recoverable_errors else None,
        )

        required_agents = analysis.get("required_agents", [])
        # Normalize agent names to node names (e.g., "Route Planning Agent" -> "route_planning_agent")
        # Filter out invalid/empty names
        required_agents = [normalize_agent_name(agent) for agent in required_agents]
        required_agents = [agent for agent in required_agents if agent]  # Remove empty strings
        agent_context = analysis.get("agent_context", {})
        # Normalize agent_context keys to node names
        agent_context = {normalize_agent_name(k): v for k, v in agent_context.items() if normalize_agent_name(k)}

        # Ensure activity_type is set in state
        activity_type = analysis.get("activity_type", "mountain_biking")
        
        # Update user_preferences with extracted information from natural language
        # This enhances text-to-adventure by using extracted data
        user_prefs = state.get("user_preferences")
        updated_preferences = dict(user_prefs) if user_prefs else {}
        
        # Use extracted location if available and not already in preferences
        if analysis.get("location") and not updated_preferences.get("region"):
            updated_preferences["region"] = analysis["location"]
        
        # Use extracted duration if available and not already in preferences
        if analysis.get("duration_days") and not updated_preferences.get("duration_days"):
            updated_preferences["duration_days"] = analysis["duration_days"]
        
        # Use extracted skill level if available and not already in preferences
        if analysis.get("skill_level") and not updated_preferences.get("skill_level"):
            updated_preferences["skill_level"] = analysis["skill_level"]
        
        # Ensure activity_type is set in preferences
        if not updated_preferences.get("activity_type"):
            updated_preferences["activity_type"] = activity_type
        
        # Clear LLM-recoverable errors that we've handled (they're in error_details for history)
        # We'll keep them in error_details but remove from active consideration
        
        return {
            "current_task": analysis.get("adventure_type", activity_type),
            "required_agents": required_agents,
            "agent_context": agent_context,
            "completed_agents": [],
            "user_preferences": updated_preferences if updated_preferences else user_prefs,
        }
    except Exception as e:
        # Orchestrator errors are critical - use standard error handling
        error_detail = ErrorCategory.create_error_dict(e, "orchestrator")
        return {
            "error_details": state.get("error_details", []) + [error_detail],
            "required_agents": ["geo_agent", "trail_agent"],  # Fallback
            "completed_agents": [],
            "agent_context": {},
        }


async def geo_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Geo agent node - provides geographic information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("geo_agent", user_input)
        
        # Extract location from user input or preferences
        user_prefs = state.get("user_preferences")
        location = user_prefs.get("region", "") if user_prefs else ""
        if not location:
            # Try to extract from user input
            location = user_input.split()[0] if user_input else "Unknown"

        # Add timeout to prevent hanging (30 seconds for geo lookup)
        geo_info = await asyncio.wait_for(
            geo_agent.get_location_info(location, context),
            timeout=30.0
        )

        return {
            "geo_info": geo_info,
            "completed_agents": ["geo_agent"],
        }
    except TimeoutError:
        logger = logging.getLogger(__name__)
        logger.warning(f"Geo agent timed out for location: {location}")
        return {
            "geo_info": {"location": location, "error": "timeout"},
            "completed_agents": ["geo_agent"],
        }
    except Exception as e:
        # Use enhanced error handling with categorization
        error_result = handle_agent_error(e, "geo_agent", state, None)
        if isinstance(error_result, Command):
            return error_result
        # Add geo_info to the result
        error_result["geo_info"] = None
        return error_result


async def trail_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Trail agent node - provides trail information for multiple activity types."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("trail_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""

        # Get activity type from preferences or default to mountain_biking
        activity_type = "mountain_biking"
        user_prefs = state.get("user_preferences")
        if user_prefs:
            activity_type = user_prefs.get("activity_type") or user_prefs.get("adventure_type", "mountain_biking")
        
        # Map skill level to difficulty based on activity type
        difficulty = None
        if user_prefs:
            skill_level = user_prefs.get("skill_level", "")
            if activity_type == "mountain_biking":
                skill_to_difficulty = {
                    "beginner": "green",
                    "intermediate": "blue",
                    "advanced": "black",
                    "expert": "double_black",
                }
            else:  # hiking, trail_running
                skill_to_difficulty = {
                    "beginner": "easy",
                    "intermediate": "intermediate",
                    "advanced": "difficult",
                    "expert": "expert",
                }
            difficulty = skill_to_difficulty.get(skill_level)

        # Add timeout to prevent hanging (45 seconds for trail search + LLM enhancement)
        trails = await asyncio.wait_for(
            trail_agent.search_trails(location, activity_type, difficulty, None, context),
            timeout=45.0
        )

        return {
            "trail_info": trails,
            "completed_agents": ["trail_agent"],
        }
    except TimeoutError:
        logger = logging.getLogger(__name__)
        logger.warning(f"Trail agent timed out for location: {location}")
        return {
            "trail_info": [],
            "completed_agents": ["trail_agent"],
        }
    except Exception as e:
        # Use enhanced error handling with categorization
        error_result = handle_agent_error(e, "trail_agent", state, [])
        if isinstance(error_result, Command):
            return error_result
        # Add trail_info to the result
        error_result["trail_info"] = []
        return error_result


async def blm_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """BLM agent node - provides BLM land information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("blm_agent", user_input)
        
        geo_info = state.get("geo_info")
        region = geo_info.get("region", "") if geo_info else ""
        if not region:
            user_prefs = state.get("user_preferences")
            region = user_prefs.get("region", "") if user_prefs else ""

        user_prefs = state.get("user_preferences")
        activity_type = user_prefs.get("adventure_type", "mountain_biking") if user_prefs else "mountain_biking"

        blm_info = await blm_agent.get_blm_information(region, activity_type, context)

        return {
            "blm_info": blm_info,
            "completed_agents": ["blm_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "blm_agent", state, [])
        if isinstance(error_result, Command):
            return error_result
        error_result["blm_info"] = []
        return error_result


async def accommodation_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Accommodation agent node - finds accommodations."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("accommodation_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""

        user_prefs = state.get("user_preferences")
        acc_type = None
        if user_prefs:
            acc_type = user_prefs.get("accommodation_preference", "camping")

        accommodations = await accommodation_agent.find_accommodations(
            location, acc_type, None, None, context
        )

        return {
            "accommodation_info": accommodations,
            "completed_agents": ["accommodation_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "accommodation_agent", state, [])
        if isinstance(error_result, Command):
            return error_result
        error_result["accommodation_info"] = []
        return error_result


async def gear_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Gear agent node - recommends gear and products."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("gear_agent", user_input)
        
        # Get activity type, fallback to adventure_type for backward compatibility
        activity_type = "mountain_biking"
        user_prefs = state.get("user_preferences")
        if user_prefs:
            activity_type = user_prefs.get("activity_type") or user_prefs.get("adventure_type", "mountain_biking")
        duration = user_prefs.get("duration_days", 1) if user_prefs else 1
        skill_level = user_prefs.get("skill_level", "intermediate") if user_prefs else "intermediate"
        gear_owned = user_prefs.get("gear_owned", []) if user_prefs else []

        gear_recs = await gear_agent.recommend_gear_for_adventure(
            activity_type, duration, skill_level, gear_owned, context
        )

        return {
            "gear_recommendations": gear_recs,
            "completed_agents": ["gear_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "gear_agent", state, [])
        if isinstance(error_result, Command):
            return error_result
        error_result["gear_recommendations"] = []
        return error_result


async def planning_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Planning agent node - creates detailed itinerary."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("planning_agent", user_input)
        
        trail_info = state.get("trail_info", [])
        trails = [dict(t) for t in trail_info] if trail_info else []
        geo_info = state.get("geo_info")
        start_location = geo_info.get("location", "") if geo_info else ""
        user_prefs = state.get("user_preferences")
        duration = user_prefs.get("duration_days", 1) if user_prefs else 1

        planning_info = await planning_agent.create_adventure_itinerary(
            trails, start_location, duration, user_prefs, context
        )

        return {
            "planning_info": planning_info,
            "completed_agents": ["planning_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "planning_agent", state, None)
        if isinstance(error_result, Command):
            return error_result
        error_result["planning_info"] = None
        return error_result


async def weather_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Weather agent node - provides weather and conditions information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("weather_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""
        
        activity_type = "mountain_biking"
        user_prefs = state.get("user_preferences")
        if user_prefs:
            activity_type = user_prefs.get("activity_type") or user_prefs.get("adventure_type", "mountain_biking")
        
        dates = user_prefs.get("dates", []) if user_prefs else None

        weather_info = await weather_agent.get_weather_info(location, dates, activity_type, context)

        return {
            "weather_info": weather_info,
            "completed_agents": ["weather_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "weather_agent", state, None)
        if isinstance(error_result, Command):
            return error_result
        error_result["weather_info"] = None
        return error_result


async def permits_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Permits agent node - provides permit and regulation information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("permits_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""
        
        activity_type = "mountain_biking"
        user_prefs = state.get("user_preferences")
        if user_prefs:
            activity_type = user_prefs.get("activity_type") or user_prefs.get("adventure_type", "mountain_biking")
        
        group_size = user_prefs.get("group_size", 1) if user_prefs else 1
        dates = user_prefs.get("dates", []) if user_prefs else None

        permits_info = await permits_agent.get_permit_info(location, activity_type, group_size, dates, context)

        return {
            "permits_info": permits_info,
            "completed_agents": ["permits_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "permits_agent", state, None)
        if isinstance(error_result, Command):
            return error_result
        error_result["permits_info"] = None
        return error_result


async def safety_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Safety agent node - provides safety and emergency information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("safety_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""
        
        activity_type = "mountain_biking"
        user_prefs = state.get("user_preferences")
        if user_prefs:
            activity_type = user_prefs.get("activity_type") or user_prefs.get("adventure_type", "mountain_biking")
        
        trail_info = state.get("trail_info", [])
        route_info = {
            "trails": [dict(t) for t in trail_info] if trail_info else [],
            "activity_type": activity_type,
        }

        safety_info = await safety_agent.get_safety_info(location, activity_type, route_info, context)

        return {
            "safety_info": safety_info,
            "completed_agents": ["safety_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "safety_agent", state, None)
        if isinstance(error_result, Command):
            return error_result
        error_result["safety_info"] = None
        return error_result


async def transportation_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Transportation agent node - provides transportation and logistics information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("transportation_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""
        
        user_prefs = state.get("user_preferences")
        route_type = user_prefs.get("route_type") if user_prefs else None

        transportation_info = await transportation_agent.get_transportation_info(location, None, route_type, context)

        return {
            "transportation_info": transportation_info,
            "completed_agents": ["transportation_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "transportation_agent", state, None)
        if isinstance(error_result, Command):
            return error_result
        error_result["transportation_info"] = None
        return error_result


async def food_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Food agent node - provides food and resupply information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("food_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""
        
        trail_info = state.get("trail_info", [])
        route_info = {
            "trails": [dict(t) for t in trail_info] if trail_info else [],
        }
        user_prefs = state.get("user_preferences")
        duration_days = user_prefs.get("duration_days", 1) if user_prefs else 1

        food_info = await food_agent.get_food_info(location, route_info, duration_days, context)

        return {
            "food_info": food_info,
            "completed_agents": ["food_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "food_agent", state, None)
        if isinstance(error_result, Command):
            return error_result
        error_result["food_info"] = None
        return error_result


async def community_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Community agent node - provides community and social information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("community_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""
        
        activity_type = "mountain_biking"
        user_prefs = state.get("user_preferences")
        if user_prefs:
            activity_type = user_prefs.get("activity_type") or user_prefs.get("adventure_type", "mountain_biking")

        community_info = await community_agent.get_community_info(location, activity_type, context)

        return {
            "community_info": community_info,
            "completed_agents": ["community_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "community_agent", state, None)
        if isinstance(error_result, Command):
            return error_result
        error_result["community_info"] = None
        return error_result


async def photography_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Photography agent node - provides photography and media information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("photography_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""
        
        trail_info = state.get("trail_info", [])
        route_info = {
            "trails": [dict(t) for t in trail_info] if trail_info else [],
        }

        photography_info = await photography_agent.get_photography_info(location, route_info, context)

        return {
            "photography_info": photography_info,
            "completed_agents": ["photography_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "photography_agent", state, None)
        if isinstance(error_result, Command):
            return error_result
        error_result["photography_info"] = None
        return error_result


async def historical_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Historical agent node - provides historical and cultural information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("historical_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""
        
        trail_info = state.get("trail_info", [])
        route_info = {
            "trails": [dict(t) for t in trail_info] if trail_info else [],
        }

        historical_info = await historical_agent.get_historical_info(location, route_info, context)

        return {
            "historical_info": historical_info,
            "completed_agents": ["historical_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "historical_agent", state, None)
        if isinstance(error_result, Command):
            return error_result
        error_result["historical_info"] = None
        return error_result


async def route_planning_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Route planning agent node - provides route planning information from RideWithGPS and Strava."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("route_planning_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""
        
        activity_type = "mountain_biking"
        user_prefs = state.get("user_preferences")
        if user_prefs:
            activity_type = user_prefs.get("activity_type") or user_prefs.get("adventure_type", "mountain_biking")
        
        distance = None
        if user_prefs:
            distance_pref = user_prefs.get("distance_preference")
            # Map distance preference to approximate miles
            if distance_pref == "short":
                distance = 10.0
            elif distance_pref == "medium":
                distance = 25.0
            elif distance_pref == "long":
                distance = 50.0
            elif distance_pref == "epic":
                distance = 100.0

        # Search both RideWithGPS and Strava routes in parallel
        ridewithgps_task = route_planning_agent.search_ridewithgps_routes(
            location, activity_type, distance, context
        )
        strava_task = route_planning_agent.search_strava_routes(
            location, activity_type, "popular", context
        )
        
        # Execute both searches concurrently
        ridewithgps_routes, strava_routes = await asyncio.gather(
            ridewithgps_task,
            strava_task,
            return_exceptions=True
        )
        
        # Handle exceptions gracefully
        if isinstance(ridewithgps_routes, Exception):
            ridewithgps_routes = []
        if isinstance(strava_routes, Exception):
            strava_routes = []

        # Combine routes from both sources
        all_routes = list(ridewithgps_routes) + list(strava_routes)

        return {
            "route_planning_info": all_routes,
            "completed_agents": ["route_planning_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "route_planning_agent", state, [])
        if isinstance(error_result, Command):
            return error_result
        error_result["route_planning_info"] = []
        return error_result


async def bikepacking_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Bikepacking agent node - provides bikepacking route information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("bikepacking_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""
        
        user_prefs = state.get("user_preferences")
        route_type = user_prefs.get("route_type") if user_prefs else None
        duration_days = user_prefs.get("duration_days", 1) if user_prefs else None

        # Search bikepacking.com and Bikepacking Roots routes in parallel
        bikepacking_task = bikepacking_agent.search_bikepacking_routes(
            location, route_type, duration_days, context
        )
        bikepacking_roots_task = bikepacking_agent.search_bikepacking_roots_routes(
            location, context
        )
        
        # Execute both searches concurrently
        bikepacking_routes, bikepacking_roots_routes = await asyncio.gather(
            bikepacking_task,
            bikepacking_roots_task,
            return_exceptions=True
        )
        
        # Handle exceptions gracefully
        if isinstance(bikepacking_routes, Exception):
            bikepacking_routes = []
        if isinstance(bikepacking_roots_routes, Exception):
            bikepacking_roots_routes = []

        # Combine routes from both sources
        all_routes = list(bikepacking_routes) + list(bikepacking_roots_routes)

        return {
            "bikepacking_info": all_routes,
            "completed_agents": ["bikepacking_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "bikepacking_agent", state, [])
        if isinstance(error_result, Command):
            return error_result
        error_result["bikepacking_info"] = []
        return error_result


async def advocacy_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    """Advocacy agent node - provides trail advocacy and long-distance route information."""
    try:
        agent_context = state.get("agent_context", {})
        user_input = state.get("user_input", "")
        context = agent_context.get("advocacy_agent", user_input)
        
        geo_info = state.get("geo_info")
        location = geo_info.get("location", "") if geo_info else ""
        if not location:
            user_prefs = state.get("user_preferences")
            location = user_prefs.get("region", "") if user_prefs else ""
        
        user_prefs = state.get("user_preferences")
        route_type = user_prefs.get("route_type") if user_prefs else None

        # Get IMBA, Adventure Cycling, and Trail Access information in parallel
        imba_task = advocacy_agent.get_imba_trail_info(location, context)
        adventure_cycling_task = advocacy_agent.search_adventure_cycling_routes(
            location, route_type, context
        )
        trail_access_task = advocacy_agent.get_trail_access_info(location)
        
        # Execute all three searches concurrently
        imba_info, adventure_cycling_routes, trail_access_info = await asyncio.gather(
            imba_task,
            adventure_cycling_task,
            trail_access_task,
            return_exceptions=True
        )
        
        # Handle exceptions gracefully
        if isinstance(imba_info, Exception):
            imba_info = {}
        if isinstance(adventure_cycling_routes, Exception):
            adventure_cycling_routes = []
        if isinstance(trail_access_info, Exception):
            trail_access_info = {}

        # Combine all advocacy information
        advocacy_info = {
            "imba_info": imba_info,
            "adventure_cycling_routes": adventure_cycling_routes,
            "trail_access_info": trail_access_info,
        }

        return {
            "advocacy_info": advocacy_info,
            "completed_agents": ["advocacy_agent"],
        }
    except Exception as e:
        error_result = handle_agent_error(e, "advocacy_agent", state, None)
        if isinstance(error_result, Command):
            return error_result
        error_result["advocacy_info"] = None
        return error_result


def create_location_agent_node(agent_name: str, agent_instance: LocationAgentBase):
    """Create a node function for a location agent.
    
    Args:
        agent_name: Name of the agent (e.g., "jerome_agent")
        agent_instance: Instance of the location agent
    
    Returns:
        Node function for the location agent
    """
    async def location_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
        """Location agent node - provides location-specific information."""
        try:
            agent_context = state.get("agent_context", {})
            user_input = state.get("user_input", "")
            context = agent_context.get(agent_name, user_input)
            
            geo_info = state.get("geo_info")
            location = geo_info.get("location", "") if geo_info else ""
            if not location:
                user_prefs = state.get("user_preferences")
                location = user_prefs.get("region", "") if user_prefs else ""
            if not location:
                location = user_input
            
            # Get activity type from preferences
            activity_type = "mountain_biking"
            user_prefs = state.get("user_preferences")
            if user_prefs:
                activity_type = user_prefs.get("activity_type") or user_prefs.get("adventure_type", "mountain_biking")
            
            # Collect existing agent outputs to enhance
            existing_outputs = {
                "geo_info": state.get("geo_info"),
                "historical_info": state.get("historical_info"),
                "trail_info": state.get("trail_info", []),
                "community_info": state.get("community_info"),
                "photography_info": state.get("photography_info"),
                "transportation_info": state.get("transportation_info"),
                "accommodation_info": state.get("accommodation_info", []),
                "food_info": state.get("food_info"),
            }
            
            location_info = await agent_instance.get_location_info(
                location, existing_outputs, context, activity_type
            )
            
            # Store in both location_info (generic) and agent-specific field (backward compat)
            result = {
                "location_info": location_info,
                "completed_agents": [agent_name],
            }
            
            return result
        except Exception as e:
            error_result = handle_agent_error(e, agent_name, state, None)
            if isinstance(error_result, Command):
                return error_result
            error_result["location_info"] = None
            return error_result
    
    return location_agent_node


# Create node functions for location agents
jerome_agent_node = create_location_agent_node("jerome_agent", jerome_agent)
sedona_agent_node = create_location_agent_node("sedona_agent", sedona_agent)
prescott_agent_node = create_location_agent_node("prescott_agent", prescott_agent)
flagstaff_agent_node = create_location_agent_node("flagstaff_agent", flagstaff_agent)
grand_canyon_agent_node = create_location_agent_node("grand_canyon_agent", grand_canyon_agent)
payson_agent_node = create_location_agent_node("payson_agent", payson_agent)
pine_agent_node = create_location_agent_node("pine_agent", pine_agent)
strawberry_agent_node = create_location_agent_node("strawberry_agent", strawberry_agent)
pinetop_agent_node = create_location_agent_node("pinetop_agent", pinetop_agent)
williams_agent_node = create_location_agent_node("williams_agent", williams_agent)
phoenix_agent_node = create_location_agent_node("phoenix_agent", phoenix_agent)
tucson_agent_node = create_location_agent_node("tucson_agent", tucson_agent)
cottonwood_agent_node = create_location_agent_node("cottonwood_agent", cottonwood_agent)
camp_verde_agent_node = create_location_agent_node("camp_verde_agent", camp_verde_agent)
show_low_agent_node = create_location_agent_node("show_low_agent", show_low_agent)
bisbee_agent_node = create_location_agent_node("bisbee_agent", bisbee_agent)
tombstone_agent_node = create_location_agent_node("tombstone_agent", tombstone_agent)
sierra_vista_agent_node = create_location_agent_node("sierra_vista_agent", sierra_vista_agent)
patagonia_agent_node = create_location_agent_node("patagonia_agent", patagonia_agent)
page_agent_node = create_location_agent_node("page_agent", page_agent)
kingman_agent_node = create_location_agent_node("kingman_agent", kingman_agent)
lake_havasu_agent_node = create_location_agent_node("lake_havasu_agent", lake_havasu_agent)
globe_miami_agent_node = create_location_agent_node("globe_miami_agent", globe_miami_agent)
springerville_eagar_agent_node = create_location_agent_node("springerville_eagar_agent", springerville_eagar_agent)
ajo_agent_node = create_location_agent_node("ajo_agent", ajo_agent)
sonoita_agent_node = create_location_agent_node("sonoita_agent", sonoita_agent)
yuma_agent_node = create_location_agent_node("yuma_agent", yuma_agent)
parker_agent_node = create_location_agent_node("parker_agent", parker_agent)


async def synthesize_node(state: AdventureState) -> Dict[str, Any]:
    """Synthesize final adventure plan from all agent outputs.
    
    If human feedback is provided (from a revision request), it will be
    incorporated into the plan synthesis.
    
    Supports early synthesis with partial data to improve response times.
    """
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        # Log state for debugging
        completed = state.get('completed_agents', [])
        required = state.get('required_agents', [])
        logger.info(f"Synthesizing plan. Completed: {completed}, Required: {required}")
        
        # Validate that we have some agent outputs before synthesizing
        has_any_data = (
            state.get("geo_info") or
            state.get("trail_info") or
            state.get("weather_info") or
            state.get("planning_info") or
            state.get("route_planning_info") or
            state.get("bikepacking_info")
        )
        
        if not has_any_data:
            logger.warning("No agent data available for synthesis. Creating minimal plan.")
            return {
                "adventure_plan": {
                    "title": "Adventure Plan",
                    "description": "Unable to generate complete plan - no agent data available.",
                    "error": "No agent outputs to synthesize",
                },
                "error_details": state.get("error_details", []) + [{"agent": "system", "type": "permanent", "message": "No agent data available for synthesis", "error_class": "SystemError"}],
            }
        
        # Include human feedback if this is a revision
        # Reduced timeout to 45 seconds for faster failure (synthesis should be quick with truncated data)
        try:
            plan = await asyncio.wait_for(
                orchestrator.synthesize_plan(state, human_feedback=state.get("human_feedback")),
                timeout=45.0
            )
        except TimeoutError:
            logger.error("Synthesize plan timed out after 45 seconds")
            return {
                "adventure_plan": {
                    "title": "Adventure Plan",
                    "description": "Plan synthesis timed out. Please try again.",
                    "error": "Synthesis timeout",
                },
                "error_details": state.get("error_details", []) + [{"agent": "system", "type": "permanent", "message": "Plan synthesis timed out", "error_class": "SystemError"}],
            }

        result = {
            "adventure_plan": plan,
        }
        # Clear human feedback after incorporating it (if it was provided)
        if state.get("human_feedback"):
            result["human_feedback"] = None
        
        logger.info("Plan synthesis completed successfully")
        return result
        
    except Exception as e:
        error_detail = create_error_detail(e, "synthesize")
        error_msg = str(e)
        logger.error(f"Synthesize error: {error_msg}", exc_info=True)
        return {
            "adventure_plan": {
                "title": "Adventure Plan",
                "description": f"Error generating plan: {error_msg}",
                "error": error_msg,
            },
            "error_details": state.get("error_details", []) + [error_detail],
        }


def should_continue(state: AdventureState) -> Literal["human_review", "synthesize"]:
    """Determine next step based on state."""
    # Check if all required agents have completed
    # Normalize agent names to handle any edge cases
    required = set(normalize_agent_name(agent) for agent in state.get("required_agents", []))
    completed = set(normalize_agent_name(agent) for agent in state.get("completed_agents", []))

    if required.issubset(completed):
        # Check if human review is needed
        if orchestrator.should_request_human_review(state):
            return "human_review"
        return "synthesize"
    
    # Still need to call more agents
    return "synthesize"  # Will be handled by routing logic


async def human_review_node(state: AdventureState) -> Dict[str, Any]:
    """Human-in-the-loop review checkpoint.
    
    Pauses execution and waits for human review of the adventure plan.
    The interrupt() call pauses the graph and waits for human input.
    When resumed, the human's decision is returned and stored in state.
    
    Interrupt Payload Format:
    The interrupt() call passes the following data structure:
    {
        "message": str,  # Review request message
        "adventure_plan": Dict[str, Any] | None,  # The plan to review
        "user_input": str,  # Original user request
        "user_preferences": Dict[str, Any] | None,  # User preferences
        "error_details": List[Dict[str, Any]],  # Any errors encountered
        "completed_agents": List[str],  # Agents that have completed
    }
    
    Resume Command Format:
    When resuming with Command(resume={...}), the payload should be:
    {
        "status": str,  # "approved", "rejected", or "needs_revision"
        "feedback": str,  # Optional feedback for revisions
    }
    """
    # Prepare review information for the human
    review_data = {
        "message": "Please review the adventure plan before finalization",
        "adventure_plan": state.get("adventure_plan"),
        "user_input": state.get("user_input", ""),
        "user_preferences": state.get("user_preferences"),
        "error_details": state.get("error_details", []),
        "completed_agents": state.get("completed_agents", []),
    }
    
    # Pause execution and wait for human decision
    # The interrupt() call returns the value passed when resuming with Command
    human_decision = interrupt(review_data)
    
    # Extract decision from the resume command
    # human_decision will be a dict with keys like "status", "feedback", etc.
    approval_status = human_decision.get("status", "pending")
    human_feedback = human_decision.get("feedback", "")
    
    return {
        "needs_human_review": False,  # Review completed
        "approval_status": approval_status,  # "approved", "rejected", "needs_revision"
        "human_feedback": human_feedback,
    }


async def archive_node(state: AdventureState) -> Dict[str, Any]:
    """Archive completed adventure plan for future use.
    
    This node saves the complete state including the adventure plan
    to the configured archive backend (SQLite, JSON files, etc.).
    
    Note: user_id and session_id can be added to state if needed for filtering.
    """
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Only archive if we have a completed plan
    if state.get("adventure_plan"):
        try:
            # Extract user_id and session_id from state if available
            # These can be set in the initial state if needed for filtering
            user_id = state.get("user_id")
            session_id = state.get("session_id")
            
            # Run archive_plan in a thread to avoid blocking the event loop
            # archive_plan may perform blocking I/O operations (e.g., os.mkdir)
            archive_id = await asyncio.to_thread(
                archive_plan, state, user_id=user_id, session_id=session_id
            )
            if archive_id:
                logger.info(f"Adventure plan archived with ID: {archive_id}")
                return {
                    "archive_id": archive_id,
                }
            else:
                logger.debug("Archiving is disabled or failed silently")
        except Exception as e:
            # Don't fail the workflow if archiving fails
            logger.error(f"Failed to archive plan: {e}", exc_info=True)
    
    return {}


# Define agent dependencies - which agents need outputs from other agents
AGENT_DEPENDENCIES: Dict[str, List[str]] = {
    "geo_agent": [],  # No dependencies - can run first
    "weather_agent": [],  # Can run in parallel with geo_agent (uses location from preferences if geo_info not available)
    "permits_agent": [],  # Can run in parallel (uses location from preferences if geo_info not available)
    "gear_agent": [],  # No dependencies on other agents
    "community_agent": [],  # Can run in parallel (uses location from preferences if geo_info not available)
    "blm_agent": [],  # Can run in parallel (uses location from preferences if geo_info not available)
    "advocacy_agent": [],  # Can run in parallel (uses location from preferences if geo_info not available)
    "transportation_agent": [],  # Can run in parallel (uses location from preferences if geo_info not available)
    "accommodation_agent": [],  # Can run in parallel (uses location from preferences if geo_info not available)
    "trail_agent": ["geo_agent"],  # Prefers geo_info but can fallback to preferences
    "route_planning_agent": [],  # Can run in parallel (uses location from preferences if geo_info not available)
    "bikepacking_agent": [],  # Can run in parallel (uses location from preferences if geo_info not available)
    "photography_agent": ["trail_agent"],  # Uses trail_info but can work without it
    "historical_agent": ["trail_agent"],  # Uses trail_info but can work without it
    "food_agent": ["trail_agent"],  # Uses trail_info but can work without it
    "safety_agent": ["trail_agent"],  # Uses trail_info but can work without it
    "planning_agent": ["trail_agent", "geo_agent"],  # Needs trail_info and geo_info
    "jerome_agent": [],  # Can run in parallel, enhances other agent outputs
}


def check_dependencies_met(agent: str, completed: set, state: AdventureState) -> bool:
    """Check if all dependencies for an agent are met.
    
    An agent's dependencies are met if:
    1. All required agent dependencies are completed, OR
    2. The agent can work with fallback data (e.g., from preferences)
    """
    dependencies = AGENT_DEPENDENCIES.get(agent, [])
    
    # If no dependencies, agent can always run
    if not dependencies:
        return True
    
    # Check if all required agent dependencies are completed
    for dep in dependencies:
        if dep not in completed:
            # Check if agent can work with fallback data
            # Most agents can work with user_preferences as fallback
            if agent in ["trail_agent", "photography_agent", "historical_agent", 
                        "food_agent", "safety_agent"]:
                # These agents prefer trail_info but can work without it
                if dep == "trail_agent":
                    continue  # Can work without trail_info
            if agent == "planning_agent":
                # Planning agent really needs trail_info and geo_info
                # But we can be lenient - it will create a minimal plan if data is missing
                if state.get("trail_info") or state.get("geo_info"):
                    continue  # Has some data, can proceed
            return False
    
    return True


def route_to_agents(state: AdventureState) -> str | List[str]:
    """Route to next required agent(s) - returns a list to enable parallel execution.
    
    Returns a list of agent names that can run in parallel (all dependencies met).
    Returns "synthesize" if all agents are completed OR if core agents are done (early synthesis).
    
    IMPORTANT: Never returns None - always returns a valid string or list of strings.
    This prevents LangGraph visualization errors.
    """
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Core agents that are essential for a basic plan
    CORE_AGENTS = {"geo_agent", "trail_agent", "weather_agent"}
    
    # Get edge mapping first to validate all returns
    try:
        edge_mapping = get_all_agent_edges()
    except (NameError, AttributeError):
        # Fallback if not available yet
        edge_mapping = {"synthesize": "synthesize"}
    
    # Normalize agent names to handle any edge cases
    # Filter out empty strings and None values from normalization
    required = {
        normalized for agent in state.get("required_agents", [])
        if agent and (normalized := normalize_agent_name(agent)) and normalized.strip() and normalized in edge_mapping
    }
    completed = {
        normalized for agent in state.get("completed_agents", [])
        if agent and (normalized := normalize_agent_name(agent)) and normalized.strip() and normalized in edge_mapping
    }
    remaining = required - completed

    # Early synthesis: If core agents are done and we have some data, we can synthesize
    # This prevents waiting for all optional agents
    core_completed = CORE_AGENTS.intersection(completed)
    has_core_data = (
        state.get("geo_info") or 
        state.get("trail_info") or 
        state.get("weather_info")
    )
    
    # If all required agents are completed, synthesize
    if not remaining:
        logger.debug("All required agents completed, routing to synthesize")
        return "synthesize"
    
    # Early synthesis: If core agents done and we have data, synthesize with what we have
    # Only do this if we have at least 2 core agents or substantial data
    if core_completed and has_core_data:
        # Check if remaining agents are all optional (non-core)
        remaining_are_optional = not any(agent in CORE_AGENTS for agent in remaining)
        if remaining_are_optional and len(core_completed) >= 2:
            logger.info(
                f"Core agents completed ({core_completed}), synthesizing early. "
                f"Optional agents remaining: {remaining}"
            )
            return "synthesize"

    # Find all agents that are ready to run (dependencies met)
    ready_agents = []
    # Get edge mapping - use global if available, otherwise build it
    try:
        edge_mapping = get_all_agent_edges()
    except NameError:
        # If get_all_agent_edges isn't available yet, build minimal mapping
        edge_mapping = {"synthesize": "synthesize"}
    
    for agent in remaining:
        # Filter out None, empty strings, or invalid agent names
        # Also ensure the agent is in the edge mapping to avoid visualization errors
        if (agent and isinstance(agent, str) and agent.strip() and 
            agent in edge_mapping and check_dependencies_met(agent, completed, state)):
            ready_agents.append(agent)
    
    # If we have ready agents, return them as a list for parallel execution
    if ready_agents:
        # LangGraph supports returning lists from conditional edges
        # When a list is returned, all nodes in the list execute in parallel
        # This significantly improves performance when multiple independent agents can run simultaneously
        # Final validation: ensure all agents are in edge mapping (prevents visualization errors)
        validated_ready = [agent for agent in ready_agents if agent in edge_mapping]
        if validated_ready:
            logger.info(f"Routing to {len(validated_ready)} agents in parallel: {validated_ready}")
            return validated_ready
        # If somehow no agents are valid, fall through to synthesize
    
    # If no agents are ready yet, we might have a circular dependency or missing data
    # Fallback: return the first remaining agent (it will handle missing data gracefully)
    if remaining:
        # Filter out None, empty strings, or invalid agent names
        # Also ensure the agent is in the edge mapping to avoid visualization errors
        valid_remaining = [
            agent for agent in remaining 
            if agent and isinstance(agent, str) and agent.strip() and agent in edge_mapping
        ]
        if valid_remaining:
            fallback_agent = valid_remaining[0]
            logger.warning(
                f"No agents ready yet. Remaining: {remaining}, Completed: {completed}. "
                f"Falling back to: {fallback_agent}"
            )
            return fallback_agent
    
    logger.debug("No remaining agents, routing to synthesize")
    return "synthesize"


def get_all_agent_edges() -> Dict[str, str]:
    """Get edge mappings for all agents.
    
    Supports both single agent names and lists of agent names for parallel execution.
    When route_to_agents returns a list, LangGraph will route to all agents in parallel.
    
    Note: When nodes return Command, LangGraph automatically routes to the specified node.
    We include "orchestrator" here for completeness, though Command handles routing directly.
    """
    agents = [
        "geo_agent",
        "weather_agent",
        "permits_agent",
        "safety_agent",
        "trail_agent",
        "route_planning_agent",
        "bikepacking_agent",
        "blm_agent",
        "advocacy_agent",
        "transportation_agent",
        "accommodation_agent",
        "food_agent",
        "gear_agent",
        "community_agent",
        "planning_agent",
        "photography_agent",
        "historical_agent",
        "jerome_agent",
        "sedona_agent",
        "prescott_agent",
        "flagstaff_agent",
        "grand_canyon_agent",
        "payson_agent",
        "pine_agent",
        "strawberry_agent",
        "pinetop_agent",
        "williams_agent",
        "phoenix_agent",
        "tucson_agent",
        "cottonwood_agent",
        "camp_verde_agent",
        "show_low_agent",
    ]
    
    # Add all registered location agents
    location_agents = get_all_location_agents()
    for agent_name in location_agents.keys():
        # Filter out None values and ensure agent_name is a valid string
        if agent_name and isinstance(agent_name, str) and agent_name not in agents:
            agents.append(agent_name)
    
    # Filter out any None or invalid values and ensure all are strings
    agents = [agent for agent in agents if agent and isinstance(agent, str) and agent.strip()]
    
    # Build edge mapping - ensure no None keys or values
    # This mapping is used by LangGraph to route conditional edges
    # All possible return values from route_to_agents MUST be keys in this dict
    edges: Dict[str, str] = {}
    
    # Add all agent nodes - each agent routes to itself
    for agent in agents:
        if agent and isinstance(agent, str) and agent.strip():
            # Ensure both key and value are valid strings
            edges[str(agent)] = str(agent)
    
    # Add special nodes that route_to_agents can return
    edges["synthesize"] = "synthesize"
    edges["orchestrator"] = "orchestrator"  # For Command-based error recovery
    edges["human_review"] = "human_review"
    edges["archive"] = "archive"
    
    # LangGraph automatically handles lists returned from conditional edges
    # Each agent name in the list will be routed to its corresponding node
    # LangGraph also automatically handles Command returns for direct routing
    
    # Final validation: ensure no None, empty string, or invalid values
    # This prevents LangGraph visualization errors when sorting edge tuples
    validated_edges: Dict[str, str] = {}
    for k, v in edges.items():
        if (k is not None and v is not None and 
            isinstance(k, str) and isinstance(v, str) and
            k.strip() and v.strip()):
            validated_edges[k.strip()] = v.strip()
    
    return validated_edges


# Build the graph
# Note: We don't pass edge mapping to conditional edges that return lists
# LangGraph handles list returns automatically without needing explicit mapping
all_agent_edges = get_all_agent_edges()

# Retry policy for nodes that make external API calls
# Retries transient failures (network issues, rate limits) with exponential backoff
api_retry_policy = RetryPolicy(
    max_attempts=3,
    initial_interval=1.0,  # Start with 1 second delay
    backoff_factor=2.0,  # Double delay on each retry
)

graph_builder = (
    StateGraph(AdventureState, context_schema=Context)
    .add_node("orchestrator", orchestrator_node)
    # Nodes with external API calls get retry policies
    .add_node("geo_agent", geo_agent_node, retry_policy=api_retry_policy)
    .add_node("weather_agent", weather_agent_node, retry_policy=api_retry_policy)
    .add_node("permits_agent", permits_agent_node, retry_policy=api_retry_policy)
    .add_node("safety_agent", safety_agent_node, retry_policy=api_retry_policy)
    .add_node("trail_agent", trail_agent_node, retry_policy=api_retry_policy)
    .add_node("route_planning_agent", route_planning_agent_node, retry_policy=api_retry_policy)
    .add_node("bikepacking_agent", bikepacking_agent_node, retry_policy=api_retry_policy)
    .add_node("blm_agent", blm_agent_node, retry_policy=api_retry_policy)
    .add_node("advocacy_agent", advocacy_agent_node, retry_policy=api_retry_policy)
    .add_node("transportation_agent", transportation_agent_node, retry_policy=api_retry_policy)
    .add_node("accommodation_agent", accommodation_agent_node, retry_policy=api_retry_policy)
    .add_node("food_agent", food_agent_node, retry_policy=api_retry_policy)
    .add_node("gear_agent", gear_agent_node, retry_policy=api_retry_policy)
    .add_node("community_agent", community_agent_node, retry_policy=api_retry_policy)
    .add_node("planning_agent", planning_agent_node, retry_policy=api_retry_policy)
    .add_node("photography_agent", photography_agent_node, retry_policy=api_retry_policy)
    .add_node("historical_agent", historical_agent_node, retry_policy=api_retry_policy)
    .add_node("jerome_agent", jerome_agent_node, retry_policy=api_retry_policy)
    .add_node("sedona_agent", sedona_agent_node, retry_policy=api_retry_policy)
    .add_node("prescott_agent", prescott_agent_node, retry_policy=api_retry_policy)
    .add_node("flagstaff_agent", flagstaff_agent_node, retry_policy=api_retry_policy)
    .add_node("grand_canyon_agent", grand_canyon_agent_node, retry_policy=api_retry_policy)
    .add_node("payson_agent", payson_agent_node, retry_policy=api_retry_policy)
    .add_node("pine_agent", pine_agent_node, retry_policy=api_retry_policy)
    .add_node("strawberry_agent", strawberry_agent_node, retry_policy=api_retry_policy)
    .add_node("pinetop_agent", pinetop_agent_node, retry_policy=api_retry_policy)
    .add_node("williams_agent", williams_agent_node, retry_policy=api_retry_policy)
    .add_node("phoenix_agent", phoenix_agent_node, retry_policy=api_retry_policy)
    .add_node("tucson_agent", tucson_agent_node, retry_policy=api_retry_policy)
    .add_node("cottonwood_agent", cottonwood_agent_node, retry_policy=api_retry_policy)
    .add_node("camp_verde_agent", camp_verde_agent_node, retry_policy=api_retry_policy)
    .add_node("show_low_agent", show_low_agent_node, retry_policy=api_retry_policy)
    .add_node("bisbee_agent", bisbee_agent_node, retry_policy=api_retry_policy)
    .add_node("tombstone_agent", tombstone_agent_node, retry_policy=api_retry_policy)
    .add_node("sierra_vista_agent", sierra_vista_agent_node, retry_policy=api_retry_policy)
    .add_node("patagonia_agent", patagonia_agent_node, retry_policy=api_retry_policy)
    .add_node("page_agent", page_agent_node, retry_policy=api_retry_policy)
    .add_node("kingman_agent", kingman_agent_node, retry_policy=api_retry_policy)
    .add_node("lake_havasu_agent", lake_havasu_agent_node, retry_policy=api_retry_policy)
    .add_node("globe_miami_agent", globe_miami_agent_node, retry_policy=api_retry_policy)
    .add_node("springerville_eagar_agent", springerville_eagar_agent_node, retry_policy=api_retry_policy)
    .add_node("ajo_agent", ajo_agent_node, retry_policy=api_retry_policy)
    .add_node("sonoita_agent", sonoita_agent_node, retry_policy=api_retry_policy)
    .add_node("yuma_agent", yuma_agent_node, retry_policy=api_retry_policy)
    .add_node("parker_agent", parker_agent_node, retry_policy=api_retry_policy)
    .add_node("synthesize", synthesize_node)
    .add_node("human_review", human_review_node)
    .add_node("archive", archive_node)
    .add_edge("__start__", "orchestrator")
    # Conditional edges: route_to_agents can return strings or lists
    # When returning lists, LangGraph handles parallel execution automatically
    # We don't provide edge mapping here - LangGraph uses return values directly as node names
    # This prevents visualization errors with None values in edge tuples
    .add_conditional_edges("orchestrator", route_to_agents)
    .add_conditional_edges("geo_agent", route_to_agents)
    .add_conditional_edges("weather_agent", route_to_agents)
    .add_conditional_edges("permits_agent", route_to_agents)
    .add_conditional_edges("safety_agent", route_to_agents)
    .add_conditional_edges("trail_agent", route_to_agents)
    .add_conditional_edges("route_planning_agent", route_to_agents)
    .add_conditional_edges("bikepacking_agent", route_to_agents)
    .add_conditional_edges("blm_agent", route_to_agents)
    .add_conditional_edges("advocacy_agent", route_to_agents)
    .add_conditional_edges("transportation_agent", route_to_agents)
    .add_conditional_edges("accommodation_agent", route_to_agents)
    .add_conditional_edges("food_agent", route_to_agents)
    .add_conditional_edges("gear_agent", route_to_agents)
    .add_conditional_edges("community_agent", route_to_agents)
    .add_conditional_edges("planning_agent", route_to_agents)
    .add_conditional_edges("photography_agent", route_to_agents)
    .add_conditional_edges("historical_agent", route_to_agents)
    .add_conditional_edges("jerome_agent", route_to_agents)
    .add_conditional_edges("sedona_agent", route_to_agents)
    .add_conditional_edges("prescott_agent", route_to_agents)
    .add_conditional_edges("flagstaff_agent", route_to_agents)
    .add_conditional_edges("grand_canyon_agent", route_to_agents)
    .add_conditional_edges("payson_agent", route_to_agents)
    .add_conditional_edges("pine_agent", route_to_agents)
    .add_conditional_edges("strawberry_agent", route_to_agents)
    .add_conditional_edges("pinetop_agent", route_to_agents)
    .add_conditional_edges("williams_agent", route_to_agents)
    .add_conditional_edges("phoenix_agent", route_to_agents)
    .add_conditional_edges("tucson_agent", route_to_agents)
    .add_conditional_edges("cottonwood_agent", route_to_agents)
    .add_conditional_edges("camp_verde_agent", route_to_agents)
    .add_conditional_edges("show_low_agent", route_to_agents)
    .add_conditional_edges("bisbee_agent", route_to_agents)
    .add_conditional_edges("tombstone_agent", route_to_agents)
    .add_conditional_edges("sierra_vista_agent", route_to_agents)
    .add_conditional_edges("patagonia_agent", route_to_agents)
    .add_conditional_edges("page_agent", route_to_agents)
    .add_conditional_edges("kingman_agent", route_to_agents)
    .add_conditional_edges("lake_havasu_agent", route_to_agents)
    .add_conditional_edges("globe_miami_agent", route_to_agents)
    .add_conditional_edges("springerville_eagar_agent", route_to_agents)
    .add_conditional_edges("ajo_agent", route_to_agents)
    .add_conditional_edges("sonoita_agent", route_to_agents)
    .add_conditional_edges("yuma_agent", route_to_agents)
    .add_conditional_edges("parker_agent", route_to_agents)
    .add_conditional_edges(
        "synthesize",
        lambda state: "human_review" if state.get("needs_human_review", False) else "archive",
        {
            "human_review": "human_review",
            "archive": "archive",
        },
    )
    .add_conditional_edges(
        "human_review",
        lambda state: "synthesize" if state.get("approval_status") == "needs_revision" else "archive",
        {
            "synthesize": "synthesize",
            "archive": "archive",
        },
    )
    .add_edge("archive", END)
)

# Compile with checkpointer if configured
# Note: When using LangGraph API, checkpointing is handled automatically
# and any checkpointer passed here will be replaced by the API's checkpointer
compile_kwargs = {"name": "Adventure Agent"}
if _checkpointer is not None:
    compile_kwargs["checkpointer"] = _checkpointer

graph = graph_builder.compile(**compile_kwargs)


def create_graph_config(
    thread_id: str | None = None,
    user_id: str | None = None,
    session_id: str | None = None,
    max_concurrency: int | None = None,
) -> Dict[str, Any]:
    """Create a configuration dict for graph invocation with max_concurrency support.
    
    Args:
        thread_id: Optional thread ID for checkpointing
        user_id: Optional user ID for tracking
        session_id: Optional session ID for grouping requests
        max_concurrency: Optional max concurrent tasks (defaults to Config.MAX_CONCURRENCY)
    
    Returns:
        Configuration dict for graph.invoke() or graph.ainvoke()
    
    Example:
        ```python
        config = create_graph_config(thread_id="thread123", max_concurrency=20)
        result = await graph.ainvoke(input_state, config=config)
        ```
    """
    config: Dict[str, Any] = {"configurable": {}}
    
    if thread_id:
        config["configurable"]["thread_id"] = thread_id
    if user_id:
        config["configurable"]["user_id"] = user_id
    if session_id:
        config["configurable"]["session_id"] = session_id
    
    # Set max_concurrency from parameter or Config
    concurrency = max_concurrency if max_concurrency is not None else Config.MAX_CONCURRENCY
    if concurrency is not None:
        config["configurable"]["max_concurrency"] = concurrency
    
    return config

