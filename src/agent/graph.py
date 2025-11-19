"""Main LangGraph for adventure agent system."""

from __future__ import annotations

from typing import Any, Dict, Literal

from langgraph.graph import StateGraph, END
from langgraph.types import RetryPolicy, interrupt
from typing_extensions import TypedDict

from agent.config import Config

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

from agent.state import AdventureState
from agent.agents import (
    OrchestratorAgent,
    BLMAgent,
    TrailAgent,
    GeoAgent,
    AccommodationAgent,
    PlanningAgent,
    GearAgent,
    WeatherAgent,
    PermitsAgent,
    SafetyAgent,
    TransportationAgent,
    FoodAgent,
    CommunityAgent,
    PhotographyAgent,
    HistoricalAgent,
    RoutePlanningAgent,
    BikepackingAgent,
    AdvocacyAgent,
)


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


async def orchestrator_node(state: AdventureState) -> Dict[str, Any]:
    """Orchestrator node - analyzes request and determines routing.
    
    Uses structured output to extract intent from natural language,
    including location, duration, and skill level if mentioned.
    """
    try:
        analysis = await orchestrator.analyze_request(
            state.user_input, state.user_preferences
        )

        required_agents = analysis.get("required_agents", [])
        agent_context = analysis.get("agent_context", {})

        # Ensure activity_type is set in state
        activity_type = analysis.get("activity_type", "mountain_biking")
        
        # Update user_preferences with extracted information from natural language
        # This enhances text-to-adventure by using extracted data
        updated_preferences = dict(state.user_preferences) if state.user_preferences else {}
        
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
        
        return {
            "current_task": analysis.get("adventure_type", activity_type),
            "required_agents": required_agents,
            "agent_context": agent_context,
            "completed_agents": [],
            "user_preferences": updated_preferences if updated_preferences else state.user_preferences,
        }
    except Exception as e:
        error_msg = f"Orchestrator error: {str(e)}"
        return {
            "errors": state.get("errors", []) + [error_msg],
            "required_agents": ["geo_agent", "trail_agent"],  # Fallback
            "completed_agents": [],
            "agent_context": {},
        }


