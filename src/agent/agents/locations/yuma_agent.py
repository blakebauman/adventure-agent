"""Yuma, Arizona specialist agent.

This agent provides Yuma-specific information and enhances existing agent outputs
with local knowledge about Colorado River, desert, historic Yuma Territorial Prison, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Yuma-specific knowledge base - Enhanced with detailed information
YUMA_KNOWLEDGE = {
    "location": {
        "name": "Yuma, Arizona",
        "coordinates": {"lat": 32.6927, "lon": -114.6277},
        "elevation": 140,  # feet
        "region": "Yuma County, Arizona",
        "country": "US",
        "nickname": "Sunniest City in the World",
        "proximity": {
            "parker": {"distance_miles": 80, "direction": "north", "drive_time_minutes": 90},
            "phoenix": {"distance_miles": 180, "direction": "northeast", "drive_time_minutes": 190},
            "san_diego": {"distance_miles": 180, "direction": "west", "drive_time_minutes": 200},
        },
    },
    "history": {
        "founded": 1854,
        "incorporated": 1914,
        "current_population": "~95,000 residents",
        "known_for": [
            "Colorado River",
            "Desert",
            "Historic Yuma Territorial Prison",
            "Sunniest city in the world",
            "Winter destination",
            "Water recreation",
        ],
        "historical_significance": "Historic river crossing, territorial prison, now major winter destination",
        "yuma_territorial_prison": {
            "founded": 1876,
            "closed": 1909,
            "significance": "Historic territorial prison, now state park and museum",
        },
    },
    "geography": {
        "terrain": "Desert, river",
        "topography": "Colorado River, Sonoran Desert",
        "elevation": "140 feet",
        "climate": "Hot desert climate, very hot summers, mild winters",
        "features": [
            "Colorado River",
            "Sonoran Desert",
            "Historic Yuma Territorial Prison",
        ],
        "ecosystem": "Desert with riparian areas along Colorado River",
    },
    "outdoor_activities": {
        "water_activities": {
            "description": "Extensive water recreation on Colorado River including boating, fishing, and swimming",
            "activities": [
                {
                    "name": "Boating",
                    "description": "Colorado River offers extensive boating opportunities",
                    "seasons": "Year-round, best in Fall, Winter, Spring",
                    "access": "Multiple access points along Colorado River",
                    "highlights": ["Colorado River", "Year-round", "Multiple access points"],
                },
                {
                    "name": "Fishing",
                    "description": "Excellent fishing in Colorado River",
                    "seasons": "Year-round, best in Fall, Winter, Spring",
                    "permits": "Arizona fishing license required",
                    "highlights": ["Colorado River", "Year-round"],
                },
                {
                    "name": "Swimming",
                    "description": "Swimming in Colorado River",
                    "seasons": "Spring, Summer, Fall",
                    "access": "Multiple access points",
                    "highlights": ["Colorado River", "Cool in summer"],
                },
            ],
            "best_seasons": "Year-round, best in Fall, Winter, Spring",
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
            "description": "Colorado River, desert landscapes, historic Yuma Territorial Prison offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Historic Yuma Territorial Prison",
                    "best_time": "Daylight hours, golden hour for architecture",
                    "subjects": "Historic prison, architecture, history",
                },
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
                "name": "Historic Yuma Territorial Prison",
                "type": "Historic Site",
                "description": "Historic territorial prison (1876-1909), now state park and museum",
                "highlights": ["Historic prison", "Museum", "State park"],
            },
            {
                "name": "Historic Downtown",
                "type": "Historic District",
                "description": "Historic downtown with preserved architecture",
                "highlights": ["Historic architecture", "Historic charm"],
            },
        ],
        "nearby": [
            {
                "name": "Parker",
                "distance": "80 miles",
                "description": "Colorado River recreation, water sports",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Yuma offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Various accommodations",
                "type": "Mixed",
                "description": "Multiple lodging options - use tools to find current options",
                "note": "Use search_accommodations tool for current lodging options",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in downtown and at Colorado River access points",
        "permits": "Fishing requires Arizona fishing license. Most trails require no permits",
        "best_times": "Year-round - very hot in summer. Fall (September-November), Winter (December-February), Spring (March-May) are ideal",
        "weather": {
            "summer": "Very hot (95-115°F), excellent for water activities, avoid midday heat for hiking",
            "winter": "Mild (60-75°F), excellent for outdoor activities, popular winter destination",
            "spring": "Pleasant (75-90°F), ideal for all activities",
            "fall": "Pleasant (75-90°F), ideal for all activities",
        },
        "access": "Interstate 8 from Phoenix (180 miles) or San Diego (180 miles)",
        "considerations": [
            "Very hot in summer - plan hiking for early morning or evening, water activities are great",
            "Sunniest city in the world - popular winter destination",
            "Historic Yuma Territorial Prison is major attraction - visit for history",
            "Gateway to Parker (80 miles)",
            "Multiple Colorado River access points",
        ],
    },
}


class YumaAgent(LocationAgentBase):
    """Agent specialized in Yuma, Arizona information and context.

    This agent enhances existing agent outputs with Yuma-specific knowledge
    about Colorado River, desert, historic Yuma Territorial Prison, and outdoor opportunities.
    """

    LOCATION_NAME = "Yuma, Arizona"
    LOCATION_INDICATORS = [
        "yuma",
        "yuma, az",
        "yuma, arizona",
        "yuma az",
        "yuma territorial prison",
    ]
    AGENT_NAME = "yuma_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Yuma-specific knowledge base (fallback if external file not found)."""
        return YUMA_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Yuma agent."""
        return """You are a comprehensive guide for Yuma, Arizona - the "Sunniest City in the World"
