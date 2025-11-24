"""Parker, Arizona specialist agent.

This agent provides Parker-specific information and enhances existing agent outputs
with local knowledge about Colorado River recreation, water sports, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Parker-specific knowledge base - Enhanced with detailed information
PARKER_KNOWLEDGE = {
    "location": {
        "name": "Parker, Arizona",
        "coordinates": {"lat": 34.1500, "lon": -114.2886},
        "elevation": 400,  # feet
        "region": "La Paz County, Arizona",
        "country": "US",
        "nickname": "Colorado River Recreation Hub",
        "proximity": {
            "lake_havasu": {"distance_miles": 30, "direction": "north", "drive_time_minutes": 35},
            "yuma": {"distance_miles": 80, "direction": "south", "drive_time_minutes": 90},
            "phoenix": {"distance_miles": 150, "direction": "east", "drive_time_minutes": 160},
        },
    },
    "history": {
        "founded": 1908,
        "incorporated": 1948,
        "current_population": "~3,000 residents",
        "known_for": [
            "Colorado River recreation",
            "Water sports",
            "Boating",
            "Fishing",
            "Desert trails",
        ],
        "historical_significance": "Founded as river town, now major Colorado River recreation destination",
    },
    "geography": {
        "terrain": "Desert, river",
        "topography": "Colorado River, Sonoran Desert",
        "elevation": "400 feet",
        "climate": "Hot desert climate, very hot summers, mild winters",
        "features": [
            "Colorado River",
            "Sonoran Desert",
            "River recreation",
        ],
        "ecosystem": "Desert with riparian areas along Colorado River",
    },
    "outdoor_activities": {
        "water_activities": {
            "description": "Extensive water recreation on Colorado River including boating, jet skiing, fishing, and swimming",
            "activities": [
                {
                    "name": "Boating",
                    "description": "Colorado River offers extensive boating opportunities",
                    "seasons": "Year-round, best in Spring, Summer, Fall",
                    "access": "Multiple marinas and boat ramps",
                    "highlights": ["Colorado River", "Year-round", "Multiple marinas"],
                },
                {
                    "name": "Jet Skiing",
                    "description": "Popular jet skiing on Colorado River",
                    "seasons": "Year-round, best in Spring, Summer, Fall",
                    "access": "Multiple access points",
                    "highlights": ["Popular", "Year-round", "Multiple access points"],
                },
                {
                    "name": "Fishing",
                    "description": "Excellent fishing in Colorado River for bass, catfish, and other species",
                    "seasons": "Year-round, best in Spring and Fall",
                    "permits": "Arizona fishing license required",
                    "highlights": ["Bass", "Catfish", "Year-round"],
                },
                {
                    "name": "Swimming",
                    "description": "Swimming in Colorado River",
                    "seasons": "Spring, Summer, Fall",
                    "access": "Multiple access points",
                    "highlights": ["Multiple access points", "Cool in summer"],
                },
            ],
            "best_seasons": "Year-round, best in Spring, Summer, Fall",
            "permits": "Fishing requires Arizona fishing license",
        },
        "hiking": {
            "description": "Desert trails in surrounding area with scenic desert views",
            "famous_trails": [
                {
                    "name": "Desert Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Desert trails in surrounding area with scenic desert views.",
                    "highlights": ["Desert scenery", "Scenic", "Varied difficulty"],
                    "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
                    "trailhead": "Various access points",
                    "features": ["Desert trails", "Scenic"],
                    "permits": "Varies by location",
                },
            ],
            "difficulty_range": "Easy to moderate",
            "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
            "trail_features": ["Desert trails", "Scenic views"],
        },
        "photography": {
            "description": "Colorado River, desert landscapes offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Colorado River",
                    "best_time": "Sunrise and sunset for scenic river shots",
                    "subjects": "River scenery, water activities, scenic views",
                },
                {
                    "name": "Desert Landscapes",
                    "best_time": "Golden hour for scenic desert shots",
                    "subjects": "Desert scenery, cacti, mountain backdrops",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring wildflowers, winter clarity",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Colorado River",
                "type": "River",
                "description": "Major river with extensive recreation opportunities",
                "activities": ["All water activities"],
            },
            {
                "name": "Sonoran Desert",
                "type": "Desert",
                "description": "Unique desert ecosystem with diverse cacti and wildlife",
                "activities": ["All desert activities"],
            },
        ],
        "cultural": [
            {
                "name": "River Recreation",
                "type": "Recreation",
                "description": "Major Colorado River recreation destination",
                "highlights": ["Water sports", "Boating", "Fishing"],
            },
        ],
        "nearby": [
            {
                "name": "Lake Havasu City",
                "distance": "30 miles",
                "description": "Colorado River, water sports, London Bridge",
            },
            {
                "name": "Yuma",
                "distance": "80 miles",
                "description": "Colorado River, desert, historic Yuma Territorial Prison",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Parker offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Various accommodations",
                "type": "Mixed",
                "description": "Multiple lodging options including RV parks - use tools to find current options",
                "note": "Use search_accommodations tool for current lodging options",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in downtown and at marinas. Popular areas may fill up on weekends - arrive early",
        "permits": "Fishing requires Arizona fishing license. Most trails require no permits",
        "best_times": "Year-round - very hot in summer. Fall (September-November) and Spring (March-May) are ideal",
        "weather": {
            "summer": "Very hot (95-115°F), excellent for water activities, avoid midday heat for hiking",
            "winter": "Mild (60-75°F), excellent for outdoor activities",
            "spring": "Pleasant (75-90°F), ideal for all activities",
            "fall": "Pleasant (75-90°F), ideal for all activities",
        },
        "access": "Highway 95 from Lake Havasu City (30 miles) or Yuma (80 miles)",
        "considerations": [
            "Very hot in summer - plan hiking for early morning or evening, water activities are great",
            "Popular water recreation destination - can be crowded on weekends",
            "Gateway to Lake Havasu City (30 miles) and Yuma (80 miles)",
            "Multiple marinas and boat ramps available",
        ],
    },
}


class ParkerAgent(LocationAgentBase):
    """Agent specialized in Parker, Arizona information and context.

    This agent enhances existing agent outputs with Parker-specific knowledge
    about Colorado River recreation, water sports, and outdoor opportunities.
    """

    LOCATION_NAME = "Parker, Arizona"
    LOCATION_INDICATORS = [
        "parker",
        "parker, az",
        "parker, arizona",
        "parker az",
        "parker, colorado river",
    ]
    AGENT_NAME = "parker_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Parker-specific knowledge base (fallback if external file not found)."""
        return PARKER_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Parker agent."""
        return """You are a comprehensive guide for Parker, Arizona - "Colorado River Recreation Hub"
