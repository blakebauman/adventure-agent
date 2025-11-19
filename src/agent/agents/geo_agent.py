"""Geographic information specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.tools import calculate_distance, get_coordinates


class GeoAgent:
    """Agent specialized in geographic information and location data."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Geo agent."""
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else 0.3,
            api_key=Config.OPENAI_API_KEY,
        )

        self.system_prompt = """You are an expert in geographic information for adventure planning.
You specialize in:
- Location geocoding and coordinates
- Distance calculations between points
- Route planning and navigation
- Regional geography (US states, Canadian provinces)
- Elevation profiles and terrain analysis
- Geographic context for adventure planning

Provide accurate geographic information for adventure planning."""

    async def get_location_info(
        self, location_name: str, context: str = ""
    ) -> Dict[str, Any]:
        """Get comprehensive location information."""
        # Use tool to get coordinates
        coord_data = get_coordinates.invoke({"location_name": location_name})

        try:
            coords = (
                json.loads(coord_data) if isinstance(coord_data, str) else coord_data
            )

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location_name}

Coordinate Data: {coord_data}

Analyze and enhance this location information. Provide:
1. Accurate coordinates
2. Region and state/province
3. Geographic context (terrain, elevation, climate)
4. Nearby points of interest
5. Access routes and transportation
6. Geographic considerations for adventure planning

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location_name=location_name,
                coord_data=json.dumps(coords),
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
                    enhanced = coords

            return {
                "location": location_name,
                "coordinates": enhanced.get("coordinates", coords.get("coordinates")),
                "region": enhanced.get("region", coords.get("region", "")),
                "country": enhanced.get("country", coords.get("country", "US")),
                "description": enhanced.get("description", ""),
                "geographic_context": enhanced.get("geographic_context", {}),
            }

        except Exception as e:
            print(f"Error in Geo agent: {e}")
            return {
                "location": location_name,
                "coordinates": None,
                "region": "",
                "country": "US",
            }

    async def calculate_route_distance(
        self, points: List[Dict[str, float]]
    ) -> Dict[str, Any]:
        """Calculate distance for a route with multiple points."""
        if len(points) < 2:
            return {"total_distance_miles": 0.0, "segments": []}

        total_distance = 0.0
        segments = []

        for i in range(len(points) - 1):
            distance_data = calculate_distance.invoke({
                "point1": points[i],
                "point2": points[i + 1],
            })

            try:
                dist_info = (
                    json.loads(distance_data)
                    if isinstance(distance_data, str)
                    else distance_data
                )
                segment_dist = dist_info.get("distance_miles", 0.0)
                total_distance += segment_dist
                segments.append({
                    "from": points[i],
                    "to": points[i + 1],
                    "distance_miles": segment_dist,
                })
            except Exception:
                pass

        return {
            "total_distance_miles": total_distance,
            "segments": segments,
        }