async def geo_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Geo agent node - provides geographic information."""
    try:
        context = state.agent_context.get("geo_agent", state.user_input)
        
        # Extract location from user input or preferences
        location = state.user_preferences.get("region", "") if state.user_preferences else ""
        if not location:
            # Try to extract from user input
            location = state.user_input.split()[0] if state.user_input else "Unknown"

        geo_info = await geo_agent.get_location_info(location, context)

        return {
            "geo_info": geo_info,
            "completed_agents": state.get("completed_agents", []) + ["geo_agent"],
        }
    except Exception as e:
        error_msg = f"Geo agent error: {str(e)}"
        return {
            "geo_info": None,
            "completed_agents": state.get("completed_agents", []) + ["geo_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def trail_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Trail agent node - provides trail information for multiple activity types."""
    try:
        context = state.agent_context.get("trail_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""

        # Get activity type from preferences or default to mountain_biking
        activity_type = "mountain_biking"
        if state.user_preferences:
            activity_type = state.user_preferences.get("activity_type") or state.user_preferences.get("adventure_type", "mountain_biking")
        
        # Map skill level to difficulty based on activity type
        difficulty = None
        if state.user_preferences:
            skill_level = state.user_preferences.get("skill_level", "")
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

        trails = await trail_agent.search_trails(location, activity_type, difficulty, None, context)

        return {
            "trail_info": trails,
            "completed_agents": state.completed_agents + ["trail_agent"],
        }
    except Exception as e:
        error_msg = f"Trail agent error: {str(e)}"
        return {
            "trail_info": [],
            "completed_agents": state.completed_agents + ["trail_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def blm_agent_node(state: AdventureState) -> Dict[str, Any]:
    """BLM agent node - provides BLM land information."""
    try:
        context = state.agent_context.get("blm_agent", state.user_input)
        
        region = state.geo_info.get("region", "") if state.geo_info else ""
        if not region:
            region = state.user_preferences.get("region", "") if state.user_preferences else ""

        activity_type = state.user_preferences.get("adventure_type", "mountain_biking") if state.user_preferences else "mountain_biking"

        blm_info = await blm_agent.get_blm_information(region, activity_type, context)

        return {
            "blm_info": blm_info,
            "completed_agents": state.completed_agents + ["blm_agent"],
        }
    except Exception as e:
        error_msg = f"BLM agent error: {str(e)}"
        return {
            "blm_info": [],
            "completed_agents": state.completed_agents + ["blm_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def accommodation_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Accommodation agent node - finds accommodations."""
    try:
        context = state.agent_context.get("accommodation_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""

        acc_type = None
        if state.user_preferences:
            acc_type = state.user_preferences.get("accommodation_preference", "camping")

        accommodations = await accommodation_agent.find_accommodations(
            location, acc_type, None, None, context
        )

        return {
            "accommodation_info": accommodations,
            "completed_agents": state.completed_agents + ["accommodation_agent"],
        }
    except Exception as e:
        error_msg = f"Accommodation agent error: {str(e)}"
        return {
            "accommodation_info": [],
            "completed_agents": state.completed_agents + ["accommodation_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def gear_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Gear agent node - recommends gear and products."""
    try:
        context = state.agent_context.get("gear_agent", state.user_input)
        
        # Get activity type, fallback to adventure_type for backward compatibility
        activity_type = "mountain_biking"
        if state.user_preferences:
            activity_type = state.user_preferences.get("activity_type") or state.user_preferences.get("adventure_type", "mountain_biking")
        duration = state.user_preferences.get("duration_days", 1) if state.user_preferences else 1
        skill_level = state.user_preferences.get("skill_level", "intermediate") if state.user_preferences else "intermediate"
        gear_owned = state.user_preferences.get("gear_owned", []) if state.user_preferences else []

        gear_recs = await gear_agent.recommend_gear_for_adventure(
            activity_type, duration, skill_level, gear_owned, context
        )

        return {
            "gear_recommendations": gear_recs,
            "completed_agents": state.completed_agents + ["gear_agent"],
        }
    except Exception as e:
        error_msg = f"Gear agent error: {str(e)}"
        return {
            "gear_recommendations": [],
            "completed_agents": state.completed_agents + ["gear_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def planning_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Planning agent node - creates detailed itinerary."""
    try:
        context = state.agent_context.get("planning_agent", state.user_input)
        
        trails = [dict(t) for t in state.trail_info] if state.trail_info else []
        start_location = state.geo_info.get("location", "") if state.geo_info else ""
        duration = state.user_preferences.get("duration_days", 1) if state.user_preferences else 1

        planning_info = await planning_agent.create_adventure_itinerary(
            trails, start_location, duration, state.user_preferences, context
        )

        return {
            "planning_info": planning_info,
            "completed_agents": state.completed_agents + ["planning_agent"],
        }
    except Exception as e:
        error_msg = f"Planning agent error: {str(e)}"
        return {
            "planning_info": None,
            "completed_agents": state.completed_agents + ["planning_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def weather_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Weather agent node - provides weather and conditions information."""
    try:
        context = state.agent_context.get("weather_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""
        
        activity_type = "mountain_biking"
        if state.user_preferences:
            activity_type = state.user_preferences.get("activity_type") or state.user_preferences.get("adventure_type", "mountain_biking")
        
        dates = state.user_preferences.get("dates", []) if state.user_preferences else None

        weather_info = await weather_agent.get_weather_info(location, dates, activity_type, context)

        return {
            "weather_info": weather_info,
            "completed_agents": state.completed_agents + ["weather_agent"],
        }
    except Exception as e:
        error_msg = f"Weather agent error: {str(e)}"
        return {
            "weather_info": None,
            "completed_agents": state.completed_agents + ["weather_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def permits_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Permits agent node - provides permit and regulation information."""
    try:
        context = state.agent_context.get("permits_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""
        
        activity_type = "mountain_biking"
        if state.user_preferences:
            activity_type = state.user_preferences.get("activity_type") or state.user_preferences.get("adventure_type", "mountain_biking")
        
        group_size = state.user_preferences.get("group_size", 1) if state.user_preferences else 1
        dates = state.user_preferences.get("dates", []) if state.user_preferences else None

        permits_info = await permits_agent.get_permit_info(location, activity_type, group_size, dates, context)

        return {
            "permits_info": permits_info,
            "completed_agents": state.completed_agents + ["permits_agent"],
        }
    except Exception as e:
        error_msg = f"Permits agent error: {str(e)}"
        return {
            "permits_info": None,
            "completed_agents": state.completed_agents + ["permits_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def safety_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Safety agent node - provides safety and emergency information."""
    try:
        context = state.agent_context.get("safety_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""
        
        activity_type = "mountain_biking"
        if state.user_preferences:
            activity_type = state.user_preferences.get("activity_type") or state.user_preferences.get("adventure_type", "mountain_biking")
        
        route_info = {
            "trails": [dict(t) for t in state.trail_info] if state.trail_info else [],
            "activity_type": activity_type,
        }

        safety_info = await safety_agent.get_safety_info(location, activity_type, route_info, context)

        return {
            "safety_info": safety_info,
            "completed_agents": state.completed_agents + ["safety_agent"],
        }
    except Exception as e:
        error_msg = f"Safety agent error: {str(e)}"
        return {
            "safety_info": None,
            "completed_agents": state.completed_agents + ["safety_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def transportation_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Transportation agent node - provides transportation and logistics information."""
    try:
        context = state.agent_context.get("transportation_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""
        
        route_type = state.user_preferences.get("route_type") if state.user_preferences else None

        transportation_info = await transportation_agent.get_transportation_info(location, None, route_type, context)

        return {
            "transportation_info": transportation_info,
            "completed_agents": state.completed_agents + ["transportation_agent"],
        }
    except Exception as e:
        error_msg = f"Transportation agent error: {str(e)}"
        return {
            "transportation_info": None,
            "completed_agents": state.completed_agents + ["transportation_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def food_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Food agent node - provides food and resupply information."""
    try:
        context = state.agent_context.get("food_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""
        
        route_info = {
            "trails": [dict(t) for t in state.trail_info] if state.trail_info else [],
        }
        duration_days = state.user_preferences.get("duration_days", 1) if state.user_preferences else 1

        food_info = await food_agent.get_food_info(location, route_info, duration_days, context)

        return {
            "food_info": food_info,
            "completed_agents": state.completed_agents + ["food_agent"],
        }
    except Exception as e:
        error_msg = f"Food agent error: {str(e)}"
        return {
            "food_info": None,
            "completed_agents": state.completed_agents + ["food_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def community_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Community agent node - provides community and social information."""
    try:
        context = state.agent_context.get("community_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""
        
        activity_type = "mountain_biking"
        if state.user_preferences:
            activity_type = state.user_preferences.get("activity_type") or state.user_preferences.get("adventure_type", "mountain_biking")

        community_info = await community_agent.get_community_info(location, activity_type, context)

        return {
            "community_info": community_info,
            "completed_agents": state.completed_agents + ["community_agent"],
        }
    except Exception as e:
        error_msg = f"Community agent error: {str(e)}"
        return {
            "community_info": None,
            "completed_agents": state.completed_agents + ["community_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def photography_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Photography agent node - provides photography and media information."""
    try:
        context = state.agent_context.get("photography_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""
        
        route_info = {
            "trails": [dict(t) for t in state.trail_info] if state.trail_info else [],
        }

        photography_info = await photography_agent.get_photography_info(location, route_info, context)

        return {
            "photography_info": photography_info,
            "completed_agents": state.completed_agents + ["photography_agent"],
        }
    except Exception as e:
        error_msg = f"Photography agent error: {str(e)}"
        return {
            "photography_info": None,
            "completed_agents": state.completed_agents + ["photography_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def historical_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Historical agent node - provides historical and cultural information."""
    try:
        context = state.agent_context.get("historical_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""
        
        route_info = {
            "trails": [dict(t) for t in state.trail_info] if state.trail_info else [],
        }

        historical_info = await historical_agent.get_historical_info(location, route_info, context)

        return {
            "historical_info": historical_info,
            "completed_agents": state.completed_agents + ["historical_agent"],
        }
    except Exception as e:
        error_msg = f"Historical agent error: {str(e)}"
        return {
            "historical_info": None,
            "completed_agents": state.completed_agents + ["historical_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def route_planning_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Route planning agent node - provides route planning information from RideWithGPS and Strava."""
    try:
        context = state.agent_context.get("route_planning_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""
        
        activity_type = "mountain_biking"
        if state.user_preferences:
            activity_type = state.user_preferences.get("activity_type") or state.user_preferences.get("adventure_type", "mountain_biking")
        
        distance = None
        if state.user_preferences:
            distance_pref = state.user_preferences.get("distance_preference")
            # Map distance preference to approximate miles
            if distance_pref == "short":
                distance = 10.0
            elif distance_pref == "medium":
                distance = 25.0
            elif distance_pref == "long":
                distance = 50.0
            elif distance_pref == "epic":
                distance = 100.0

        # Search both RideWithGPS and Strava routes
        ridewithgps_routes = await route_planning_agent.search_ridewithgps_routes(
            location, activity_type, distance, context
        )
        strava_routes = await route_planning_agent.search_strava_routes(
            location, activity_type, "popular", context
        )

        # Combine routes from both sources
        all_routes = list(ridewithgps_routes) + list(strava_routes)

        return {
            "route_planning_info": all_routes,
            "completed_agents": state.completed_agents + ["route_planning_agent"],
        }
    except Exception as e:
        error_msg = f"Route planning agent error: {str(e)}"
        return {
            "route_planning_info": [],
            "completed_agents": state.completed_agents + ["route_planning_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def bikepacking_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Bikepacking agent node - provides bikepacking route information."""
    try:
        context = state.agent_context.get("bikepacking_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""
        
        route_type = state.user_preferences.get("route_type") if state.user_preferences else None
        duration_days = state.user_preferences.get("duration_days", 1) if state.user_preferences else None

        # Search bikepacking.com routes
        bikepacking_routes = await bikepacking_agent.search_bikepacking_routes(
            location, route_type, duration_days, context
        )
        
        # Search Bikepacking Roots routes
        bikepacking_roots_routes = await bikepacking_agent.search_bikepacking_roots_routes(
            location, context
        )

        # Combine routes from both sources
        all_routes = list(bikepacking_routes) + list(bikepacking_roots_routes)

        return {
            "bikepacking_info": all_routes,
            "completed_agents": state.completed_agents + ["bikepacking_agent"],
        }
    except Exception as e:
        error_msg = f"Bikepacking agent error: {str(e)}"
        return {
            "bikepacking_info": [],
            "completed_agents": state.completed_agents + ["bikepacking_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def advocacy_agent_node(state: AdventureState) -> Dict[str, Any]:
    """Advocacy agent node - provides trail advocacy and long-distance route information."""
    try:
        context = state.agent_context.get("advocacy_agent", state.user_input)
        
        location = state.geo_info.get("location", "") if state.geo_info else ""
        if not location:
            location = state.user_preferences.get("region", "") if state.user_preferences else ""
        
        route_type = state.user_preferences.get("route_type") if state.user_preferences else None

        # Get IMBA trail information
        imba_info = await advocacy_agent.get_imba_trail_info(location, context)
        
        # Get Adventure Cycling routes
        adventure_cycling_routes = await advocacy_agent.search_adventure_cycling_routes(
            location, route_type, context
        )
        
        # Get trail access information
        trail_access_info = await advocacy_agent.get_trail_access_info(location)

        # Combine all advocacy information
        advocacy_info = {
            "imba_info": imba_info,
            "adventure_cycling_routes": adventure_cycling_routes,
            "trail_access_info": trail_access_info,
        }

        return {
            "advocacy_info": advocacy_info,
            "completed_agents": state.completed_agents + ["advocacy_agent"],
        }
    except Exception as e:
        error_msg = f"Advocacy agent error: {str(e)}"
        return {
            "advocacy_info": None,
            "completed_agents": state.completed_agents + ["advocacy_agent"],
            "errors": state.get("errors", []) + [error_msg],
        }


async def synthesize_node(state: AdventureState) -> Dict[str, Any]:
    """Synthesize final adventure plan from all agent outputs.
    
    If human feedback is provided (from a revision request), it will be
    incorporated into the plan synthesis.
    """
    try:
        # Include human feedback if this is a revision
        plan = await orchestrator.synthesize_plan(state, human_feedback=state.human_feedback)

        result = {
            "adventure_plan": plan,
        }
        # Clear human feedback after incorporating it (if it was provided)
        if state.human_feedback:
            result["human_feedback"] = None
        return result
    except Exception as e:
        error_msg = f"Synthesize error: {str(e)}"
        return {
            "adventure_plan": None,
            "errors": state.get("errors", []) + [error_msg],
        }


def should_continue(state: AdventureState) -> Literal["human_review", "synthesize"]:
    """Determine next step based on state."""
    # Check if all required agents have completed
    required = set(state.get("required_agents", []))
    completed = set(state.get("completed_agents", []))

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
    """
    # Prepare review information for the human
    review_data = {
        "message": "Please review the adventure plan before finalization",
        "adventure_plan": state.adventure_plan,
        "user_input": state.user_input,
        "user_preferences": state.user_preferences,
        "errors": state.get("errors", []),
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


def route_to_agents(state: AdventureState) -> str:
    """Route to next required agent."""
    required = set(state.get("required_agents", []))
    completed = set(state.get("completed_agents", []))
    remaining = required - completed

    if not remaining:
        return "synthesize"

    # Priority order: geo -> weather -> permits -> safety -> trail -> route_planning -> bikepacking -> 
    # blm -> advocacy -> transportation -> accommodation -> food -> gear -> community -> planning -> 
    # photography -> historical
    priority = [
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
    ]
    
    for agent in priority:
        if agent in remaining:
            return agent

    return "synthesize"


def get_all_agent_edges() -> Dict[str, str]:
    """Get edge mappings for all agents."""
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
    ]
    edges = {agent: agent for agent in agents}
    edges["synthesize"] = "synthesize"
    return edges


# Build the graph
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
    .add_node("synthesize", synthesize_node)
    .add_node("human_review", human_review_node)
    .add_edge("__start__", "orchestrator")
    .add_conditional_edges("orchestrator", route_to_agents, all_agent_edges)
    .add_conditional_edges("geo_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("weather_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("permits_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("safety_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("trail_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("route_planning_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("bikepacking_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("blm_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("advocacy_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("transportation_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("accommodation_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("food_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("gear_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("community_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("planning_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("photography_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges("historical_agent", route_to_agents, all_agent_edges)
    .add_conditional_edges(
        "synthesize",
        lambda state: "human_review" if state.needs_human_review else END,
        {
            "human_review": "human_review",
            END: END,
        },
    )
    .add_conditional_edges(
        "human_review",
        lambda state: "synthesize" if state.approval_status == "needs_revision" else END,
        {
            "synthesize": "synthesize",
            END: END,
        },
    )
)

# Compile with checkpointer if configured
# Note: When using LangGraph API, checkpointing is handled automatically
# and any checkpointer passed here will be replaced by the API's checkpointer
compile_kwargs = {"name": "Adventure Agent"}
if _checkpointer is not None:
    compile_kwargs["checkpointer"] = _checkpointer

graph = graph_builder.compile(**compile_kwargs)
