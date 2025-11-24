"""Advocacy and information specialist agent for IMBA and Adventure Cycling."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.models import create_llm
from agent.tools import (
    get_trail_access_info,
    search_adventure_cycling_routes,
    search_imba_trails,
)
from agent.utils import invoke_tool_async


class AdvocacyAgent:
    """Agent specialized in trail advocacy, access, and long-distance cycling routes.

    IMBA (International Mountain Bicycling Association): https://www.imba.com/
    - Trail advocacy and access information
    - Local trail networks
    - Trail conditions and maintenance
    - Trail building resources

    Adventure Cycling Association: https://www.adventurecycling.org/
    - Long-distance cycling routes
    - Route maps and planning
    - Touring resources
    - Network of cycling routes
    """

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Advocacy agent."""
        self.llm = create_llm(
            agent_name="advocacy",
            model_name=model_name,
            temperature=temperature if temperature is not None else 0.3,
        )

        self.system_prompt = """You are an expert in trail advocacy, access, and long-distance cycling routes.
You specialize in:
- IMBA trail networks and access information
- Adventure Cycling Association long-distance routes
- Trail conditions and maintenance
- Local trail advocacy groups
- Route planning for multi-day tours
- Trail access rights and regulations

Provide detailed information about trail access, advocacy, and long-distance route planning."""

    async def get_imba_trail_info(
        self, location: str, context: str = ""
    ) -> Dict[str, Any]:
        """Get IMBA trail network information for a location."""
        trail_data = await invoke_tool_async(
            search_imba_trails,
            {"location": location}
        )

        try:
            data = json.loads(trail_data) if isinstance(trail_data, str) else trail_data

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}

IMBA Trail Data: {trail_data}

Analyze and enhance this IMBA trail information. Provide:
1. Trail network overview
2. Trail access and conditions
3. Local advocacy groups
4. Trail maintenance status
5. Best trails for different skill levels
6. Access points and parking

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                trail_data=json.dumps(data),
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
                    enhanced = data

            return enhanced

        except Exception as e:
            print(f"Error in Advocacy agent (IMBA): {e}")
            return {}

    async def search_adventure_cycling_routes(
        self, location: str, route_type: str | None = None, context: str = ""
    ) -> List[Dict[str, Any]]:
        """Search for Adventure Cycling Association routes."""
        route_data = await invoke_tool_async(
            search_adventure_cycling_routes,
            {
                "location": location,
                "route_type": route_type,
            }
        )

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

Adventure Cycling Routes: {routes}

Analyze and enhance these long-distance cycling routes. Provide:
1. Route descriptions and highlights
2. Route length and difficulty
3. Best sections and segments
4. Accommodation and resupply points
5. Best times to ride
6. Route planning considerations

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                route_type=route_type or "any",
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

            return enhanced.get("routes", routes)

        except Exception as e:
            print(f"Error in Advocacy agent (Adventure Cycling): {e}")
            return []

    async def get_trail_access_info(self, location: str) -> Dict[str, Any]:
        """Get trail access and advocacy information."""
        access_data = await invoke_tool_async(
            get_trail_access_info,
            {"location": location}
        )
        try:
            return (
                json.loads(access_data)
                if isinstance(access_data, str)
                else access_data
            )
        except Exception:
            return {"location": location, "access_info": {}}

