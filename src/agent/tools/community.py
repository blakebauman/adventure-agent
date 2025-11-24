"""Community and social tools."""

from __future__ import annotations

import json

from langchain.tools import tool

from agent.config import Config
from agent.tools.web_search import WebSearchTool


@tool
def find_local_clubs(location: str, activity_type: str = "mountain_biking") -> str:
    """Find local clubs for an activity type.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with local clubs
    """
    try:
        # Use web search via Tavily for local clubs
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                activity_display = activity_type.replace("_", " ").title()
                query = f"{location} {activity_display} club organization"
                results = search_tool.search_web(query)
                
                if results:
                    clubs = []
                    
                    for result in results[:5]:
                        title = result.get("title", "")
                        content = result.get("content", "")
                        url = result.get("url", "")
                        
                        if "club" in title.lower() or "organization" in title.lower():
                            # Extract club information
                            activities = ["Group rides", "Trail maintenance"]
                            if "maintenance" in content.lower() or "trail work" in content.lower():
                                activities.append("Trail maintenance")
                            if "ride" in content.lower() or "group" in content.lower():
                                activities.append("Group rides")
                            
                            clubs.append({
                                "name": title[:100] if title else f"Local {activity_display} Club",
                                "contact": "See website for contact information",
                                "activities": activities,
                                "url": url,
                            })
                    
                    if clubs:
                        return json.dumps({
                            "location": location,
                            "activity_type": activity_type,
                            "clubs": clubs,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for local clubs: {e}")
    except Exception as e:
        print(f"Local clubs search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "clubs": [
            {
                "name": f"Local {activity_type.replace('_', ' ').title()} Club",
                "contact": "Find on social media",
                "activities": ["Group rides", "Trail maintenance"],
            }
        ],
        "source": "placeholder",
    })


@tool
def find_meetup_groups(location: str, activity_type: str = "mountain_biking") -> str:
    """Find Meetup groups for an activity type.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with Meetup groups
    """
    try:
        # Use web search via Tavily for Meetup groups
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                activity_display = activity_type.replace("_", " ").title()
                query = f"{location} {activity_display} meetup group"
                results = search_tool.search_web(query)
                
                if results:
                    meetup_groups = []
                    
                    for result in results[:5]:
                        title = result.get("title", "")
                        content = result.get("content", "")
                        url = result.get("url", "")
                        
                        if "meetup" in title.lower() or "meetup.com" in url.lower():
                            # Extract member count if available
                            members = "Active group"
                            if "member" in content.lower():
                                import re
                                member_match = re.search(r"(\d+)\s*member", content.lower())
                                if member_match:
                                    members = f"{member_match.group(1)} members"
                            
                            meetup_groups.append({
                                "name": title[:100] if title else f"{activity_display} Meetup",
                                "platform": "Meetup.com",
                                "members": members,
                                "url": url,
                            })
                    
                    if meetup_groups:
                        return json.dumps({
                            "location": location,
                            "activity_type": activity_type,
                            "meetup_groups": meetup_groups,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for Meetup groups: {e}")
    except Exception as e:
        print(f"Meetup groups search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "meetup_groups": [
            {
                "name": f"{activity_type.replace('_', ' ').title()} Meetup",
                "platform": "Meetup.com",
                "members": "Active group",
            }
        ],
        "source": "placeholder",
    })


@tool
def find_upcoming_events(location: str, activity_type: str = "mountain_biking") -> str:
    """Find upcoming events for an activity type.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with upcoming events
    """
    try:
        # Use web search via Tavily for upcoming events
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                activity_display = activity_type.replace("_", " ").title()
                query = f"{location} {activity_display} events upcoming 2024"
                results = search_tool.search_web(query)
                
                if results:
                    events = []
                    
                    for result in results[:5]:
                        title = result.get("title", "")
                        content = result.get("content", "")
                        url = result.get("url", "")
                        
                        if "event" in title.lower() or "festival" in title.lower() or "race" in title.lower():
                            # Try to extract date
                            date = "Upcoming"
                            import re
                            date_match = re.search(r"(\w+\s+\d{1,2},?\s+\d{4})|(\d{1,2}/\d{1,2}/\d{4})", content)
                            if date_match:
                                date = date_match.group(0)
                            
                            event_type = "Community event"
                            if "race" in title.lower():
                                event_type = "Race"
                            elif "festival" in title.lower():
                                event_type = "Festival"
                            elif "workshop" in title.lower():
                                event_type = "Workshop"
                            
                            events.append({
                                "name": title[:100] if title else "Trail Festival",
                                "date": date,
                                "type": event_type,
                                "url": url,
                            })
                    
                    if events:
                        return json.dumps({
                            "location": location,
                            "activity_type": activity_type,
                            "events": events,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for upcoming events: {e}")
    except Exception as e:
        print(f"Upcoming events search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "events": [
            {
                "name": "Trail Festival",
                "date": "Upcoming",
                "type": "Community event",
            }
        ],
        "source": "placeholder",
    })


