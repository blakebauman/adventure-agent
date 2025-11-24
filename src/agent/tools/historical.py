"""Historical and cultural tools."""

from __future__ import annotations

import json
from typing import Any, Dict

import httpx
from langchain.tools import tool

from agent.config import Config
from agent.tools.geo import get_coordinates
from agent.tools.web_search import WebSearchTool


@tool
def find_historical_sites(location: str, route_info: Dict[str, Any] | None = None) -> str:
    """Find historical sites along a route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with historical sites
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        historical_sites = []
        
        # Use Google Places API to find historical sites
        if Config.GOOGLE_PLACES_API_KEY:
            try:
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 10000,  # 10km radius
                        "type": "museum",
                        "keyword": "historical monument",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        places = data.get("results", [])
                        
                        for place in places[:5]:
                            name = place.get("name", "Historical Site")
                            description = "Local historical significance"
                            
                            # Get more details if available
                            place_id = place.get("place_id")
                            if place_id:
                                details_url = "https://maps.googleapis.com/maps/api/place/details/json"
                                details_params = {
                                    "place_id": place_id,
                                    "fields": "name,formatted_address,editorial_summary",
                                    "key": Config.GOOGLE_PLACES_API_KEY,
                                }
                                
                                try:
                                    details_response = client.get(details_url, params=details_params, timeout=10.0)
                                    if details_response.status_code == 200:
                                        details_data = details_response.json().get("result", {})
                                        summary = details_data.get("editorial_summary", {}).get("overview", "")
                                        if summary:
                                            description = summary[:200] + "..." if len(summary) > 200 else summary
                                except Exception:
                                    pass
                            
                            historical_sites.append({
                                "name": name,
                                "location": place.get("vicinity", location),
                                "description": description,
                                "coordinates": {
                                    "lat": place.get("geometry", {}).get("location", {}).get("lat"),
                                    "lon": place.get("geometry", {}).get("location", {}).get("lng"),
                                },
                            })
                        
                        if historical_sites:
                            return json.dumps({
                                "location": location,
                                "historical_sites": historical_sites,
                                "source": "google_places",
                            })
            except Exception as e:
                print(f"Google Places API error for historical sites: {e}")
        
        # Fallback: Use web search via Tavily
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} historical sites monuments markers"
                results = search_tool.search_web(query)
                
                if results:
                    for result in results[:5]:
                        title = result.get("title", "")
                        content = result.get("content", "")
                        
                        if "historical" in title.lower() or "monument" in title.lower() or "marker" in title.lower():
                            description = content[:200] + "..." if len(content) > 200 else content
                            historical_sites.append({
                                "name": title[:100] if title else "Historical Marker",
                                "location": location,
                                "description": description or "Local historical significance",
                            })
                    
                    if historical_sites:
                        return json.dumps({
                            "location": location,
                            "historical_sites": historical_sites,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for historical sites: {e}")
    except Exception as e:
        print(f"Historical sites search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "historical_sites": [
            {
                "name": "Historical Marker",
                "location": "Mile 2",
                "description": "Local historical significance",
            }
        ],
        "source": "placeholder",
    })


@tool
def find_cultural_sites(location: str, route_info: Dict[str, Any] | None = None) -> str:
    """Find cultural sites along a route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with cultural sites
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        cultural_sites = []
        
        # Use Google Places API to find cultural sites
        if Config.GOOGLE_PLACES_API_KEY:
            try:
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 10000,  # 10km radius
                        "type": "museum",
                        "keyword": "cultural heritage",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        places = data.get("results", [])
                        
                        for place in places[:5]:
                            name = place.get("name", "Cultural Site")
                            significance = "Cultural importance"
                            
                            cultural_sites.append({
                                "name": name,
                                "location": place.get("vicinity", location),
                                "significance": significance,
                                "coordinates": {
                                    "lat": place.get("geometry", {}).get("location", {}).get("lat"),
                                    "lon": place.get("geometry", {}).get("location", {}).get("lng"),
                                },
                            })
                        
                        if cultural_sites:
                            return json.dumps({
                                "location": location,
                                "cultural_sites": cultural_sites,
                                "source": "google_places",
                            })
            except Exception as e:
                print(f"Google Places API error for cultural sites: {e}")
        
        # Fallback: Use web search via Tavily
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} cultural sites heritage"
                results = search_tool.search_web(query)
                
                if results:
                    for result in results[:5]:
                        title = result.get("title", "")
                        content = result.get("content", "")
                        
                        if "cultural" in title.lower() or "heritage" in title.lower():
                            significance = content[:200] + "..." if len(content) > 200 else content
                            cultural_sites.append({
                                "name": title[:100] if title else "Cultural Site",
                                "location": location,
                                "significance": significance or "Cultural importance",
                            })
                    
                    if cultural_sites:
                        return json.dumps({
                            "location": location,
                            "cultural_sites": cultural_sites,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for cultural sites: {e}")
    except Exception as e:
        print(f"Cultural sites search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "cultural_sites": [
            {
                "name": "Cultural Site",
                "location": "Along route",
                "significance": "Cultural importance",
            }
        ],
        "source": "placeholder",
    })


