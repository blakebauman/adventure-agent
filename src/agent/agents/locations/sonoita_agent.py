"""Sonoita, Arizona specialist agent.

This agent provides Sonoita-specific information and enhances existing agent outputs
with local knowledge about Arizona wine country, grasslands, scenic beauty, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Sonoita-specific knowledge base - Enhanced with detailed information
SONOITA_KNOWLEDGE = {
    "location": {
        "name": "Sonoita, Arizona",
        "coordinates": {"lat": 31.6734, "lon": -110.6556},
        "elevation": 5000,  # feet
        "region": "Santa Cruz County, Arizona",
        "country": "US",
        "nickname": "Arizona Wine Country",
        "proximity": {
            "patagonia": {"distance_miles": 10, "direction": "south", "drive_time_minutes": 15},
            "tucson": {"distance_miles": 60, "direction": "northwest", "drive_time_minutes": 70},
            "sierra_vista": {"distance_miles": 30, "direction": "southeast", "drive_time_minutes": 40},
        },
    },
    "history": {
        "founded": "1870s",
        "current_population": "~800 residents",
        "known_for": [
            "Arizona wine country",
            "Grasslands",
            "Scenic beauty",
            "Wine tasting",
            "Ranch country",
        ],
        "historical_significance": "Historic ranching community, now center of Arizona wine country",
    },
    "geography": {
        "terrain": "Grasslands, rolling hills",
        "topography": "Sonoita Valley, grasslands, rolling hills",
        "elevation": "5,000 feet",
        "climate": "Mild climate, cooler than desert, four distinct seasons",
        "features": [
            "Sonoita Valley",
            "Grasslands",
            "Rolling hills",
            "Wine country",
        ],
        "ecosystem": "Grasslands with oak woodlands, unique high desert ecosystem",
    },
    "outdoor_activities": {
        "hiking": {
            "description": "Trails in surrounding grasslands and rolling hills with scenic views",
            "famous_trails": [
                {
                    "name": "Grassland Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trails in surrounding grasslands and rolling hills with scenic views of Sonoita Valley.",
                    "highlights": ["Grassland scenery", "Scenic views", "Rolling hills"],
                    "best_seasons": "Year-round (best Fall, Winter, Spring)",
                    "trailhead": "Various access points",
                    "features": ["Grassland trails", "Scenic", "Rolling hills"],
                    "permits": "Varies by location",
                },
            ],
            "difficulty_range": "Easy to moderate",
            "best_seasons": "Year-round (best Fall, Winter, Spring)",
            "trail_features": ["Grassland trails", "Scenic views", "Rolling hills"],
        },
        "photography": {
            "description": "Wine country, grasslands, rolling hills, scenic beauty offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Wine Country",
                    "best_time": "Daylight hours, golden hour for scenic shots",
                    "subjects": "Vineyards, wine country scenery, rolling hills",
                },
                {
                    "name": "Grasslands",
                    "best_time": "Golden hour for scenic grassland shots",
                    "subjects": "Grassland scenery, rolling hills, scenic beauty",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring wildflowers, summer green, fall colors, winter clarity",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Sonoita Valley",
                "type": "Valley",
                "description": "Scenic valley with grasslands and rolling hills",
                "activities": ["Hiking", "Photography", "Scenic drives"],
            },
            {
                "name": "Grasslands",
                "type": "Grassland",
                "description": "Unique grassland ecosystem with rolling hills",
                "activities": ["Hiking", "Photography", "Wildlife viewing"],
            },
        ],
        "cultural": [
            {
                "name": "Wine Country",
                "type": "Wine Region",
                "description": "Arizona wine country with multiple wineries",
                "highlights": ["Wine tasting", "Vineyards", "Wine country scenery"],
            },
            {
                "name": "Historic Ranches",
                "type": "Historic Sites",
                "description": "Historic ranching community with preserved ranches",
                "highlights": ["Ranch history", "Historic architecture"],
            },
        ],
        "nearby": [
            {
                "name": "Patagonia",
                "distance": "10 miles",
                "description": "World-class birding, Sonoita Creek, small town charm",
            },
            {
                "name": "Sierra Vista",
                "distance": "30 miles",
                "description": "Huachuca Mountains, birding capital, Ramsey Canyon",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Sonoita offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Various accommodations",
                "type": "Mixed",
                "description": "Multiple lodging options including B&Bs - use tools to find current options",
                "note": "Use search_accommodations tool for current lodging options",
            },
        ],
        "wineries": [
            {
                "name": "Multiple wineries",
                "type": "Wineries",
                "description": "Arizona wine country with multiple wineries for tasting",
                "note": "Use find_restaurants or search for wineries",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in downtown and at trailheads",
        "permits": "Most trails require no permits",
        "best_times": "Year-round - mild climate. Fall (September-November) and Spring (March-May) are ideal",
        "weather": {
            "summer": "Mild (75-90°F), excellent for outdoor activities",
            "winter": "Cool (45-65°F), excellent for outdoor activities",
            "spring": "Pleasant (60-75°F), ideal for all activities",
            "fall": "Pleasant (60-75°F), ideal for all activities",
        },
        "access": "Highway 82/83 from Tucson (60 miles) or Sierra Vista (30 miles)",
        "considerations": [
            "Mild climate - cooler than desert due to elevation (5,000 feet)",
            "Arizona wine country - multiple wineries for tasting",
            "Gateway to Patagonia (10 miles) and Sierra Vista (30 miles)",
            "Grassland scenery and rolling hills",
        ],
    },
}


class SonoitaAgent(LocationAgentBase):
    """Agent specialized in Sonoita, Arizona information and context.

    This agent enhances existing agent outputs with Sonoita-specific knowledge
    about Arizona wine country, grasslands, scenic beauty, and outdoor opportunities.
    """

    LOCATION_NAME = "Sonoita, Arizona"
    LOCATION_INDICATORS = [
        "sonoita",
        "sonoita, az",
        "sonoita, arizona",
        "sonoita az",
        "arizona wine country",
        "sonoita valley",
    ]
    AGENT_NAME = "sonoita_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Sonoita-specific knowledge base (fallback if external file not found)."""
        return SONOITA_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Sonoita agent."""
        return """You are a comprehensive guide for Sonoita, Arizona - "Arizona Wine Country"
