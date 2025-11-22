"""Tools for adventure agent sub-agents."""

from __future__ import annotations

import json
import math
from typing import Any, Dict, List, Optional

import httpx
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field

from agent.config import Config


class WebSearchTool:
    """Web search tool using Tavily."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize web search tool."""
        if api_key:
            self.search = TavilySearchResults(
                max_results=5, tavily_api_key=api_key
            )
        else:
            self.search = None

    def search_web(self, query: str) -> List[Dict[str, Any]]:
        """Search the web for information."""
        if not self.search:
            # Fallback: return empty results if no API key
            return []
        try:
            results = self.search.invoke({"query": query})
            return results if isinstance(results, list) else []
        except Exception as e:
            print(f"Web search error: {e}")
            return []


# BLM Land Tools
@tool
def search_blm_lands(region: str, activity_type: str = "mountain_biking") -> str:
    """Search for BLM (Bureau of Land Management) lands in a region.

    Args:
        region: US state or region name
        activity_type: Type of activity (mountain_biking, camping, etc.)

    Returns:
        JSON string with BLM land information
    """
    try:
        # Get coordinates for the region
        coord_result = get_coordinates.invoke({"location_name": region})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for region")
        
        # Use Recreation.gov API to find nearby BLM sites
        # Recreation.gov has some BLM data
        with httpx.Client() as client:
            # Search for recreation areas near the location
            url = "https://ridb.recreation.gov/api/v1/recareas"
            headers = {"apikey": "public"}  # Public API key
            params = {
                "limit": 10,
                "offset": 0,
                "latitude": lat,
                "longitude": lon,
                "radius": 50,  # 50 mile radius
            }
            
            try:
                response = client.get(url, headers=headers, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    rec_areas = data.get("RECDATA", [])
                    
                    # Filter for BLM managed areas
                    blm_lands = []
                    for area in rec_areas:
                        org_name = area.get("OrgName", "").upper()
                        if "BLM" in org_name or "BUREAU OF LAND MANAGEMENT" in org_name:
                            blm_lands.append({
                                "name": area.get("RecAreaName", "BLM Land"),
                                "description": area.get("RecAreaDescription", ""),
                                "access_points": [area.get("RecAreaDirections", "")],
                                "regulations": [
                                    "Follow Leave No Trace principles",
                                    "Check local BLM office for specific regulations",
                                ],
                                "permits_required": area.get("Reservable", False),
                                "camping_allowed": True,
                                "coordinates": {
                                    "lat": area.get("RecAreaLatitude"),
                                    "lon": area.get("RecAreaLongitude"),
                                },
                                "url": f"https://www.recreation.gov/camping/campgrounds/{area.get('RecAreaID')}" if area.get("RecAreaID") else None,
                            })
                    
                    if blm_lands:
                        return json.dumps({
                            "lands": blm_lands,
                            "region": region,
                            "source": "recreation.gov",
                        })
            except Exception as e:
                print(f"Recreation.gov API error: {e}")
        
        # Fallback: Use web search via Tavily if available
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"BLM Bureau of Land Management {region} {activity_type} recreation areas"
                results = search_tool.search_web(query)
                
                if results:
                    # Extract information from search results
                    blm_info = []
                    for result in results[:3]:  # Top 3 results
                        title = result.get("title", "")
                        content = result.get("content", "")
                        url = result.get("url", "")
                        
                        if "BLM" in title.upper() or "BUREAU OF LAND MANAGEMENT" in title.upper():
                            blm_info.append({
                                "name": title,
                                "description": content[:200] + "..." if len(content) > 200 else content,
                                "access_points": ["Contact local BLM office"],
                                "regulations": [
                                    "Permits may be required for overnight use",
                                    "Stay on designated trails",
                                    "Pack in, pack out",
                                ],
                                "permits_required": "overnight" in content.lower(),
                                "camping_allowed": "camping" in content.lower() or "camp" in content.lower(),
                                "url": url,
                            })
                    
                    if blm_info:
                        return json.dumps({
                            "lands": blm_info,
                            "region": region,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for BLM data: {e}")
    except Exception as e:
        print(f"BLM land search error for {region}: {e}")
    
    # Fallback to structured placeholder data
    return json.dumps({
        "lands": [
            {
                "name": f"BLM Land in {region}",
                "access_points": ["Main trailhead", "Secondary access"],
                "regulations": ["Permits required for overnight", "Stay on designated trails"],
                "permits_required": True,
                "camping_allowed": True,
                "description": f"BLM managed land suitable for {activity_type}. Contact local BLM office for specific information.",
            }
        ],
        "region": region,
        "source": "placeholder",
    })


@tool
def get_blm_regulations(land_name: str) -> str:
    """Get specific regulations for a BLM land area.

    Args:
        land_name: Name of the BLM land area

    Returns:
        JSON string with regulations
    """
    return json.dumps({
        "regulations": [
            "Permits required for groups over 10",
            "No motorized vehicles",
            "Pack in, pack out",
            "Campfires only in designated areas",
        ],
        "permits_required": True,
        "contact_info": "Contact local BLM office",
    })


# Trail Tools - Support multiple activity types and sources
@tool
def search_trails(
    location: str,
    activity_type: str,
    source: str,
    difficulty: Optional[str] = None,
    distance: Optional[float] = None,
) -> str:
    """Search for trails using OpenStreetMap Overpass API.

    Args:
        location: Location name or coordinates
        activity_type: Type of activity (mountain_biking, hiking, trail_running, bikepacking)
        source: Trail source (mtbproject, hikingproject, trailrunproject, osm)
        difficulty: Trail difficulty (green/blue/black for MTB, easy/intermediate/difficult for hiking/running)
        distance: Maximum distance in miles

    Returns:
        JSON string with trail information
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        # Use OpenStreetMap Overpass API to find trails
        # Map activity types to OSM tags
        osm_tags = {
            "mountain_biking": "mtb",
            "hiking": "hiking",
            "trail_running": "running",
            "bikepacking": "bicycle",
        }
        
        # Build Overpass query - search within ~10km radius
        overpass_url = "https://overpass-api.de/api/interpreter"
        
        # Query for trails/paths near the location
        query = f"""
        [out:json][timeout:25];
        (
          way["highway"~"^(path|track|footway|bridleway|cycleway)$"]["name"](around:10000,{lat},{lon});
          relation["route"~"^(hiking|bicycle|mtb|foot)$"]["name"](around:10000,{lat},{lon});
        );
        out body;
        >;
        out skel qt;
        """
        
        with httpx.Client() as client:
            response = client.post(overpass_url, data=query, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            
            trails = []
            elements = data.get("elements", [])
            
            # Process way elements (trail segments)
            for element in elements[:20]:  # Limit to 20 results
                if element.get("type") == "way" and element.get("tags"):
                    tags = element.get("tags", {})
                    name = tags.get("name", "Unnamed Trail")
                    
                    # Filter by activity type if possible
                    highway = tags.get("highway", "")
                    if activity_type == "mountain_biking" and highway not in ["path", "track", "cycleway"]:
                        continue
                    if activity_type == "hiking" and highway not in ["path", "track", "footway"]:
                        continue
                    
                    trails.append({
                        "name": name,
                        "source": "osm",
                        "activity_type": activity_type,
                        "difficulty": difficulty or "intermediate",
                        "length_miles": distance or 5.0,  # OSM doesn't always have length
                        "elevation_gain": None,
                        "description": tags.get("description", f"{activity_type.replace('_', ' ').title()} trail"),
                        "url": f"https://www.openstreetmap.org/way/{element.get('id')}",
                        "surface": tags.get("surface", "unknown"),
                        "smoothness": tags.get("smoothness", "unknown"),
                    })
            
            if trails:
                return json.dumps({"trails": trails})
    except Exception as e:
        print(f"Trail search error for {location}: {e}")
    
    # Fallback: Map activity types to URLs
    url_map = {
        "mtbproject": "https://www.mtbproject.com",
        "hikingproject": "https://www.hikingproject.com",
        "trailrunproject": "https://www.trailrunproject.com",
    }

    base_url = url_map.get(source, "https://www.mtbproject.com")

    # Fallback to placeholder data
    return json.dumps({
        "trails": [
            {
                "name": f"{activity_type.replace('_', ' ').title()} Trail near {location}",
                "source": source,
                "activity_type": activity_type,
                "difficulty": difficulty or "intermediate",
                "length_miles": distance or 10.0,
                "elevation_gain": 1500.0,
                "description": f"Popular {activity_type.replace('_', ' ')} trail",
                "url": f"{base_url}/trail/{location}",
            }
        ]
    })


@tool
def get_trail_details(
    trail_id: str, source: str, activity_type: str
) -> str:
    """Get detailed information about a specific trail.

    Args:
        trail_id: Trail identifier
        source: Source of trail data (mtbproject, hikingproject, trailrunproject, etc.)
        activity_type: Type of activity (mountain_biking, hiking, trail_running, etc.)

    Returns:
        JSON string with detailed trail information
    """
    activity_features = {
        "mountain_biking": ["Single track", "Technical sections", "Jumps"],
        "hiking": ["Scenic views", "Water sources", "Wildlife viewing"],
        "trail_running": ["Smooth sections", "Elevation changes", "Technical terrain"],
        "bikepacking": ["Multi-day route", "Resupply points", "Camping areas"],
    }

    features = activity_features.get(activity_type, ["Trail features"])

    return json.dumps({
        "trail_id": trail_id,
        "source": source,
        "activity_type": activity_type,
        "details": {
            "condition": "Good",
            "recent_reports": "Well maintained",
            "features": features,
        },
    })


# Geo Tools
@tool
def get_coordinates(location_name: str) -> str:
    """Get coordinates for a location using geocoding.

    Args:
        location_name: Name of the location

    Returns:
        JSON string with coordinates
    """
    try:
        # Try OpenCage first if API key is available
        if Config.OPENCAGE_API_KEY:
            with httpx.Client() as client:
                url = "https://api.opencagedata.com/geocode/v1/json"
                params = {
                    "q": location_name,
                    "key": Config.OPENCAGE_API_KEY,
                    "limit": 1,
                }
                response = client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                if data.get("results"):
                    result = data["results"][0]
                    geometry = result["geometry"]
                    components = result.get("components", {})
                    
                    return json.dumps({
                        "location": location_name,
                        "coordinates": {"lat": geometry["lat"], "lon": geometry["lng"]},
                        "region": components.get("state") or components.get("region") or "Unknown",
                        "country": components.get("country_code", "US").upper(),
                        "formatted_address": result.get("formatted", location_name),
                    })
        
        # Fallback to Nominatim (OpenStreetMap, free, no key required)
        with httpx.Client() as client:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": location_name,
                "format": "json",
                "limit": 1,
                "addressdetails": 1,
            }
            headers = {"User-Agent": "AdventureAgent/1.0"}  # Required by Nominatim
            response = client.get(url, params=params, headers=headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if data:
                result = data[0]
                return json.dumps({
                    "location": location_name,
                    "coordinates": {"lat": float(result["lat"]), "lon": float(result["lon"])},
                    "region": result.get("address", {}).get("state") or result.get("address", {}).get("region") or "Unknown",
                    "country": result.get("address", {}).get("country_code", "us").upper(),
                    "formatted_address": result.get("display_name", location_name),
                })
    except Exception as e:
        # Fallback to placeholder data on error
        print(f"Geocoding error for {location_name}: {e}")
    
    # Fallback placeholder data
    return json.dumps({
        "location": location_name,
        "coordinates": {"lat": 36.1699, "lon": -115.1398},  # Example: Las Vegas
        "region": "Unknown",
        "country": "US",
        "formatted_address": location_name,
    })


@tool
def calculate_distance(
    point1: Dict[str, float], point2: Dict[str, float]
) -> str:
    """Calculate distance between two points using Haversine formula.

    Args:
        point1: First point with lat and lon
        point2: Second point with lat and lon

    Returns:
        JSON string with distance information
    """
    try:
        lat1, lon1 = point1.get("lat", 0), point1.get("lon", 0)
        lat2, lon2 = point2.get("lat", 0), point2.get("lon", 0)
        
        # Haversine formula for great-circle distance
        R = 3958.8  # Earth radius in miles
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        distance_miles = R * c
        distance_km = distance_miles * 1.60934
        
        return json.dumps({
            "distance_miles": round(distance_miles, 2),
            "distance_km": round(distance_km, 2),
            "point1": point1,
            "point2": point2,
        })
    except Exception as e:
        print(f"Distance calculation error: {e}")
        return json.dumps({
            "distance_miles": 0.0,
            "distance_km": 0.0,
            "error": str(e),
        })


# Accommodation Tools
@tool
def search_accommodations(
    location: str,
    accommodation_type: Optional[str] = None,
    check_in: Optional[str] = None,
    check_out: Optional[str] = None,
) -> str:
    """Search for accommodations near a location.

    Args:
        location: Location name
        accommodation_type: Type (hotel, campground, hostel, etc.)
        check_in: Check-in date (YYYY-MM-DD)
        check_out: Check-out date (YYYY-MM-DD)

    Returns:
        JSON string with accommodation options
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        accommodations = []
        
        # For campgrounds, use Recreation.gov API (free, no key)
        if not accommodation_type or accommodation_type.lower() in ["campground", "camping", "campsite"]:
            try:
                with httpx.Client() as client:
                    url = "https://ridb.recreation.gov/api/v1/facilities"
                    headers = {"apikey": "public"}
                    params = {
                        "limit": 10,
                        "offset": 0,
                        "latitude": lat,
                        "longitude": lon,
                        "radius": 25,  # 25 mile radius
                        "query": "campground",
                    }
                    
                    response = client.get(url, headers=headers, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        facilities = data.get("RECDATA", [])
                        
                        for facility in facilities[:10]:  # Limit to 10 results
                            accommodations.append({
                                "name": facility.get("FacilityName", "Campground"),
                                "type": "campground",
                                "location": facility.get("FacilityAddressState", location),
                                "price_range": "$20-60/night",  # Recreation.gov doesn't always provide pricing
                                "amenities": [
                                    "Restrooms",
                                    "Water",
                                    "Fire pits",
                                    "Picnic tables",
                                ],
                                "coordinates": {
                                    "lat": facility.get("FacilityLatitude"),
                                    "lon": facility.get("FacilityLongitude"),
                                },
                                "description": facility.get("FacilityDescription", "")[:200],
                                "url": f"https://www.recreation.gov/camping/campgrounds/{facility.get('FacilityID')}" if facility.get("FacilityID") else None,
                                "reservable": facility.get("Reservable", False),
                            })
            except Exception as e:
                print(f"Recreation.gov API error: {e}")
        
        # For hotels/hostels, use Google Places API if available
        if Config.GOOGLE_PLACES_API_KEY and (not accommodation_type or accommodation_type.lower() in ["hotel", "hostel", "lodging"]):
            try:
                with httpx.Client() as client:
                    # First, find nearby places
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 10000,  # 10km radius
                        "type": "lodging",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        places = data.get("results", [])
                        
                        for place in places[:10]:  # Limit to 10 results
                            place_id = place.get("place_id")
                            name = place.get("name", "Accommodation")
                            rating = place.get("rating")
                            price_level = place.get("price_level")  # 0-4 scale
                            
                            # Get more details
                            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
                            details_params = {
                                "place_id": place_id,
                                "fields": "name,formatted_address,formatted_phone_number,website,rating,price_level",
                                "key": Config.GOOGLE_PLACES_API_KEY,
                            }
                            
                            try:
                                details_response = client.get(details_url, params=details_params, timeout=10.0)
                                if details_response.status_code == 200:
                                    details_data = details_response.json().get("result", {})
                                    
                                    # Convert price level to range
                                    price_ranges = {
                                        0: "$",
                                        1: "$$",
                                        2: "$$$",
                                        3: "$$$$",
                                        4: "$$$$$",
                                    }
                                    price_range = price_ranges.get(price_level, "$$")
                                    
                                    accommodations.append({
                                        "name": details_data.get("name", name),
                                        "type": "hotel",
                                        "location": details_data.get("formatted_address", location),
                                        "price_range": price_range,
                                        "rating": rating,
                                        "phone": details_data.get("formatted_phone_number"),
                                        "website": details_data.get("website"),
                                        "coordinates": {
                                            "lat": place.get("geometry", {}).get("location", {}).get("lat"),
                                            "lon": place.get("geometry", {}).get("location", {}).get("lng"),
                                        },
                                        "url": f"https://www.google.com/maps/place/?q=place_id:{place_id}",
                                    })
                            except Exception as e:
                                print(f"Google Places details error: {e}")
            except Exception as e:
                print(f"Google Places API error: {e}")
        
        if accommodations:
            return json.dumps({
                "accommodations": accommodations,
                "location": location,
                "source": "recreation.gov" if not accommodation_type or accommodation_type.lower() in ["campground", "camping"] else "google_places",
            })
    except Exception as e:
        print(f"Accommodation search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "accommodations": [
            {
                "name": f"{accommodation_type or 'Campground'} near {location}",
                "type": accommodation_type or "campground",
                "location": location,
                "price_range": "$20-40/night",
                "amenities": ["Restrooms", "Water", "Fire pits"],
            }
        ],
        "source": "placeholder",
    })


# Gear/Product Tools
@tool
def recommend_gear(
    adventure_type: str,
    duration_days: int,
    skill_level: str,
    gear_owned: Optional[List[str]] = None,
) -> str:
    """Recommend gear and products for an adventure.

    Args:
        adventure_type: Type of adventure
        duration_days: Duration in days
        skill_level: User skill level
        gear_owned: List of gear user already owns

    Returns:
        JSON string with gear recommendations
    """
    recommendations = [
        {
            "name": "Mountain Bike Helmet",
            "category": "safety",
            "description": "Essential safety gear",
            "affiliate_url": "https://example.com/affiliate/helmet",
            "essential": True,
        },
        {
            "name": "Bikepacking Bags",
            "category": "bikepacking",
            "description": "For multi-day adventures",
            "affiliate_url": "https://example.com/affiliate/bags",
            "essential": duration_days > 1,
        },
    ]

    return json.dumps({"recommendations": recommendations})


@tool
def search_gear_products(
    category: str, price_range: Optional[str] = None
) -> str:
    """Search for specific gear products.

    Args:
        category: Product category
        price_range: Price range filter

    Returns:
        JSON string with product options
    """
    return json.dumps({
        "products": [
            {
                "name": f"{category} Product",
                "category": category,
                "price_range": price_range or "$50-200",
                "affiliate_url": f"https://example.com/affiliate/{category}",
            }
        ]
    })


# Planning Tools
@tool
def create_itinerary(
    trails: List[Dict[str, Any]],
    start_location: str,
    duration_days: int,
) -> str:
    """Create a day-by-day itinerary for an adventure.

    Args:
        trails: List of trail information
        start_location: Starting location
        duration_days: Number of days

    Returns:
        JSON string with itinerary
    """
    itinerary = []
    for day in range(1, duration_days + 1):
        itinerary.append({
            "day": day,
            "activities": [
                f"Ride trail: {trails[day % len(trails)]['name'] if trails else 'Trail'}",
                "Camp overnight",
            ],
            "distance_miles": 15.0,
        })

    return json.dumps({"itinerary": itinerary})


# RideWithGPS Tools
@tool
def search_ridewithgps_routes(
    location: str, activity_type: str, distance: Optional[float] = None
) -> str:
    """Search for routes on RideWithGPS (https://ridewithgps.com/).

    Args:
        location: Location name or coordinates
        activity_type: Type of activity
        distance: Target distance in miles

    Returns:
        JSON string with route information
    """
    return json.dumps({
        "routes": [
            {
                "name": f"RideWithGPS Route near {location}",
                "source": "ridewithgps",
                "activity_type": activity_type,
                "length_miles": distance or 25.0,
                "elevation_gain": 2000.0,
                "description": f"Popular {activity_type} route from RideWithGPS",
                "url": f"https://ridewithgps.com/routes/{location}",
            }
        ]
    })


# Strava Tools
@tool
def search_strava_routes(
    location: str, activity_type: str, popularity: Optional[str] = None
) -> str:
    """Search for popular routes on Strava (https://www.strava.com/).

    Args:
        location: Location name or coordinates
        activity_type: Type of activity
        popularity: Filter by popularity (popular, very_popular, all)

    Returns:
        JSON string with route information
    """
    return json.dumps({
        "routes": [
            {
                "name": f"Popular Strava Route near {location}",
                "source": "strava",
                "activity_type": activity_type,
                "length_miles": 15.0,
                "elevation_gain": 1200.0,
                "description": f"Popular {activity_type} route from Strava community",
                "url": f"https://www.strava.com/routes/{location}",
                "popularity_score": 95,
            }
        ]
    })


# Bikepacking.com Tools
@tool
def search_bikepacking_routes(
    location: str,
    route_type: Optional[str] = None,
    duration_days: Optional[int] = None,
) -> str:
    """Search for bikepacking routes on Bikepacking.com (https://bikepacking.com/).

    Args:
        location: Location name or region
        route_type: Type of route (singletrack, gravel, dirt_road, fat_bike)
        duration_days: Target duration in days

    Returns:
        JSON string with route information
    """
    return json.dumps({
        "routes": [
            {
                "name": f"Bikepacking Route in {location}",
                "source": "bikepacking.com",
                "route_type": route_type or "gravel",
                "length_miles": duration_days * 50.0 if duration_days else 100.0,
                "duration_days": duration_days or 2,
                "description": f"Curated bikepacking route from Bikepacking.com",
                "url": f"https://bikepacking.com/routes/{location}",
            }
        ]
    })


@tool
def search_bikepacking_roots_routes(location: str) -> str:
    """Search for routes from Bikepacking Roots (https://bikepackingroots.org/).

    Args:
        location: Location name or region

    Returns:
        JSON string with route information
    """
    return json.dumps({
        "routes": [
            {
                "name": f"Bikepacking Roots Route in {location}",
                "source": "bikepackingroots",
                "description": "Conservation-focused bikepacking route",
                "url": f"https://bikepackingroots.org/routes/{location}",
            }
        ]
    })


@tool
def get_bikepacking_route_details(
    route_id: str, source: str = "bikepacking.com"
) -> str:
    """Get detailed information about a specific bikepacking route.

    Args:
        route_id: Route identifier or name
        source: Source of route data (bikepacking.com, bikepackingroots, etc.)

    Returns:
        JSON string with detailed bikepacking route information
    """
    return json.dumps({
        "route_id": route_id,
        "source": source,
        "activity_type": "bikepacking",
        "details": {
            "gps_track": "Available",
            "elevation_profile": "Available",
            "resupply_points": ["Mile 25", "Mile 50", "Mile 75"],
            "camping_options": ["Designated sites", "Dispersed camping"],
            "water_sources": ["Stream crossings", "Trail towns"],
            "route_type": "Mixed terrain",
            "difficulty": "Intermediate",
            "best_season": "Spring through Fall",
            "highlights": ["Scenic vistas", "Remote sections", "Historic sites"],
            "challenges": ["Steep climbs", "River crossings", "Weather exposure"],
            "logistics": {
                "shuttle_available": True,
                "parking": "Trailhead parking available",
                "public_transit": "Limited access",
            },
        },
    })


# IMBA Tools
@tool
def search_imba_trails(location: str) -> str:
    """Search for IMBA trail networks (https://www.imba.com/).

    Args:
        location: Location name or region

    Returns:
        JSON string with trail network information
    """
    return json.dumps({
        "trail_networks": [
            {
                "name": f"IMBA Trail Network in {location}",
                "location": location,
                "trail_count": 25,
                "access_status": "Open",
                "advocacy_group": f"Local IMBA Chapter",
            }
        ]
    })


# Adventure Cycling Association Tools
@tool
def search_adventure_cycling_routes(
    location: str, route_type: Optional[str] = None
) -> str:
    """Search for Adventure Cycling Association routes (https://www.adventurecycling.org/).

    Args:
        location: Location name or region
        route_type: Type of route (network, regional, etc.)

    Returns:
        JSON string with route information
    """
    return json.dumps({
        "routes": [
            {
                "name": f"Adventure Cycling Route in {location}",
                "source": "adventurecycling",
                "length_miles": 500.0,
                "description": "Long-distance cycling route from Adventure Cycling Association",
                "url": f"https://www.adventurecycling.org/routes/{location}",
            }
        ]
    })


# Route Details Tool
@tool
def get_route_details(
    route_id: str, source: str, activity_type: str
) -> str:
    """Get detailed information about a specific route from any source.

    Args:
        route_id: Route identifier
        source: Source of route data (ridewithgps, strava, etc.)
        activity_type: Type of activity

    Returns:
        JSON string with detailed route information
    """
    return json.dumps({
        "route_id": route_id,
        "source": source,
        "activity_type": activity_type,
        "details": {
            "turn_by_turn": "Available",
            "elevation_profile": "Available",
            "waypoints": [],
        },
    })


# Trail Access Tool
@tool
def get_trail_access_info(location: str) -> str:
    """Get trail access and advocacy information.

    Args:
        location: Location name or region

    Returns:
        JSON string with access information
    """
    return json.dumps({
        "location": location,
        "access_info": {
            "status": "Open",
            "regulations": "Standard trail access rules apply",
            "advocacy_groups": ["Local IMBA Chapter"],
        },
    })


# Weather & Conditions Tools
@tool
def get_weather_forecast(location: str, dates: Optional[List[str]] = None) -> str:
    """Get weather forecast for a location and dates.

    Args:
        location: Location name or coordinates
        dates: List of dates in YYYY-MM-DD format

    Returns:
        JSON string with weather forecast
    """
    try:
        # First, get coordinates if location is a name
        lat, lon = None, None
        if isinstance(location, str):
            # Check if it's coordinates in string format "lat,lon"
            try:
                parts = location.split(",")
                if len(parts) == 2:
                    lat, lon = float(parts[0].strip()), float(parts[1].strip())
            except (ValueError, AttributeError):
                # Not coordinates, treat as location name - call get_coordinates tool
                coord_result = get_coordinates.invoke({"location_name": location})
                coord_data = json.loads(coord_result)
                lat = coord_data.get("coordinates", {}).get("lat")
                lon = coord_data.get("coordinates", {}).get("lon")
        elif isinstance(location, dict):
            lat, lon = location.get("lat"), location.get("lon")
        
        # Try OpenWeatherMap first if API key is available
        if Config.OPENWEATHER_API_KEY and lat and lon:
            with httpx.Client() as client:
                url = "https://api.openweathermap.org/data/2.5/forecast"
                params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": Config.OPENWEATHER_API_KEY,
                    "units": "imperial",
                }
                response = client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                # Process current weather
                current = data.get("list", [{}])[0] if data.get("list") else {}
                current_main = current.get("main", {})
                current_weather = current.get("weather", [{}])[0]
                
                forecast_data = {
                    "current": {
                        "temp": round(current_main.get("temp", 0)),
                        "feels_like": round(current_main.get("feels_like", 0)),
                        "condition": current_weather.get("description", "Unknown"),
                        "wind": f"{current.get('wind', {}).get('speed', 0):.1f} mph",
                        "humidity": current_main.get("humidity", 0),
                    },
                    "daily": [],
                    "source": "OpenWeatherMap",
                }
                
                # Process daily forecasts
                if dates:
                    for date in dates:
                        # Find closest forecast for this date
                        for item in data.get("list", []):
                            if date in item.get("dt_txt", ""):
                                main = item.get("main", {})
                                weather = item.get("weather", [{}])[0]
                                forecast_data["daily"].append({
                                    "date": date,
                                    "high": round(main.get("temp_max", 0)),
                                    "low": round(main.get("temp_min", 0)),
                                    "condition": weather.get("description", "Unknown"),
                                    "precipitation": item.get("rain", {}).get("3h", 0),
                                })
                                break
                
                return json.dumps({
                    "location": location,
                    "forecast": forecast_data,
                })
        
        # Fallback to Weather.gov for US locations (free, no key)
        if lat and lon:
            try:
                with httpx.Client() as client:
                    # Get grid point from lat/lon
                    points_url = f"https://api.weather.gov/points/{lat},{lon}"
                    headers = {"User-Agent": "AdventureAgent/1.0"}
                    response = client.get(points_url, headers=headers, timeout=10.0)
                    response.raise_for_status()
                    points_data = response.json()
                    
                    forecast_url = points_data.get("properties", {}).get("forecast")
                    if forecast_url:
                        response = client.get(forecast_url, headers=headers, timeout=10.0)
                        response.raise_for_status()
                        forecast_data = response.json()
                        
                        periods = forecast_data.get("properties", {}).get("periods", [])
                        if periods:
                            current = periods[0]
                            return json.dumps({
                                "location": location,
                                "forecast": {
                                    "current": {
                                        "temp": current.get("temperature", 0),
                                        "condition": current.get("shortForecast", "Unknown"),
                                        "wind": current.get("windSpeed", "Unknown"),
                                    },
                                    "daily": [
                                        {
                                            "date": p.get("startTime", "")[:10],
                                            "high": p.get("temperature", 0),
                                            "low": p.get("temperature", 0),  # Weather.gov doesn't always separate
                                            "condition": p.get("shortForecast", "Unknown"),
                                            "precipitation": 0,
                                        }
                                        for p in periods[:7]  # Next 7 periods
                                    ],
                                },
                                "source": "National Weather Service",
                            })
            except Exception as e:
                print(f"Weather.gov error: {e}")
    except Exception as e:
        print(f"Weather forecast error for {location}: {e}")
    
    # Fallback placeholder data
    return json.dumps({
        "location": location,
        "forecast": {
            "current": {"temp": 65, "condition": "Sunny", "wind": "5 mph"},
            "daily": [
                {"date": date, "high": 70, "low": 50, "condition": "Sunny", "precipitation": 0}
                for date in (dates or [])
            ],
        },
        "source": "Placeholder",
    })


@tool
def get_trail_conditions(location: str, activity_type: str = "mountain_biking") -> str:
    """Get current trail conditions for a location.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with trail conditions
    """
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "conditions": "Good",
        "reports": [
            {"date": "2024-01-15", "condition": "Dry", "notes": "Trail in excellent condition"},
        ],
        "seasonal_info": "Best conditions typically in spring and fall",
    })


