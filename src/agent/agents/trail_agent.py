"""Generic trail specialist agent supporting multiple activity types."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.state import TrailInfo
from agent.tools import get_trail_details, search_trails


# Activity type to trail source mapping
ACTIVITY_SOURCES = {
    "mountain_biking": {
        "primary": "mtbproject",
        "sources": ["mtbproject.com", "trailforks.com"],
        "name": "MTB Project",
    },
    "hiking": {
        "primary": "hikingproject",
        "sources": ["hikingproject.com"],
        "name": "Hiking Project",
    },
    "trail_running": {
        "primary": "trailrunproject",
        "sources": ["trailrunproject.com"],
        "name": "Trail Run Project",
    },
    "bikepacking": {
        "primary": "mtbproject",
        "sources": ["mtbproject.com", "bikepacking.com"],
        "name": "MTB Project / Bikepacking",
    },
}


class TrailAgent:
    """Agent specialized in trails for multiple activity types.

    Supports:
    - Mountain biking (MTB Project)
    - Hiking (Hiking Project)
    - Trail running (Trail Run Project)
    - Bikepacking
    """

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Trail agent."""
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else 0.3,
            api_key=Config.OPENAI_API_KEY,
        )

    def _get_system_prompt(self, activity_type: str) -> str:
        """Get system prompt for specific activity type."""
        activity_info = ACTIVITY_SOURCES.get(
            activity_type, ACTIVITY_SOURCES["mountain_biking"]
        )
        activity_name = activity_info["name"]

        base_prompt = f"""You are an expert on {activity_type.replace('_', ' ')} trails, specializing in:
- {activity_name} trail data
- Trail difficulty ratings and conditions
- Trail features, elevation profiles, and descriptions
- Recent trail reports and conditions
- Trail connectivity and route planning
- Best practices for {activity_type.replace('_', ' ')} adventures

Provide detailed, accurate trail information for adventure planning."""

        if activity_type == "mountain_biking":
            base_prompt += "\n- Technical features, jumps, and bike-specific considerations"
        elif activity_type == "hiking":
            base_prompt += "\n- Scenic viewpoints, water sources, and hiking-specific considerations"
        elif activity_type == "trail_running":
            base_prompt += "\n- Running-friendly terrain, elevation profiles, and running-specific considerations"
        elif activity_type == "bikepacking":
            base_prompt += "\n- Multi-day routes, resupply points, and bikepacking-specific considerations"

        return base_prompt

    async def search_trails(
        self,
        location: str,
        activity_type: str,
        difficulty: str | None = None,
        distance: float | None = None,
        context: str = "",
    ) -> List[TrailInfo]:
        """Search for trails in a location for a specific activity type.

        Args:
            location: Location name or region
            activity_type: Type of activity (mountain_biking, hiking, trail_running, bikepacking)
            difficulty: Trail difficulty filter
            distance: Maximum distance in miles
            context: Additional context from orchestrator

        Returns:
            List of trail information
        """
        # Get activity-specific source info
        activity_info = ACTIVITY_SOURCES.get(
            activity_type, ACTIVITY_SOURCES["mountain_biking"]
        )
        source = activity_info["primary"]

        # Use tool to search trails
        trail_data = search_trails.invoke({
            "location": location,
            "activity_type": activity_type,
            "source": source,
            "difficulty": difficulty,
            "distance": distance,
        })

        try:
            data = json.loads(trail_data) if isinstance(trail_data, str) else trail_data
            trails = data.get("trails", [])

            # Enhance with LLM analysis
            system_prompt = self._get_system_prompt(activity_type)
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}
Activity Type: {activity_type}
Difficulty: {difficulty}
Max Distance: {distance}

Trail Data: {trail_data}

Analyze and enhance this trail information. Provide:
1. Detailed trail descriptions
2. Difficulty assessment
3. Best features and highlights
4. Trail conditions and recent reports
5. Connectivity to other trails
6. Best times to visit/ride/run
7. Any warnings or considerations
8. Activity-specific recommendations

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                activity_type=activity_type.replace("_", " "),
                difficulty=difficulty or "any",
                distance=distance or "unlimited",
                trail_data=json.dumps(trails),
            )

            response = await self.llm.ainvoke(messages)
            content = response.content

            # Parse enhanced data
            import re

            json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
            if json_match:
                enhanced = json.loads(json_match.group(1))
            else:
                json_match = re.search(r"\{.*\}", content, re.DOTALL)
                if json_match:
                    enhanced = json.loads(json_match.group(0))
                else:
                    enhanced = {"trails": trails}

            # Convert to TrailInfo format
            result = []
            for trail in enhanced.get("trails", trails):
                result.append({
                    "name": trail.get("name", ""),
                    "source": trail.get("source", source),
                    "difficulty": trail.get("difficulty"),
                    "length_miles": trail.get("length_miles"),
                    "elevation_gain": trail.get("elevation_gain"),
                    "description": trail.get("description", ""),
                    "url": trail.get("url"),
                    "coordinates": trail.get("coordinates"),
                    "activity_type": activity_type,
                })

            return result

        except Exception as e:
            print(f"Error in Trail agent: {e}")
            return []

    async def get_trail_details(
        self, trail_id: str, source: str, activity_type: str
    ) -> Dict[str, Any]:
        """Get detailed information about a specific trail.

        Args:
            trail_id: Trail identifier
            source: Source of trail data
            activity_type: Type of activity

        Returns:
            Detailed trail information
        """
        details_data = get_trail_details.invoke({
            "trail_id": trail_id,
            "source": source,
            "activity_type": activity_type,
        })
        try:
            return (
                json.loads(details_data)
                if isinstance(details_data, str)
                else details_data
            )
        except Exception:
            return {"trail_id": trail_id, "details": {}}