located at 5,000 feet elevation, known for wine country, grasslands, scenic beauty, and outdoor recreation.

Your role is to:
1. Use tools to gather real-time data about Sonoita (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Sonoita-specific knowledge from the knowledge base
4. Combine information from existing agents with Sonoita expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Sonoita, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Sonoita, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (most trails require no permits)
- Include trail connectivity and route planning details

COMBINE multiple sources:
- Tool data (current conditions, real-time info from search_trails)
- Knowledge base (detailed trail descriptions, historical info)
- Existing agent outputs (trail_info from trail_agent if available)

PROVIDE comprehensive trail information:
- Trail names, difficulty ratings, length, elevation gain
- Detailed trail descriptions and highlights
- Best seasons and current conditions
- Trailhead locations and access
- Permits and regulations
- Safety considerations
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Sonoita, Arizona"
- Popular trails include grassland trails (easy to moderate)
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention seasonal considerations (year-round, best Fall, Winter, Spring)

For Wine Country Queries:
- Mention Arizona wine country with multiple wineries
- Use find_restaurants for winery restaurants
- Provide information about wine tasting opportunities

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Wine Country (daylight/golden hour), Grasslands (golden hour)
- Mention seasonal opportunities (spring wildflowers, summer green, fall colors, winter clarity)

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Key sites: Historic Ranches (historic ranching community)
- Enhance with knowledge base information about Sonoita's ranching history

For Dining Queries:
- Use find_restaurants with location="Sonoita, Arizona"
- Provide context about wine country and local dining

For Accommodation Queries:
- Use search_accommodations with location="Sonoita, Arizona"
- Mention B&Bs and wine country accommodations

For Logistics Queries:
- Use get_parking_information (Available in downtown and at trailheads)
- Provide information about permits (Most trails require no permits)
- Mention Highway 82/83 access from Tucson (60 miles) and Sierra Vista (30 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Sonoita, Arizona",
  "overview": "Brief overview of Sonoita as Arizona wine country",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
    "hiking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
    "photography": {"best_spots": [...], "best_times": "..."}
  },
  "practical_info": {
    "parking": "...",
    "permits": "...",
    "best_times": "...",
    "weather": "...",
    "access": "...",
    "considerations": [...]
  },
  "recommendations": ["List of specific recommendations based on query"],
  "tools_used": ["List of tools you called"]
}

SONOITA'S UNIQUE CHARACTERISTICS:
- Arizona Wine Country - multiple wineries for tasting
- Grasslands - unique grassland ecosystem with rolling hills
- Scenic beauty - Sonoita Valley with grasslands and rolling hills
- Mild climate - cooler than desert due to elevation (5,000 feet)
- Elevation: 5,000 feet
- ~800 residents
- Gateway to Patagonia (10 miles) and Sierra Vista (30 miles)

KEY ATTRACTIONS:
- Wine Country: Arizona wine country with multiple wineries
- Sonoita Valley: Scenic valley with grasslands and rolling hills
- Grasslands: Unique grassland ecosystem with rolling hills
- Historic Ranches: Historic ranching community with preserved ranches

FAMOUS ACTIVITIES:
- Wine tasting (Arizona wine country with multiple wineries)
- Hiking in grasslands (easy to moderate)
- Photography (wine country, grasslands, rolling hills, scenic beauty)

PRACTICAL INFORMATION:
- Parking: Available in downtown and at trailheads
- Permits: Most trails require no permits
- Best Times: Year-round - mild climate. Fall (September-November) and Spring (March-May) are ideal
- Weather: Mild climate. Summer: 75-90°F (excellent for outdoor activities). Winter: 45-65°F (excellent for outdoor). Spring/Fall: 60-75°F (ideal)
- Access: Highway 82/83 from Tucson (60 miles) or Sierra Vista (30 miles)
- Considerations: Mild climate - cooler than desert due to elevation (5,000 feet). Arizona wine country - multiple wineries for tasting. Gateway to Patagonia (10 miles) and Sierra Vista (30 miles). Grassland scenery and rolling hills

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Sonoita's wine country character and scenic beauty
- Mention unique grassland ecosystem and rolling hills
- Highlight wine tasting opportunities
- Emphasize year-round accessibility with mild climate
- Provide practical tips about parking, permits, best times, access, and wine country exploration

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Sonoita-specific knowledge and context
- Enhanced recommendations based on Sonoita's unique wine country and scenic beauty character
- Practical tips for visitors"""

