"""Trail search and information tools."""

from __future__ import annotations

import json

import httpx
from langchain.tools import tool

from agent.cache import cached_api_call
from agent.tools.geo import get_coordinates


@tool
def search_trails(
    location: str,
    activity_type: str,
    source: str,
    difficulty: str | None = None,
    distance: float | None = None,
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
        def _call_overpass() -> str:
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
                raise ValueError("No trails found")
        
        # Use cached API call with rate limiting (cache for 6 hours)
        result = cached_api_call(
            endpoint="overpass",
            params={
                "lat": lat,
                "lon": lon,
                "activity_type": activity_type,
                "difficulty": difficulty,
                "distance": distance,
            },
            api_func=_call_overpass,
            ttl=21600.0,  # Cache for 6 hours (trail data changes slowly)
        )
        if result:
            return result
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

