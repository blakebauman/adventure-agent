"""Weather and conditions specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.models import create_llm
from agent.tools import (
    check_weather_alerts,
    get_seasonal_information,
    get_trail_conditions,
    get_weather_forecast,
)
from agent.utils import invoke_tool_async


class WeatherAgent:
    """Agent specialized in weather, trail conditions, and seasonal information."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Weather agent."""
        self.llm = create_llm(
            agent_name="weather",
            model_name=model_name,
            temperature=temperature if temperature is not None else 0.3,
        )

        self.system_prompt = """You are an expert on weather and trail conditions for adventure planning.
You specialize in:
- Real-time weather forecasts for adventure dates
- Trail condition reports (muddy, dry, snow-covered, etc.)
- Seasonal trail access information
- Best time of year recommendations
- Safety considerations based on weather
- Weather alerts and warnings
- Mountain weather patterns
- Avalanche conditions (for winter activities)
- River crossing conditions

Provide accurate, detailed weather and condition information for safe adventure planning.
Always prioritize safety considerations."""

    async def get_weather_info(
        self,
        location: str,
        dates: List[str] | None = None,
        activity_type: str = "mountain_biking",
        context: str = "",
    ) -> Dict[str, Any]:
        """Get comprehensive weather and conditions information.

        Args:
            location: Location name or coordinates
            dates: List of dates in YYYY-MM-DD format
            activity_type: Type of activity
            context: Additional context from orchestrator

        Returns:
            Dictionary with weather and conditions information
        """
        # Get weather forecast - wrap in thread to avoid blocking
        forecast_data = await invoke_tool_async(
            get_weather_forecast,
            {
                "location": location,
                "dates": dates or [],
            }
        )

        # Get trail conditions
        conditions_data = await invoke_tool_async(
            get_trail_conditions,
            {
                "location": location,
                "activity_type": activity_type,
            }
        )

        # Get seasonal information
        seasonal_data = await invoke_tool_async(
            get_seasonal_information,
            {
                "location": location,
                "activity_type": activity_type,
            }
        )

        # Check for weather alerts
        alerts_data = await invoke_tool_async(
            check_weather_alerts,
            {
                "location": location,
            }
        )

        try:
            forecast = (
                json.loads(forecast_data) if isinstance(forecast_data, str) else forecast_data
            )
            conditions = (
                json.loads(conditions_data) if isinstance(conditions_data, str) else conditions_data
            )
            seasonal = (
                json.loads(seasonal_data) if isinstance(seasonal_data, str) else seasonal_data
            )
            alerts = (
                json.loads(alerts_data) if isinstance(alerts_data, str) else alerts_data
            )

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}
Activity Type: {activity_type}
Dates: {dates}

Weather Forecast: {forecast}
Trail Conditions: {conditions}
Seasonal Information: {seasonal}
Weather Alerts: {alerts}

Analyze and enhance this weather and conditions information. Provide:
1. Detailed weather forecast for the adventure dates
2. Current trail conditions and recommendations
3. Best time of year for this activity in this location
4. Safety considerations based on weather
5. Any weather alerts or warnings
6. Activity-specific weather considerations
7. Recommendations for timing or preparation

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                activity_type=activity_type.replace("_", " "),
                dates=", ".join(dates) if dates else "Not specified",
                forecast=json.dumps(forecast),
                conditions=json.dumps(conditions),
                seasonal=json.dumps(seasonal),
                alerts=json.dumps(alerts),
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
                "forecast": forecast,
                "trail_conditions": conditions,
                "seasonal_info": seasonal,
                "alerts": alerts,
                "analysis": enhanced,
                "safety_recommendations": enhanced.get("safety_recommendations", []),
                "best_time_of_year": enhanced.get("best_time_of_year", ""),
            }

        except Exception as e:
            print(f"Error in Weather agent: {e}")
            return {
                "location": location,
                "forecast": {},
                "trail_conditions": {},
                "seasonal_info": {},
                "alerts": [],
                "analysis": {},
                "safety_recommendations": [],
            }

    async def get_trail_conditions_only(
        self, location: str, activity_type: str = "mountain_biking"
    ) -> Dict[str, Any]:
        """Get only trail conditions information."""
        conditions_data = await invoke_tool_async(
            get_trail_conditions,
            {
            "location": location,
            "activity_type": activity_type,
        })
        try:
            return (
                json.loads(conditions_data)
                if isinstance(conditions_data, str)
                else conditions_data
            )
        except Exception:
            return {"conditions": "Unknown", "reports": []}

