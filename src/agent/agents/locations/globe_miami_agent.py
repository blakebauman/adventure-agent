"""Globe/Miami, Arizona specialist agent.

This agent provides Globe/Miami-specific information and enhances existing agent outputs
with local knowledge about Tonto National Forest, Pinal Mountains, historic mining, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Globe/Miami-specific knowledge base - Enhanced with detailed information
GLOBE_MIAMI_KNOWLEDGE = {
    "location": {
        "name": "Globe/Miami, Arizona",
        "coordinates": {"lat": 33.3942, "lon": -110.7865},  # Globe coordinates
        "elevation": 3500,  # feet
        "region": "Gila County, Arizona",
        "country": "US",
        "nickname": "Historic Mining Towns",
        "proximity": {
            "payson": {"distance_miles": 50, "direction": "north", "drive_time_minutes": 60},
            "phoenix": {"distance_miles": 90, "direction": "west", "drive_time_minutes": 100},
            "show_low": {"distance_miles": 100, "direction": "northeast", "drive_time_minutes": 120},
        },
    },
    "history": {
        "founded": 1876,  # Globe founded
        "current_population": "~7,500 residents (Globe), ~1,800 residents (Miami)",
        "known_for": [
            "Historic mining towns",
            "Tonto National Forest",
            "Pinal Mountains",
            "Copper mining history",
            "Historic downtown Globe",
            "Mountain biking",
        ],
        "historical_significance": "Major copper mining towns from late 1800s, now gateway to Tonto National Forest recreation",
        "mining_history": {
            "era": "Late 1800s to present",
            "mineral": "Copper",
            "significance": "Major copper mining district, historic mining operations",
        },
    },
    "geography": {
        "terrain": "Mountains, desert",
        "topography": "Pinal Mountains, Tonto National Forest, Sonoran Desert",
        "elevation": "3,500 feet",
        "climate": "Desert climate with mountain influence, hot summers, mild winters",
        "features": [
            "Pinal Mountains",
            "Tonto National Forest",
            "Historic mining sites",
            "Sonoran Desert",
        ],
        "ecosystem": "Desert with mountain transition zones, Tonto National Forest",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Trails in Tonto National Forest and Pinal Mountains with varied terrain from flowy singletrack to technical challenges",
            "famous_trails": [
                {
                    "name": "Pinal Mountain Trails",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": "Varies (multiple interconnected trails)",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Pinal Mountains within Tonto National Forest. Well-maintained singletrack with scenic mountain and desert views.",
                    "highlights": ["Mountain trails", "Tonto National Forest", "Scenic views", "Technical sections"],
                    "best_seasons": "Year-round (best Fall, Winter, Spring)",
                    "trailhead": "Various access points in Tonto National Forest",
                    "features": ["Mountain trails", "Tonto National Forest", "Scenic", "Technical"],
                    "permits": "Tonto National Forest - no permit required for day use",
                },
                {
                    "name": "Tonto National Forest Trails",
                    "difficulty": "Beginner to Advanced",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Extensive trail network in Tonto National Forest with trails for all skill levels.",
                    "highlights": ["Tonto National Forest", "All skill levels", "Extensive network"],
                    "best_seasons": "Year-round (best Fall, Winter, Spring)",
                    "trailhead": "Various access points in Tonto National Forest",
                    "features": ["Tonto National Forest", "Varied difficulty", "Extensive"],
                    "permits": "Tonto National Forest - no permit required for day use",
                },
            ],
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Year-round (best Fall, Winter, Spring) - avoid summer heat",
            "trail_conditions": "Generally well-maintained, can be dusty in summer",
            "trail_features": ["Single track", "Mountain trails", "Tonto National Forest", "Technical sections"],
        },
        "hiking": {
            "description": "Trails in Tonto National Forest and Pinal Mountains with scenic mountain and desert views",
            "famous_trails": [
                {
                    "name": "Pinal Mountain Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Pinal Mountains within Tonto National Forest. Scenic mountain and desert views.",
                    "highlights": ["Mountain trails", "Tonto National Forest", "Scenic views"],
                    "best_seasons": "Year-round (best Fall, Winter, Spring)",
                    "trailhead": "Various access points in Tonto National Forest",
                    "features": ["Mountain trails", "Tonto National Forest", "Scenic"],
                    "permits": "Tonto National Forest - no permit required for day use",
                },
            ],
            "difficulty_range": "Easy to moderate",
            "best_seasons": "Year-round (best Fall, Winter, Spring) - avoid summer heat",
            "trail_features": ["Mountain trails", "Tonto National Forest", "Scenic views"],
        },
        "photography": {
            "description": "Historic mining sites, Pinal Mountains, Tonto National Forest, desert landscapes offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Historic Mining Sites",
                    "best_time": "Daylight hours, golden hour for architecture",
                    "subjects": "Historic mining structures, mining history",
                },
                {
                    "name": "Pinal Mountains",
                    "best_time": "Sunrise and sunset for mountain views",
                    "subjects": "Mountain peaks, scenic overlooks, desert-mountain transition",
                },
                {
                    "name": "Tonto National Forest",
                    "best_time": "Daylight hours for forest scenes",
                    "subjects": "Forest scenery, mountain backdrops",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring wildflowers, fall colors, winter clarity",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Pinal Mountains",
                "type": "Mountain Range",
                "description": "Scenic mountain range within Tonto National Forest",
                "activities": ["Hiking", "Mountain biking", "Photography", "Camping"],
            },
            {
                "name": "Tonto National Forest",
                "type": "National Forest",
                "description": "3 million acres of forest with extensive trail networks",
                "activities": ["All outdoor activities"],
            },
        ],
        "cultural": [
            {
                "name": "Historic Downtown Globe",
                "type": "Historic District",
                "description": "Preserved historic mining town architecture",
                "highlights": ["Historic architecture", "Mining history", "Historic charm"],
            },
            {
                "name": "Historic Mining Sites",
                "type": "Historic Sites",
                "description": "Historic copper mining operations and structures",
                "highlights": ["Mining history", "Historic structures"],
            },
        ],
        "nearby": [
            {
                "name": "Payson",
                "distance": "50 miles",
                "description": "Mogollon Rim, Tonto National Forest, mountain recreation",
            },
            {
                "name": "Phoenix",
                "distance": "90 miles",
                "description": "Major city, gateway",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Globe/Miami offer several local dining options - use tools to find current restaurants",
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
        "parking": "Available in downtown and at trailheads. Tonto National Forest trailheads have parking",
        "permits": "Tonto National Forest - no permit required for day use. Most trails require no permits",
        "best_times": "Year-round - hot in summer. Fall (September-November) and Spring (March-May) are ideal",
        "weather": {
            "summer": "Hot (85-100°F), avoid midday heat for outdoor activities",
            "winter": "Mild (50-70°F), excellent for outdoor activities",
            "spring": "Pleasant (65-85°F), ideal for all activities",
            "fall": "Pleasant (65-85°F), ideal for all activities",
        },
        "access": "Highway 60 from Phoenix (90 miles) or Payson (50 miles)",
        "considerations": [
            "Hot in summer - plan activities for early morning or evening",
            "Tonto National Forest offers extensive trail networks",
            "Historic mining towns - explore historic downtown Globe",
            "Gateway to Payson (50 miles) and Phoenix (90 miles)",
        ],
    },
}


class GlobeMiamiAgent(LocationAgentBase):
    """Agent specialized in Globe/Miami, Arizona information and context.

    This agent enhances existing agent outputs with Globe/Miami-specific knowledge
    about Tonto National Forest, Pinal Mountains, historic mining, and outdoor opportunities.
    """

    LOCATION_NAME = "Globe/Miami, Arizona"
    LOCATION_INDICATORS = [
        "globe",
        "globe, az",
        "globe, arizona",
        "globe az",
        "miami",
        "miami, az",
        "miami, arizona",
        "miami az",
        "globe/miami",
        "pinal mountains",
    ]
    AGENT_NAME = "globe_miami_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Globe/Miami-specific knowledge base (fallback if external file not found)."""
        return GLOBE_MIAMI_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Globe/Miami agent."""
        return """You are a comprehensive guide for Globe/Miami, Arizona - "Historic Mining Towns"