@tool
def find_group_rides(location: str, activity_type: str = "mountain_biking") -> str:
    """Find group ride information.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with group ride information
    """
    try:
        # Use web search via Tavily for group rides
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                activity_display = activity_type.replace("_", " ").title()
                query = f"{location} {activity_display} group ride schedule"
                results = search_tool.search_web(query)
                
                if results:
                    group_rides = []
                    
                    for result in results[:3]:
                        content = result.get("content", "").lower()
                        title = result.get("title", "")
                        
                        # Extract common group ride patterns
                        day = "Saturday"
                        time = "9:00 AM"
                        skill_level = "All levels"
                        
                        # Try to extract day
                        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                        for d in days:
                            if d in content:
                                day = d.capitalize()
                                break
                        
                        # Try to extract time
                        import re
                        time_match = re.search(r"(\d{1,2}):?(\d{2})?\s*(am|pm)", content)
                        if time_match:
                            hour = time_match.group(1)
                            minute = time_match.group(2) or "00"
                            period = time_match.group(3).upper()
                            time = f"{hour}:{minute} {period}"
                        
                        # Check for skill level
                        if "beginner" in content:
                            skill_level = "Beginner"
                        elif "intermediate" in content:
                            skill_level = "Intermediate"
                        elif "advanced" in content or "expert" in content:
                            skill_level = "Advanced"
                        
                        group_rides.append({
                            "day": day,
                            "time": time,
                            "location": "Trailhead",
                            "skill_level": skill_level,
                        })
                    
                    if group_rides:
                        return json.dumps({
                            "location": location,
                            "activity_type": activity_type,
                            "group_rides": group_rides,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for group rides: {e}")
    except Exception as e:
        print(f"Group rides search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "group_rides": [
            {
                "day": "Saturday",
                "time": "9:00 AM",
                "location": "Trailhead",
                "skill_level": "All levels",
            }
        ],
        "source": "placeholder",
    })


@tool
def find_volunteer_opportunities(location: str) -> str:
    """Find volunteer opportunities (trail work days, etc.).

    Args:
        location: Location name or region

    Returns:
        JSON string with volunteer opportunities
    """
    try:
        # Use web search via Tavily for volunteer opportunities
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} volunteer trail work day"
                results = search_tool.search_web(query)
                
                if results:
                    volunteer_opportunities = []
                    
                    for result in results[:5]:
                        title = result.get("title", "")
                        content = result.get("content", "")
                        url = result.get("url", "")
                        
                        if "volunteer" in title.lower() or "trail work" in title.lower() or "maintenance" in title.lower():
                            # Extract organization and frequency
                            organization = "Local trail organization"
                            if "organization" in content.lower() or "group" in content.lower():
                                # Try to extract organization name
                                import re
                                org_match = re.search(r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:trail|organization|group)", content)
                                if org_match:
                                    organization = org_match.group(1)
                            
                            frequency = "Monthly"
                            if "weekly" in content.lower():
                                frequency = "Weekly"
                            elif "monthly" in content.lower():
                                frequency = "Monthly"
                            elif "quarterly" in content.lower():
                                frequency = "Quarterly"
                            
                            volunteer_type = "Trail work day"
                            if "maintenance" in content.lower():
                                volunteer_type = "Trail maintenance"
                            elif "cleanup" in content.lower():
                                volunteer_type = "Trail cleanup"
                            
                            volunteer_opportunities.append({
                                "type": volunteer_type,
                                "organization": organization,
                                "frequency": frequency,
                                "url": url,
                            })
                    
                    if volunteer_opportunities:
                        return json.dumps({
                            "location": location,
                            "volunteer_opportunities": volunteer_opportunities,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for volunteer opportunities: {e}")
    except Exception as e:
        print(f"Volunteer opportunities search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "volunteer_opportunities": [
            {
                "type": "Trail work day",
                "organization": "Local trail organization",
                "frequency": "Monthly",
            }
        ],
        "source": "placeholder",
    })

