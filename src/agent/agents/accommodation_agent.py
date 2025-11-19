"""Accommodation specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.state import AccommodationInfo
from agent.tools import search_accommodations


class AccommodationAgent:
    """Agent specialized in finding accommodations for adventures."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Accommodation agent."""
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else 0.3,
            api_key=Config.OPENAI_API_KEY,
        )

        self.system_prompt = """You are an expert in finding accommodations for adventure trips.
You specialize in:
- Campgrounds (BLM, National Forest, State Parks, private)
- Hotels and motels near trailheads
- Hostels and budget accommodations
- Backcountry camping options
- Booking availability and pricing
- Amenities and facilities

Provide detailed accommodation options suitable for adventure travelers."""

    async def find_accommodations(
        self,
        location: str,
        accommodation_type: str | None = None,
        check_in: str | None = None,
        check_out: str | None = None,
        context: str = "",
    ) -> List[AccommodationInfo]:
        """Find accommodations near a location."""
        # Use tool to search accommodations
        acc_data = search_accommodations.invoke({
            "location": location,
            "accommodation_type": accommodation_type,
            "check_in": check_in,
            "check_out": check_out,
        })

        try:
            data = json.loads(acc_data) if isinstance(acc_data, str) else acc_data
            accommodations = data.get("accommodations", [])

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}
Type: {accommodation_type}
Check-in: {check_in}
Check-out: {check_out}

Accommodation Data: {acc_data}

Analyze and enhance this accommodation information. Provide:
1. Detailed descriptions
2. Proximity to trails and adventure activities
3. Amenities and facilities
4. Pricing and value assessment
5. Booking requirements
6. Best options for adventure travelers

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                accommodation_type=accommodation_type or "any",
                check_in=check_in or "flexible",
                check_out=check_out or "flexible",
                acc_data=json.dumps(accommodations),
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
                    enhanced = {"accommodations": accommodations}

            # Convert to AccommodationInfo format
            result = []
            for acc in enhanced.get("accommodations", accommodations):
                result.append({
                    "name": acc.get("name", ""),
                    "type": acc.get("type", accommodation_type or "campground"),
                    "location": acc.get("location", location),
                    "coordinates": acc.get("coordinates"),
                    "price_range": acc.get("price_range"),
                    "amenities": acc.get("amenities", []),
                    "booking_url": acc.get("booking_url"),
                })

            return result

        except Exception as e:
            print(f"Error in Accommodation agent: {e}")
            return []

