"""Bikepacking specialist agent for Bikepacking.com and Bikepacking Roots."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.state import TrailInfo
from agent.tools import (
    search_bikepacking_routes,
    search_bikepacking_roots_routes,
    get_bikepacking_route_details,
)


class BikepackingAgent:
    """Agent specialized in bikepacking routes and resources.

    Bikepacking.com: https://bikepacking.com/
    - Curated bikepacking routes worldwide
    - Route guides with GPS maps
    - Gear reviews and planning resources
    - Over 300 original routes

    Bikepacking Roots: https://bikepackingroots.org/
    - Route development and conservation
    - Route planning resources
    - Conservation-focused routes
    """

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Bikepacking agent."""
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else 0.3,
            api_key=Config.OPENAI_API_KEY,
        )

        self.system_prompt = """You are an expert in bikepacking routes and multi-day cycling adventures.
You specialize in:
- Bikepacking.com curated routes and guides
- Bikepacking Roots route development
- Multi-day route planning
- Resupply points and logistics
- Route types: singletrack, gravel, dirt-road, fat-bike
- Route length categories: overnighters, weekend, week-long, odyssey
- Conservation and Leave No Trace principles

Provide detailed bikepacking route information for adventure planning."""

    async def search_bikepacking_routes(
        self,
        location: str,
        route_type: str | None = None,
        duration_days: int | None = None,
        context: str = "",
    ) -> List[TrailInfo]:
        """Search for bikepacking routes on Bikepacking.com.

        Args:
            location: Location name or region
            route_type: Type of route (singletrack, gravel, dirt_road, fat_bike)
            duration_days: Target duration in days
            context: Additional context

        Returns:
            List of route information
        """
        route_data = search_bikepacking_routes.invoke({
            "location": location,
            "route_type": route_type,
            "duration_days": duration_days,
        })

        try:
            data = json.loads(route_data) if isinstance(route_data, str) else route_data
            routes = data.get("routes", [])

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}
Route Type: {route_type}
Duration: {duration_days} days

Bikepacking.com Routes: {routes}

Analyze and enhance these bikepacking routes. Provide:
1. Detailed route descriptions
2. Route type and terrain characteristics
3. Resupply points and logistics
4. Camping and accommodation options
5. Best times to ride
6. Route highlights and challenges
7. Conservation considerations

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                route_type=route_type or "any",
                duration_days=duration_days or "flexible",
                routes=json.dumps(routes),
            )

            response = await self.llm.ainvoke(messages)
            content = response.content

            import re
            json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
            if json_match:
                enhanced = json.loads(json_match.group(1))
            else:
                json_match = re.search(r"\{.*\}", content, re.DOTALL)
                if json_match:
                    enhanced = json.loads(json_match.group(0))
                else:
                    enhanced = {"routes": routes}

            result = []
            for route in enhanced.get("routes", routes):
                result.append({
                    "name": route.get("name", ""),
                    "source": "bikepacking.com",
                    "activity_type": "bikepacking",
                    "difficulty": route.get("difficulty"),
                    "length_miles": route.get("length_miles"),
                    "elevation_gain": route.get("elevation_gain"),
                    "description": route.get("description", ""),
                    "url": route.get("url"),
                    "coordinates": route.get("coordinates"),
                    "route_type": route.get("route_type"),
                    "duration_days": route.get("duration_days"),
                })

            return result

        except Exception as e:
            print(f"Error in Bikepacking agent: {e}")
            return []

    async def search_bikepacking_roots_routes(
        self, location: str, context: str = ""
    ) -> List[TrailInfo]:
        """Search for routes from Bikepacking Roots."""
        route_data = search_bikepacking_roots_routes.invoke({"location": location})

        try:
            data = json.loads(route_data) if isinstance(route_data, str) else route_data
            routes = data.get("routes", [])

            result = []
            for route in routes:
                result.append({
                    "name": route.get("name", ""),
                    "source": "bikepackingroots",
                    "activity_type": "bikepacking",
                    "difficulty": route.get("difficulty"),
                    "length_miles": route.get("length_miles"),
                    "description": route.get("description", ""),
                    "url": route.get("url"),
                    "coordinates": route.get("coordinates"),
                })

            return result

        except Exception as e:
            print(f"Error in Bikepacking Roots agent: {e}")
            return []

