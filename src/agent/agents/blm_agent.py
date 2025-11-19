"""BLM Land specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.state import BLMLandInfo
from agent.tools import get_blm_regulations, search_blm_lands


class BLMAgent:
    """Agent specialized in BLM (Bureau of Land Management) lands information."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the BLM agent."""
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else 0.3,
            api_key=Config.OPENAI_API_KEY,
        )

        self.system_prompt = """You are an expert on Bureau of Land Management (BLM) lands 
in the United States. You specialize in:
- BLM land locations and access points
- Regulations and permit requirements
- Camping and recreation opportunities
- Trail access and restrictions
- Multi-use land management policies

Provide accurate, detailed information about BLM lands for adventure planning.
Always check current regulations and permit requirements."""

    async def get_blm_information(
        self, region: str, activity_type: str, context: str = ""
    ) -> list[BLMLandInfo]:
        """Get BLM land information for a region."""
        # Use tool to search for BLM lands
        blm_data = search_blm_lands.invoke({
            "region": region,
            "activity_type": activity_type,
        })

        try:
            data = json.loads(blm_data) if isinstance(blm_data, str) else blm_data
            lands = data.get("lands", [])

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Region: {region}
Activity: {activity_type}

BLM Data: {blm_data}

Analyze and enhance this BLM land information. Provide detailed information about:
1. Access points and how to reach them
2. Current regulations and permit requirements
3. Camping options and restrictions
4. Trail access and quality
5. Best times to visit
6. Any special considerations

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                region=region,
                activity_type=activity_type,
                blm_data=json.dumps(lands),
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
                    enhanced = {"lands": lands}

            # Convert to BLMLandInfo format
            result = []
            for land in enhanced.get("lands", lands):
                result.append({
                    "land_name": land.get("name", ""),
                    "access_points": land.get("access_points", []),
                    "regulations": land.get("regulations", []),
                    "permits_required": land.get("permits_required", False),
                    "camping_allowed": land.get("camping_allowed", False),
                    "description": land.get("description", ""),
                    "coordinates": land.get("coordinates"),
                })

            return result

        except Exception as e:
            print(f"Error in BLM agent: {e}")
            return []

    async def get_regulations(self, land_name: str) -> Dict[str, Any]:
        """Get specific regulations for a BLM land."""
        regulations_data = get_blm_regulations.invoke({"land_name": land_name})
        try:
            return (
                json.loads(regulations_data)
                if isinstance(regulations_data, str)
                else regulations_data
            )
        except Exception:
            return {"regulations": [], "permits_required": False}