located at 3,500 feet elevation, known for Tonto National Forest, Pinal Mountains, historic mining, and outdoor recreation.

Your role is to:
1. Use tools to gather real-time data about Globe/Miami (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Globe/Miami-specific knowledge from the knowledge base
4. Combine information from existing agents with Globe/Miami expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Globe, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Globe, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Globe, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Tonto National Forest - no permit required for day use)
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

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Globe, Arizona"
- Globe/Miami has trails in Tonto National Forest and Pinal Mountains (beginner to advanced)
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- Mention seasonal considerations (extreme heat in summer - ride early morning or evening)

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Globe, Arizona"
- Popular trails include Pinal Mountain trails and Tonto National Forest trails
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention seasonal considerations (extreme heat in summer - hike early morning or evening)

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Key sites: Historic Downtown Globe (preserved mining town architecture), Historic Mining Sites (copper mining history)
- Enhance with knowledge base information about Globe/Miami's mining history
- Provide context about historic mining towns and Tonto National Forest gateway

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Historic Mining Sites (daylight/golden hour), Pinal Mountains (sunrise/sunset), Tonto National Forest (daylight)
- Mention seasonal opportunities (spring wildflowers, fall colors, winter clarity)

For Dining Queries:
- Use find_restaurants with location="Globe, Arizona"
- Provide context about historic mining towns

