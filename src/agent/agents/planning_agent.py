"""Planning and itinerary specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.tools import create_itinerary


class PlanningAgent:
    """Agent specialized in creating detailed adventure plans and itineraries."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Planning agent."""
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else 0.3,
            api_key=Config.OPENAI_API_KEY,
        )

        self.system_prompt = """You are an expert in adventure planning and itinerary creation.
You specialize in:
- Day-by-day itinerary planning
- Route optimization
- Logistics and timing
- Distance and duration calculations
- Rest stops and resupply points
- Safety considerations
- Contingency planning

Create detailed, practical adventure plans that are safe and enjoyable."""

    async def create_adventure_itinerary(
        self,
        trails: List[Dict[str, Any]],
        start_location: str,
        duration_days: int,
        preferences: Dict[str, Any] | None = None,
        context: str = "",
    ) -> Dict[str, Any]:
        """Create a detailed day-by-day itinerary."""
        # Use tool to create base itinerary
        itinerary_data = create_itinerary.invoke({
            "trails": trails,
            "start_location": start_location,
            "duration_days": duration_days,
        })

        try:
            data = (
                json.loads(itinerary_data)
                if isinstance(itinerary_data, str)
                else itinerary_data
            )
            base_itinerary = data.get("itinerary", [])

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Start Location: {start_location}
Duration: {duration_days} days
User Preferences: {preferences}

Trails: {trails}
Base Itinerary: {base_itinerary}

Create a comprehensive, detailed itinerary. Include for each day:
1. Morning activities and start time
2. Trail routes and distances
3. Elevation profiles and difficulty
4. Rest stops and lunch locations
5. Afternoon activities
6. Camping/accommodation for the night
7. Daily distance and elevation totals
8. Safety considerations
9. Weather considerations
10. Resupply points if needed

Return enhanced itinerary in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                start_location=start_location,
                duration_days=duration_days,
                preferences=json.dumps(preferences or {}),
                trails=json.dumps(trails),
                base_itinerary=json.dumps(base_itinerary),
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
                    enhanced = {"itinerary": base_itinerary}

            return {
                "itinerary": enhanced.get("itinerary", base_itinerary),
                "total_distance_miles": enhanced.get("total_distance_miles", 0.0),
                "estimated_duration_days": duration_days,
                "difficulty": enhanced.get("difficulty", "moderate"),
                "logistics": enhanced.get("logistics", {}),
            }

        except Exception as e:
            print(f"Error in Planning agent: {e}")
            return {
                "itinerary": [],
                "total_distance_miles": 0.0,
                "estimated_duration_days": duration_days,
                "difficulty": "unknown",
            }

