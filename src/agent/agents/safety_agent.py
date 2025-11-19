"""Safety and emergency specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.tools import (
    get_emergency_contacts,
    get_safety_information,
    check_wildlife_alerts,
    get_avalanche_forecast,
    get_river_conditions,
    assess_route_safety,
)


class SafetyAgent:
    """Agent specialized in safety information, emergency contacts, and risk assessment."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Safety agent."""
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else 0.3,
            api_key=Config.OPENAI_API_KEY,
        )

        self.system_prompt = """You are an expert on safety and emergency preparedness for outdoor adventures.
You specialize in:
- Emergency contact information for different regions
- Safety recommendations for various activities
- Risk assessment for routes and trails
- Wildlife encounter protocols (bears, mountain lions, etc.)
- Avalanche forecasts and safety (for winter activities)
- River crossing conditions and safety
- Search and rescue information
- First aid considerations
- Safety equipment recommendations
- Weather-related safety concerns

Provide accurate, detailed safety information to help adventurers prepare and stay safe.
Always prioritize safety and risk mitigation."""

    async def get_safety_info(
        self,
        location: str,
        activity_type: str = "mountain_biking",
        route_info: Optional[Dict[str, Any]] = None,
        context: str = "",
    ) -> Dict[str, Any]:
        """Get comprehensive safety and emergency information.

        Args:
            location: Location name or region
            activity_type: Type of activity
            route_info: Information about the route/trail
            context: Additional context from orchestrator

        Returns:
            Dictionary with safety and emergency information
        """
        # Get emergency contacts
        emergency_contacts = get_emergency_contacts.invoke({
            "location": location,
        })

        # Get safety information
        safety_info = get_safety_information.invoke({
            "location": location,
            "activity_type": activity_type,
        })

        # Check wildlife alerts
        wildlife_alerts = check_wildlife_alerts.invoke({
            "location": location,
        })

        # Get avalanche forecast (if applicable)
        avalanche_forecast = {}
        if activity_type in ["skiing", "snowboarding", "winter_hiking"]:
            avalanche_forecast = get_avalanche_forecast.invoke({
                "location": location,
            })

        # Get river conditions (if applicable)
        river_conditions = {}
        if route_info and route_info.get("has_river_crossings"):
            river_conditions = get_river_conditions.invoke({
                "location": location,
            })

        # Assess route safety
        route_safety = assess_route_safety.invoke({
            "location": location,
            "activity_type": activity_type,
            "route_info": route_info or {},
        })

        try:
            contacts = (
                json.loads(emergency_contacts) if isinstance(emergency_contacts, str) else emergency_contacts
            )
            safety = (
                json.loads(safety_info) if isinstance(safety_info, str) else safety_info
            )
            wildlife = (
                json.loads(wildlife_alerts) if isinstance(wildlife_alerts, str) else wildlife_alerts
            )
            avalanche = (
                json.loads(avalanche_forecast) if isinstance(avalanche_forecast, str) else avalanche_forecast
            ) if avalanche_forecast else {}
            river = (
                json.loads(river_conditions) if isinstance(river_conditions, str) else river_conditions
            ) if river_conditions else {}
            safety_assessment = (
                json.loads(route_safety) if isinstance(route_safety, str) else route_safety
            )

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}
Activity Type: {activity_type}
Route Info: {route_info}

Emergency Contacts: {contacts}
Safety Information: {safety}
Wildlife Alerts: {wildlife}
Avalanche Forecast: {avalanche}
River Conditions: {river}
Route Safety Assessment: {safety_assessment}

Analyze and enhance this safety information. Provide:
1. Comprehensive emergency contact information
2. Safety recommendations specific to the activity and location
3. Risk assessment for the route
4. Wildlife encounter protocols
5. Avalanche safety (if applicable)
6. River crossing safety (if applicable)
7. First aid considerations
8. Safety equipment recommendations
9. Weather-related safety concerns
10. Search and rescue information

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                activity_type=activity_type.replace("_", " "),
                route_info=json.dumps(route_info) if route_info else "Not provided",
                contacts=json.dumps(contacts),
                safety=json.dumps(safety),
                wildlife=json.dumps(wildlife),
                avalanche=json.dumps(avalanche) if avalanche else "Not applicable",
                river=json.dumps(river) if river else "Not applicable",
                safety_assessment=json.dumps(safety_assessment),
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
                "emergency_contacts": contacts,
                "safety_information": safety,
                "wildlife_alerts": wildlife,
                "avalanche_forecast": avalanche if avalanche else None,
                "river_conditions": river if river else None,
                "route_safety_assessment": safety_assessment,
                "analysis": enhanced,
                "safety_recommendations": enhanced.get("safety_recommendations", []),
                "risk_level": enhanced.get("risk_level", "moderate"),
                "safety_checklist": enhanced.get("safety_checklist", []),
            }

        except Exception as e:
            print(f"Error in Safety agent: {e}")
            return {
                "location": location,
                "emergency_contacts": {},
                "safety_information": {},
                "wildlife_alerts": {},
                "avalanche_forecast": None,
                "river_conditions": None,
                "route_safety_assessment": {},
                "analysis": {},
                "safety_recommendations": [],
                "risk_level": "unknown",
                "safety_checklist": [],
            }

