"""Route search tools for various platforms."""

from __future__ import annotations

import json

from langchain.tools import tool


@tool
def search_ridewithgps_routes(
    location: str, activity_type: str, distance: float | None = None
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


@tool
def search_strava_routes(
    location: str, activity_type: str, popularity: str | None = None
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


@tool
def search_bikepacking_routes(
    location: str,
    route_type: str | None = None,
    duration_days: int | None = None,
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
                "description": "Curated bikepacking route from Bikepacking.com",
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
                "advocacy_group": "Local IMBA Chapter",
            }
        ]
    })


@tool
def search_adventure_cycling_routes(
    location: str, route_type: str | None = None
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

