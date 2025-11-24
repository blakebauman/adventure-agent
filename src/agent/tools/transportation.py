"""Transportation and logistics tools."""

from __future__ import annotations

import json

import httpx
from langchain.tools import tool

from agent.config import Config
from agent.tools.geo import get_coordinates, calculate_distance
from agent.tools.web_search import WebSearchTool


@tool
def get_parking_information(location: str, trailhead: str | None = None) -> str:
    """Get parking information for a location or trailhead.

    Args:
        location: Location name or region
        trailhead: Specific trailhead name

    Returns:
        JSON string with parking information
    """
    try:
        # Get coordinates for location
        search_location = trailhead or location
        coord_result = get_coordinates.invoke({"location_name": search_location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        # Use Google Places API to find parking
        if Config.GOOGLE_PLACES_API_KEY:
            try:
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 2000,  # 2km radius
                        "type": "parking",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        places = data.get("results", [])
                        
                        if places:
                            parking_place = places[0]
                            parking_info = {
                                "available": True,
                                "spaces": "Check on arrival",
                                "fee": "Varies",
                                "restrictions": "Check posted signs",
                                "location": parking_place.get("vicinity", location),
                            }
                            
                            return json.dumps({
                                "location": location,
                                "trailhead": trailhead,
                                "parking": parking_info,
                                "source": "google_places",
                            })
            except Exception as e:
                print(f"Google Places API error for parking: {e}")
        
        # Fallback: Use web search via Tavily
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{search_location} parking trailhead"
                results = search_tool.search_web(query)
                
                if results:
                    parking_info = {
                        "available": True,
                        "spaces": "Check on arrival",
                        "fee": "Varies",
                        "restrictions": "Check posted signs",
                    }
                    
                    # Extract parking information from search results
                    for result in results[:2]:
                        content = result.get("content", "").lower()
                        if "parking" in content:
                            if "fee" in content or "$" in content:
                                parking_info["fee"] = "Fee may apply"
                            if "overnight" in content and "no" in content:
                                parking_info["restrictions"] = "No overnight parking"
                            break
                    
                    return json.dumps({
                        "location": location,
                        "trailhead": trailhead,
                        "parking": parking_info,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for parking: {e}")
    except Exception as e:
        print(f"Parking information error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "trailhead": trailhead,
        "parking": {
            "available": True,
            "spaces": 20,
            "fee": "$5 per day",
            "restrictions": "No overnight parking",
        },
        "source": "placeholder",
    })


@tool
def find_shuttle_services(location: str, route_type: str | None = None) -> str:
    """Find shuttle services for a location.

    Args:
        location: Location name or region
        route_type: Type of route (point_to_point, etc.)

    Returns:
        JSON string with shuttle services
    """
    try:
        # Use web search via Tavily for shuttle services
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} shuttle service trailhead"
                results = search_tool.search_web(query)
                
                if results:
                    shuttle_services = []
                    
                    for result in results[:3]:
                        title = result.get("title", "")
                        content = result.get("content", "")
                        url = result.get("url", "")
                        
                        if "shuttle" in title.lower() or "shuttle" in content.lower():
                            shuttle_services.append({
                                "name": title[:50] if title else "Local Shuttle Service",
                                "route": "Trailhead to trailhead",
                                "cost": "Contact for pricing",
                                "contact": "See website for details",
                                "url": url,
                            })
                    
                    if shuttle_services:
                        return json.dumps({
                            "location": location,
                            "shuttle_services": shuttle_services,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for shuttle services: {e}")
    except Exception as e:
        print(f"Shuttle service search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "shuttle_services": [
            {
                "name": "Local Shuttle Service",
                "route": "Trailhead to trailhead",
                "cost": "$25 per person",
                "contact": "Contact local shuttle service",
            }
        ],
        "source": "placeholder",
    })


@tool
def get_public_transportation(location: str, trailhead: str | None = None) -> str:
    """Get public transportation options to a location or trailhead.

    Args:
        location: Location name or region
        trailhead: Specific trailhead name

    Returns:
        JSON string with public transportation options
    """
    try:
        # Get coordinates for location
        search_location = trailhead or location
        coord_result = get_coordinates.invoke({"location_name": search_location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        # Use Google Places API to find transit stations
        if Config.GOOGLE_PLACES_API_KEY:
            try:
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 10000,  # 10km radius
                        "type": "transit_station",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        places = data.get("results", [])
                        
                        if places:
                            transit_station = places[0]
                            return json.dumps({
                                "location": location,
                                "trailhead": trailhead,
                                "public_transit": {
                                    "available": True,
                                    "options": [
                                        {
                                            "type": "Transit Station",
                                            "name": transit_station.get("name", "Transit Station"),
                                            "location": transit_station.get("vicinity", location),
                                            "distance": "Check route planner",
                                        }
                                    ],
                                    "notes": "Limited public transportation to trailheads - check local transit authority",
                                },
                                "source": "google_places",
                            })
            except Exception as e:
                print(f"Google Places API error for public transit: {e}")
        
        # Fallback: Use web search via Tavily
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{search_location} public transportation bus"
                results = search_tool.search_web(query)
                
                if results:
                    options = []
                    for result in results[:2]:
                        title = result.get("title", "")
                        if "bus" in title.lower() or "transit" in title.lower():
                            options.append({
                                "type": "Bus/Transit",
                                "name": title[:50],
                                "location": location,
                            })
                    
                    return json.dumps({
                        "location": location,
                        "trailhead": trailhead,
                        "public_transit": {
                            "available": len(options) > 0,
                            "options": options,
                            "notes": "Limited public transportation to trailheads",
                        },
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for public transit: {e}")
    except Exception as e:
        print(f"Public transportation error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "public_transit": {
            "available": False,
            "options": [],
            "notes": "Limited public transportation to trailheads",
        },
        "source": "placeholder",
    })


@tool
def find_bike_transport_options(location: str) -> str:
    """Find bike transport options for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with bike transport options
    """
    try:
        # Use web search via Tavily for bike transport
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} bike transport bike rack bus"
                results = search_tool.search_web(query)
                
                if results:
                    options = []
                    restrictions = "Check with service provider"
                    
                    for result in results[:3]:
                        content = result.get("content", "").lower()
                        if "bike rack" in content or "bike friendly" in content:
                            options.append("Bike racks on buses")
                        if "shuttle" in content and "bike" in content:
                            options.append("Bike-friendly shuttles")
                        if "restriction" in content:
                            restrictions = "Check with service provider for specific restrictions"
                    
                    if not options:
                        options = ["Bike racks on buses", "Bike-friendly shuttles"]
                    
                    return json.dumps({
                        "location": location,
                        "bike_transport": {
                            "options": options,
                            "restrictions": restrictions,
                        },
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for bike transport: {e}")
    except Exception as e:
        print(f"Bike transport search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "bike_transport": {
            "options": ["Bike racks on buses", "Bike-friendly shuttles"],
            "restrictions": "Check with service provider",
        },
        "source": "placeholder",
    })


@tool
def get_car_rental_recommendations(location: str) -> str:
    """Get car rental recommendations for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with car rental recommendations
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        # Use Google Places API to find car rental companies
        if Config.GOOGLE_PLACES_API_KEY:
            try:
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 20000,  # 20km radius
                        "type": "car_rental",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        places = data.get("results", [])
                        
                        car_rentals = []
                        for place in places[:5]:  # Limit to 5 results
                            name = place.get("name", "Car Rental")
                            vicinity = place.get("vicinity", location)
                            rating = place.get("rating")
                            
                            car_rentals.append({
                                "company": name,
                                "location": vicinity,
                                "recommended": rating and rating >= 4.0 if rating else False,
                                "rating": rating,
                            })
                        
                        if car_rentals:
                            return json.dumps({
                                "location": location,
                                "car_rentals": car_rentals,
                                "source": "google_places",
                            })
            except Exception as e:
                print(f"Google Places API error for car rentals: {e}")
    except Exception as e:
        print(f"Car rental search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "car_rentals": [
            {
                "company": "Local rental company",
                "location": "Near airport",
                "recommended": True,
            }
        ],
        "source": "placeholder",
    })