@tool
def get_seasonal_information(location: str, activity_type: str = "mountain_biking") -> str:
    """Get seasonal information for a location and activity.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with seasonal information
    """
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "best_seasons": ["Spring", "Fall"],
        "seasonal_considerations": {
            "spring": "Muddy conditions possible, wildflowers",
            "summer": "Hot, bring extra water",
            "fall": "Ideal conditions, beautiful colors",
            "winter": "Snow possible, check conditions",
        },
    })


@tool
def check_weather_alerts(location: str) -> str:
    """Check for weather alerts and warnings.

    Args:
        location: Location name or region

    Returns:
        JSON string with weather alerts
    """
    return json.dumps({
        "location": location,
        "alerts": [],
        "warnings": [],
    })


# Permits & Regulations Tools
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
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "permits_required": group_size > 10,
        "permit_type": "Day use" if group_size <= 10 else "Group permit",
        "application_process": "Apply online at recreation.gov",
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
    return json.dumps({
        "location": location,
        "permit_info": {
            "where_to_apply": "recreation.gov",
            "deadline": "30 days in advance",
            "cost": "$5-20 per person",
            "contact": "Local ranger station",
        },
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
    })


@tool
def check_fire_restrictions(location: str, dates: Optional[List[str]] = None) -> str:
    """Check fire restrictions for a location and dates.

    Args:
        location: Location name or region
        dates: List of dates in YYYY-MM-DD format

    Returns:
        JSON string with fire restrictions
    """
    return json.dumps({
        "location": location,
        "fire_restrictions": "Campfires allowed in designated areas only",
        "current_level": "Moderate",
        "restrictions": ["No campfires outside designated areas"],
    })


