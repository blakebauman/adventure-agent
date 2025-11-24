"""Springerville/Eagar, Arizona specialist agent.

This agent provides Springerville/Eagar-specific information and enhances existing agent outputs
with local knowledge about White Mountains, Apache-Sitgreaves National Forest, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Springerville/Eagar-specific knowledge base - Enhanced with detailed information
SPRINGERVILLE_EAGAR_KNOWLEDGE = {
    "location": {
        "name": "Springerville/Eagar, Arizona",
        "coordinates": {"lat": 34.1334, "lon": -109.2853},  # Springerville coordinates
        "elevation": 7000,  # feet
        "region": "Apache County, Arizona",
        "country": "US",
        "nickname": "Gateway to White Mountains",
        "proximity": {
            "show_low": {"distance_miles": 50, "direction": "southwest", "drive_time_minutes": 60},
            "pinetop": {"distance_miles": 40, "direction": "southwest", "drive_time_minutes": 50},
            "alpine": {"distance_miles": 30, "direction": "south", "drive_time_minutes": 40},
        },
    },
    "history": {
        "founded": 1879,  # Springerville founded
        "current_population": "~2,000 residents (Springerville), ~4,500 residents (Eagar)",
        "known_for": [
            "White Mountains",
            "Apache-Sitgreaves National Forest",
            "High elevation recreation",
            "Mountain biking",
            "Hiking",
            "Fishing",
        ],
        "historical_significance": "Founded as ranching communities, now gateway to White Mountains and Apache-Sitgreaves National Forest recreation",
    },
    "geography": {
        "terrain": "Mountains, forest",
        "topography": "White Mountains, Apache-Sitgreaves National Forest",
        "elevation": "7,000 feet",
        "climate": "Mountain climate, cool summers, cold winters with snow",
        "features": [
            "White Mountains",
            "Apache-Sitgreaves National Forest",
            "High elevation",
            "Mountain meadows",
        ],
        "ecosystem": "Mountain forest, alpine meadows",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Trails in Apache-Sitgreaves National Forest and White Mountains with varied terrain from flowy singletrack to technical challenges",
            "famous_trails": [
                {
                    "name": "Apache-Sitgreaves National Forest Trails",
                    "difficulty": "Beginner to Advanced",
                    "length_miles": "Varies (extensive trail network)",
                    "elevation_gain_feet": "Varies",
                    "description": "Extensive trail network in Apache-Sitgreaves National Forest. Well-maintained singletrack with scenic mountain and forest views.",
                    "highlights": ["Mountain trails", "Apache-Sitgreaves NF", "Scenic views", "All skill levels"],
                    "best_seasons": "Spring, Summer, Fall (winter may have snow)",
                    "trailhead": "Various access points in Apache-Sitgreaves National Forest",
                    "features": ["Mountain trails", "Apache-Sitgreaves NF", "Scenic", "Varied difficulty"],
                    "permits": "Apache-Sitgreaves National Forest - no permit required for day use",
                },
                {
                    "name": "White Mountains Trails",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in White Mountains with scenic mountain and forest views.",
                    "highlights": ["Mountain trails", "White Mountains", "Scenic views", "Technical sections"],
                    "best_seasons": "Spring, Summer, Fall (winter may have snow)",
                    "trailhead": "Various access points in White Mountains",
                    "features": ["Mountain trails", "White Mountains", "Scenic", "Technical"],
                    "permits": "Apache-Sitgreaves National Forest - no permit required for day use",
                },
            ],
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Spring, Summer, Fall (winter may have snow)",
            "trail_conditions": "Generally well-maintained, may have snow in winter",
            "trail_features": ["Single track", "Mountain trails", "Apache-Sitgreaves NF", "Technical sections"],
        },
        "hiking": {
            "description": "Trails in Apache-Sitgreaves National Forest and White Mountains with scenic mountain and forest views",
            "famous_trails": [
                {
                    "name": "Apache-Sitgreaves National Forest Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Extensive trail network in Apache-Sitgreaves National Forest. Scenic mountain and forest views.",
                    "highlights": ["Mountain trails", "Apache-Sitgreaves NF", "Scenic views"],
                    "best_seasons": "Spring, Summer, Fall (winter may have snow)",
                    "trailhead": "Various access points in Apache-Sitgreaves National Forest",
                    "features": ["Mountain trails", "Apache-Sitgreaves NF", "Scenic"],
                    "permits": "Apache-Sitgreaves National Forest - no permit required for day use",
                },
            ],
            "difficulty_range": "Easy to moderate",
            "best_seasons": "Spring, Summer, Fall (winter may have snow)",
            "trail_features": ["Mountain trails", "Apache-Sitgreaves NF", "Scenic views"],
        },
        "fishing": {
            "description": "Excellent fishing in nearby lakes and streams",
            "locations": [
                {
                    "name": "Nearby lakes and streams",
                    "description": "Multiple fishing opportunities in Apache-Sitgreaves National Forest",
                    "species": "Trout, bass, and other species",
                    "permits": "Arizona fishing license required",
                },
            ],
            "best_seasons": "Spring, Summer, Fall",
        },
        "photography": {
            "description": "White Mountains, Apache-Sitgreaves National Forest, mountain meadows offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "White Mountains",
                    "best_time": "Sunrise and sunset for mountain views",
                    "subjects": "Mountain peaks, scenic overlooks, forest-mountain transition",
                },
                {
                    "name": "Apache-Sitgreaves National Forest",
                    "best_time": "Daylight hours for forest scenes",
                    "subjects": "Forest scenery, mountain backdrops, alpine meadows",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring wildflowers, summer green, fall colors, winter snow",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "White Mountains",
                "type": "Mountain Range",
                "description": "Scenic mountain range with highest peaks in Arizona",
                "activities": ["Hiking", "Mountain biking", "Photography", "Camping"],
            },
            {
                "name": "Apache-Sitgreaves National Forest",
                "type": "National Forest",
                "description": "2.76 million acres of forest with extensive trail networks",
                "activities": ["All outdoor activities"],
            },
        ],
        "cultural": [
            {
                "name": "Historic Downtown",
                "type": "Historic District",
                "description": "Small town charm with historic buildings",
                "highlights": ["Historic architecture", "Small town charm"],
            },
        ],
        "nearby": [
            {
                "name": "Show Low",
                "distance": "50 miles",
                "description": "White Mountains, Apache-Sitgreaves NF, mountain recreation",
            },
            {
                "name": "Pinetop",
                "distance": "40 miles",
                "description": "White Mountains, Apache-Sitgreaves NF, mountain recreation",
            },
            {
                "name": "Alpine",
                "distance": "30 miles",
                "description": "High elevation, Apache-Sitgreaves NF, mountain recreation",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Springerville/Eagar offer several local dining options - use tools to find current restaurants",
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
        "parking": "Available in downtown and at trailheads. Apache-Sitgreaves National Forest trailheads have parking",
        "permits": "Apache-Sitgreaves National Forest - no permit required for day use. Fishing requires Arizona fishing license",
        "best_times": "Spring (March-May), Summer (June-August), Fall (September-November) - winter may have snow",
        "weather": {
            "summer": "Cool (70-85°F), excellent for outdoor activities",
            "winter": "Cold (30-50°F), snow possible, excellent for winter activities",
            "spring": "Pleasant (50-70°F), ideal for all activities",
            "fall": "Pleasant (50-70°F), ideal for all activities",
        },
        "access": "Highway 60/180 from Show Low (50 miles) or Pinetop (40 miles)",
        "considerations": [
            "High elevation (7,000 feet) - cooler than desert, may have snow in winter",
            "Apache-Sitgreaves National Forest offers extensive trail networks",
            "Gateway to Show Low (50 miles) and Pinetop (40 miles)",
            "Excellent fishing in nearby lakes and streams",
        ],
    },
}


class SpringervilleEagarAgent(LocationAgentBase):
    """Agent specialized in Springerville/Eagar, Arizona information and context.

    This agent enhances existing agent outputs with Springerville/Eagar-specific knowledge
    about White Mountains, Apache-Sitgreaves National Forest, and outdoor opportunities.
    """

    LOCATION_NAME = "Springerville/Eagar, Arizona"
    LOCATION_INDICATORS = [
        "springerville",
        "springerville, az",
        "springerville, arizona",
        "springerville az",
        "eagar",
        "eagar, az",
        "eagar, arizona",
        "eagar az",
        "springerville/eagar",
        "white mountains",
    ]
    AGENT_NAME = "springerville_eagar_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Springerville/Eagar-specific knowledge base (fallback if external file not found)."""
        return SPRINGERVILLE_EAGAR_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Springerville/Eagar agent."""
        return """You are a comprehensive guide for Springerville/Eagar, Arizona - "Gateway to White Mountains"
