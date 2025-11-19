"""Route planning specialist agent for RideWithGPS and Strava."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.state import TrailInfo
from agent.tools import search_ridewithgps_routes, search_strava_routes, get_route_details


class RoutePlanningAgent:
    """Agent specialized in route planning using RideWithGPS and Strava.

    RideWithGPS: https://ridewithgps.com/
    - Route planning and navigation
    - Large library of cycling routes
    - Turn-by-turn navigation
    - Offline maps

    Strava: https://www.strava.com/
    - Popular routes and segments
    - Community-driven route data
    - Heat maps showing popular routes
    - Route planning tools
    """

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Route Planning agent."""
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else 0.3,
            api_key=Config.OPENAI_API_KEY,
        )

        self.system_prompt = """You are an expert in route planning for cycling and outdoor adventures.
You specialize in:
- RideWithGPS route planning and navigation
- Strava popular routes and segments
- Route optimization and wayfinding
- Community-curated routes
- Turn-by-turn navigation planning
- Route sharing and collaboration

Provide detailed route planning information for adventure planning."""

    async def search_ridewithgps_routes(
        self,
        location: str,
        activity_type: str,
        distance: float | None = None,
        context: str = "",
    ) -> List[TrailInfo]:
        """Search for routes on RideWithGPS.

        Args:
            location: Location name or region
            activity_type: Type of activity
            distance: Target distance in miles
            context: Additional context

        Returns:
            List of route information
        """
        route_data = search_ridewithgps_routes.invoke({
            "location": location,
            "activity_type": activity_type,
            "distance": distance,
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
Activity Type: {activity_type}
Target Distance: {distance}

RideWithGPS Routes: {routes}

Analyze and enhance these routes. Provide:
1. Route descriptions and highlights
2. Elevation profiles and difficulty
3. Navigation considerations
4. Best times to ride
5. Route quality and popularity
6. Turn-by-turn considerations

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                activity_type=activity_type.replace("_", " "),
                distance=distance or "flexible",
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
                    "source": "ridewithgps",
                    "activity_type": activity_type,
                    "difficulty": route.get("difficulty"),
                    "length_miles": route.get("length_miles"),
                    "elevation_gain": route.get("elevation_gain"),
                    "description": route.get("description", ""),
                    "url": route.get("url"),
                    "coordinates": route.get("coordinates"),
                })

            return result

        except Exception as e:
            print(f"Error in Route Planning agent (RideWithGPS): {e}")
            return []

    async def search_strava_routes(
        self,
        location: str,
        activity_type: str,
        popularity: str | None = None,
        context: str = "",
    ) -> List[TrailInfo]:
        """Search for popular routes on Strava.

        Args:
            location: Location name or region
            activity_type: Type of activity
            popularity: Filter by popularity (popular, very_popular, all)
            context: Additional context

        Returns:
            List of route information
        """
        route_data = search_strava_routes.invoke({
            "location": location,
            "activity_type": activity_type,
            "popularity": popularity or "popular",
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
Activity Type: {activity_type}
Popularity: {popularity}

Strava Routes: {routes}

Analyze and enhance these popular routes. Provide:
1. Why these routes are popular
2. Route descriptions and highlights
3. Elevation profiles and difficulty
4. Best segments and features
5. Community insights
6. Best times to ride/run

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                activity_type=activity_type.replace("_", " "),
                popularity=popularity or "popular",
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
                    "source": "strava",
                    "activity_type": activity_type,
                    "difficulty": route.get("difficulty"),
                    "length_miles": route.get("length_miles"),
                    "elevation_gain": route.get("elevation_gain"),
                    "description": route.get("description", ""),
                    "url": route.get("url"),
                    "coordinates": route.get("coordinates"),
                    "popularity_score": route.get("popularity_score"),
                })

            return result

        except Exception as e:
            print(f"Error in Route Planning agent (Strava): {e}")
            return []

    async def get_route_details(
        self, route_id: str, source: str, activity_type: str
    ) -> Dict[str, Any]:
        """Get detailed information about a specific route."""
        details_data = get_route_details.invoke({
            "route_id": route_id,
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
            return {"route_id": route_id, "details": {}}

