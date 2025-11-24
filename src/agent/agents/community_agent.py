"""Community and social specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.models import create_llm
from agent.tools import (
    find_group_rides,
    find_local_clubs,
    find_meetup_groups,
    find_upcoming_events,
    find_volunteer_opportunities,
)


class CommunityAgent:
    """Agent specialized in local clubs, events, and community resources."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Community agent."""
        self.llm = create_llm(
            agent_name="community",
            model_name=model_name,
            temperature=temperature if temperature is not None else 0.3,
        )

        self.system_prompt = """You are an expert on community and social resources for outdoor adventures.
You specialize in:
- Local cycling and hiking clubs
- Meetup groups for outdoor activities
- Upcoming events and gatherings
- Group ride information
- Trail work days and volunteer opportunities
- Community resources and connections
- Local knowledge and insider tips

Provide accurate, detailed community information to help adventurers connect with local communities."""

    async def get_community_info(
        self,
        location: str,
        activity_type: str = "mountain_biking",
        context: str = "",
    ) -> Dict[str, Any]:
        """Get comprehensive community and social information.

        Args:
            location: Location name or region
            activity_type: Type of activity
            context: Additional context from orchestrator

        Returns:
            Dictionary with community information
        """
        # Find local clubs
        clubs = find_local_clubs.invoke({
            "location": location,
            "activity_type": activity_type,
        })

        # Find meetup groups
        meetups = find_meetup_groups.invoke({
            "location": location,
            "activity_type": activity_type,
        })

        # Find upcoming events
        events = find_upcoming_events.invoke({
            "location": location,
            "activity_type": activity_type,
        })

        # Find group rides
        group_rides = find_group_rides.invoke({
            "location": location,
            "activity_type": activity_type,
        })

        # Find volunteer opportunities
        volunteer = find_volunteer_opportunities.invoke({
            "location": location,
        })

        try:
            clubs_data = (
                json.loads(clubs) if isinstance(clubs, str) else clubs
            )
            meetups_data = (
                json.loads(meetups) if isinstance(meetups, str) else meetups
            )
            events_data = (
                json.loads(events) if isinstance(events, str) else events
            )
            rides_data = (
                json.loads(group_rides) if isinstance(group_rides, str) else group_rides
            )
            volunteer_data = (
                json.loads(volunteer) if isinstance(volunteer, str) else volunteer
            )

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location}
Activity Type: {activity_type}

Local Clubs: {clubs}
Meetup Groups: {meetups}
Upcoming Events: {events}
Group Rides: {rides}
Volunteer Opportunities: {volunteer}

Analyze and enhance this community information. Provide:
1. Local clubs and organizations
2. Meetup groups for the activity
3. Upcoming events and gatherings
4. Group ride information
5. Volunteer opportunities (trail work days, etc.)
6. Community resources and connections
7. Local knowledge and insider tips
8. How to get involved

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location=location,
                activity_type=activity_type.replace("_", " "),
                clubs=json.dumps(clubs_data),
                meetups=json.dumps(meetups_data),
                events=json.dumps(events_data),
                rides=json.dumps(rides_data),
                volunteer=json.dumps(volunteer_data),
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
                "local_clubs": clubs_data,
                "meetup_groups": meetups_data,
                "upcoming_events": events_data,
                "group_rides": rides_data,
                "volunteer_opportunities": volunteer_data,
                "analysis": enhanced,
                "community_resources": enhanced.get("community_resources", []),
                "insider_tips": enhanced.get("insider_tips", []),
            }

        except Exception as e:
            print(f"Error in Community agent: {e}")
            return {
                "location": location,
                "local_clubs": {},
                "meetup_groups": {},
                "upcoming_events": {},
                "group_rides": {},
                "volunteer_opportunities": {},
                "analysis": {},
                "community_resources": [],
                "insider_tips": [],
            }

