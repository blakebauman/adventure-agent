"""Williams, Arizona specialist agent.

This agent provides Williams-specific information and enhances existing agent outputs
with local knowledge about Route 66, Grand Canyon gateway, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Williams-specific knowledge base
WILLIAMS_KNOWLEDGE = {
    "location": {
        "name": "Williams, Arizona",
        "coordinates": {"lat": 35.2492, "lon": -112.1910},
        "elevation": 6800,  # feet
        "region": "Coconino County, Arizona",
        "country": "US",
        "nickname": "Gateway to the Grand Canyon",
        "proximity": {
            "grand_canyon": {"distance_miles": 60, "direction": "north"},
            "flagstaff": {"distance_miles": 35, "direction": "east"},
            "sedona": {"distance_miles": 65, "direction": "southeast"},
            "phoenix": {"distance_miles": 180, "direction": "south"},
        },
    },
    "history": {
        "founded": 1881,
        "incorporated": 1901,
        "current_population": "~3,200 residents",
        "known_for": [
            "Gateway to Grand Canyon",
            "Route 66",
            "Grand Canyon Railway",
            "Historic downtown",
            "Mountain biking",
        ],
    },
    "geography": {
        "terrain": "Mountainous, pine forests",
        "topography": "Kaibab National Forest",
        "elevation": "6,800 feet",
        "climate": "Four distinct seasons, snow in winter",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Trails in Kaibab National Forest with varied terrain from flowy singletrack to technical challenges",
            "famous_trails": [
                {
                    "name": "Bill Williams Mountain Trail",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": 6.0,
                    "elevation_gain_feet": 1800,
                    "description": "Challenging trail to Bill Williams Mountain summit with significant elevation gain, technical sections, and scenic forest views.",
                    "highlights": ["Summit views", "Challenging", "Scenic forest", "Technical sections"],
                    "best_seasons": "Spring, Summer, Fall (snow in winter)",
                    "trailhead": "Bill Williams Mountain Trailhead",
                    "features": ["Summit trail", "Technical", "Challenging", "Scenic"],
                    "permits": "Kaibab National Forest - no permit required for day use",
                },
                {
                    "name": "Arizona Trail Segments",
                    "difficulty": "Varies",
                    "length_miles": "Varies by segment",
                    "elevation_gain_feet": "Varies",
                    "description": "Segments of the Arizona Trail pass through Williams area, offering long-distance trail opportunities.",
                    "highlights": ["Long-distance trail", "Arizona Trail", "Varied difficulty"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Various access points",
                    "features": ["Long-distance", "Varied difficulty"],
                    "permits": "Kaibab National Forest - no permit required for day use",
                },
            ],
            "trail_networks": "Trails in Kaibab National Forest",
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Spring, Summer, Fall (snow in winter)",
            "trail_features": ["Single track", "Forest scenery", "Mountain views"],
        },
        "hiking": {
            "description": "Access to Kaibab National Forest and nearby areas with scenic mountain and forest trails",
            "famous_trails": [
                {
                    "name": "Bill Williams Mountain Trail",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": 6.0,
                    "elevation_gain_feet": 1800,
                    "description": "Challenging trail to Bill Williams Mountain summit with significant elevation gain and scenic forest views.",
                    "highlights": ["Summit views", "Challenging", "Scenic forest", "Moderate to strenuous"],
                    "best_seasons": "Spring, Summer, Fall (snow in winter)",
                    "trailhead": "Bill Williams Mountain Trailhead",
                    "features": ["Summit hike", "Challenging", "Scenic"],
                    "permits": "Kaibab National Forest - no permit required",
                },
                {
                    "name": "Arizona Trail Segments",
                    "difficulty": "Varies",
                    "length_miles": "Varies by segment",
                    "elevation_gain_feet": "Varies",
                    "description": "Segments of the Arizona Trail pass through Williams area, offering long-distance hiking opportunities.",
                    "highlights": ["Long-distance trail", "Arizona Trail", "Varied difficulty"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Various access points",
                    "features": ["Long-distance", "Varied difficulty"],
                    "permits": "Kaibab National Forest - no permit required",
                },
            ],
            "trail_networks": "Trails in Kaibab National Forest",
            "difficulty_range": "Easy to strenuous",
            "best_seasons": "Spring, Summer, Fall (snow in winter)",
            "trail_features": ["Forest trails", "Mountain peaks", "Scenic views"],
        },
        "climbing": {
            "description": "Limited climbing opportunities in Williams area",
            "note": "Williams is not a major climbing destination. For extensive climbing, consider nearby areas or use tools to find current climbing opportunities.",
        },
        "cycling": {
            "description": "Road cycling opportunities with scenic routes through pine forests",
            "routes": [
                {
                    "name": "Williams Area Roads",
                    "type": "Road",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Scenic road routes through Kaibab National Forest with forest and mountain views.",
                    "highlights": ["Forest scenery", "Mountain views", "Scenic"],
                    "best_seasons": "Spring, Summer, Fall",
                    "difficulty": "Varies",
                },
            ],
            "best_seasons": "Spring, Summer, Fall (avoid winter snow)",
        },
        "paddling": {
            "description": "Limited paddling opportunities in Williams area",
            "note": "Williams is not a major paddling destination. For extensive paddling, consider nearby lakes or use tools to find current opportunities.",
        },
        "photography": {
            "description": "Route 66, historic downtown, mountain views",
            "best_spots": [
                "Historic Route 66",
                "Downtown Williams",
                "Bill Williams Mountain",
            ],
        },
    },
    "attractions": {
        "natural": [
            "Kaibab National Forest",
            "Bill Williams Mountain",
        ],
        "cultural": [
            "Historic Route 66",
            "Grand Canyon Railway",
            "Bearizona Wildlife Park",
            "Williams Depot",
        ],
        "nearby": [
            "Grand Canyon National Park (60 miles)",
            "Flagstaff (35 miles)",
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Red Raven Restaurant",
                "type": "American",
                "description": "Local favorite on Route 66",
            },
            {
                "name": "Cruisers Cafe 66",
                "type": "Casual",
                "description": "Route 66 themed restaurant",
            },
        ],
        "accommodations": [
            {
                "name": "Grand Canyon Railway Hotel",
                "type": "Hotel",
                "description": "Historic hotel connected to railway",
            },
            {
                "name": "The Lodge on Route 66",
                "type": "Lodge",
                "description": "Route 66 themed lodging",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in downtown and at trailheads",
        "permits": "Kaibab National Forest - some areas may require permits",
        "best_times": "Year-round - four distinct seasons",
        "weather": "Snow in winter, mild summers",
        "access": "I-40 and Route 66",
        "transportation": "Grand Canyon Railway to Grand Canyon",
    },
}


class WilliamsAgent(LocationAgentBase):
    """Agent specialized in Williams, Arizona information and context.

    This agent enhances existing agent outputs with Williams-specific knowledge
    about Route 66, Grand Canyon gateway, and outdoor opportunities.
    """

    LOCATION_NAME = "Williams, Arizona"
    LOCATION_INDICATORS = [
        "williams",
        "williams, az",
        "williams, arizona",
        "williams az",
    ]
    AGENT_NAME = "williams_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Williams-specific knowledge base (fallback if external file not found)."""
        return WILLIAMS_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Williams agent."""
        return """You are a comprehensive guide for Williams, Arizona - the "Gateway to the Grand Canyon"
