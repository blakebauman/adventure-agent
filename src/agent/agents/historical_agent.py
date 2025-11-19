"""Historical and cultural specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.tools import (
    find_historical_sites,
    find_cultural_sites,
    get_local_history,
    get_visitation_guidelines,
)


class HistoricalAgent:
    """Agent specialized in historical sites, cultural significance, and local history."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Historical agent."""
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else 0.3,
            api_key=Config.OPENAI_API_KEY,
        )

        self.system_prompt = """You are an expert on historical and cultural sites for outdoor adventures.
You specialize in:
- Historical sites along routes
- Cultural significance of areas
- Local history and stories
- Native American sites and history
- Historical route information
- Educational opportunities
- Respectful visitation guidelines
- Cultural sensitivity and protocols

Provide accurate, detailed historical and cultural information to help adventurers appreciate the areas they visit."""

    async def get_historical_info(
        self,
        location: str,
        route_info: Optional[Dict[str, Any]] = None,
        context: str = "",
    ) -> Dict[str, Any]:
        """Get comprehensive historical and cultural information.

        Args:
            location: Location name or region
            route_info: Information about the route
            context: Additional context from orchestrator

        Returns:
            Dictionary with historical and cultural information
        """
        # Find historical sites
        historical = find_historical_sites.invoke({
            "location": location,
            "route_info": route_info or {},
        })

        # Find cultural sites
        cultural = find_cultural_sites.invoke({
            "location": location,
            "route_info": route_info or {},
        })

        # Get local history
        local_history = get_local_history.invoke({
            "location": location,
        })

        # Get visitation guidelines
        guidelines = get_visitation_guidelines.invoke({
            "location": location,
        })

        try:
            historical_data = (
                json.loads(historical) if isinstance(historical, str) else historical
            )
            cultural_data = (
                json.loads(cultural) if isinstance(cultural, str) else cultural
            )
            history_data = (
                json.loads(local_history) if isinstance(local_history, str) else local_history
            )
            guidelines_data = (
                json.loads(guidelines) if isinstance(guidelines, str) else guidelines
            )

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}
Route Info: {route_info}

Historical Sites: {historical}
Cultural Sites: {cultural}
Local History: {history}
Visitation Guidelines: {guidelines}

Analyze and enhance this historical and cultural information. Provide:
1. Historical sites along the route
2. Cultural significance of the area
3. Local history and stories
4. Native American sites and history (if applicable)
5. Educational opportunities
6. Respectful visitation guidelines
7. Cultural sensitivity and protocols
8. Historical route information

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                route_info=json.dumps(route_info) if route_info else "Not provided",
                historical=json.dumps(historical_data),
                cultural=json.dumps(cultural_data),
                history=json.dumps(history_data),
                guidelines=json.dumps(guidelines_data),
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
                "historical_sites": historical_data,
                "cultural_sites": cultural_data,
                "local_history": history_data,
                "visitation_guidelines": guidelines_data,
                "analysis": enhanced,
                "educational_opportunities": enhanced.get("educational_opportunities", []),
                "cultural_protocols": enhanced.get("cultural_protocols", []),
            }

        except Exception as e:
            print(f"Error in Historical agent: {e}")
            return {
                "location": location,
                "historical_sites": {},
                "cultural_sites": {},
                "local_history": {},
                "visitation_guidelines": {},
                "analysis": {},
                "educational_opportunities": [],
                "cultural_protocols": [],
            }

