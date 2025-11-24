"""Arizona cities and towns registry for location agents.

This module maintains a registry of Arizona cities and towns that have
location-specific agents, and tracks which ones are planned for future development.
"""

from __future__ import annotations

from typing import Dict, List

# Registry of Arizona cities/towns with location agents
ARIZONA_LOCATION_AGENTS: Dict[str, Dict[str, str]] = {
    "jerome": {
        "agent_name": "jerome_agent",
        "location_name": "Jerome, Arizona",
        "status": "active",
        "description": "Historic mining town, ghost town revival, artistic community",
    },
    "sedona": {
        "agent_name": "sedona_agent",
        "location_name": "Sedona, Arizona",
        "status": "active",
        "description": "Red rock formations, world-class MTB trails, spiritual vortex sites",
    },
    "prescott": {
        "agent_name": "prescott_agent",
        "location_name": "Prescott, Arizona",
        "status": "active",
        "description": "Historic territorial capital, Whiskey Row, mountain biking",
    },
    "flagstaff": {
        "agent_name": "flagstaff_agent",
        "location_name": "Flagstaff, Arizona",
        "status": "active",
        "description": "Mountain town, San Francisco Peaks, Grand Canyon gateway",
    },
    "grand_canyon": {
        "agent_name": "grand_canyon_agent",
        "location_name": "Grand Canyon National Park, Arizona",
        "status": "active",
        "description": "One of the Seven Natural Wonders, North and South Rim, iconic hiking",
    },
    "payson": {
        "agent_name": "payson_agent",
        "location_name": "Payson, Arizona",
        "status": "active",
        "description": "Mogollon Rim gateway, Tonto National Forest, outdoor recreation",
    },
    "pine": {
        "agent_name": "pine_agent",
        "location_name": "Pine, Arizona",
        "status": "active",
        "description": "Mogollon Rim community, Tonto National Forest, small mountain town",
    },
    "strawberry": {
        "agent_name": "strawberry_agent",
        "location_name": "Strawberry, Arizona",
        "status": "active",
        "description": "Mogollon Rim community, historic buildings, small mountain town",
    },
    "pinetop": {
        "agent_name": "pinetop_agent",
        "location_name": "Pinetop-Lakeside, Arizona",
        "status": "active",
        "description": "White Mountains, lakes, fishing, outdoor recreation",
    },
    "williams": {
        "agent_name": "williams_agent",
        "location_name": "Williams, Arizona",
        "status": "active",
        "description": "Route 66, Grand Canyon gateway, Grand Canyon Railway",
    },
    "phoenix": {
        "agent_name": "phoenix_agent",
        "location_name": "Phoenix, Arizona",
        "status": "active",
        "description": "Valley of the Sun, desert trails, urban mountain biking",
    },
    "tucson": {
        "agent_name": "tucson_agent",
        "location_name": "Tucson, Arizona",
        "status": "active",
        "description": "Sonoran Desert, Saguaro National Park, Mount Lemmon",
    },
    "cottonwood": {
        "agent_name": "cottonwood_agent",
        "location_name": "Cottonwood, Arizona",
        "status": "active",
        "description": "Verde Valley, wine country, Old Town, gateway to Jerome and Sedona",
    },
    "camp_verde": {
        "agent_name": "camp_verde_agent",
        "location_name": "Camp Verde, Arizona",
        "status": "active",
        "description": "Verde Valley, Montezuma Castle, Montezuma Well, Fort Verde",
    },
    "show_low": {
        "agent_name": "show_low_agent",
        "location_name": "Show Low, Arizona",
        "status": "active",
        "description": "White Mountains, Ponderosa pine forests, outdoor recreation",
    },
    "bisbee": {
        "agent_name": "bisbee_agent",
        "location_name": "Bisbee, Arizona",
        "status": "active",
        "description": "Historic mining town, arts community, Mule Mountains",
    },
    "tombstone": {
        "agent_name": "tombstone_agent",
        "location_name": "Tombstone, Arizona",
        "status": "active",
        "description": "Wild West history, O.K. Corral, Boot Hill Cemetery",
    },
    "sierra_vista": {
        "agent_name": "sierra_vista_agent",
        "location_name": "Sierra Vista, Arizona",
        "status": "active",
        "description": "Huachuca Mountains, birding capital, Ramsey Canyon",
    },
    "patagonia": {
        "agent_name": "patagonia_agent",
        "location_name": "Patagonia, Arizona",
        "status": "active",
        "description": "World-class birding, Sonoita Creek, small town charm",
    },
    "page": {
        "agent_name": "page_agent",
        "location_name": "Page, Arizona",
        "status": "active",
        "description": "Lake Powell, Antelope Canyon, Horseshoe Bend",
    },
    "kingman": {
        "agent_name": "kingman_agent",
        "location_name": "Kingman, Arizona",
        "status": "active",
        "description": "Route 66, gateway to Grand Canyon West, Hualapai Mountains",
    },
    "lake_havasu": {
        "agent_name": "lake_havasu_agent",
        "location_name": "Lake Havasu City, Arizona",
        "status": "active",
        "description": "Colorado River, water sports, London Bridge, desert trails",
    },
    "globe": {
        "agent_name": "globe_miami_agent",
        "location_name": "Globe/Miami, Arizona",
        "status": "active",
        "description": "Tonto National Forest, Pinal Mountains, historic mining, mountain biking",
    },
    "miami": {
        "agent_name": "globe_miami_agent",
        "location_name": "Globe/Miami, Arizona",
        "status": "active",
        "description": "Tonto National Forest, Pinal Mountains, historic mining, mountain biking",
    },
    "springerville": {
        "agent_name": "springerville_eagar_agent",
        "location_name": "Springerville/Eagar, Arizona",
        "status": "active",
        "description": "White Mountains, Apache-Sitgreaves NF, high elevation recreation",
    },
    "eagar": {
        "agent_name": "springerville_eagar_agent",
        "location_name": "Springerville/Eagar, Arizona",
        "status": "active",
        "description": "White Mountains, Apache-Sitgreaves NF, high elevation recreation",
    },
    "ajo": {
        "agent_name": "ajo_agent",
        "location_name": "Ajo, Arizona",
        "status": "active",
        "description": "Organ Pipe Cactus National Monument gateway, desert wilderness",
    },
    "sonoita": {
        "agent_name": "sonoita_agent",
        "location_name": "Sonoita, Arizona",
        "status": "active",
        "description": "Arizona wine country, grasslands, scenic beauty",
    },
    "yuma": {
        "agent_name": "yuma_agent",
        "location_name": "Yuma, Arizona",
        "status": "active",
        "description": "Colorado River, desert, historic Yuma Territorial Prison",
    },
    "parker": {
        "agent_name": "parker_agent",
        "location_name": "Parker, Arizona",
        "status": "active",
        "description": "Colorado River recreation, water sports",
    },
}

