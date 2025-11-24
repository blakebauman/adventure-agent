"""Transportation and logistics specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.models import create_llm
from agent.tools import (
    find_bike_transport_options,
    find_shuttle_services,
    get_car_rental_recommendations,
    get_parking_information,
    get_public_transportation,
)
from agent.utils import invoke_tool_async


class TransportationAgent:
    """Agent specialized in transportation, parking, and logistics for getting to/from trailheads."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Transportation agent."""
        self.llm = create_llm(
            agent_name="transportation",
            model_name=model_name,
            temperature=temperature if temperature is not None else 0.3,
        )

        self.system_prompt = """You are an expert on transportation and logistics for outdoor adventures.
You specialize in:
- Parking information and availability at trailheads
- Shuttle services for point-to-point routes
- Public transportation to trailheads
- Bike-friendly transit options
- Car rental recommendations
- Getting to/from trailheads
- Multi-day trip logistics
- Vehicle access and restrictions

Provide accurate, detailed transportation information to help adventurers plan their trips."""

    async def get_transportation_info(
        self,
        location: str,
        trailhead: str | None = None,
        route_type: str | None = None,
        context: str = "",
    ) -> Dict[str, Any]:
        """Get comprehensive transportation and logistics information.

        Args:
            location: Location name or region
            trailhead: Specific trailhead name
            route_type: Type of route (loop, point_to_point, out_and_back)
            context: Additional context from orchestrator

        Returns:
            Dictionary with transportation information
        """
        # Get parking information - wrap in thread to avoid blocking
        parking = await invoke_tool_async(
            get_parking_information,
            {
                "location": location,
                "trailhead": trailhead,
            }
        )

        # Find shuttle services
        shuttles = await invoke_tool_async(
            find_shuttle_services,
            {
                "location": location,
                "route_type": route_type,
            }
        )

        # Get public transportation
        public_transit = await invoke_tool_async(
            get_public_transportation,
            {
                "location": location,
                "trailhead": trailhead,
            }
        )

        # Find bike transport options
        bike_transport = await invoke_tool_async(
            find_bike_transport_options,
            {
                "location": location,
            }
        )

        # Get car rental recommendations
        car_rentals = await invoke_tool_async(
            get_car_rental_recommendations,
            {
                "location": location,
            }
        )

        try:
            parking_data = (
                json.loads(parking) if isinstance(parking, str) else parking
            )
            shuttle_data = (
                json.loads(shuttles) if isinstance(shuttles, str) else shuttles
            )
            transit_data = (
                json.loads(public_transit) if isinstance(public_transit, str) else public_transit
            )
            bike_data = (
                json.loads(bike_transport) if isinstance(bike_transport, str) else bike_transport
            )
            rental_data = (
                json.loads(car_rentals) if isinstance(car_rentals, str) else car_rentals
            )

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}
Trailhead: {trailhead}
Route Type: {route_type}

Parking Information: {parking}
Shuttle Services: {shuttles}
Public Transportation: {transit}
Bike Transport Options: {bike}
Car Rental Recommendations: {rentals}

Analyze and enhance this transportation information. Provide:
1. Detailed parking information (availability, fees, restrictions)
2. Shuttle service options for point-to-point routes
3. Public transportation options
4. Bike-friendly transit and transport options
5. Car rental recommendations
6. Best transportation options for the route type
7. Logistics recommendations
8. Access considerations

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                trailhead=trailhead or "Not specified",
                route_type=route_type or "Not specified",
                parking=json.dumps(parking_data),
                shuttles=json.dumps(shuttle_data),
                transit=json.dumps(transit_data),
                bike=json.dumps(bike_data),
                rentals=json.dumps(rental_data),
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
                "trailhead": trailhead,
                "parking": parking_data,
                "shuttle_services": shuttle_data,
                "public_transportation": transit_data,
                "bike_transport": bike_data,
                "car_rentals": rental_data,
                "analysis": enhanced,
                "recommended_options": enhanced.get("recommended_options", []),
                "logistics_tips": enhanced.get("logistics_tips", []),
            }

        except Exception as e:
            print(f"Error in Transportation agent: {e}")
            return {
                "location": location,
                "trailhead": trailhead,
                "parking": {},
                "shuttle_services": {},
                "public_transportation": {},
                "bike_transport": {},
                "car_rentals": {},
                "analysis": {},
                "recommended_options": [],
                "logistics_tips": [],
            }

