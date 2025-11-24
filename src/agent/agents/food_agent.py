"""Food and resupply specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.models import create_llm
from agent.tools import (
    find_grocery_stores,
    find_restaurants,
    find_resupply_points,
    find_water_sources,
    get_local_food_recommendations,
)
from agent.utils import invoke_tool_async


class FoodAgent:
    """Agent specialized in food options, resupply points, and water sources."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Food agent."""
        self.llm = create_llm(
            agent_name="food",
            model_name=model_name,
            temperature=temperature if temperature is not None else 0.3,
        )

        self.system_prompt = """You are an expert on food and resupply options for outdoor adventures.
You specialize in:
- Grocery stores near routes and trailheads
- Restaurants and cafes along routes
- Water source locations and quality
- Resupply points for multi-day trips
- Local food specialties and recommendations
- Food storage and bear safety
- Dietary restrictions and options
- Meal planning for adventures

Provide accurate, detailed food and resupply information to help adventurers plan their nutrition."""

    async def get_food_info(
        self,
        location: str,
        route_info: Dict[str, Any] | None = None,
        duration_days: int | None = None,
        context: str = "",
    ) -> Dict[str, Any]:
        """Get comprehensive food and resupply information.

        Args:
            location: Location name or region
            route_info: Information about the route
            duration_days: Duration of the trip in days
            context: Additional context from orchestrator

        Returns:
            Dictionary with food and resupply information
        """
        # Find grocery stores - wrap in thread to avoid blocking
        groceries = await invoke_tool_async(
            find_grocery_stores,
            {
                "location": location,
                "route_info": route_info or {},
            }
        )

        # Find restaurants
        restaurants = await invoke_tool_async(
            find_restaurants,
            {
                "location": location,
                "route_info": route_info or {},
            }
        )

        # Find water sources
        water = await invoke_tool_async(
            find_water_sources,
            {
                "location": location,
                "route_info": route_info or {},
            }
        )

        # Find resupply points
        resupply = await invoke_tool_async(
            find_resupply_points,
            {
                "location": location,
                "duration_days": duration_days or 1,
            }
        )

        # Get local food recommendations
        local_food = await invoke_tool_async(
            get_local_food_recommendations,
            {
                "location": location,
            }
        )

        try:
            grocery_data = (
                json.loads(groceries) if isinstance(groceries, str) else groceries
            )
            restaurant_data = (
                json.loads(restaurants) if isinstance(restaurants, str) else restaurants
            )
            water_data = (
                json.loads(water) if isinstance(water, str) else water
            )
            resupply_data = (
                json.loads(resupply) if isinstance(resupply, str) else resupply
            )
            local_food_data = (
                json.loads(local_food) if isinstance(local_food, str) else local_food
            )

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}
Route Info: {route_info}
Duration: {duration_days} days

Grocery Stores: {groceries}
Restaurants: {restaurants}
Water Sources: {water}
Resupply Points: {resupply}
Local Food Recommendations: {local_food}

Analyze and enhance this food and resupply information. Provide:
1. Grocery store locations and recommendations
2. Restaurant and cafe options along the route
3. Water source locations and quality information
4. Resupply point recommendations for multi-day trips
5. Local food specialties and must-try options
6. Meal planning recommendations
7. Food storage and bear safety considerations
8. Dietary restriction options

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                route_info=json.dumps(route_info) if route_info else "Not provided",
                duration_days=str(duration_days) if duration_days else "Not specified",
                groceries=json.dumps(grocery_data),
                restaurants=json.dumps(restaurant_data),
                water=json.dumps(water_data),
                resupply=json.dumps(resupply_data),
                local_food=json.dumps(local_food_data),
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
                "grocery_stores": grocery_data,
                "restaurants": restaurant_data,
                "water_sources": water_data,
                "resupply_points": resupply_data,
                "local_food": local_food_data,
                "analysis": enhanced,
                "meal_planning": enhanced.get("meal_planning", {}),
                "resupply_strategy": enhanced.get("resupply_strategy", []),
            }

        except Exception as e:
            print(f"Error in Food agent: {e}")
            return {
                "location": location,
                "grocery_stores": {},
                "restaurants": {},
                "water_sources": {},
                "resupply_points": {},
                "local_food": {},
                "analysis": {},
                "meal_planning": {},
                "resupply_strategy": [],
            }

