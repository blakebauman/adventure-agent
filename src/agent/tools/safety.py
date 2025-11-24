"""Safety and emergency tools."""

from __future__ import annotations

import json
from typing import Any, Dict

import httpx
from langchain.tools import tool

from agent.config import Config
from agent.tools.geo import get_coordinates
from agent.tools.web_search import WebSearchTool


@tool
def get_emergency_contacts(location: str) -> str:
    """Get emergency contact information for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with emergency contacts
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        emergency_contacts = {
            "emergency_911": "911",
            "location": location,
        }
        
        # Use Google Places API to find hospitals if available
        if Config.GOOGLE_PLACES_API_KEY:
            try:
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 50000,  # 50km radius
                        "type": "hospital",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        places = data.get("results", [])
                        
                        if places:
                            nearest_hospital = places[0]
                            hospital_name = nearest_hospital.get("name", "Nearest Hospital")
                            hospital_address = nearest_hospital.get("vicinity", location)
                            
                            # Get phone number if available
                            place_id = nearest_hospital.get("place_id")
                            if place_id:
                                details_url = "https://maps.googleapis.com/maps/api/place/details/json"
                                details_params = {
                                    "place_id": place_id,
                                    "fields": "formatted_phone_number",
                                    "key": Config.GOOGLE_PLACES_API_KEY,
                                }
                                
                                try:
                                    details_response = client.get(details_url, params=details_params, timeout=10.0)
                                    if details_response.status_code == 200:
                                        details_data = details_response.json().get("result", {})
                                        phone = details_data.get("formatted_phone_number")
                                        if phone:
                                            emergency_contacts["medical_services"] = {
                                                "name": hospital_name,
                                                "address": hospital_address,
                                                "phone": phone,
                                            }
                                except Exception:
                                    pass
                            
                            if "medical_services" not in emergency_contacts:
                                emergency_contacts["medical_services"] = {
                                    "name": hospital_name,
                                    "address": hospital_address,
                                }
            except Exception as e:
                print(f"Google Places API error for hospitals: {e}")
        
        # Use web search via Tavily for additional emergency contacts
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} emergency contacts sheriff search and rescue"
                results = search_tool.search_web(query)
                
                if results:
                    for result in results[:2]:
                        content = result.get("content", "").lower()
                        if "sheriff" in content and "phone" in content:
                            # Try to extract phone number
                            import re
                            phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", result.get("content", ""))
                            if phone_match:
                                emergency_contacts["local_sheriff"] = phone_match.group(0)
                                break
                    
                    # Check for search and rescue
                    for result in results[:2]:
                        content = result.get("content", "").lower()
                        if "search and rescue" in content or "sar" in content:
                            emergency_contacts["search_rescue"] = "Local search and rescue - contact sheriff's office"
                            break
                    
                    # Check for ranger station
                    for result in results[:2]:
                        content = result.get("content", "").lower()
                        if "ranger station" in content:
                            emergency_contacts["ranger_station"] = "Contact local ranger station"
                            break
            except Exception as e:
                print(f"Web search error for emergency contacts: {e}")
        
        # Set defaults if not found
        if "local_sheriff" not in emergency_contacts:
            emergency_contacts["local_sheriff"] = "Contact local sheriff's office"
        if "search_rescue" not in emergency_contacts:
            emergency_contacts["search_rescue"] = "Local search and rescue"
        if "ranger_station" not in emergency_contacts:
            emergency_contacts["ranger_station"] = "Contact local ranger station"
        if "medical_services" not in emergency_contacts:
            emergency_contacts["medical_services"] = "Nearest hospital information"
        
        return json.dumps({
            **emergency_contacts,
            "source": "api" if Config.GOOGLE_PLACES_API_KEY or Config.TAVILY_API_KEY else "placeholder",
        })
    except Exception as e:
        print(f"Emergency contacts error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "emergency_911": "911",
        "local_sheriff": "Contact local sheriff's office",
        "search_rescue": "Local search and rescue",
        "ranger_station": "Contact local ranger station",
        "medical_services": "Nearest hospital information",
        "source": "placeholder",
    })


@tool
def get_safety_information(location: str, activity_type: str = "mountain_biking") -> str:
    """Get safety information for a location and activity.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with safety information
    """
    try:
        # Use web search via Tavily for safety information
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} {activity_type} safety tips hazards"
                results = search_tool.search_web(query)
                
                if results:
                    safety_tips = []
                    common_hazards = []
                    
                    # Extract safety information from search results
                    for result in results[:3]:
                        content = result.get("content", "").lower()
                        title = result.get("title", "").lower()
                        
                        # Common safety tips
                        if "water" in content and ("carry" in content or "bring" in content):
                            safety_tips.append("Carry plenty of water")
                        if "tell someone" in content or "share plans" in content:
                            safety_tips.append("Tell someone your plans")
                        if "first aid" in content:
                            safety_tips.append("Bring first aid kit")
                        if "weather" in content:
                            safety_tips.append("Check weather before going")
                        if "sun protection" in content or "sunscreen" in content:
                            safety_tips.append("Use sun protection")
                        if "cell phone" in content or "communication" in content:
                            safety_tips.append("Bring communication device")
                        
                        # Common hazards
                        if "dehydration" in content:
                            common_hazards.append("Dehydration")
                        if "heat" in content and ("exhaustion" in content or "stroke" in content):
                            common_hazards.append("Heat exhaustion")
                        if "wildlife" in content:
                            common_hazards.append("Wildlife encounters")
                        if "snake" in content:
                            common_hazards.append("Snake encounters")
                        if "flash flood" in content:
                            common_hazards.append("Flash floods")
                    
                    # Ensure we have at least basic safety tips
                    if not safety_tips:
                        safety_tips = [
                            "Carry plenty of water",
                            "Tell someone your plans",
                            "Bring first aid kit",
                            "Check weather before going",
                        ]
                    
                    if not common_hazards:
                        common_hazards = ["Dehydration", "Heat exhaustion", "Wildlife encounters"]
                    
                    return json.dumps({
                        "location": location,
                        "activity_type": activity_type,
                        "safety_tips": list(set(safety_tips))[:10],  # Remove duplicates, limit to 10
                        "common_hazards": list(set(common_hazards))[:10],
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for safety information: {e}")
    except Exception as e:
        print(f"Safety information error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "safety_tips": [
            "Carry plenty of water",
            "Tell someone your plans",
            "Bring first aid kit",
            "Check weather before going",
        ],
        "common_hazards": ["Dehydration", "Heat exhaustion", "Wildlife encounters"],
        "source": "placeholder",
    })


@tool
def check_wildlife_alerts(location: str) -> str:
    """Check for wildlife alerts (bears, mountain lions, etc.).

    Args:
        location: Location name or region

    Returns:
        JSON string with wildlife alerts
    """
    try:
        # Use web search via Tavily for wildlife alerts
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} wildlife alerts bears mountain lions"
                results = search_tool.search_web(query)
                
                if results:
                    alerts = []
                    wildlife_present = []
                    safety_protocols = {
                        "bears": "Store food properly, make noise",
                        "mountain_lions": "Travel in groups, avoid dawn/dusk",
                    }
                    
                    # Extract wildlife information
                    for result in results[:3]:
                        content = result.get("content", "").lower()
                        title = result.get("title", "").lower()
                        
                        # Check for alerts
                        if "alert" in content or "warning" in content:
                            if "bear" in content:
                                alerts.append("Bear activity reported")
                                safety_protocols["bears"] = "Store food properly, make noise, carry bear spray"
                            if "mountain lion" in content or "cougar" in content:
                                alerts.append("Mountain lion activity reported")
                                safety_protocols["mountain_lions"] = "Travel in groups, avoid dawn/dusk, do not run"
                        
                        # Check for wildlife presence
                        if "bear" in content and "present" in content:
                            wildlife_present.append("Bears")
                        if "mountain lion" in content or "cougar" in content:
                            wildlife_present.append("Mountain Lions")
                        if "deer" in content:
                            wildlife_present.append("Deer")
                        if "bird" in content:
                            wildlife_present.append("Birds")
                        if "snake" in content:
                            wildlife_present.append("Snakes")
                    
                    if not wildlife_present:
                        wildlife_present = ["Deer", "Birds"]
                    
                    return json.dumps({
                        "location": location,
                        "alerts": alerts,
                        "wildlife_present": list(set(wildlife_present)),
                        "safety_protocols": safety_protocols,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for wildlife alerts: {e}")
    except Exception as e:
        print(f"Wildlife alerts error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "alerts": [],
        "wildlife_present": ["Deer", "Birds"],
        "safety_protocols": {
            "bears": "Store food properly, make noise",
            "mountain_lions": "Travel in groups, avoid dawn/dusk",
        },
        "source": "placeholder",
    })


@tool
def get_avalanche_forecast(location: str) -> str:
    """Get avalanche forecast for a location (winter activities).

    Args:
        location: Location name or region

    Returns:
        JSON string with avalanche forecast
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        # Use National Weather Service API for avalanche forecast
        # NWS doesn't have a direct avalanche API, but we can check for winter weather alerts
        try:
            with httpx.Client() as client:
                # Get forecast zone (simplified - NWS uses zones, not direct lat/lon)
                # For Arizona, avalanche risk is generally low, but we'll check for winter weather
                url = f"https://api.weather.gov/alerts/active"
                headers = {"User-Agent": "AdventureAgent/1.0"}
                params = {
                    "point": f"{lat},{lon}",
                }
                
                response = client.get(url, headers=headers, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    features = data.get("features", [])
                    
                    # Check for winter weather alerts
                    winter_alerts = []
                    for feature in features:
                        properties = feature.get("properties", {})
                        event = properties.get("event", "").lower()
                        if "winter" in event or "snow" in event or "avalanche" in event:
                            winter_alerts.append({
                                "event": properties.get("event", ""),
                                "headline": properties.get("headline", ""),
                                "description": properties.get("description", "")[:200],
                            })
                    
                    if winter_alerts:
                        return json.dumps({
                            "location": location,
                            "avalanche_danger": "Check current conditions",
                            "forecast": "Winter weather alerts active - check avalanche conditions",
                            "alerts": winter_alerts,
                            "source": "nws",
                        })
        except Exception as e:
            print(f"NWS API error for avalanche forecast: {e}")
        
        # Fallback: Use web search via Tavily
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} avalanche forecast danger"
                results = search_tool.search_web(query)
                
                if results:
                    avalanche_danger = "Low"
                    forecast = "Stable conditions"
                    
                    for result in results[:2]:
                        content = result.get("content", "").lower()
                        if "avalanche" in content:
                            if "high" in content or "extreme" in content:
                                avalanche_danger = "High"
                                forecast = "Dangerous conditions - avoid avalanche terrain"
                            elif "moderate" in content:
                                avalanche_danger = "Moderate"
                                forecast = "Use caution in avalanche terrain"
                    
                    return json.dumps({
                        "location": location,
                        "avalanche_danger": avalanche_danger,
                        "forecast": forecast,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for avalanche forecast: {e}")
    except Exception as e:
        print(f"Avalanche forecast error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "avalanche_danger": "Low",
        "forecast": "Stable conditions",
        "source": "placeholder",
    })


@tool
def get_river_conditions(location: str) -> str:
    """Get river crossing conditions for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with river conditions
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        # Use USGS Water Services API for river conditions
        try:
            with httpx.Client() as client:
                # Find nearby stream gauges
                url = "https://waterservices.usgs.gov/nwis/iv/"
                params = {
                    "format": "json",
                    "bBox": f"{lon-0.5},{lat-0.5},{lon+0.5},{lat+0.5}",  # 1 degree box
                    "parameterCd": "00060",  # Streamflow
                    "siteType": "ST",  # Stream
                }
                
                response = client.get(url, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    time_series = data.get("value", {}).get("timeSeries", [])
                    
                    if time_series:
                        # Get the first stream gauge data
                        series = time_series[0]
                        values = series.get("values", [{}])[0].get("value", [])
                        if values:
                            flow_value = float(values[0].get("value", 0))
                            unit = series.get("variable", {}).get("unit", {}).get("unitCode", "")
                            
                            # Determine conditions based on flow
                            if flow_value < 100:
                                river_conditions = "Safe for crossing"
                                water_level = "Low"
                                flow_rate = "Low"
                            elif flow_value < 500:
                                river_conditions = "Moderate - use caution"
                                water_level = "Normal"
                                flow_rate = "Moderate"
                            else:
                                river_conditions = "Dangerous - do not cross"
                                water_level = "High"
                                flow_rate = "High"
                            
                            return json.dumps({
                                "location": location,
                                "river_conditions": river_conditions,
                                "water_level": water_level,
                                "flow_rate": flow_rate,
                                "flow_value": flow_value,
                                "unit": unit,
                                "source": "usgs",
                            })
        except Exception as e:
            print(f"USGS API error for river conditions: {e}")
        
        # Fallback: Use web search via Tavily
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} river conditions water level"
                results = search_tool.search_web(query)
                
                if results:
                    river_conditions = "Safe for crossing"
                    water_level = "Normal"
                    flow_rate = "Moderate"
                    
                    for result in results[:2]:
                        content = result.get("content", "").lower()
                        if "high water" in content or "flood" in content:
                            river_conditions = "Dangerous - do not cross"
                            water_level = "High"
                            flow_rate = "High"
                        elif "low water" in content:
                            water_level = "Low"
                            flow_rate = "Low"
                    
                    return json.dumps({
                        "location": location,
                        "river_conditions": river_conditions,
                        "water_level": water_level,
                        "flow_rate": flow_rate,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for river conditions: {e}")
    except Exception as e:
        print(f"River conditions error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "river_conditions": "Safe for crossing",
        "water_level": "Normal",
        "flow_rate": "Moderate",
        "source": "placeholder",
    })


@tool
def assess_route_safety(
    location: str, activity_type: str = "mountain_biking", route_info: Dict[str, Any] | None = None
) -> str:
    """Assess safety of a route.

    Args:
        location: Location name or region
        activity_type: Type of activity
        route_info: Information about the route

    Returns:
        JSON string with safety assessment
    """
    try:
        # Use web search via Tavily for route safety assessment
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                route_name = route_info.get("name", "") if route_info else ""
                query = f"{location} {route_name} {activity_type} safety conditions"
                results = search_tool.search_web(query)
                
                if results:
                    risk_level = "Moderate"
                    safety_considerations = []
                    recommendations = []
                    
                    # Extract safety information
                    for result in results[:3]:
                        content = result.get("content", "").lower()
                        
                        # Check for risk level indicators
                        if "dangerous" in content or "hazardous" in content:
                            risk_level = "High"
                        elif "safe" in content and "well-maintained" in content:
                            risk_level = "Low"
                        
                        # Safety considerations
                        if "well-maintained" in content:
                            safety_considerations.append("Well-maintained trail")
                        if "cell coverage" in content or "cell service" in content:
                            safety_considerations.append("Good cell coverage")
                        if "difficulty" in content:
                            safety_considerations.append("Moderate difficulty")
                        if "remote" in content:
                            safety_considerations.append("Remote area - plan accordingly")
                        
                        # Recommendations
                        if "partner" in content or "group" in content:
                            recommendations.append("Travel with a partner")
                        if "emergency" in content or "supplies" in content:
                            recommendations.append("Bring emergency supplies")
                        if "water" in content:
                            recommendations.append("Carry plenty of water")
                    
                    # Ensure we have at least basic considerations
                    if not safety_considerations:
                        safety_considerations = [
                            "Well-maintained trail",
                            "Moderate difficulty",
                            "Good cell coverage",
                        ]
                    
                    if not recommendations:
                        recommendations = ["Travel with a partner", "Bring emergency supplies"]
                    
                    return json.dumps({
                        "location": location,
                        "activity_type": activity_type,
                        "risk_level": risk_level,
                        "safety_considerations": list(set(safety_considerations))[:10],
                        "recommendations": list(set(recommendations))[:10],
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for route safety: {e}")
    except Exception as e:
        print(f"Route safety assessment error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "risk_level": "Moderate",
        "safety_considerations": [
            "Well-maintained trail",
            "Moderate difficulty",
            "Good cell coverage",
        ],
        "recommendations": ["Travel with a partner", "Bring emergency supplies"],
        "source": "placeholder",
    })