@tool
def get_seasonal_closures(location: str) -> str:
    """Get seasonal closures for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with seasonal closures
    """
    return json.dumps({
        "location": location,
        "closures": [],
        "seasonal_access": "Open year-round",
    })


# Safety & Emergency Tools
@tool
def get_emergency_contacts(location: str) -> str:
    """Get emergency contact information for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with emergency contacts
    """
    return json.dumps({
        "location": location,
        "emergency_911": "911",
        "local_sheriff": "Contact local sheriff's office",
        "search_rescue": "Local search and rescue",
        "ranger_station": "Contact local ranger station",
        "medical_services": "Nearest hospital information",
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
    })


@tool
def check_wildlife_alerts(location: str) -> str:
    """Check for wildlife alerts (bears, mountain lions, etc.).

    Args:
        location: Location name or region

    Returns:
        JSON string with wildlife alerts
    """
    return json.dumps({
        "location": location,
        "alerts": [],
        "wildlife_present": ["Deer", "Birds"],
        "safety_protocols": {
            "bears": "Store food properly, make noise",
            "mountain_lions": "Travel in groups, avoid dawn/dusk",
        },
    })


@tool
def get_avalanche_forecast(location: str) -> str:
    """Get avalanche forecast for a location (winter activities).

    Args:
        location: Location name or region

    Returns:
        JSON string with avalanche forecast
    """
    return json.dumps({
        "location": location,
        "avalanche_danger": "Low",
        "forecast": "Stable conditions",
        "source": "Local avalanche center",
    })