@tool
def get_local_history(location: str) -> str:
    """Get local history for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with local history
    """
    try:
        # Use web search via Tavily for local history
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} history historical events"
                results = search_tool.search_web(query)
                
                if results:
                    summary = "Rich local history"
                    key_events = []
                    
                    # Extract historical information
                    for result in results[:3]:
                        content = result.get("content", "")
                        title = result.get("title", "")
                        
                        # Try to extract key events
                        import re
                        # Look for dates and events
                        date_pattern = r"(\d{4})"
                        dates = re.findall(date_pattern, content)
                        
                        # Extract sentences with dates
                        sentences = re.split(r'[.!?]+', content)
                        for sentence in sentences:
                            if any(date in sentence for date in dates[:3]):  # Limit to first 3 dates
                                event = sentence.strip()[:150]  # Limit length
                                if event and len(event) > 20:  # Ensure meaningful content
                                    key_events.append(event)
                                    if len(key_events) >= 5:  # Limit to 5 events
                                        break
                        
                        # Get summary from first result
                        if result == results[0] and content:
                            summary = content[:300] + "..." if len(content) > 300 else content
                    
                    # Ensure we have at least basic information
                    if not key_events:
                        key_events = ["Historical event 1", "Historical event 2"]
                    
                    return json.dumps({
                        "location": location,
                        "history": {
                            "summary": summary,
                            "key_events": key_events[:5],  # Limit to 5 events
                        },
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for local history: {e}")
    except Exception as e:
        print(f"Local history error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "history": {
            "summary": "Rich local history",
            "key_events": ["Historical event 1", "Historical event 2"],
        },
        "source": "placeholder",
    })


@tool
def get_visitation_guidelines(location: str) -> str:
    """Get respectful visitation guidelines for cultural and historical sites.

    Args:
        location: Location name or region

    Returns:
        JSON string with visitation guidelines
    """
    try:
        # Use web search via Tavily for visitation guidelines
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} cultural historical sites visitation guidelines rules"
                results = search_tool.search_web(query)
                
                if results:
                    guidelines = []
                    
                    # Extract guidelines from search results
                    for result in results[:3]:
                        content = result.get("content", "").lower()
                        
                        # Common guideline patterns
                        if "respect" in content and "cultural" in content:
                            guidelines.append("Respect cultural sites")
                        if "artifact" in content and ("remove" in content or "take" in content):
                            guidelines.append("Do not remove artifacts")
                        if "rule" in content or "regulation" in content:
                            guidelines.append("Follow posted rules")
                        if "custom" in content or "tradition" in content:
                            guidelines.append("Be respectful of local customs")
                        if "photography" in content and ("permit" in content or "restrict" in content):
                            guidelines.append("Check photography restrictions")
                        if "sacred" in content:
                            guidelines.append("Respect sacred sites")
                    
                    # Ensure we have at least basic guidelines
                    if not guidelines:
                        guidelines = [
                            "Respect cultural sites",
                            "Do not remove artifacts",
                            "Follow posted rules",
                            "Be respectful of local customs",
                        ]
                    
                    return json.dumps({
                        "location": location,
                        "guidelines": list(set(guidelines))[:10],  # Remove duplicates, limit to 10
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for visitation guidelines: {e}")
    except Exception as e:
        print(f"Visitation guidelines error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "guidelines": [
            "Respect cultural sites",
            "Do not remove artifacts",
            "Follow posted rules",
            "Be respectful of local customs",
        ],
        "source": "placeholder",
    })

