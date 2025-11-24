"""Orchestrator agent for managing adventure planning workflow."""

from __future__ import annotations

from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from agent.agents.location_agent_base import (
    find_location_agent_for_location,
)
from agent.arizona_registry import is_arizona_location
from agent.config import Config
from agent.models import create_llm
from agent.state import AdventureState


class AdventureAnalysis(BaseModel):
    """Structured analysis of user adventure request extracted from natural language."""

    activity_type: str = Field(
        description="Type of activity: mountain_biking, hiking, trail_running, bikepacking, or other"
    )
    adventure_type: str | None = Field(
        default=None,
        description="General type or theme of the adventure (e.g., 'epic mountain bike tour', 'scenic hiking trip')"
    )
    location: str | None = Field(
        default=None,
        description="Location, region, or area mentioned in the request (e.g., 'Colorado', 'Sedona, Arizona')"
    )
    duration_days: int | None = Field(
        default=None,
        description="Number of days for the adventure, if mentioned"
    )
    skill_level: str | None = Field(
        default=None,
        description="Skill level mentioned: beginner, intermediate, advanced, expert"
    )
    required_agents: List[str] = Field(
        description="List of agent node names that should be called. Must use exact node names: geo_agent, trail_agent, weather_agent, permits_agent, safety_agent, route_planning_agent, bikepacking_agent, blm_agent, advocacy_agent, transportation_agent, accommodation_agent, food_agent, gear_agent, community_agent, planning_agent, photography_agent, historical_agent, and location-specific agents (jerome_agent, sedona_agent, prescott_agent, etc.). IMPORTANT: Do NOT use 'location-specific_agents' or 'location_specific_agents' as an agent name - use the specific location agent name instead (e.g., jerome_agent, sedona_agent)."
    )
    agent_context: Dict[str, str] = Field(
        default_factory=dict,
        description="Context-specific information for each agent (agent_name -> context string)"
    )
    priority_order: List[str] | None = Field(
        default=None,
        description="Suggested priority order for calling agents"
    )