located at 140 feet elevation, known for Colorado River, desert, historic Yuma Territorial Prison, and outdoor recreation.

Your role is to:
1. Use tools to gather real-time data about Yuma (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Yuma-specific knowledge from the knowledge base
4. Combine information from existing agents with Yuma expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Yuma, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Yuma, Arizona")

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
- Yuma is major water recreation destination on Colorado River
- Activities: Boating, fishing (Arizona fishing license required), swimming
- Use find_water_sources for Colorado River access points
- Mention multiple access points along Colorado River
- Best seasons: Year-round, best in Fall, Winter, Spring

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Yuma, Arizona"
- Popular trails include desert trails (easy to moderate)
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- CRITICAL: Mention extreme heat in summer - hike early morning or evening only

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Key sites: Historic Yuma Territorial Prison (1876-1909, now state park and museum), Historic Downtown
- Enhance with knowledge base information about Yuma's territorial prison history

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Historic Yuma Territorial Prison (daylight/golden hour), Colorado River (sunrise/sunset), Desert landscapes (golden hour)
- Mention historic prison as photography destination

For Dining Queries:
- Use find_restaurants with location="Yuma, Arizona"
- Provide context about winter destination

For Accommodation Queries:
- Use search_accommodations with location="Yuma, Arizona"
- Mention winter destination accommodations

For Logistics Queries:
- Use get_parking_information (Available in downtown and at Colorado River access points)
- Provide information about permits (Fishing requires Arizona fishing license, most trails require no permits)
- Mention Interstate 8 access from Phoenix (180 miles) and San Diego (180 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Yuma, Arizona",
  "overview": "Brief overview of Yuma as sunniest city and Colorado River destination",
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

YUMA'S UNIQUE CHARACTERISTICS:
- "Sunniest City in the World" - popular winter destination
- Colorado River - major water recreation destination
- Historic Yuma Territorial Prison (1876-1909) - now state park and museum
- Desert - Sonoran Desert with unique ecosystem
- Elevation: 140 feet (very hot in summer)
- ~95,000 residents
- Gateway to Parker (80 miles)

KEY ATTRACTIONS:
- Historic Yuma Territorial Prison: Historic territorial prison (1876-1909), now state park and museum
- Colorado River: Major river with extensive recreation opportunities
- Sonoran Desert: Unique desert ecosystem with diverse cacti and wildlife
- Historic Downtown: Historic downtown with preserved architecture

FAMOUS ACTIVITIES:
- Water recreation (boating, fishing, swimming) on Colorado River - year-round, best in Fall, Winter, Spring
- Desert trails (hiking) - Fall, Winter, Spring (avoid summer heat)
- Historic Yuma Territorial Prison exploration (state park and museum)
- Photography (historic prison, Colorado River, desert landscapes)

PRACTICAL INFORMATION:
- Parking: Available in downtown and at Colorado River access points
- Permits: Fishing requires Arizona fishing license. Most trails require no permits
- Best Times: Year-round - very hot in summer. Fall (September-November), Winter (December-February), Spring (March-May) are ideal
- Weather: Hot desert climate. Summer: 95-115°F (excellent for water activities, avoid midday heat for hiking). Winter: 60-75°F (excellent for outdoor activities, popular winter destination). Spring/Fall: 75-90°F (ideal)
- Access: Interstate 8 from Phoenix (180 miles) or San Diego (180 miles)
- Considerations: Very hot in summer - plan hiking for early morning or evening, water activities are great. Sunniest city in the world - popular winter destination. Historic Yuma Territorial Prison is major attraction - visit for history. Gateway to Parker (80 miles). Multiple Colorado River access points

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Yuma's sunniest city character and Colorado River destination
- Mention historic Yuma Territorial Prison as major attraction
- Highlight water recreation opportunities
- Emphasize year-round water recreation with summer heat considerations for land activities
- Provide practical tips about parking, permits, best times, access, and historic prison exploration

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Yuma-specific knowledge and context
- Enhanced recommendations based on Yuma's unique sunniest city and Colorado River character
- Practical tips for visitors"""