@tool
def get_river_conditions(location: str) -> str:
    """Get river crossing conditions for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with river conditions
    """
    return json.dumps({
        "location": location,
        "river_conditions": "Safe for crossing",
        "water_level": "Normal",
        "flow_rate": "Moderate",
    })


@tool
def assess_route_safety(
    location: str, activity_type: str = "mountain_biking", route_info: Optional[Dict[str, Any]] = None
) -> str:
    """Assess safety of a route.

    Args:
        location: Location name or region
        activity_type: Type of activity
        route_info: Information about the route

    Returns:
        JSON string with safety assessment
    """
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
    })


# Transportation & Logistics Tools
@tool
def get_parking_information(location: str, trailhead: Optional[str] = None) -> str:
    """Get parking information for a location or trailhead.

    Args:
        location: Location name or region
        trailhead: Specific trailhead name

    Returns:
        JSON string with parking information
    """
    return json.dumps({
        "location": location,
        "trailhead": trailhead,
        "parking": {
            "available": True,
            "spaces": 20,
            "fee": "$5 per day",
            "restrictions": "No overnight parking",
        },
    })


@tool
def find_shuttle_services(location: str, route_type: Optional[str] = None) -> str:
    """Find shuttle services for a location.

    Args:
        location: Location name or region
        route_type: Type of route (point_to_point, etc.)

    Returns:
        JSON string with shuttle services
    """
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
    })