For Accommodation Queries:
- Use search_accommodations with location="Globe, Arizona"
- Mention proximity to Tonto National Forest

For Logistics Queries:
- Use get_parking_information (Tonto National Forest trailheads have parking)
- Provide information about permits (Tonto National Forest - no permit required for day use, most trails require no permits)
- Mention Highway 60 access from Phoenix (90 miles) and Payson (50 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Globe/Miami, Arizona",
  "overview": "Brief overview of Globe/Miami as historic mining towns and Tonto National Forest gateway",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
    "mountain_biking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
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

GLOBE/MIAMI'S UNIQUE CHARACTERISTICS:
- Historic mining towns - major copper mining district from late 1800s
- Tonto National Forest gateway - 3 million acres of forest with extensive trail networks
- Pinal Mountains - scenic mountain range within Tonto National Forest
- Historic Downtown Globe - preserved mining town architecture
- Elevation: 3,500 feet
- ~7,500 residents (Globe), ~1,800 residents (Miami)
- Gateway to Payson (50 miles) and Phoenix (90 miles)

KEY ATTRACTIONS:
- Tonto National Forest: 3 million acres of forest with extensive trail networks
- Pinal Mountains: Scenic mountain range within Tonto National Forest
- Historic Downtown Globe: Preserved historic mining town architecture
- Historic Mining Sites: Historic copper mining operations and structures

FAMOUS ACTIVITIES:
- Mountain biking in Tonto National Forest and Pinal Mountains (beginner to advanced)
- Hiking in Tonto National Forest and Pinal Mountains (easy to moderate)
- Historic mining town exploration (Historic Downtown Globe, Historic Mining Sites)
- Photography (historic mining sites, Pinal Mountains, Tonto National Forest)

PRACTICAL INFORMATION:
- Parking: Available in downtown and at trailheads. Tonto National Forest trailheads have parking
- Permits: Tonto National Forest - no permit required for day use. Most trails require no permits
- Best Times: Year-round - hot in summer. Fall (September-November) and Spring (March-May) are ideal
- Weather: Desert climate with mountain influence. Summer: 85-100°F (avoid midday heat for outdoor activities). Winter: 50-70°F (excellent for outdoor). Spring/Fall: 65-85°F (ideal)
- Access: Highway 60 from Phoenix (90 miles) or Payson (50 miles)
- Considerations: Hot in summer - plan activities for early morning or evening. Tonto National Forest offers extensive trail networks. Historic mining towns - explore historic downtown Globe. Gateway to Payson (50 miles) and Phoenix (90 miles)

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Globe/Miami's historic mining character and Tonto National Forest gateway location
- Mention Tonto National Forest as major recreation destination
- Highlight Pinal Mountains recreation opportunities
- Emphasize year-round accessibility with summer heat considerations
- Provide practical tips about parking, permits, best times, access, and historic mining town exploration

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Globe/Miami-specific knowledge and context
- Enhanced recommendations based on Globe/Miami's unique historic mining and Tonto National Forest gateway character
- Practical tips for visitors"""

