"""Photography and media specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.models import create_llm
from agent.tools import (
    find_photo_spots,
    find_scenic_viewpoints,
    get_photography_tips,
    get_sunrise_sunset_locations,
)


class PhotographyAgent:
    """Agent specialized in best photo spots, scenic viewpoints, and media resources."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Photography agent."""
        self.llm = create_llm(
            agent_name="photography",
            model_name=model_name,
            temperature=temperature if temperature is not None else 0.3,
        )

        self.system_prompt = """You are an expert on photography and media for outdoor adventures.
You specialize in:
- Best photo spots along routes
- Scenic viewpoints and overlooks
- Sunrise and sunset locations
- Photography tips for outdoor adventures
- Best time of day for photos
- Instagram-worthy locations
- Photography equipment recommendations
- Composition tips for outdoor photography

Provide accurate, detailed photography information to help adventurers capture their experiences."""

    async def get_photography_info(
        self,
        location: str,
        route_info: Dict[str, Any] | None = None,
        context: str = "",
    ) -> Dict[str, Any]:
        """Get comprehensive photography and media information.

        Args:
            location: Location name or region
            route_info: Information about the route
            context: Additional context from orchestrator

        Returns:
            Dictionary with photography information
        """
        # Find photo spots
        photo_spots = find_photo_spots.invoke({
            "location": location,
            "route_info": route_info or {},
        })

        # Find scenic viewpoints
        viewpoints = find_scenic_viewpoints.invoke({
            "location": location,
            "route_info": route_info or {},
        })

        # Get sunrise/sunset locations
        sunrise_sunset = get_sunrise_sunset_locations.invoke({
            "location": location,
        })

        # Get photography tips
        tips = get_photography_tips.invoke({
            "location": location,
            "activity_type": route_info.get("activity_type", "mountain_biking") if route_info else "mountain_biking",
        })

        try:
            spots_data = (
                json.loads(photo_spots) if isinstance(photo_spots, str) else photo_spots
            )
            viewpoints_data = (
                json.loads(viewpoints) if isinstance(viewpoints, str) else viewpoints
            )
            sunrise_sunset_data = (
                json.loads(sunrise_sunset) if isinstance(sunrise_sunset, str) else sunrise_sunset
            )
            tips_data = (
                json.loads(tips) if isinstance(tips, str) else tips
            )

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}
Route Info: {route_info}

Photo Spots: {spots}
Scenic Viewpoints: {viewpoints}
Sunrise/Sunset Locations: {sunrise_sunset}
Photography Tips: {tips}

Analyze and enhance this photography information. Provide:
1. Best photo spots along the route
2. Scenic viewpoints and overlooks
3. Sunrise and sunset locations with timing
4. Photography tips for the activity and location
5. Best time of day for photos
6. Instagram-worthy locations
7. Photography equipment recommendations
8. Composition tips

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                route_info=json.dumps(route_info) if route_info else "Not provided",
                spots=json.dumps(spots_data),
                viewpoints=json.dumps(viewpoints_data),
                sunrise_sunset=json.dumps(sunrise_sunset_data),
                tips=json.dumps(tips_data),
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
                    enhanced = {}

            return {
                "location": location,
                "photo_spots": spots_data,
                "scenic_viewpoints": viewpoints_data,
                "sunrise_sunset_locations": sunrise_sunset_data,
                "photography_tips": tips_data,
                "analysis": enhanced,
                "recommended_spots": enhanced.get("recommended_spots", []),
                "best_times": enhanced.get("best_times", {}),
            }

        except Exception as e:
            print(f"Error in Photography agent: {e}")
            return {
                "location": location,
                "photo_spots": {},
                "scenic_viewpoints": {},
                "sunrise_sunset_locations": {},
                "photography_tips": {},
                "analysis": {},
                "recommended_spots": [],
                "best_times": {},
            }