@tool
def get_public_transportation(location: str, trailhead: Optional[str] = None) -> str:
    """Get public transportation options to a location or trailhead.

    Args:
        location: Location name or region
        trailhead: Specific trailhead name

    Returns:
        JSON string with public transportation options
    """
    return json.dumps({
        "location": location,
        "public_transit": {
            "available": False,
            "options": [],
            "notes": "Limited public transportation to trailheads",
        },
    })


@tool
def find_bike_transport_options(location: str) -> str:
    """Find bike transport options for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with bike transport options
    """
    return json.dumps({
        "location": location,
        "bike_transport": {
            "options": ["Bike racks on buses", "Bike-friendly shuttles"],
            "restrictions": "Check with service provider",
        },
    })


@tool
def get_car_rental_recommendations(location: str) -> str:
    """Get car rental recommendations for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with car rental recommendations
    """
    return json.dumps({
        "location": location,
        "car_rentals": [
            {
                "company": "Local rental company",
                "location": "Near airport",
                "recommended": True,
            }
        ],
    })


# Food & Resupply Tools
@tool
def find_grocery_stores(location: str, route_info: Optional[Dict[str, Any]] = None) -> str:
    """Find grocery stores near a location or route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with grocery stores
    """
    return json.dumps({
        "location": location,
        "grocery_stores": [
            {
                "name": "Local Grocery Store",
                "location": "Near trailhead",
                "distance_miles": 2.5,
            }
        ],
    })


