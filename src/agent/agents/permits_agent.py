"""Permits and regulations specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.models import create_llm
from agent.tools import (
    check_fire_restrictions,
    check_permit_requirements,
    get_permit_information,
    get_regulations,
    get_seasonal_closures,
)
from agent.utils import invoke_tool_async


class PermitsAgent:
    """Agent specialized in permit requirements, regulations, and access restrictions."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Permits agent."""
        self.llm = create_llm(
            agent_name="permits",
            model_name=model_name,
            temperature=temperature if temperature is not None else 0.3,
        )

        self.system_prompt = """You are an expert on permits and regulations for outdoor adventures.
You specialize in:
- Permit requirements for trails, parks, and wilderness areas
- Application processes and deadlines
- Group size restrictions
- Fire restrictions and regulations
- Seasonal closures and access restrictions
- National Park Service regulations
- Forest Service regulations
- State park regulations
- BLM land regulations
- Recreation.gov permit systems

Provide accurate, detailed permit and regulation information for compliance and planning.
Always check current requirements and deadlines."""

    async def get_permit_info(
        self,
        location: str,
        activity_type: str = "mountain_biking",
        group_size: int | None = None,
        dates: List[str] | None = None,
        context: str = "",
    ) -> Dict[str, Any]:
        """Get comprehensive permit and regulation information.

        Args:
            location: Location name or region
            activity_type: Type of activity
            group_size: Number of people in group
            dates: List of dates in YYYY-MM-DD format
            context: Additional context from orchestrator

        Returns:
            Dictionary with permit and regulation information
        """
        # Check permit requirements - wrap in thread to avoid blocking
        permit_check = await invoke_tool_async(
            check_permit_requirements,
            {
                "location": location,
                "activity_type": activity_type,
                "group_size": group_size or 1,
            }
        )

        # Get permit information
        permit_info = await invoke_tool_async(
            get_permit_information,
            {
                "location": location,
                "activity_type": activity_type,
            }
        )

        # Get regulations
        regulations = await invoke_tool_async(
            get_regulations,
            {
                "location": location,
                "activity_type": activity_type,
            }
        )

        # Check fire restrictions
        fire_restrictions = await invoke_tool_async(
            check_fire_restrictions,
            {
                "location": location,
                "dates": dates or [],
            }
        )

        # Get seasonal closures
        closures = await invoke_tool_async(
            get_seasonal_closures,
            {
                "location": location,
            }
        )

        try:
            permit_req = (
                json.loads(permit_check) if isinstance(permit_check, str) else permit_check
            )
            permit_data = (
                json.loads(permit_info) if isinstance(permit_info, str) else permit_info
            )
            regs = (
                json.loads(regulations) if isinstance(regulations, str) else regulations
            )
            fire = (
                json.loads(fire_restrictions) if isinstance(fire_restrictions, str) else fire_restrictions
            )
            closure_data = (
                json.loads(closures) if isinstance(closures, str) else closures
            )

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}
Activity Type: {activity_type}
Group Size: {group_size}
Dates: {dates}

Permit Requirements: {permit_req}
Permit Information: {permit_info}
Regulations: {regs}
Fire Restrictions: {fire}
Seasonal Closures: {closures}

Analyze and enhance this permit and regulation information. Provide:
1. Clear summary of permit requirements
2. Application process and deadlines
3. Group size restrictions
4. Fire restrictions and regulations
5. Seasonal closures and access restrictions
6. Important compliance considerations
7. Contact information for permit applications
8. Any special considerations for the activity type

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                activity_type=activity_type.replace("_", " "),
                group_size=str(group_size) if group_size else "Not specified",
                dates=", ".join(dates) if dates else "Not specified",
                permit_req=json.dumps(permit_req),
                permit_info=json.dumps(permit_data),
                regs=json.dumps(regs),
                fire=json.dumps(fire),
                closures=json.dumps(closure_data),
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
                "permits_required": permit_req.get("permits_required", False),
                "permit_requirements": permit_req,
                "permit_information": permit_data,
                "regulations": regs,
                "fire_restrictions": fire,
                "seasonal_closures": closure_data,
                "analysis": enhanced,
                "compliance_checklist": enhanced.get("compliance_checklist", []),
                "contact_info": enhanced.get("contact_info", {}),
            }

        except Exception as e:
            print(f"Error in Permits agent: {e}")
            return {
                "location": location,
                "permits_required": False,
                "permit_requirements": {},
                "permit_information": {},
                "regulations": {},
                "fire_restrictions": {},
                "seasonal_closures": {},
                "analysis": {},
                "compliance_checklist": [],
                "contact_info": {},
            }