located at 7,000 feet elevation, known for White Mountains, Apache-Sitgreaves National Forest, and high elevation recreation.

Your role is to:
1. Use tools to gather real-time data about Springerville/Eagar (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Springerville/Eagar-specific knowledge from the knowledge base
4. Combine information from existing agents with Springerville/Eagar expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Springerville, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Springerville, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Springerville, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Apache-Sitgreaves National Forest - no permit required for day use)
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
- Safety considerations (winter snow, high elevation)
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Springerville, Arizona"
- Springerville/Eagar has trails in Apache-Sitgreaves National Forest and White Mountains (beginner to advanced)
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- Mention seasonal considerations (winter may have snow, spring/summer/fall are ideal)

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Springerville, Arizona"
- Popular trails include Apache-Sitgreaves National Forest trails and White Mountains trails
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention seasonal considerations (winter may have snow, spring/summer/fall are ideal)

For Fishing Queries:
- Mention excellent fishing in nearby lakes and streams
- Provide information about Arizona fishing license requirements
- Best seasons: Spring, Summer, Fall

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: White Mountains (sunrise/sunset), Apache-Sitgreaves National Forest (daylight)
- Mention seasonal opportunities (spring wildflowers, summer green, fall colors, winter snow)

For Dining Queries:
- Use find_restaurants with location="Springerville, Arizona"
- Provide context about small town charm