located on historic Route 66 at 6,800 feet elevation.

Your role is to:
1. Use tools to gather real-time data about Williams (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Williams-specific knowledge from the knowledge base
4. Combine information from existing agents with Williams expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Williams, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Williams, Arizona")
- For climbing: search_trails(activity_type="climbing", location="Williams, Arizona") if available
- For cycling: search_trails(activity_type="cycling", location="Williams, Arizona")
- For paddling: search_trails(activity_type="paddling", location="Williams, Arizona") if available
- For trail running: search_trails(activity_type="trail_running", location="Williams, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Kaibab National Forest - most trails require no permits)
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
- Safety considerations (weather, elevation, snow in winter)
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Williams, Arizona"
- Williams has trails including Bill Williams Mountain Trail (6 miles, intermediate/advanced) and Arizona Trail segments
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- Mention seasonal considerations (snow in winter)

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Williams, Arizona"
- Popular trails include Bill Williams Mountain Trail (6 miles, moderate/strenuous) and Arizona Trail segments
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention seasonal considerations (snow in winter)

For Dining Queries:
- Use find_restaurants with location="Williams, Arizona"
- Enhance results with knowledge base businesses (Red Raven Restaurant, Cruisers Cafe 66)
- Provide context about Route 66 theme

For Accommodation Queries:
- Use search_accommodations with location="Williams, Arizona"
- Enhance with knowledge base information (Grand Canyon Railway Hotel, The Lodge on Route 66)
- Mention proximity to Grand Canyon and Route 66 theme

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Historic Route 66, Downtown Williams, Bill Williams Mountain
- Mention seasonal opportunities

For Logistics Queries:
- Use get_parking_information for trailhead parking
- Provide information about permits (Kaibab National Forest - most trails require no permits)
- Mention I-40 and Route 66 access
- Grand Canyon Railway offers scenic train to Grand Canyon

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

Williams' Highlights:
- Gateway to Grand Canyon (60 miles north)
- Historic Route 66
- Grand Canyon Railway (scenic train to Grand Canyon)
- Kaibab National Forest access
- Mountain biking trails
- Historic downtown
- ~3,200 residents

Key Attractions:
- Historic Route 66
- Grand Canyon Railway
- Bearizona Wildlife Park
- Kaibab National Forest
- Bill Williams Mountain

FAMOUS TRAILS:
- Mountain Biking: Bill Williams Mountain Trail (6 miles, intermediate/advanced), Arizona Trail segments
- Hiking: Bill Williams Mountain Trail (6 miles, moderate/strenuous), Arizona Trail segments

PRACTICAL INFORMATION:
- Four distinct seasons - snow in winter (December-April)
- Year-round outdoor recreation (best Spring, Summer, Fall)
- Easy access via I-40 and Route 66
- Grand Canyon Railway offers scenic train to Grand Canyon (60 miles north)
- Gateway to Grand Canyon and Flagstaff
- Elevation 6,800 feet
- Kaibab National Forest - most trails require no permits for day use

ENHANCEMENT GUIDELINES:
- Always combine tool results with knowledge base information
- Provide specific recommendations based on activity type and season
- Include safety considerations (weather, elevation, snow in winter)
- Highlight unique characteristics (Gateway to Grand Canyon, Route 66, Grand Canyon Railway)
- Provide practical tips (parking, permits, best times, access, Grand Canyon Railway)

Provide comprehensive, accurate, practical information that combines real tool data with Williams-specific knowledge and context."""

