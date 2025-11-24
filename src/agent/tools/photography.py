"""Photography and media tools."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict

import httpx
from langchain.tools import tool

from agent.config import Config
from agent.tools.geo import get_coordinates, calculate_distance
from agent.tools.web_search import WebSearchTool


@tool
def find_photo_spots(location: str, route_info: Dict[str, Any] | None = None) -> str:
    """Find best photo spots along a route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with photo spots
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        photo_spots = []
        
        # Use Google Places API to find scenic spots
        if Config.GOOGLE_PLACES_API_KEY:
            try:
                with httpx.Client() as client:
                    # Search for tourist attractions and scenic spots
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 10000,  # 10km radius
                        "type": "tourist_attraction",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        places = data.get("results", [])
                        
                        for place in places[:5]:  # Limit to 5 results
                            name = place.get("name", "Photo Spot")
                            rating = place.get("rating")
                            
                            # Determine best time based on location type
                            best_time = "Sunrise or sunset"
                            if "overlook" in name.lower() or "vista" in name.lower():
                                best_time = "Sunrise or sunset"
                            elif "canyon" in name.lower():
                                best_time = "Midday for light beams"
                            
                            photo_spots.append({
                                "name": name,
                                "location": place.get("vicinity", location),
                                "best_time": best_time,
                                "rating": rating,
                                "coordinates": {
                                    "lat": place.get("geometry", {}).get("location", {}).get("lat"),
                                    "lon": place.get("geometry", {}).get("location", {}).get("lng"),
                                },
                            })
                        
                        if photo_spots:
                            return json.dumps({
                                "location": location,
                                "photo_spots": photo_spots,
                                "source": "google_places",
                            })
            except Exception as e:
                print(f"Google Places API error for photo spots: {e}")
        
        # Fallback: Use web search via Tavily
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} best photo spots scenic views"
                results = search_tool.search_web(query)
                
                if results:
                    for result in results[:3]:
                        title = result.get("title", "")
                        content = result.get("content", "")
                        
                        if "photo" in title.lower() or "scenic" in title.lower() or "viewpoint" in title.lower():
                            photo_spots.append({
                                "name": title[:100] if title else "Scenic Overlook",
                                "location": location,
                                "best_time": "Sunrise or sunset",
                            })
                    
                    if photo_spots:
                        return json.dumps({
                            "location": location,
                            "photo_spots": photo_spots,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for photo spots: {e}")
    except Exception as e:
        print(f"Photo spots search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "photo_spots": [
            {
                "name": "Scenic Overlook",
                "location": "Mile 3",
                "best_time": "Sunrise or sunset",
            }
        ],
        "source": "placeholder",
    })


