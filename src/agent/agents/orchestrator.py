"""Orchestrator agent for managing adventure planning workflow."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from agent.config import Config
from agent.state import AdventureState


class AdventureAnalysis(BaseModel):
    """Structured analysis of user adventure request extracted from natural language."""

    activity_type: str = Field(
        description="Type of activity: mountain_biking, hiking, trail_running, bikepacking, or other"
    )
    adventure_type: Optional[str] = Field(
        default=None,
        description="General type or theme of the adventure (e.g., 'epic mountain bike tour', 'scenic hiking trip')"
    )
    location: Optional[str] = Field(
        default=None,
        description="Location, region, or area mentioned in the request (e.g., 'Colorado', 'Sedona, Arizona')"
    )
    duration_days: Optional[int] = Field(
        default=None,
        description="Number of days for the adventure, if mentioned"
    )
    skill_level: Optional[str] = Field(
        default=None,
        description="Skill level mentioned: beginner, intermediate, advanced, expert"
    )
    required_agents: List[str] = Field(
        description="List of agent names that should be called to fulfill this request"
    )
    agent_context: Dict[str, str] = Field(
        default_factory=dict,
        description="Context-specific information for each agent (agent_name -> context string)"
    )
    priority_order: Optional[List[str]] = Field(
        default=None,
        description="Suggested priority order for calling agents"
    )


class OrchestratorAgent:
    """Main orchestrator agent that manages the adventure planning workflow."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the orchestrator agent."""
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else Config.OPENAI_TEMPERATURE,
            api_key=Config.OPENAI_API_KEY,
        )
        # Create a version with structured output for better intent extraction
        self.llm_structured = self.llm.with_structured_output(AdventureAnalysis)

        self.system_prompt = """You are an expert adventure planning orchestrator. 
Your role is to:
1. Understand user preferences and initial input
2. Determine which specialized agents need to be called
3. Coordinate information gathering from multiple sources
4. Synthesize a complete adventure plan

Available specialized agents:
- BLM Agent: Expert on Bureau of Land Management lands, access, regulations
- Trail Agent: Expert on trails for multiple activity types:
  * Mountain biking (MTB Project: mtbproject.com)
  * Hiking (Hiking Project: hikingproject.com)
  * Trail running (Trail Run Project: trailrunproject.com)
- Route Planning Agent: Expert on route planning tools:
  * RideWithGPS (ridewithgps.com) - Route planning, navigation, large route library
  * Strava (strava.com) - Popular routes, segments, community-driven data
- Bikepacking Agent: Expert on bikepacking routes:
  * Bikepacking.com - Curated bikepacking routes worldwide
  * Bikepacking Roots - Conservation-focused route development
- Advocacy Agent: Expert on trail advocacy and long-distance routes:
  * IMBA (imba.com) - Trail networks, access, advocacy
  * Adventure Cycling Association - Long-distance cycling routes
- Geo Agent: Geographic information, coordinates, distances, route planning
- Weather Agent: Real-time weather forecasts, trail conditions, seasonal information
- Permits Agent: Permit requirements, regulations, fire restrictions, seasonal closures
- Safety Agent: Safety information, emergency contacts, risk assessment, wildlife alerts
- Transportation Agent: Parking, shuttles, public transit, bike transport, car rentals
- Accommodation Agent: Hotels, campgrounds, lodging options
- Food Agent: Grocery stores, restaurants, water sources, resupply points
- Gear Agent: Gear and product recommendations from affiliate partners
- Community Agent: Local clubs, events, group rides, volunteer opportunities
- Planning Agent: Itinerary creation, logistics, day-by-day planning
- Photography Agent: Best photo spots, scenic viewpoints, sunrise/sunset locations
- Historical Agent: Historical sites, cultural significance, local history

You should analyze the user's request and determine which agents are needed.
Support multiple activity types: mountain_biking, hiking, trail_running, bikepacking.
For bikepacking adventures, consider using Bikepacking Agent.
For route planning and navigation, consider Route Planning Agent.
For trail access and advocacy, consider Advocacy Agent.
Return your analysis in a structured format."""

    async def analyze_request(
        self, user_input: str, preferences: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """Analyze user request and determine required agents using structured output.
        
        Uses Pydantic models for type-safe intent extraction from natural language.
        Falls back to manual JSON parsing if structured output fails.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            (
                "human",
                """User Request: {user_input}

User Preferences: {preferences}

Analyze this natural language request and extract:
1. Activity type (mountain_biking, hiking, trail_running, bikepacking, etc.)
2. Location/region mentioned
3. Duration in days (if mentioned)
4. Skill level (if mentioned)
5. Which specialized agents should be called
6. Context information for each agent
7. Suggested priority order for calling agents

Extract all information you can from the natural language text, even if not explicitly stated.""",
            ),
        ])

        messages = prompt.format_messages(
            user_input=user_input,
            preferences=preferences or {},
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
            
            return result
            
        except Exception as e:
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
        self, state: AdventureState, human_feedback: Optional[str] = None
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
- BLM land information (if applicable)
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
- BLM Info: {blm_info}
- Transportation Info: {transportation_info}
- Accommodation Info: {accommodation_info}
- Food Info: {food_info}
- Gear Recommendations: {gear_recommendations}
- Community Info: {community_info}
- Planning Info: {planning_info}
- Photography Info: {photography_info}
- Historical Info: {historical_info}"""

        if human_feedback:
            human_prompt += "\n\nHuman Review Feedback: {human_feedback}\n\nPlease revise the plan based on this feedback."

        human_prompt += "\n\nCreate a comprehensive adventure plan in JSON format."

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", human_prompt),
        ])

        format_kwargs = {
            "user_input": state.user_input,
            "preferences": state.user_preferences or {},
            "geo_info": state.geo_info or {},
            "weather_info": state.weather_info or {},
            "permits_info": state.permits_info or {},
            "safety_info": state.safety_info or {},
            "trail_info": state.trail_info,
            "blm_info": state.blm_info,
            "transportation_info": state.transportation_info or {},
            "accommodation_info": state.accommodation_info,
            "food_info": state.food_info or {},
            "gear_recommendations": state.gear_recommendations,
            "community_info": state.community_info or {},
            "planning_info": state.planning_info or {},
            "photography_info": state.photography_info or {},
            "historical_info": state.historical_info or {},
        }
        
        if human_feedback:
            format_kwargs["human_feedback"] = human_feedback

        messages = prompt.format_messages(**format_kwargs)

        response = await self.llm.ainvoke(messages)
        content = response.content

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
        except json.JSONDecodeError:
            return {
                "title": "Adventure Plan",
                "description": "Generated adventure plan",
                "error": "Failed to parse plan",
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

