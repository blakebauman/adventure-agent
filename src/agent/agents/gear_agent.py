"""Gear and product recommendation specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.models import create_llm
from agent.state import GearRecommendation
from agent.tools import recommend_gear, search_gear_products
from agent.utils import invoke_tool_async


class GearAgent:
    """Agent specialized in gear and product recommendations (affiliate revenue model)."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Gear agent."""
        self.llm = create_llm(
            agent_name="gear",
            model_name=model_name,
            temperature=temperature if temperature is not None else 0.3,
        )

        self.system_prompt = """You are an expert in outdoor gear and equipment for adventures.
You specialize in:
- Mountain bike gear and accessories
- Bikepacking equipment
- Camping and outdoor gear
- Safety equipment
- Clothing and apparel
- Product recommendations from affiliate partners

Provide honest, helpful gear recommendations. Always include affiliate links for revenue.
Focus on quality products that enhance the adventure experience."""

    async def recommend_gear_for_adventure(
        self,
        adventure_type: str,
        duration_days: int,
        skill_level: str,
        gear_owned: List[str] | None = None,
        context: str = "",
    ) -> List[GearRecommendation]:
        """Recommend gear for an adventure."""
        # Use tool to get recommendations - wrap in thread to avoid blocking
        gear_data = await invoke_tool_async(
            recommend_gear,
            {
                "adventure_type": adventure_type,
                "duration_days": duration_days,
                "skill_level": skill_level,
                "gear_owned": gear_owned or [],
            }
        )

        try:
            data = json.loads(gear_data) if isinstance(gear_data, str) else gear_data
            recommendations = data.get("recommendations", [])

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Adventure Type: {adventure_type}
Duration: {duration_days} days
Skill Level: {skill_level}
Gear Already Owned: {gear_owned}

Gear Data: {gear_data}

Analyze and enhance these gear recommendations. Provide:
1. Detailed product descriptions
2. Why each item is recommended
3. Essential vs. optional items
4. Product quality and value assessment
5. Affiliate links for all recommendations
6. Gear combinations and compatibility

Return enhanced information in JSON format with affiliate links.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                adventure_type=adventure_type,
                duration_days=duration_days,
                skill_level=skill_level,
                gear_owned=json.dumps(gear_owned or []),
                gear_data=json.dumps(recommendations),
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
                    enhanced = {"recommendations": recommendations}

            # Convert to GearRecommendation format
            result = []
            for gear in enhanced.get("recommendations", recommendations):
                result.append({
                    "name": gear.get("name", ""),
                    "category": gear.get("category", "general"),
                    "description": gear.get("description", ""),
                    "affiliate_url": gear.get(
                        "affiliate_url", "https://example.com/affiliate"
                    ),
                    "price_range": gear.get("price_range"),
                    "essential": gear.get("essential", False),
                })

            return result

        except Exception as e:
            print(f"Error in Gear agent: {e}")
            return []

    async def search_specific_gear(
        self, category: str, price_range: str | None = None
    ) -> List[Dict[str, Any]]:
        """Search for specific gear products."""
        products_data = await invoke_tool_async(
            search_gear_products,
            {
                "category": category,
                "price_range": price_range,
            }
        )
        try:
            data = (
                json.loads(products_data)
                if isinstance(products_data, str)
                else products_data
            )
            return data.get("products", [])
        except Exception:
            return []