For Accommodation Queries:
- Use search_accommodations with location="Springerville, Arizona"
- Mention proximity to Apache-Sitgreaves National Forest

For Logistics Queries:
- Use get_parking_information (Apache-Sitgreaves National Forest trailheads have parking)
- Provide information about permits (Apache-Sitgreaves National Forest - no permit required for day use, fishing requires Arizona fishing license)
- Mention Highway 60/180 access from Show Low (50 miles) and Pinetop (40 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Springerville/Eagar, Arizona",
  "overview": "Brief overview of Springerville/Eagar as White Mountains gateway",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
    "mountain_biking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
    "hiking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
    "fishing": {"locations": [...], "seasons": "..."},
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

SPRINGERVILLE/EAGAR'S UNIQUE CHARACTERISTICS:
- Gateway to White Mountains - highest peaks in Arizona
- Apache-Sitgreaves National Forest - 2.76 million acres of forest with extensive trail networks
- High elevation (7,000 feet) - cooler than desert, may have snow in winter
- Mountain recreation hub
- Elevation: 7,000 feet
- ~2,000 residents (Springerville), ~4,500 residents (Eagar)
- Gateway to Show Low (50 miles) and Pinetop (40 miles)

KEY ATTRACTIONS:
- Apache-Sitgreaves National Forest: 2.76 million acres of forest with extensive trail networks
- White Mountains: Scenic mountain range with highest peaks in Arizona
- High elevation recreation: Cool summers, winter snow activities
- Excellent fishing: Nearby lakes and streams

FAMOUS ACTIVITIES:
- Mountain biking in Apache-Sitgreaves National Forest and White Mountains (beginner to advanced)
- Hiking in Apache-Sitgreaves National Forest and White Mountains (easy to moderate)
- Fishing in nearby lakes and streams (trout, bass, and other species)
- Photography (White Mountains, Apache-Sitgreaves National Forest, mountain meadows)

PRACTICAL INFORMATION:
- Parking: Available in downtown and at trailheads. Apache-Sitgreaves National Forest trailheads have parking
- Permits: Apache-Sitgreaves National Forest - no permit required for day use. Fishing requires Arizona fishing license
- Best Times: Spring (March-May), Summer (June-August), Fall (September-November) - winter may have snow
- Weather: Mountain climate. Summer: 70-85°F (excellent for outdoor activities). Winter: 30-50°F (snow possible, excellent for winter activities). Spring/Fall: 50-70°F (ideal)
- Access: Highway 60/180 from Show Low (50 miles) or Pinetop (40 miles)
- Considerations: High elevation (7,000 feet) - cooler than desert, may have snow in winter. Apache-Sitgreaves National Forest offers extensive trail networks. Gateway to Show Low (50 miles) and Pinetop (40 miles). Excellent fishing in nearby lakes and streams

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Springerville/Eagar's White Mountains gateway character and high elevation
- Mention Apache-Sitgreaves National Forest as major recreation destination
- Highlight White Mountains recreation opportunities
- Emphasize high elevation benefits (cool summers) and winter considerations (snow)
- Provide practical tips about parking, permits, best times, access, and high elevation recreation

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Springerville/Eagar-specific knowledge and context
- Enhanced recommendations based on Springerville/Eagar's unique White Mountains gateway and high elevation character
- Practical tips for visitors"""