located at 400 feet elevation, known for Colorado River recreation, water sports, and outdoor opportunities.

Your role is to:
1. Use tools to gather real-time data about Parker (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Parker-specific knowledge from the knowledge base
4. Combine information from existing agents with Parker expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Parker, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Parker, Arizona")

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
- Safety considerations (extreme heat in summer)
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Water Activities Queries:
- Parker is major water recreation destination on Colorado River
- Activities: Boating, jet skiing, fishing (bass, catfish - Arizona fishing license required), swimming
- Use find_water_sources for Colorado River access points
- Mention multiple marinas and boat ramps
- Provide information about Arizona fishing license requirements
- Best seasons: Year-round, best in Spring, Summer, Fall

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Parker, Arizona"
- Popular trails include desert trails (easy to moderate)
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- CRITICAL: Mention extreme heat in summer - hike early morning or evening only

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Colorado River (sunrise/sunset), Desert landscapes (golden hour)
- Mention seasonal opportunities (spring wildflowers, winter clarity)

For Dining Queries:
- Use find_restaurants with location="Parker, Arizona"
- Provide context about recreation destination

For Accommodation Queries:
- Use search_accommodations with location="Parker, Arizona"
- Mention RV parks and recreation destination accommodations

For Logistics Queries:
- Use get_parking_information (Popular areas may fill up on weekends - arrive early)
- Provide information about permits (Fishing requires Arizona fishing license, most trails require no permits)
- Mention Highway 95 access from Lake Havasu City (30 miles) and Yuma (80 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Parker, Arizona",
  "overview": "Brief overview of Parker as Colorado River recreation hub",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
    "water_activities": {"activities": [...], "seasons": "..."},
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

PARKER'S UNIQUE CHARACTERISTICS:
- Colorado River Recreation Hub - major water recreation destination
- Colorado River - extensive recreation opportunities
- Water sports - boating, jet skiing, fishing, swimming
- Desert trails - easy to moderate hiking
- Elevation: 400 feet (very hot in summer)
- ~3,000 residents
- Gateway to Lake Havasu City (30 miles) and Yuma (80 miles)

KEY ATTRACTIONS:
- Colorado River: Major river with extensive recreation opportunities
- Sonoran Desert: Unique desert ecosystem with diverse cacti and wildlife
- River Recreation: Major Colorado River recreation destination

FAMOUS ACTIVITIES:
- Water recreation (boating, jet skiing, fishing, swimming) on Colorado River - year-round, best in Spring, Summer, Fall
- Desert trails (hiking) - Fall, Winter, Spring (avoid summer heat)
- Photography (Colorado River, desert landscapes)

PRACTICAL INFORMATION:
- Parking: Available in downtown and at marinas. Popular areas may fill up on weekends - arrive early
- Permits: Fishing requires Arizona fishing license. Most trails require no permits
- Best Times: Year-round - very hot in summer. Fall (September-November) and Spring (March-May) are ideal
- Weather: Hot desert climate. Summer: 95-115°F (excellent for water activities, avoid midday heat for hiking). Winter: 60-75°F (excellent for outdoor activities). Spring/Fall: 75-90°F (ideal)
- Access: Highway 95 from Lake Havasu City (30 miles) or Yuma (80 miles)
- Considerations: Very hot in summer - plan hiking for early morning or evening, water activities are great. Popular water recreation destination - can be crowded on weekends. Gateway to Lake Havasu City (30 miles) and Yuma (80 miles). Multiple marinas and boat ramps available

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Parker's Colorado River recreation hub character
- Mention water recreation as primary activity
- Highlight desert trail opportunities (with summer heat warnings)
- Emphasize year-round water recreation with summer heat considerations for land activities
- Provide practical tips about parking, permits, best times, access, and water recreation

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Parker-specific knowledge and context
- Enhanced recommendations based on Parker's unique Colorado River recreation hub character
- Practical tips for visitors"""