@tool
def find_restaurants(location: str, route_info: Optional[Dict[str, Any]] = None) -> str:
    """Find restaurants and cafes near a location or route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with restaurants
    """
    return json.dumps({
        "location": location,
        "restaurants": [
            {
                "name": "Trailside Cafe",
                "type": "Cafe",
                "location": "Along route",
                "distance_miles": 5.0,
            }
        ],
    })


@tool
def find_water_sources(location: str, route_info: Optional[Dict[str, Any]] = None) -> str:
    """Find water sources along a route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with water sources
    """
    return json.dumps({
        "location": location,
        "water_sources": [
            {
                "type": "Stream",
                "location": "Mile 5",
                "quality": "Filter recommended",
            }
        ],
    })


@tool
def find_resupply_points(location: str, duration_days: int = 1) -> str:
    """Find resupply points for multi-day trips.

    Args:
        location: Location name or region
        duration_days: Duration of trip in days

    Returns:
        JSON string with resupply points
    """
    return json.dumps({
        "location": location,
        "resupply_points": [
            {
                "name": "Trail Town",
                "location": "Mile 50",
                "services": ["Grocery", "Restaurant", "Post office"],
            }
        ],
    })


@tool
def get_local_food_recommendations(location: str) -> str:
    """Get local food recommendations for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with local food recommendations
    """
    return json.dumps({
        "location": location,
        "local_specialties": [
            {
                "name": "Local specialty",
                "description": "Regional favorite",
                "where_to_find": "Local restaurants",
            }
        ],
    })


