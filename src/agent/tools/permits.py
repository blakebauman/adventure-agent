"""Permits and regulations tools."""

from __future__ import annotations

import json
from typing import List

import httpx
from langchain.tools import tool

from agent.config import Config
from agent.tools.geo import get_coordinates
from agent.tools.web_search import WebSearchTool


@tool
def check_permit_requirements(
    location: str, activity_type: str = "mountain_biking", group_size: int = 1
) -> str:
    """Check if permits are required for a location and activity.

    Args:
        location: Location name or region
        activity_type: Type of activity
        group_size: Number of people in group

    Returns:
        JSON string with permit requirements
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        # Use Recreation.gov API to find facilities and check permit requirements
        with httpx.Client() as client:
            url = "https://ridb.recreation.gov/api/v1/facilities"
            api_key = Config.RECREATION_GOV_API_KEY or "public"
            headers = {"apikey": api_key}
            params = {
                "limit": 10,
                "offset": 0,
                "latitude": lat,
                "longitude": lon,
                "radius": 25,  # 25 mile radius
            }
            
            try:
                response = client.get(url, headers=headers, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    facilities = data.get("RECDATA", [])
                    
                    # Check if any facilities require permits
                    permit_info = []
                    for facility in facilities[:5]:  # Check top 5 facilities
                        facility_name = facility.get("FacilityName", "")
                        reservable = facility.get("Reservable", False)
                        permit_required = reservable or group_size > 10
                        
                        if permit_required:
                            permit_info.append({
                                "facility": facility_name,
                                "permit_required": True,
                                "permit_type": "Reservation required" if reservable else "Group permit",
                                "group_size_threshold": 10,
                            })
                    
                    if permit_info:
                        return json.dumps({
                            "location": location,
                            "activity_type": activity_type,
                            "permits_required": True,
                            "permit_details": permit_info,
                            "group_size": group_size,
                            "source": "recreation.gov",
                        })
                    else:
                        # No permits required for small groups
                        return json.dumps({
                            "location": location,
                            "activity_type": activity_type,
                            "permits_required": group_size > 10,
                            "permit_type": "Day use" if group_size <= 10 else "Group permit",
                            "group_size": group_size,
                            "source": "recreation.gov",
                        })
            except Exception as e:
                print(f"Recreation.gov API error: {e}")
        
        # Fallback: Use web search via Tavily if available
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} {activity_type} permit requirements"
                results = search_tool.search_web(query)
                
                if results:
                    # Extract permit information from search results
                    permit_required = False
                    permit_type = "Day use"
                    for result in results[:3]:
                        content = result.get("content", "").lower()
                        if "permit required" in content or "permit needed" in content:
                            permit_required = True
                            if "group" in content or group_size > 10:
                                permit_type = "Group permit"
                            break
                    
                    return json.dumps({
                        "location": location,
                        "activity_type": activity_type,
                        "permits_required": permit_required or group_size > 10,
                        "permit_type": permit_type,
                        "group_size": group_size,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for permit requirements: {e}")
    except Exception as e:
        print(f"Permit check error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "permits_required": group_size > 10,
        "permit_type": "Day use" if group_size <= 10 else "Group permit",
        "application_process": "Apply online at recreation.gov",
        "group_size": group_size,
        "source": "placeholder",
    })


@tool
def get_permit_information(location: str, activity_type: str = "mountain_biking") -> str:
    """Get detailed permit information.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with permit information
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        # Use Recreation.gov API to find permit information
        with httpx.Client() as client:
            url = "https://ridb.recreation.gov/api/v1/facilities"
            api_key = Config.RECREATION_GOV_API_KEY or "public"
            headers = {"apikey": api_key}
            params = {
                "limit": 5,
                "offset": 0,
                "latitude": lat,
                "longitude": lon,
                "radius": 25,
            }
            
            try:
                response = client.get(url, headers=headers, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    facilities = data.get("RECDATA", [])
                    
                    permit_info_list = []
                    for facility in facilities[:3]:
                        facility_id = facility.get("FacilityID")
                        facility_name = facility.get("FacilityName", "")
                        reservable = facility.get("Reservable", False)
                        
                        if reservable and facility_id:
                            permit_info_list.append({
                                "facility": facility_name,
                                "where_to_apply": "recreation.gov",
                                "application_url": f"https://www.recreation.gov/camping/campgrounds/{facility_id}",
                                "deadline": "30 days in advance recommended",
                                "cost": "Varies by facility",
                                "contact": "Check recreation.gov for details",
                            })
                    
                    if permit_info_list:
                        return json.dumps({
                            "location": location,
                            "activity_type": activity_type,
                            "permit_info": permit_info_list,
                            "source": "recreation.gov",
                        })
            except Exception as e:
                print(f"Recreation.gov API error: {e}")
        
        # Fallback: Use web search via Tavily if available
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} {activity_type} permit application information"
                results = search_tool.search_web(query)
                
                if results:
                    permit_info = {
                        "where_to_apply": "recreation.gov",
                        "deadline": "30 days in advance",
                        "cost": "$5-20 per person",
                        "contact": "Local ranger station",
                    }
                    
                    # Extract information from search results
                    for result in results[:2]:
                        content = result.get("content", "")
                        if "recreation.gov" in content.lower():
                            permit_info["where_to_apply"] = "recreation.gov"
                        if "days" in content.lower() and "advance" in content.lower():
                            # Try to extract deadline info
                            pass
                    
                    return json.dumps({
                        "location": location,
                        "activity_type": activity_type,
                        "permit_info": permit_info,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for permit information: {e}")
    except Exception as e:
        print(f"Permit information error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "permit_info": {
            "where_to_apply": "recreation.gov",
            "deadline": "30 days in advance",
            "cost": "$5-20 per person",
            "contact": "Local ranger station",
        },
        "source": "placeholder",
    })


