"""Base class for location-specific agents.

This module provides a base class and registry system for location-specific agents
that can be easily extended to support new cities, towns, and regions.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from agent.agents.location_response_schemas import LocationGuideResponse
from agent.config import Config
from agent.models import create_llm
from agent.tools import (
    find_cultural_sites,
    find_grocery_stores,
    find_historical_sites,
    find_photo_spots,
    find_restaurants,
    find_scenic_viewpoints,
    find_shuttle_services,
    find_water_sources,
    get_coordinates,
    get_local_history,
    get_parking_information,
    search_accommodations,
    search_trails,
)


class LocationAgentBase(ABC):
    """Base class for location-specific agents.

    This class provides a common interface and implementation for location-specific
    agents that enhance adventure planning with local knowledge.
    """

    # Location identifiers - subclasses should override
    LOCATION_NAME: str = ""
    LOCATION_INDICATORS: List[str] = []
    AGENT_NAME: str = ""  # e.g., "jerome_agent", "sedona_agent"

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the location agent."""
        # Use AGENT_NAME if available, otherwise fall back to class name
        agent_name = self.AGENT_NAME.replace("_agent", "") if self.AGENT_NAME else self.__class__.__name__.lower().replace("agent", "")
        self.llm = create_llm(
            agent_name=agent_name,
            model_name=model_name,
            temperature=temperature if temperature is not None else 0.3,
        )

        # Create structured output LLM for final response generation
        # Use function_calling method to avoid schema validation issues with nested Dict types
        self.structured_llm = self.llm.with_structured_output(
            LocationGuideResponse, method="function_calling"
        )

        # Define tools available to location agents
        self.tools = [
            get_coordinates,
            search_trails,
            find_historical_sites,
            find_cultural_sites,
            get_local_history,
            find_restaurants,
            find_grocery_stores,
            get_parking_information,
            find_shuttle_services,
            find_photo_spots,
            find_scenic_viewpoints,
            search_accommodations,
            find_water_sources,
        ]

        # Create the agent with tools
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self._get_system_prompt(),
        )

    def get_location_knowledge(self) -> Dict[str, Any]:
        """Get location-specific knowledge from multiple sources.

        Priority order:
        1. External knowledge file (knowledge/{agent_name}.json) if exists
        2. Default knowledge from _get_default_knowledge() (fallback)

        This allows knowledge to be:
        - Loaded from external JSON files (easy updates without code changes)
        - Defined in agent class as default/curated knowledge (backward compatible)
        - Combined with dynamic tool data at runtime

        Returns:
            Dictionary containing location-specific knowledge (history, attractions, etc.)
        """
        # Try to load from external knowledge file first
        external_knowledge = self._load_external_knowledge()
        if external_knowledge:
            return external_knowledge

        # Fallback to default knowledge (backward compatible)
        return self._get_default_knowledge()

    def _load_external_knowledge(self) -> Dict[str, Any] | None:
        """Load knowledge from external source (JSON file, database, etc.).

        Currently supports:
        - JSON files in knowledge/ directory: knowledge/{agent_name}.json

        Future enhancements:
        - Database queries
        - Vector store retrieval
        - API calls
        - Environment-specific sources

        Returns:
            Knowledge dictionary if found, None otherwise
        """
        # Try JSON file in knowledge/ directory
        knowledge_dir = Path(__file__).parent.parent.parent.parent / "knowledge"
        json_path = knowledge_dir / f"{self.AGENT_NAME}.json"

        if json_path.exists():
            try:
                with open(json_path, encoding="utf-8") as f:
                    knowledge = json.load(f)
                    print(f"Loaded external knowledge from {json_path}")
                    return knowledge
            except Exception as e:
                print(f"Error loading external knowledge from {json_path}: {e}")
                # Fall through to default knowledge

        return None

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get default/curated knowledge base (fallback).

        Subclasses should override this to provide curated knowledge.
        This is used when external knowledge files don't exist.
        This knowledge is carefully curated and provides essential location context.

        Returns:
            Dictionary containing location-specific knowledge
        """
        # Default implementation - subclasses should override
        return {
            "location": {
                "name": self.LOCATION_NAME,
            }
        }

    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Get the system prompt for this location agent.

        Returns:
            System prompt string with location-specific information
        """
        pass

    def is_location_match(self, location: str) -> bool:
        """Check if location string matches this agent's location.

        Args:
            location: Location name to check

        Returns:
            True if location matches this agent's location
        """
        location_lower = location.lower()
        return any(
            indicator.lower() in location_lower
            for indicator in self.LOCATION_INDICATORS
        )

    async def get_location_info(
        self,
        location: str,
        existing_agent_outputs: Dict[str, Any] | None = None,
        context: str = "",
        activity_type: str = "mountain_biking",
    ) -> Dict[str, Any]:
        """Get comprehensive location-specific information.

        Args:
            location: Location name
            existing_agent_outputs: Outputs from other agents to enhance
            context: Additional context from orchestrator
            activity_type: Type of activity (mountain_biking, hiking, etc.)

        Returns:
            Dictionary with location-specific information and enhancements
        """
        # Verify this matches our location
        if not self.is_location_match(location):
            return {
                "location": location,
                "is_match": False,
                "agent_name": self.AGENT_NAME,
                "message": f"Location is not {self.LOCATION_NAME}",
            }

        existing_outputs = existing_agent_outputs or {}
        knowledge_base = self.get_location_knowledge()

        # Build the query for the agent
        query_parts = [
            f"Location: {location}",
            f"Activity Type: {activity_type}",
        ]
        if context:
            query_parts.append(f"Context: {context}")

        # Add information about what other agents have found
        if existing_outputs:
            query_parts.append("\nExisting agent outputs to enhance:")
            if existing_outputs.get("geo_info"):
                query_parts.append(
                    f"- Geo info: {json.dumps(existing_outputs['geo_info'])}"
                )
            if existing_outputs.get("trail_info"):
                query_parts.append(
                    f"- Trail info: {json.dumps(existing_outputs['trail_info'])}"
                )
            if existing_outputs.get("historical_info"):
                query_parts.append(
                    f"- Historical info: {json.dumps(existing_outputs['historical_info'])}"
                )
            if existing_outputs.get("accommodation_info"):
                query_parts.append(
                    f"- Accommodation info: {json.dumps(existing_outputs['accommodation_info'])}"
                )
            if existing_outputs.get("food_info"):
                query_parts.append(
                    f"- Food info: {json.dumps(existing_outputs['food_info'])}"
                )

        query_parts.append(
            f"\n{self.LOCATION_NAME} Knowledge Base:\n{json.dumps(knowledge_base, indent=2)}"
        )

        query_parts.append(
            "\nYour task: Use tools to gather relevant information about this location, "
            "then provide a comprehensive guide. Select which tools are most relevant "
            "based on the activity type and context. Enhance tool results with "
            "location-specific knowledge from the knowledge base above."
        )

        user_query = "\n".join(query_parts)

        try:
            # Step 1: Use the agent to dynamically select and call tools
            response = await self.agent.ainvoke({
                "messages": [
                    SystemMessage(content=self._get_system_prompt()),
                    HumanMessage(content=user_query),
                ],
            })

            # Extract tool calls and gather information from agent response
            messages = response.get("messages", [])
            tool_calls = []
            conversation_context = []
            
            if messages:
                for msg in messages:
                    # Extract tool calls
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            tool_name = tc.get("name", "unknown")
                            tool_calls.append(tool_name)
                    # Collect all message content for context
                    if hasattr(msg, "content") and msg.content:
                        conversation_context.append(str(msg.content))

            # Step 2: Use structured output LLM to generate final response
            # Build comprehensive context from agent conversation
            conversation_summary = "\n".join(conversation_context[-10:]) if conversation_context else "No tool results available."
            
            synthesis_prompt = f"""Based on the tool results and knowledge base, provide a comprehensive guide for {self.LOCATION_NAME}.

Agent Conversation and Tool Results:
{conversation_summary}

Knowledge Base:
{json.dumps(knowledge_base, indent=2)}

Activity Type: {activity_type}
Context: {context if context else "General inquiry"}

Provide a complete structured guide covering:
- Location overview (coordinates, elevation, region, proximity) - use knowledge base coordinates if available
- Outdoor activities (for the specified activity type: {activity_type})
- Key attractions
- Local businesses (restaurants, accommodations, shops)
- Practical information (parking, permits, best times, weather, access)
- Recommendations

Ensure all information is accurate and enhanced with knowledge base details. Use the LocationGuideResponse schema structure."""

            # Generate structured response
            try:
                structured_response = await self.structured_llm.ainvoke(synthesis_prompt)
            except Exception as structured_error:
                # Fallback to original parsing if structured output fails
                print(f"Structured output failed for {self.AGENT_NAME}, falling back to JSON parsing: {structured_error}")
                final_message = messages[-1] if messages else None
                content = final_message.content if final_message else ""
                
                # Parse JSON from content
                import re
                json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
                if json_match:
                    enhanced = json.loads(json_match.group(1))
                else:
                    json_match = re.search(r"\{.*\}", content, re.DOTALL)
                    if json_match:
                        enhanced = json.loads(json_match.group(0))
                    else:
                        enhanced = {"guide": content, "location": location, "activity_type": activity_type}
                
                return {
                    "location": location,
                    "is_match": True,
                    "agent_name": self.AGENT_NAME,
                    "location_name": self.LOCATION_NAME,
                    "location_knowledge": knowledge_base,
                    "location_guide": enhanced,
                    "enhanced_info": enhanced,
                    "tools_used": tool_calls,
                    "error": f"Structured output failed: {str(structured_error)}",
                }

            # Convert Pydantic model to dict for backward compatibility
            enhanced_dict = structured_response.model_dump() if hasattr(structured_response, "model_dump") else structured_response.dict()
            
            # Normalize data: handle cases where LLM returns unexpected formats
            # Fix famous_trails if they're dicts instead of strings
            if "outdoor_activities" in enhanced_dict:
                for activity in enhanced_dict["outdoor_activities"]:
                    if "famous_trails" in activity:
                        trails = activity["famous_trails"]
                        if trails and isinstance(trails[0], dict):
                            # Extract name from dict objects
                            activity["famous_trails"] = [
                                trail.get("name", str(trail)) if isinstance(trail, dict) else trail
                                for trail in trails
                            ]
            
            # Fix weather if it's a string instead of dict
            if "practical_info" in enhanced_dict and enhanced_dict["practical_info"]:
                practical_info = enhanced_dict["practical_info"]
                if "weather" in practical_info and isinstance(practical_info["weather"], str):
                    practical_info["weather"] = {"description": practical_info["weather"]}
            
            # Ensure coordinates exist in overview (use knowledge base if available)
            if "overview" in enhanced_dict and enhanced_dict["overview"]:
                overview = enhanced_dict["overview"]
                if not overview.get("coordinates") and knowledge_base:
                    # Try to extract coordinates from knowledge base
                    kb_coords = knowledge_base.get("coordinates")
                    if kb_coords:
                        overview["coordinates"] = kb_coords

            # Add metadata for backward compatibility
            return {
                "location": location,
                "is_match": True,
                "agent_name": self.AGENT_NAME,
                "location_name": self.LOCATION_NAME,
                "location_knowledge": knowledge_base,
                "location_guide": enhanced_dict,
                "enhanced_info": enhanced_dict,  # For backward compatibility
                "tools_used": tool_calls,
                # Include the structured response as dict (not Pydantic model) for JSON serialization
                "structured_response": enhanced_dict,
            }

        except Exception as e:
            print(f"Error in {self.AGENT_NAME}: {e}")
            return {
                "location": location,
                "is_match": True,
                "agent_name": self.AGENT_NAME,
                "location_name": self.LOCATION_NAME,
                "location_knowledge": knowledge_base,
                "enhanced_info": {},
                "error": str(e),
            }