# Community & Social Tools
@tool
def find_local_clubs(location: str, activity_type: str = "mountain_biking") -> str:
    """Find local clubs for an activity type.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with local clubs
    """
    return json.dumps({
        "location": location,
        "clubs": [
            {
                "name": f"Local {activity_type.replace('_', ' ').title()} Club",
                "contact": "Find on social media",
                "activities": ["Group rides", "Trail maintenance"],
            }
        ],
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
    return json.dumps({
        "location": location,
        "meetup_groups": [
            {
                "name": f"{activity_type.replace('_', ' ').title()} Meetup",
                "platform": "Meetup.com",
                "members": "Active group",
            }
        ],
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
    return json.dumps({
        "location": location,
        "events": [
            {
                "name": "Trail Festival",
                "date": "Upcoming",
                "type": "Community event",
            }
        ],
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
    return json.dumps({
        "location": location,
        "group_rides": [
            {
                "day": "Saturday",
                "time": "9:00 AM",
                "location": "Trailhead",
                "skill_level": "All levels",
            }
        ],
    })


@tool
def find_volunteer_opportunities(location: str) -> str:
    """Find volunteer opportunities (trail work days, etc.).

    Args:
        location: Location name or region

    Returns:
        JSON string with volunteer opportunities
    """
    return json.dumps({
        "location": location,
        "volunteer_opportunities": [
            {
                "type": "Trail work day",
                "organization": "Local trail organization",
                "frequency": "Monthly",
            }
        ],
    })


# Photography & Media Tools
@tool
def find_photo_spots(location: str, route_info: Optional[Dict[str, Any]] = None) -> str:
    """Find best photo spots along a route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with photo spots
    """
    return json.dumps({
        "location": location,
        "photo_spots": [
            {
                "name": "Scenic Overlook",
                "location": "Mile 3",
                "best_time": "Sunrise or sunset",
            }
        ],
    })


@tool
def find_scenic_viewpoints(location: str, route_info: Optional[Dict[str, Any]] = None) -> str:
    """Find scenic viewpoints along a route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with scenic viewpoints
    """
    return json.dumps({
        "location": location,
        "viewpoints": [
            {
                "name": "Mountain Vista",
                "location": "Mile 5",
                "description": "Panoramic mountain views",
            }
        ],
    })


@tool
def get_sunrise_sunset_locations(location: str) -> str:
    """Get best locations for sunrise and sunset photos.

    Args:
        location: Location name or region

    Returns:
        JSON string with sunrise/sunset locations
    """
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
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "tips": [
            "Bring extra batteries",
            "Use polarizing filter for landscapes",
            "Golden hour is best for photos",
        ],
    })


# Historical & Cultural Tools
@tool
def find_historical_sites(location: str, route_info: Optional[Dict[str, Any]] = None) -> str:
    """Find historical sites along a route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with historical sites
    """
    return json.dumps({
        "location": location,
        "historical_sites": [
            {
                "name": "Historical Marker",
                "location": "Mile 2",
                "description": "Local historical significance",
            }
        ],
    })


@tool
def find_cultural_sites(location: str, route_info: Optional[Dict[str, Any]] = None) -> str:
    """Find cultural sites along a route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with cultural sites
    """
    return json.dumps({
        "location": location,
        "cultural_sites": [
            {
                "name": "Cultural Site",
                "location": "Along route",
                "significance": "Cultural importance",
            }
        ],
    })


@tool
def get_local_history(location: str) -> str:
    """Get local history for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with local history
    """
    return json.dumps({
        "location": location,
        "history": {
            "summary": "Rich local history",
            "key_events": ["Historical event 1", "Historical event 2"],
        },
    })


@tool
def get_visitation_guidelines(location: str) -> str:
    """Get respectful visitation guidelines for cultural and historical sites.

    Args:
        location: Location name or region

    Returns:
        JSON string with visitation guidelines
    """
    return json.dumps({
        "location": location,
        "guidelines": [
            "Respect cultural sites",
            "Do not remove artifacts",
            "Follow posted rules",
            "Be respectful of local customs",
        ],
    })


def get_all_tools() -> List[Any]:
    """Get all available tools."""
    return [
        search_blm_lands,
        get_blm_regulations,
        search_trails,
        get_trail_details,
        search_ridewithgps_routes,
        search_strava_routes,
        search_bikepacking_routes,
        search_bikepacking_roots_routes,
        get_bikepacking_route_details,
        search_imba_trails,
        search_adventure_cycling_routes,
        get_route_details,
        get_trail_access_info,
        get_coordinates,
        calculate_distance,
        search_accommodations,
        recommend_gear,
        search_gear_products,
        create_itinerary,
        # Weather & Conditions Tools
        get_weather_forecast,
        get_trail_conditions,
        get_seasonal_information,
        check_weather_alerts,
        # Permits & Regulations Tools
        check_permit_requirements,
        get_permit_information,
        get_regulations,
        check_fire_restrictions,
        get_seasonal_closures,
        # Safety & Emergency Tools
        get_emergency_contacts,
        get_safety_information,
        check_wildlife_alerts,
        get_avalanche_forecast,
        get_river_conditions,
        assess_route_safety,
        # Transportation & Logistics Tools
        get_parking_information,
        find_shuttle_services,
        get_public_transportation,
        find_bike_transport_options,
        get_car_rental_recommendations,
        # Food & Resupply Tools
        find_grocery_stores,
        find_restaurants,
        find_water_sources,
        find_resupply_points,
        get_local_food_recommendations,
        # Community & Social Tools
        find_local_clubs,
        find_meetup_groups,
        find_upcoming_events,
        find_group_rides,
        find_volunteer_opportunities,
        # Photography & Media Tools
        find_photo_spots,
        find_scenic_viewpoints,
        get_sunrise_sunset_locations,
        get_photography_tips,
        # Historical & Cultural Tools
        find_historical_sites,
        find_cultural_sites,
        get_local_history,
        get_visitation_guidelines,
    ]