# Planned Arizona cities/towns for future agents
PLANNED_ARIZONA_LOCATIONS: List[Dict[str, str]] = [
    # All planned locations have been implemented
    # Future locations can be added here as needed
]

# Major Arizona regions
ARIZONA_REGIONS = {
    "northern_arizona": {
        "cities": ["Flagstaff", "Sedona", "Prescott", "Jerome", "Williams", "Page", "Grand Canyon"],
        "description": "High elevation, pine forests, red rock country, Grand Canyon, Lake Powell",
    },
    "central_arizona": {
        "cities": ["Phoenix", "Scottsdale", "Tempe", "Mesa", "Payson"],
        "description": "Valley of the Sun, desert, urban mountain biking",
    },
    "southern_arizona": {
        "cities": [
            "Tucson",
            "Bisbee",
            "Tombstone",
            "Sierra Vista",
            "Patagonia",
            "Nogales",
            "Sonoita",
            "Ajo",
        ],
        "description": "Sonoran Desert, Saguaro National Park, border region, mining towns, birding",
    },
    "eastern_arizona": {
        "cities": ["Show Low", "Pinetop-Lakeside", "Springerville"],
        "description": "White Mountains, high elevation, pine forests",
    },
    "western_arizona": {
        "cities": ["Lake Havasu City", "Kingman", "Bullhead City", "Yuma", "Parker"],
        "description": "Colorado River, desert, water recreation",
    },
}


def get_arizona_location_agent(location: str) -> Dict[str, str] | None:
    """Get location agent info for an Arizona city/town.

    Args:
        location: Location name (case-insensitive)

    Returns:
        Agent info dict or None if not found
    """
    location_lower = location.lower().strip()
    # Remove common suffixes
    location_lower = location_lower.replace(", arizona", "").replace(", az", "").strip()

    return ARIZONA_LOCATION_AGENTS.get(location_lower)


def get_all_arizona_agents() -> Dict[str, Dict[str, str]]:
    """Get all active Arizona location agents.

    Returns:
        Dictionary of location agents
    """
    return {
        name: info
        for name, info in ARIZONA_LOCATION_AGENTS.items()
        if info.get("status") == "active"
    }


def get_planned_locations() -> List[Dict[str, str]]:
    """Get list of planned Arizona locations for future agents.

    Returns:
        List of planned locations with priority
    """
    return PLANNED_ARIZONA_LOCATIONS.copy()


def is_arizona_location(location: str) -> bool:
    """Check if a location is in Arizona.

    Args:
        location: Location name

    Returns:
        True if location appears to be in Arizona
    """
    location_lower = location.lower()
    arizona_indicators = [
        "arizona",
        "az",
        "phoenix",
        "tucson",
        "flagstaff",
        "sedona",
        "prescott",
        "jerome",
        "scottsdale",
        "tempe",
        "mesa",
        "bisbee",
        "page",
        "williams",
        "cottonwood",
        "payson",
        "show low",
        "pinetop",
        "grand canyon",
    ]

    # Check if any indicator is in the location string
    return any(indicator in location_lower for indicator in arizona_indicators)


def get_arizona_region(location: str) -> str | None:
    """Get the Arizona region for a location.

    Args:
        location: Location name

    Returns:
        Region name or None
    """
    location_lower = location.lower()
    for region_name, region_info in ARIZONA_REGIONS.items():
        for city in region_info["cities"]:
            if city.lower() in location_lower:
                return region_name
    return None