class OrchestratorAgent:
    """Main orchestrator agent that manages the adventure planning workflow."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the orchestrator agent."""
        self.llm = create_llm(
            agent_name="orchestrator",
            model_name=model_name,
            temperature=temperature,
        )
        # Create a version with structured output for better intent extraction
        # Use function_calling method for better compatibility with complex Pydantic models
        self.llm_structured = self.llm.with_structured_output(AdventureAnalysis, method="function_calling")

        self.system_prompt = """You are an expert Arizona adventure planning orchestrator. 
This is the Arizona Adventure Agentic Workflow - specializing in adventures throughout Arizona.

Your role is to:
1. Understand user preferences and initial input (assume Arizona unless specified otherwise)
2. Determine which specialized agents need to be called
3. Coordinate information gathering from multiple sources
4. Synthesize a complete Arizona adventure plan
5. Automatically detect Arizona cities/towns and route to location-specific agents

Available specialized agents (use exact node names in required_agents):
- blm_agent: Expert on Bureau of Land Management lands, access, regulations
- trail_agent: Expert on trails for multiple activity types:
  * Mountain biking (MTB Project: mtbproject.com)
  * Hiking (Hiking Project: hikingproject.com)
  * Trail running (Trail Run Project: trailrunproject.com)
- route_planning_agent: Expert on route planning tools:
  * RideWithGPS (ridewithgps.com) - Route planning, navigation, large route library
  * Strava (strava.com) - Popular routes, segments, community-driven data
- bikepacking_agent: Expert on bikepacking routes:
  * Bikepacking.com - Curated bikepacking routes worldwide
  * Bikepacking Roots - Conservation-focused route development
- advocacy_agent: Expert on trail advocacy and long-distance routes:
  * IMBA (imba.com) - Trail networks, access, advocacy
  * Adventure Cycling Association - Long-distance cycling routes
- geo_agent: Geographic information, coordinates, distances, route planning
- weather_agent: Real-time weather forecasts, trail conditions, seasonal information
- permits_agent: Permit requirements, regulations, fire restrictions, seasonal closures
- safety_agent: Safety information, emergency contacts, risk assessment, wildlife alerts
- transportation_agent: Parking, shuttles, public transit, bike transport, car rentals
- accommodation_agent: Hotels, campgrounds, lodging options
- food_agent: Grocery stores, restaurants, water sources, resupply points
- gear_agent: Gear and product recommendations from affiliate partners
- community_agent: Local clubs, events, group rides, volunteer opportunities
- planning_agent: Itinerary creation, logistics, day-by-day planning
- photography_agent: Best photo spots, scenic viewpoints, sunrise/sunset locations
- historical_agent: Historical sites, cultural significance, local history
- Location-specific agents (automatically detected): jerome_agent, sedona_agent, prescott_agent, etc.
  These agents provide location-specific historical context, local attractions, and enhance other agent outputs.

You should analyze the user's request and determine which agents are needed.
IMPORTANT: This system specializes in Arizona adventures. Default to Arizona context unless user specifies otherwise.
IMPORTANT: Location-specific agents are automatically added when an Arizona city/town is detected (Jerome, Sedona, Prescott, Flagstaff, Phoenix, Tucson, etc.).
Support multiple activity types: mountain_biking, hiking, trail_running, bikepacking.
For bikepacking adventures, consider using bikepacking_agent.
For route planning and navigation, consider route_planning_agent.
For trail access and advocacy, consider advocacy_agent.
IMPORTANT: Use the exact node names (e.g., route_planning_agent, not "Route Planning Agent") in the required_agents list.
Return your analysis in a structured format."""

    async def analyze_request(
        self,
        user_input: str,
        preferences: Dict[str, Any] | None = None,
        error_context: List[Dict[str, Any]] | None = None,
    ) -> Dict[str, Any]:
        """Analyze user request and determine required agents using structured output.
        
        Uses Pydantic models for type-safe intent extraction from natural language.
        Falls back to manual JSON parsing if structured output fails.
        """
        # Build error context message if errors were provided
        error_context_msg = ""
        if error_context:
            error_context_msg = "\n\nIMPORTANT: Previous agent executions encountered recoverable errors:\n"
            for err in error_context:
                error_context_msg += f"- {err.get('agent', 'unknown')}: {err.get('message', 'unknown error')}\n"
            error_context_msg += "\nPlease adjust the agent selection or context to avoid these errors."

        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            (
                "human",
                """User Request: {user_input}

User Preferences: {preferences}
{error_context}

Analyze this natural language request and extract:
1. Activity type (mountain_biking, hiking, trail_running, bikepacking, etc.)
2. Location/region mentioned
3. Duration in days (if mentioned)
4. Skill level (if mentioned)
5. Which specialized agents should be called (use exact node names: geo_agent, trail_agent, etc.)
6. Context information for each agent (use exact node names as keys)
7. Suggested priority order for calling agents

IMPORTANT: When listing agents in required_agents, use the exact node names (e.g., route_planning_agent, blm_agent) not human-readable names (e.g., "Route Planning Agent", "BLM Agent").
CRITICAL: Do NOT use 'location-specific_agents' or 'location_specific_agents' as an agent name. If you need a location agent, use the specific location agent name (e.g., jerome_agent, sedona_agent, payson_agent) based on the location mentioned in the user request.

Extract all information you can from the natural language text, even if not explicitly stated.""",
            ),
        ])

        messages = prompt.format_messages(
            user_input=user_input,
            preferences=preferences or {},
            error_context=error_context_msg,
        )

        try:
            # Use structured output for type-safe extraction
            analysis: AdventureAnalysis = await self.llm_structured.ainvoke(messages)
            
            # Convert Pydantic model to dict for backward compatibility
            result = analysis.model_dump(exclude_none=True)
            
            # Ensure activity_type is always set (should be guaranteed by Pydantic, but double-check)
            if not result.get("activity_type"):
                # Try to infer from adventure_type or preferences
                adv_type = result.get("adventure_type", "")
                if adv_type:
                    if "hiking" in adv_type.lower():
                        result["activity_type"] = "hiking"
                    elif "running" in adv_type.lower() or "trail run" in adv_type.lower():
                        result["activity_type"] = "trail_running"
                    elif "bikepacking" in adv_type.lower():
                        result["activity_type"] = "bikepacking"
                    else:
                        result["activity_type"] = "mountain_biking"
                else:
                    # Fallback to preferences or default
                    activity = preferences.get("activity_type", "mountain_biking") if preferences else "mountain_biking"
                    result["activity_type"] = activity
            
            # Ensure required_agents is not empty
            if not result.get("required_agents"):
                result["required_agents"] = ["geo_agent", "trail_agent"]
            
            # Ensure agent_context exists
            if "agent_context" not in result:
                result["agent_context"] = {}
            
            # Dynamically detect location agents based on location
            location = result.get("location", "")
            
            # If no location specified, default to Arizona context
            if not location:
                # Check if user input mentions Arizona
                if is_arizona_location(user_input):
                    # Extract location from user input
                    location = user_input
                else:
                    # Default to Arizona for Arizona Adventure Agentic Workflow
                    location = "Arizona"
                    result["location"] = "Arizona"
            
            # Check if location is in Arizona
            if location and is_arizona_location(location):
                # Try to find a specific city/town agent
                location_agent = find_location_agent_for_location(location)
                if location_agent:
                    agent_name = location_agent.AGENT_NAME
                    if agent_name not in result["required_agents"]:
                        result["required_agents"].append(agent_name)
                        result["agent_context"][agent_name] = (
                            f"Provide detailed information about {location_agent.LOCATION_NAME}, "
                            f"leveraging existing agent outputs for {result.get('activity_type', 'adventure')} "
                            f"in {location_agent.LOCATION_NAME}."
                        )
            
            return result
            
        except Exception:
            # Fallback to manual JSON parsing if structured output fails
            # This maintains backward compatibility
            import json
            import re
            
            try:
                response = await self.llm.ainvoke(messages)
                content = response.content

                # Extract JSON from markdown if present
                json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
                if json_match:
                    content = json_match.group(1)
                else:
                    # Try to find JSON object
                    json_match = re.search(r"\{.*\}", content, re.DOTALL)
                    if json_match:
                        content = json_match.group(0)

                result = json.loads(content)
                
                # Dynamically detect location agents based on location
                location = result.get("location", "")
                
                # If no location specified, default to Arizona context
                if not location:
                    if is_arizona_location(user_input):
                        location = user_input
                    else:
                        location = "Arizona"
                        result["location"] = "Arizona"
                
                # Check if location is in Arizona
                if location and is_arizona_location(location):
                    location_agent = find_location_agent_for_location(location)
                    if location_agent:
                        agent_name = location_agent.AGENT_NAME
                        if "required_agents" not in result:
                            result["required_agents"] = []
                        if agent_name not in result["required_agents"]:
                            result["required_agents"].append(agent_name)
                            if "agent_context" not in result:
                                result["agent_context"] = {}
                            result["agent_context"][agent_name] = (
                                f"Provide detailed information about {location_agent.LOCATION_NAME}, "
                                f"leveraging existing agent outputs for adventure in {location_agent.LOCATION_NAME}."
                            )
                
                # Backward compatibility: check for Jerome in user input
                user_input_lower = user_input.lower() if user_input else ""
                if "jerome" in user_input_lower and "jerome_agent" not in result.get("required_agents", []):
                    if "required_agents" not in result:
                        result["required_agents"] = []
                    result["required_agents"].append("jerome_agent")
                    if "agent_context" not in result:
                        result["agent_context"] = {}
                    result["agent_context"]["jerome_agent"] = user_input
                
                # Ensure activity_type is set
                if "activity_type" not in result:
                    adv_type = result.get("adventure_type", "")
                    if "hiking" in adv_type.lower():
                        result["activity_type"] = "hiking"
                    elif "running" in adv_type.lower() or "trail run" in adv_type.lower():
                        result["activity_type"] = "trail_running"
                    elif "bikepacking" in adv_type.lower():
                        result["activity_type"] = "bikepacking"
                    else:
                        result["activity_type"] = "mountain_biking"
                
                return result
            except (json.JSONDecodeError, Exception):
                # Final fallback if everything fails
                activity = preferences.get("activity_type", "mountain_biking") if preferences else "mountain_biking"
                return {
                    "activity_type": activity,
                    "adventure_type": activity,
                    "required_agents": ["geo_agent", "trail_agent"],
                    "agent_context": {
                        "geo_agent": user_input,
                        "trail_agent": user_input,
                    },
                    "priority_order": ["geo_agent", "trail_agent"],
                }

    async def synthesize_plan(
        self, state: AdventureState, human_feedback: str | None = None
    ) -> Dict[str, Any]:
        """Synthesize final adventure plan from all agent outputs.
        
        Args:
            state: Current adventure state with all agent outputs
            human_feedback: Optional feedback from human review for revisions
        """
        system_prompt = """You are synthesizing a complete adventure plan from multiple specialized agents.
Create a comprehensive, well-structured adventure plan that includes:
- Title and description
- Location details
- Weather and conditions information
- Permit requirements and regulations
- Safety information and emergency contacts
- Trail information
- Route planning information (RideWithGPS, Strava routes)
- Bikepacking routes (if applicable)
- BLM land information (if applicable)
- Trail advocacy and access information
- Transportation and logistics
- Accommodation options
- Food and resupply information
- Gear recommendations
- Community resources
- Day-by-day itinerary
- Photography opportunities
- Historical and cultural sites
- Total distance and duration
- Difficulty assessment"""

        if human_feedback:
            system_prompt += "\n\nIMPORTANT: This is a revision request. The human reviewer has provided feedback that must be incorporated into the plan. Address all concerns and suggestions in the feedback."

        human_prompt = """User Request: {user_input}
User Preferences: {preferences}

Agent Outputs:
- Geo Info: {geo_info}
- Weather Info: {weather_info}
- Permits Info: {permits_info}
- Safety Info: {safety_info}
- Trail Info: {trail_info}
- Route Planning Info: {route_planning_info}
- Bikepacking Info: {bikepacking_info}
- BLM Info: {blm_info}
- Advocacy Info: {advocacy_info}
- Transportation Info: {transportation_info}
- Accommodation Info: {accommodation_info}
- Food Info: {food_info}
- Gear Recommendations: {gear_recommendations}
- Community Info: {community_info}
- Planning Info: {planning_info}
- Photography Info: {photography_info}
- Historical Info: {historical_info}
- Location Info: {location_info}"""

        if human_feedback:
            human_prompt += "\n\nHuman Review Feedback: {human_feedback}\n\nPlease revise the plan based on this feedback."

        human_prompt += "\n\nCreate a comprehensive adventure plan in JSON format."

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", human_prompt),
        ])

        # Truncate large lists and dicts to prevent token overflow and speed up synthesis
        # Using optimized truncation based on LangChain best practices
        def truncate_list(data: list, max_items: int = 5) -> list:
            """Truncate list to max_items, keeping first items."""
            if not isinstance(data, list):
                return data
            return data[:max_items] if len(data) > max_items else data
        
        def truncate_dict(data: dict, max_chars: int = 2000) -> dict:
            """Truncate dict values if total JSON size exceeds max_chars.
            
            Uses LangChain best practices for token optimization:
            - Keeps essential keys first
            - Truncates large values
            - Preserves structure for LLM parsing
            - Handles Pydantic models by converting to dict
            """
            if data is None:
                return {}
            
            # Handle Pydantic models by converting to dict
            try:
                from pydantic import BaseModel
                if isinstance(data, BaseModel):
                    data = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
            except (ImportError, AttributeError):
                pass
            
            if not isinstance(data, dict):
                # If it's not a dict and not a Pydantic model, try to convert
                try:
                    if hasattr(data, '__dict__'):
                        data = data.__dict__
                    else:
                        return {"value": str(data)[:500]}
                except Exception:
                    return {"value": str(data)[:500]}
            
            import json
            
            # Helper to recursively convert Pydantic models and other non-serializable objects
            def make_serializable(obj):
                """Recursively convert objects to JSON-serializable format."""
                try:
                    from pydantic import BaseModel
                    if isinstance(obj, BaseModel):
                        return obj.model_dump() if hasattr(obj, 'model_dump') else obj.dict()
                except (ImportError, AttributeError):
                    pass
                
                if isinstance(obj, dict):
                    return {k: make_serializable(v) for k, v in obj.items()}
                elif isinstance(obj, (list, tuple)):
                    return [make_serializable(item) for item in obj]
                elif hasattr(obj, '__dict__'):
                    return make_serializable(obj.__dict__)
                else:
                    try:
                        json.dumps(obj)  # Test if serializable
                        return obj
                    except (TypeError, ValueError):
                        return str(obj)[:500]  # Convert to string if not serializable
            
            # Convert to serializable format
            serializable_data = make_serializable(data)
            
            try:
                json_str = json.dumps(serializable_data)
            except (TypeError, ValueError) as e:
                # If still can't serialize, return minimal dict
                return {"error": "Could not serialize data", "type": str(type(data))}
            
            if len(json_str) <= max_chars:
                return serializable_data
            
            # Keep only essential keys for large dicts
            essential_keys = ["location", "title", "description", "summary", "name", "error"]
            truncated = {k: v for k, v in serializable_data.items() if k in essential_keys}
            if not truncated:
                # If no essential keys, just take first few items
                truncated = dict(list(serializable_data.items())[:3])
            
            # Further truncate if still too large
            try:
                json_str = json.dumps(truncated)
            except (TypeError, ValueError):
                return {"error": "Could not serialize truncated data"}
            
            if len(json_str) > max_chars:
                # Truncate string values
                for key, value in truncated.items():
                    if isinstance(value, str) and len(value) > 500:
                        truncated[key] = value[:500] + "..."
                    elif isinstance(value, (dict, list)):
                        # Recursively truncate nested structures
                        truncated[key] = make_serializable(value)
                        try:
                            if len(json.dumps(truncated[key])) > 500:
                                truncated[key] = str(truncated[key])[:500] + "..."
                        except (TypeError, ValueError):
                            truncated[key] = str(value)[:500] + "..."
            
            return truncated
        
        format_kwargs = {
            "user_input": state.get("user_input", ""),
            "preferences": state.get("user_preferences") or {},
            "geo_info": truncate_dict(state.get("geo_info") or {}),
            "weather_info": truncate_dict(state.get("weather_info") or {}),
            "permits_info": truncate_dict(state.get("permits_info") or {}),
            "safety_info": truncate_dict(state.get("safety_info") or {}),
            "trail_info": truncate_list(state.get("trail_info", []), max_items=10),
            "route_planning_info": truncate_list(state.get("route_planning_info", []), max_items=5),
            "bikepacking_info": truncate_list(state.get("bikepacking_info", []), max_items=5),
            "blm_info": truncate_list(state.get("blm_info", []), max_items=5),
            "advocacy_info": truncate_dict(state.get("advocacy_info") or {}),
            "transportation_info": truncate_dict(state.get("transportation_info") or {}),
            "accommodation_info": truncate_list(state.get("accommodation_info", []), max_items=5),
            "food_info": truncate_dict(state.get("food_info") or {}),
            "gear_recommendations": truncate_list(state.get("gear_recommendations", []), max_items=10),
            "community_info": truncate_dict(state.get("community_info") or {}),
            "planning_info": truncate_dict(state.get("planning_info") or {}),
            "photography_info": truncate_dict(state.get("photography_info") or {}),
            "historical_info": truncate_dict(state.get("historical_info") or {}),
            "location_info": truncate_dict(state.get("location_info") or {}),
        }
        
        if human_feedback:
            format_kwargs["human_feedback"] = human_feedback

        messages = prompt.format_messages(**format_kwargs)

        try:
            response = await self.llm.ainvoke(messages)
            content = response.content if response and hasattr(response, 'content') else None
            
            if not content:
                return {
                    "title": "Adventure Plan",
                    "description": "Unable to generate plan - LLM returned empty response",
                    "error": "Empty LLM response",
                }

            # Parse JSON from response
            import json
            import re

            json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            else:
                json_match = re.search(r"\{.*\}", content, re.DOTALL)
                if json_match:
                    content = json_match.group(0)

            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                # Return a plan with the raw content if JSON parsing fails
                return {
                    "title": "Adventure Plan",
                    "description": content[:500] if content else "Generated adventure plan",
                    "raw_content": content,
                    "error": f"Failed to parse plan as JSON: {str(e)}",
                }
        except Exception as e:
            return {
                "title": "Adventure Plan",
                "description": f"Error generating plan: {str(e)}",
                "error": str(e),
            }

    def should_request_human_review(self, state: AdventureState) -> bool:
        """Determine if human review is needed."""
        # Request review for:
        # - Complex multi-day adventures
        # - High-cost recommendations
        # - When errors occurred
        # - When user preferences are unclear
        if state.errors:
            return True

        if state.user_preferences:
            duration = state.user_preferences.get("duration_days", 0)
            if duration and duration > 7:
                return True

        return False