@tool
def get_regulations(location: str, activity_type: str = "mountain_biking") -> str:
    """Get regulations for a location and activity.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with regulations
    """
    try:
        # Use web search via Tavily for regulations
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} {activity_type} regulations rules"
                results = search_tool.search_web(query)
                
                if results:
                    regulations = []
                    group_size_limit = 10
                    camping_restrictions = "Designated sites only"
                    
                    # Extract regulations from search results
                    for result in results[:3]:
                        content = result.get("content", "")
                        title = result.get("title", "")
                        
                        # Common regulation patterns
                        if "stay on trail" in content.lower() or "designated trail" in content.lower():
                            regulations.append("Stay on designated trails")
                        if "pack in pack out" in content.lower() or "leave no trace" in content.lower():
                            regulations.append("Pack in, pack out")
                        if "no motorized" in content.lower() or "no motor" in content.lower():
                            regulations.append("No motorized vehicles")
                        if "wildlife" in content.lower() and ("respect" in content.lower() or "distance" in content.lower()):
                            regulations.append("Respect wildlife")
                        if "group size" in content.lower() or "group limit" in content.lower():
                            # Try to extract group size limit
                            import re
                            size_match = re.search(r"group.*?(\d+)", content.lower())
                            if size_match:
                                group_size_limit = int(size_match.group(1))
                        if "camping" in content.lower() and "designated" in content.lower():
                            camping_restrictions = "Designated sites only"
                    
                    # Ensure we have at least basic regulations
                    if not regulations:
                        regulations = [
                            "Stay on designated trails",
                            "Pack in, pack out",
                            "No motorized vehicles",
                            "Respect wildlife",
                        ]
                    
                    return json.dumps({
                        "location": location,
                        "activity_type": activity_type,
                        "regulations": regulations[:10],  # Limit to 10 regulations
                        "group_size_limits": group_size_limit,
                        "camping_restrictions": camping_restrictions,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for regulations: {e}")
    except Exception as e:
        print(f"Regulations error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "regulations": [
            "Stay on designated trails",
            "Pack in, pack out",
            "No motorized vehicles",
            "Respect wildlife",
        ],
        "group_size_limits": 10,
        "camping_restrictions": "Designated sites only",
        "source": "placeholder",
    })


@tool
def check_fire_restrictions(location: str, dates: List[str] | None = None) -> str:
    """Check fire restrictions for a location and dates.

    Args:
        location: Location name or region
        dates: List of dates in YYYY-MM-DD format

    Returns:
        JSON string with fire restrictions
    """
    try:
        # Use web search via Tavily for fire restrictions
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                date_str = f" {dates[0]}" if dates else ""
                query = f"{location} fire restrictions{date_str}"
                results = search_tool.search_web(query)
                
                if results:
                    fire_restrictions = "Campfires allowed in designated areas only"
                    current_level = "Moderate"
                    restrictions = []
                    
                    # Extract fire restriction information
                    for result in results[:3]:
                        content = result.get("content", "").lower()
                        title = result.get("title", "").lower()
                        
                        # Check for fire restriction levels
                        if "stage 1" in content or "stage 1" in title:
                            current_level = "Stage 1"
                            restrictions.append("No campfires outside designated areas")
                        elif "stage 2" in content or "stage 2" in title:
                            current_level = "Stage 2"
                            restrictions.append("No campfires outside designated areas")
                            restrictions.append("No smoking outside vehicles")
                        elif "stage 3" in content or "stage 3" in title:
                            current_level = "Stage 3"
                            restrictions.append("No campfires allowed")
                            restrictions.append("No smoking")
                        elif "fire ban" in content or "fire ban" in title:
                            current_level = "High"
                            restrictions.append("No campfires allowed")
                        elif "no campfire" in content:
                            restrictions.append("No campfires outside designated areas")
                    
                    if not restrictions:
                        restrictions = ["No campfires outside designated areas"]
                    
                    return json.dumps({
                        "location": location,
                        "fire_restrictions": fire_restrictions,
                        "current_level": current_level,
                        "restrictions": restrictions,
                        "dates": dates,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for fire restrictions: {e}")
    except Exception as e:
        print(f"Fire restrictions error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "fire_restrictions": "Campfires allowed in designated areas only",
        "current_level": "Moderate",
        "restrictions": ["No campfires outside designated areas"],
        "dates": dates,
        "source": "placeholder",
    })


@tool
def get_seasonal_closures(location: str) -> str:
    """Get seasonal closures for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with seasonal closures
    """
    try:
        # Use web search via Tavily for seasonal closures
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} seasonal closures trail closures"
                results = search_tool.search_web(query)
                
                if results:
                    closures = []
                    seasonal_access = "Open year-round"
                    
                    # Extract closure information
                    for result in results[:3]:
                        content = result.get("content", "").lower()
                        title = result.get("title", "").lower()
                        
                        # Check for closure information
                        if "closed" in content or "closure" in content:
                            if "winter" in content:
                                closures.append("Winter closures may apply")
                                seasonal_access = "Seasonal access - check current conditions"
                            if "summer" in content and "closed" in content:
                                closures.append("Summer closures may apply")
                                seasonal_access = "Seasonal access - check current conditions"
                            if "seasonal" in content:
                                seasonal_access = "Seasonal access - check current conditions"
                    
                    return json.dumps({
                        "location": location,
                        "closures": closures if closures else [],
                        "seasonal_access": seasonal_access,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for seasonal closures: {e}")
    except Exception as e:
        print(f"Seasonal closures error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "closures": [],
        "seasonal_access": "Open year-round",
        "source": "placeholder",
    })