# Registry for location agents
_LOCATION_AGENTS: Dict[str, LocationAgentBase] = {}


def register_location_agent(agent: LocationAgentBase) -> None:
    """Register a location agent in the global registry.

    Args:
        agent: Location agent instance to register
    """
    agent_name = getattr(agent, "AGENT_NAME", None)
    if not agent_name:
        raise ValueError("Agent must have AGENT_NAME set")
    _LOCATION_AGENTS[agent_name] = agent


def get_location_agent(agent_name: str) -> LocationAgentBase | None:
    """Get a location agent by name.

    Args:
        agent_name: Name of the agent (e.g., "jerome_agent")

    Returns:
        Location agent instance or None if not found
    """
    return _LOCATION_AGENTS.get(agent_name)


def get_all_location_agents() -> Dict[str, LocationAgentBase]:
    """Get all registered location agents.

    Returns:
        Dictionary mapping agent names to agent instances
    """
    return _LOCATION_AGENTS.copy()


def find_location_agent_for_location(location: str) -> LocationAgentBase | None:
    """Find a location agent that matches the given location.

    Args:
        location: Location name to match

    Returns:
        Matching location agent or None
    """
    location_lower = location.lower()
    for agent in _LOCATION_AGENTS.values():
        if agent.is_location_match(location_lower):
            return agent
    return None


def get_location_agent_names() -> List[str]:
    """Get list of all registered location agent names.

    Returns:
        List of agent names (e.g., ["jerome_agent", "sedona_agent"])
    """
    return list(_LOCATION_AGENTS.keys())