@tool
def find_scenic_viewpoints(location: str, route_info: Dict[str, Any] | None = None) -> str:
    """Find scenic viewpoints along a route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with scenic viewpoints
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        viewpoints = []
        
        # Use Google Places API to find viewpoints
        if Config.GOOGLE_PLACES_API_KEY:
            try:
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 10000,  # 10km radius
                        "keyword": "overlook viewpoint vista",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        places = data.get("results", [])
                        
                        for place in places[:5]:
                            name = place.get("name", "Viewpoint")
                            description = "Panoramic views"
                            
                            # Customize description based on name
                            if "mountain" in name.lower():
                                description = "Panoramic mountain views"
                            elif "canyon" in name.lower():
                                description = "Canyon views"
                            elif "desert" in name.lower():
                                description = "Desert landscape views"
                            
                            viewpoints.append({
                                "name": name,
                                "location": place.get("vicinity", location),
                                "description": description,
                                "coordinates": {
                                    "lat": place.get("geometry", {}).get("location", {}).get("lat"),
                                    "lon": place.get("geometry", {}).get("location", {}).get("lng"),
                                },
                            })
                        
                        if viewpoints:
                            return json.dumps({
                                "location": location,
                                "viewpoints": viewpoints,
                                "source": "google_places",
                            })
            except Exception as e:
                print(f"Google Places API error for viewpoints: {e}")
        
        # Fallback: Use web search via Tavily
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} scenic viewpoints overlook"
                results = search_tool.search_web(query)
                
                if results:
                    for result in results[:3]:
                        title = result.get("title", "")
                        if "viewpoint" in title.lower() or "overlook" in title.lower() or "vista" in title.lower():
                            viewpoints.append({
                                "name": title[:100] if title else "Mountain Vista",
                                "location": location,
                                "description": "Panoramic mountain views",
                            })
                    
                    if viewpoints:
                        return json.dumps({
                            "location": location,
                            "viewpoints": viewpoints,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for viewpoints: {e}")
    except Exception as e:
        print(f"Viewpoints search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "viewpoints": [
            {
                "name": "Mountain Vista",
                "location": "Mile 5",
                "description": "Panoramic mountain views",
            }
        ],
        "source": "placeholder",
    })


@tool
def get_sunrise_sunset_locations(location: str) -> str:
    """Get best locations for sunrise and sunset photos.

    Args:
        location: Location name or region

    Returns:
        JSON string with sunrise/sunset locations
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        # Use web search via Tavily for sunrise/sunset locations
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} sunrise sunset photography locations best spots"
                results = search_tool.search_web(query)
                
                if results:
                    sunrise_locations = []
                    sunset_locations = []
                    
                    for result in results[:5]:
                        title = result.get("title", "")
                        content = result.get("content", "").lower()
                        
                        # Determine if it's a sunrise or sunset location
                        is_sunrise = "sunrise" in content or "east" in content or "morning" in content
                        is_sunset = "sunset" in content or "west" in content or "evening" in content
                        
                        # Try to extract time
                        import re
                        time_match = re.search(r"(\d{1,2}):?(\d{2})?\s*(am|pm)", content)
                        best_time = "6:00 AM" if is_sunrise else "7:00 PM"
                        if time_match:
                            hour = time_match.group(1)
                            minute = time_match.group(2) or "00"
                            period = time_match.group(3).upper()
                            best_time = f"{hour}:{minute} {period}"
                        
                        if is_sunrise or (not is_sunset and "sunrise" in title.lower()):
                            sunrise_locations.append({
                                "name": title[:100] if title else "East Overlook",
                                "best_time": best_time,
                            })
                        elif is_sunset or "sunset" in title.lower():
                            sunset_locations.append({
                                "name": title[:100] if title else "West Overlook",
                                "best_time": best_time,
                            })
                    
                    # If we found locations, return them
                    if sunrise_locations or sunset_locations:
                        # Ensure we have at least one of each
                        if not sunrise_locations:
                            sunrise_locations = [{"name": "East Overlook", "best_time": "6:00 AM"}]
                        if not sunset_locations:
                            sunset_locations = [{"name": "West Overlook", "best_time": "7:00 PM"}]
                        
                        return json.dumps({
                            "location": location,
                            "sunrise_locations": sunrise_locations[:3],
                            "sunset_locations": sunset_locations[:3],
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for sunrise/sunset locations: {e}")
        
        # Calculate approximate sunrise/sunset times based on location
        # Simple approximation: Arizona is roughly UTC-7, so adjust for timezone
        # For summer (longer days), sunrise ~5:30-6:00 AM, sunset ~7:00-7:30 PM
        # For winter (shorter days), sunrise ~6:30-7:00 AM, sunset ~5:00-5:30 PM
        current_month = datetime.now().month
        is_summer = 4 <= current_month <= 9  # April through September
        
        sunrise_time = "6:00 AM" if is_summer else "7:00 AM"
        sunset_time = "7:00 PM" if is_summer else "5:30 PM"
        
        return json.dumps({
            "location": location,
            "sunrise_locations": [
                {
                    "name": "East Overlook",
                    "best_time": sunrise_time,
                }
            ],
            "sunset_locations": [
                {
                    "name": "West Overlook",
                    "best_time": sunset_time,
                }
            ],
            "source": "calculated",
        })
    except Exception as e:
        print(f"Sunrise/sunset locations error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "sunrise_locations": [
            {
                "name": "East Overlook",
                "best_time": "6:00 AM",
            }
        ],
        "sunset_locations": [
            {
                "name": "West Overlook",
                "best_time": "7:00 PM",
            }
        ],
        "source": "placeholder",
    })


@tool
def get_photography_tips(location: str, activity_type: str = "mountain_biking") -> str:
    """Get photography tips for an activity and location.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with photography tips
    """
    try:
        # Use web search via Tavily for photography tips
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                activity_display = activity_type.replace("_", " ").title()
                query = f"{location} {activity_display} photography tips"
                results = search_tool.search_web(query)
                
                if results:
                    tips = []
                    
                    for result in results[:3]:
                        content = result.get("content", "").lower()
                        
                        # Extract common photography tips
                        if "battery" in content or "extra" in content:
                            tips.append("Bring extra batteries")
                        if "filter" in content and ("polariz" in content or "polar" in content):
                            tips.append("Use polarizing filter for landscapes")
                        if "golden hour" in content or "sunrise" in content or "sunset" in content:
                            tips.append("Golden hour is best for photos")
                        if "tripod" in content:
                            tips.append("Use tripod for low light conditions")
                        if "composition" in content:
                            tips.append("Pay attention to composition and framing")
                        if "weather" in content:
                            tips.append("Check weather conditions before shooting")
                    
                    # Ensure we have at least basic tips
                    if not tips:
                        tips = [
                            "Bring extra batteries",
                            "Use polarizing filter for landscapes",
                            "Golden hour is best for photos",
                        ]
                    
                    return json.dumps({
                        "location": location,
                        "activity_type": activity_type,
                        "tips": list(set(tips))[:10],  # Remove duplicates, limit to 10
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for photography tips: {e}")
    except Exception as e:
        print(f"Photography tips error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "tips": [
            "Bring extra batteries",
            "Use polarizing filter for landscapes",
            "Golden hour is best for photos",
        ],
        "source": "placeholder",
    })

