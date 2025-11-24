"""Tools for adventure agent sub-agents.

This module provides all tools organized by category. Tools can be imported
directly from this module for backward compatibility.
"""

from __future__ import annotations

from typing import Any, List

# Import accommodation tools
from agent.tools.accommodation import search_accommodations

# Import BLM tools
from agent.tools.blm import get_blm_regulations, search_blm_lands

# Import community tools
from agent.tools.community import (
    find_group_rides,
    find_local_clubs,
    find_meetup_groups,
    find_upcoming_events,
    find_volunteer_opportunities,
)

# Import food tools
from agent.tools.food import (
    find_grocery_stores,
    find_restaurants,
    find_resupply_points,
    find_water_sources,
    get_local_food_recommendations,
)

# Import gear tools
from agent.tools.gear import recommend_gear, search_gear_products

# Import geo tools
from agent.tools.geo import calculate_distance, get_coordinates

# Import historical tools
from agent.tools.historical import (
    find_cultural_sites,
    find_historical_sites,
    get_local_history,
    get_visitation_guidelines,
)

# Import permits tools
from agent.tools.permits import (
    check_fire_restrictions,
    check_permit_requirements,
    get_permit_information,
    get_regulations,
    get_seasonal_closures,
)

# Import photography tools
from agent.tools.photography import (
    find_photo_spots,
    find_scenic_viewpoints,
    get_photography_tips,
    get_sunrise_sunset_locations,
)

# Import planning tools
from agent.tools.planning import create_itinerary

# Import route tools
from agent.tools.routes import (
    get_bikepacking_route_details,
    get_route_details,
    search_adventure_cycling_routes,
    search_bikepacking_roots_routes,
    search_bikepacking_routes,
    search_imba_trails,
    search_ridewithgps_routes,
    search_strava_routes,
)

# Import safety tools
from agent.tools.safety import (
    assess_route_safety,
    check_wildlife_alerts,
    get_avalanche_forecast,
    get_emergency_contacts,
    get_river_conditions,
    get_safety_information,
)

# Import trail tools
from agent.tools.trails import (
    get_trail_access_info,
    get_trail_details,
    search_trails,
)

# Import transportation tools
from agent.tools.transportation import (
    find_bike_transport_options,
    find_shuttle_services,
    get_car_rental_recommendations,
    get_parking_information,
    get_public_transportation,
)

# Import weather tools
from agent.tools.weather import (
    check_weather_alerts,
    get_seasonal_information,
    get_trail_conditions,
    get_weather_forecast,
)

# Import WebSearchTool class
from agent.tools.web_search import WebSearchTool


def get_all_tools() -> List[Any]:
    """Get all available tools."""
    return [
        # BLM tools
        search_blm_lands,
        get_blm_regulations,
        # Trail tools
        search_trails,
        get_trail_details,
        # Route tools
        search_ridewithgps_routes,
        search_strava_routes,
        search_bikepacking_routes,
        search_bikepacking_roots_routes,
        get_bikepacking_route_details,
        search_imba_trails,
        search_adventure_cycling_routes,
        get_route_details,
        get_trail_access_info,
        # Geo tools
        get_coordinates,
        calculate_distance,
        # Accommodation tools
        search_accommodations,
        # Gear tools
        recommend_gear,
        search_gear_products,
        # Planning tools
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


__all__ = [
    # WebSearchTool class
    "WebSearchTool",
    # BLM tools
    "search_blm_lands",
    "get_blm_regulations",
    # Trail tools
    "search_trails",
    "get_trail_details",
    "get_trail_access_info",
    # Route tools
    "search_ridewithgps_routes",
    "search_strava_routes",
    "search_bikepacking_routes",
    "search_bikepacking_roots_routes",
    "get_bikepacking_route_details",
    "search_imba_trails",
    "search_adventure_cycling_routes",
    "get_route_details",
    # Geo tools
    "get_coordinates",
    "calculate_distance",
    # Accommodation tools
    "search_accommodations",
    # Gear tools
    "recommend_gear",
    "search_gear_products",
    # Planning tools
    "create_itinerary",
    # Weather tools
    "get_weather_forecast",
    "get_trail_conditions",
    "get_seasonal_information",
    "check_weather_alerts",
    # Permits tools
    "check_permit_requirements",
    "get_permit_information",
    "get_regulations",
    "check_fire_restrictions",
    "get_seasonal_closures",
    # Safety tools
    "get_emergency_contacts",
    "get_safety_information",
    "check_wildlife_alerts",
    "get_avalanche_forecast",
    "get_river_conditions",
    "assess_route_safety",
    # Transportation tools
    "get_parking_information",
    "find_shuttle_services",
    "get_public_transportation",
    "find_bike_transport_options",
    "get_car_rental_recommendations",
    # Food tools
    "find_grocery_stores",
    "find_restaurants",
    "find_water_sources",
    "find_resupply_points",
    "get_local_food_recommendations",
    # Community tools
    "find_local_clubs",
    "find_meetup_groups",
    "find_upcoming_events",
    "find_group_rides",
    "find_volunteer_opportunities",
    # Photography tools
    "find_photo_spots",
    "find_scenic_viewpoints",
    "get_sunrise_sunset_locations",
    "get_photography_tips",
    # Historical tools
    "find_historical_sites",
    "find_cultural_sites",
    "get_local_history",
    "get_visitation_guidelines",
    # Function
    "get_all_tools",
]

