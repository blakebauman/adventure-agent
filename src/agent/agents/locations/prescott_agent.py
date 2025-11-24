"""Prescott, Arizona specialist agent.

This agent provides Prescott-specific information and enhances existing agent outputs
with local knowledge about Prescott's history, trails, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Prescott-specific knowledge base
PRESCOTT_KNOWLEDGE = {
    "location": {
        "name": "Prescott, Arizona",
        "coordinates": {"lat": 34.5400, "lon": -112.4685},
        "elevation": 5370,  # feet
        "region": "Yavapai County, Arizona",
        "country": "US",
        "nickname": "Everybody's Hometown",
        "proximity": {
            "jerome": {"distance_miles": 45, "direction": "northeast"},
            "sedona": {"distance_miles": 60, "direction": "northeast"},
            "flagstaff": {"distance_miles": 95, "direction": "north"},
            "phoenix": {"distance_miles": 100, "direction": "south"},
        },
    },
    "history": {
        "founded": 1864,
        "territorial_capital": "First territorial capital of Arizona (1864-1867, 1877-1889)",
        "current_population": "~45,000 residents",
        "known_for": [
            "Historic territorial capital",
            "Whiskey Row",
            "Prescott National Forest",
            "Mountain biking and hiking",
            "Rodeo and Western heritage",
            "Four distinct seasons",
        ],
    },
    "geography": {
        "terrain": "Mountainous, pine forests",
        "topography": "Bradshaw Mountains, Granite Dells",
        "elevation": "5,370 feet - mile-high city",
        "climate": "Four distinct seasons, mild summers, snow in winter",
        "lakes": [
            "Watson Lake",
            "Goldwater Lake",
            "Lynx Lake",
        ],
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Extensive trail network in Prescott National Forest with varied terrain from flowy singletrack to technical challenges",
            "famous_trails": [
                {
                    "name": "Groom Creek Loop",
                    "difficulty": "Intermediate",
                    "length_miles": 12.0,
                    "elevation_gain_feet": 1500,
                    "description": "Popular intermediate trail loop with good flow, moderate technical sections, and scenic forest views. One of Prescott's most popular MTB trails.",
                    "highlights": ["Good flow", "Moderate technical", "Scenic forest", "Popular", "Loop trail"],
                    "best_seasons": "Year-round (best Spring, Summer, Fall)",
                    "trailhead": "Groom Creek Trailhead",
                    "features": ["Single track", "Flow", "Moderate technical", "Scenic"],
                    "permits": "Prescott National Forest - no permit required for day use",
                },
                {
                    "name": "Spence Basin",
                    "difficulty": "Beginner to Intermediate",
                    "length_miles": "8+ miles of interconnected trails",
                    "elevation_gain_feet": "Varies by route",
                    "description": "Extensive trail system with trails for all skill levels. Well-maintained singletrack with good flow and scenic forest views.",
                    "highlights": ["Trail system", "All skill levels", "Well-maintained", "Good flow", "Scenic"],
                    "best_seasons": "Year-round",
                    "trailhead": "Spence Basin Trailhead",
                    "features": ["Trail system", "Varied difficulty", "Flow", "Scenic"],
                    "permits": "Prescott National Forest - no permit required",
                },
                {
                    "name": "Thumb Butte Trail",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": 4.0,
                    "elevation_gain_feet": 1000,
                    "description": "Challenging trail to Thumb Butte with technical sections, significant elevation gain, and scenic views. Popular with intermediate to advanced riders.",
                    "highlights": ["Technical sections", "Challenging", "Scenic views", "Popular", "Intermediate to advanced"],
                    "best_seasons": "Year-round",
                    "trailhead": "Thumb Butte Trailhead",
                    "features": ["Technical", "Challenging", "Scenic"],
                    "permits": "Prescott National Forest - no permit required",
                },
                {
                    "name": "Copper Basin Loop",
                    "difficulty": "Advanced",
                    "length_miles": 15.0,
                    "elevation_gain_feet": 2500,
                    "description": "Challenging advanced trail loop with significant elevation gain, technical sections, and scenic mountain views. For experienced riders only.",
                    "highlights": ["Challenging", "Technical", "Significant elevation", "Advanced", "Scenic"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Copper Basin Trailhead",
                    "features": ["Technical", "Challenging", "Advanced", "Scenic"],
                    "permits": "Prescott National Forest - no permit required",
                    "warnings": ["Advanced only", "Strenuous", "Significant elevation gain"],
                },
            ],
            "trail_networks": "Extensive interconnected trail systems in Prescott National Forest",
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Year-round (cooler in summer than Phoenix, snow possible in winter)",
            "trail_conditions": "Generally well-maintained, can be muddy in spring, snow-covered in winter",
            "trail_features": ["Single track", "Technical sections", "Flow trails", "Forest scenery", "Mountain views"],
        },
        "hiking": {
            "description": "Hundreds of miles of trails in Prescott National Forest with varied terrain from easy lake loops to challenging mountain summits",
            "famous_trails": [
                {
                    "name": "Granite Mountain Trail",
                    "difficulty": "Strenuous",
                    "length_miles": 8.0,
                    "elevation_gain_feet": 2000,
                    "description": "Challenging strenuous trail to Granite Mountain summit with significant elevation gain, technical sections, and spectacular 360-degree views. Popular summit hike.",
                    "highlights": [
                        "Summit views",
                        "Spectacular 360-degree views",
                        "Challenging",
                        "Popular",
                        "Strenuous"
                    ],
                    "best_seasons": "Spring, Summer, Fall (snow possible in winter)",
                    "trailhead": "Granite Mountain Trailhead",
                    "features": ["Summit hike", "Challenging", "Scenic views", "Strenuous"],
                    "permits": "Prescott National Forest - no permit required",
                    "warnings": ["Strenuous", "Significant elevation gain", "Check weather"],
                },
                {
                    "name": "Thumb Butte Trail",
                    "difficulty": "Moderate",
                    "length_miles": 4.0,
                    "elevation_gain_feet": 1000,
                    "description": "Popular moderate trail to Thumb Butte summit with good elevation gain, scenic views, and moderate difficulty. Very popular - arrive early.",
                    "highlights": ["Summit views", "Scenic", "Popular", "Moderate difficulty", "Iconic"],
                    "best_seasons": "Year-round",
                    "trailhead": "Thumb Butte Trailhead (limited parking - arrive early)",
                    "features": ["Summit hike", "Moderate", "Scenic", "Popular"],
                    "permits": "Prescott National Forest - no permit required",
                    "warnings": ["Very popular - arrive early", "Limited parking"],
                },
                {
                    "name": "Lynx Lake Loop",
                    "difficulty": "Easy",
                    "length_miles": 2.4,
                    "elevation_gain_feet": 100,
                    "description": "Easy family-friendly loop trail around Lynx Lake with minimal elevation gain, scenic lake views, and easy access. Perfect for families and beginners.",
                    "highlights": ["Family-friendly", "Easy", "Lake views", "Beginner-friendly", "Scenic"],
                    "best_seasons": "Year-round",
                    "trailhead": "Lynx Lake Trailhead",
                    "features": ["Family-friendly", "Easy", "Lake views"],
                    "permits": "Prescott National Forest - no permit required",
                },
                {
                    "name": "Watson Lake Loop",
                    "difficulty": "Easy to Moderate",
                    "length_miles": 4.8,
                    "elevation_gain_feet": 300,
                    "description": "Scenic loop trail around Watson Lake with Granite Dells views, moderate sections, and scenic lake and rock formations. Popular trail.",
                    "highlights": ["Granite Dells views", "Lake views", "Scenic", "Moderate", "Popular"],
                    "best_seasons": "Year-round",
                    "trailhead": "Watson Lake Trailhead",
                    "features": ["Lake views", "Granite Dells", "Scenic", "Moderate"],
                    "permits": "Prescott National Forest - no permit required",
                },
                {
                    "name": "Groom Creek Loop",
                    "difficulty": "Moderate",
                    "length_miles": 12.0,
                    "elevation_gain_feet": 1500,
                    "description": "Moderate loop trail through Groom Creek area with good elevation gain, forest scenery, and moderate difficulty. Popular day hike.",
                    "highlights": ["Loop trail", "Forest scenery", "Moderate difficulty", "Popular", "Good elevation"],
                    "best_seasons": "Year-round",
                    "trailhead": "Groom Creek Trailhead",
                    "features": ["Loop trail", "Moderate", "Forest scenery"],
                    "permits": "Prescott National Forest - no permit required",
                },
            ],
            "trail_networks": "Hundreds of miles of interconnected hiking trails in Prescott National Forest",
            "difficulty_range": "Easy to strenuous",
            "best_seasons": "Year-round (mild summers, snow possible in winter)",
            "trail_features": ["Forest trails", "Mountain peaks", "Lake loops", "Summit hikes", "Scenic views"],
        },
        "climbing": {
            "description": "Limited climbing opportunities in Prescott area, primarily bouldering",
            "areas": [
                {
                    "name": "Granite Dells Bouldering",
                    "type": "Bouldering",
                    "routes": "Various",
                    "difficulty_range": "V0-V8",
                    "description": "Bouldering opportunities in Granite Dells area. Limited developed areas.",
                    "access": "Various locations in Granite Dells, check local guidebooks",
                    "best_seasons": "Spring, Summer, Fall (avoid winter snow)",
                },
            ],
            "note": "Prescott is not a major climbing destination. For extensive climbing, consider nearby areas or use tools to find current climbing opportunities.",
        },
        "cycling": {
            "description": "Road and gravel cycling opportunities with scenic routes through pine forests and mountain terrain",
            "routes": [
                {
                    "name": "Prescott Loop",
                    "type": "Road",
                    "length_miles": 25.0,
                    "elevation_gain_feet": 2000,
                    "description": "Scenic road loop around Prescott with moderate elevation gain and forest/mountain views.",
                    "highlights": ["Forest views", "Moderate difficulty", "Scenic loop", "Mountain views"],
                    "best_seasons": "Year-round (best Spring, Summer, Fall)",
                    "difficulty": "Moderate",
                },
                {
                    "name": "Groom Creek Road",
                    "type": "Road/Gravel",
                    "length_miles": 15.0,
                    "elevation_gain_feet": 1200,
                    "description": "Scenic road/gravel route through Groom Creek area with moderate elevation and forest scenery.",
                    "highlights": ["Forest scenery", "Moderate difficulty", "Scenic"],
                    "best_seasons": "Spring, Summer, Fall",
                    "difficulty": "Moderate",
                },
            ],
            "best_seasons": "Year-round (best Spring, Summer, Fall, avoid winter snow)",
            "trail_features": ["Road routes", "Gravel routes", "Forest scenery", "Varied difficulty"],
        },
        "paddling": {
            "description": "Limited paddling opportunities in Prescott area. Mostly nearby lakes.",
            "routes": [
                {
                    "name": "Watson Lake",
                    "type": "Flatwater",
                    "length_miles": "Varies",
                    "difficulty": "Class I",
                    "description": "Flatwater paddling on Watson Lake with Granite Dells views. Popular for kayaking and paddleboarding.",
                    "put_in": "Watson Lake access points",
                    "take_out": "Same as put-in",
                    "best_seasons": "Year-round (best Spring, Summer, Fall)",
                },
                {
                    "name": "Lynx Lake",
                    "type": "Flatwater",
                    "length_miles": "Varies",
                    "difficulty": "Class I",
                    "description": "Flatwater paddling on Lynx Lake. Popular for kayaking and canoeing.",
                    "put_in": "Lynx Lake access points",
                    "take_out": "Same as put-in",
                    "best_seasons": "Year-round",
                },
            ],
            "best_seasons": "Year-round (best Spring, Summer, Fall)",
        },
        "photography": {
            "description": "Historic architecture, mountain views, Granite Dells",
            "best_spots": [
                "Whiskey Row (historic downtown)",
                "Granite Dells",
                "Watson Lake",
                "Thumb Butte",
                "Prescott Courthouse Plaza",
            ],
        },
    },
    "attractions": {
        "historical": [
            "Whiskey Row (historic saloons)",
            "Prescott Courthouse Plaza",
            "Sharlot Hall Museum",
            "Phippen Museum (Western art)",
            "Smoki Museum (Native American artifacts)",
        ],
        "natural": [
            "Granite Dells",
            "Watson Lake",
            "Goldwater Lake",
            "Lynx Lake",
            "Thumb Butte",
        ],
        "cultural": [
            "World's Oldest Rodeo (since 1888)",
            "Prescott Film Festival",
            "Bluegrass Festival",
            "Folk Arts Fair",
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "The Palace Restaurant",
                "type": "Historic Restaurant",
                "description": "Historic saloon and restaurant on Whiskey Row",
            },
            {
                "name": "El Gato Azul",
                "type": "Mediterranean",
                "description": "Mediterranean cuisine in historic building",
            },
            {
                "name": "Farm Provisions",
                "type": "Farm-to-Table",
                "description": "Local, seasonal cuisine",
            },
        ],
        "shops": [
            {
                "name": "Whiskey Row",
                "type": "Historic District",
                "description": "Historic saloons, shops, and restaurants",
            },
        ],
        "accommodations": [
            {
                "name": "Hassayampa Inn",
                "type": "Historic Hotel",
                "description": "Historic hotel in downtown Prescott",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in downtown and at trailheads",
        "permits": "Prescott National Forest - some areas may require permits",
        "best_times": "Year-round - mild summers, four seasons",
        "weather": "Four distinct seasons, snow in winter, mild summers",
        "access": "Easy access from Phoenix (100 miles) via I-17",
    },
}


class PrescottAgent(LocationAgentBase):
    """Agent specialized in Prescott, Arizona information and context.

    This agent enhances existing agent outputs with Prescott-specific knowledge
    about the historic territorial capital, trails, and outdoor opportunities.
    """

    LOCATION_NAME = "Prescott, Arizona"
    LOCATION_INDICATORS = [
        "prescott",
        "prescott, az",
        "prescott, arizona",
        "prescott az",
    ]
    AGENT_NAME = "prescott_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Prescott-specific knowledge base (fallback if external file not found)."""
        return PRESCOTT_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Prescott agent."""
        return """You are a comprehensive guide for Prescott, Arizona - "Everybody's Hometown"
and the first territorial capital of Arizona.

Your role is to:
1. Use tools to gather real-time data about Prescott (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Prescott-specific knowledge from the knowledge base
4. Combine information from existing agents with Prescott expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Prescott, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Prescott, Arizona")
- For climbing: search_trails(activity_type="climbing", location="Prescott, Arizona") if available
- For cycling: search_trails(activity_type="cycling", location="Prescott, Arizona")
- For paddling: search_trails(activity_type="paddling", location="Prescott, Arizona") if available
- For trail running: search_trails(activity_type="trail_running", location="Prescott, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Prescott National Forest - most trails require no permits)
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
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Prescott, Arizona"
- Prescott has extensive MTB trails including Groom Creek Loop (12 miles, intermediate), Spence Basin (8+ miles, all levels), Thumb Butte Trail (4 miles, intermediate/advanced), and Copper Basin Loop (15 miles, advanced)
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- Mention seasonal considerations (snow in winter, mud in spring)

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Prescott, Arizona"
- Popular trails include Granite Mountain Trail (8 miles, strenuous, summit views), Thumb Butte Trail (4 miles, moderate, very popular), Lynx Lake Loop (2.4 miles, easy, family-friendly), Watson Lake Loop (4.8 miles, easy/moderate, Granite Dells views), and Groom Creek Loop (12 miles, moderate)
- Use find_scenic_viewpoints for Granite Dells and mountain views
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention that Thumb Butte is very popular - arrive early

For Dining Queries:
- Use find_restaurants with location="Prescott, Arizona"
- Enhance results with knowledge base businesses (The Palace Restaurant on Whiskey Row, El Gato Azul, Farm Provisions)
- Provide context about historic Whiskey Row

For Accommodation Queries:
- Use search_accommodations with location="Prescott, Arizona"
- Enhance with knowledge base information (Hassayampa Inn - historic hotel)
- Mention proximity to trails and historic downtown

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Whiskey Row (historic downtown), Granite Dells, Watson Lake, Thumb Butte, Prescott Courthouse Plaza
- Mention seasonal opportunities

For Logistics Queries:
- Use get_parking_information for trailhead parking (limited at popular trails like Thumb Butte - arrive early)
- Provide information about permits (Prescott National Forest - most trails require no permits)
- Mention I-17 access from Phoenix (100 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

Prescott's Highlights:
- First territorial capital of Arizona (1864-1867, 1877-1889)
- Historic Whiskey Row with preserved saloons
- Extensive trail network in Prescott National Forest
- Mountain biking and hiking destination
- Four distinct seasons (mild summers, snow in winter)
- Elevation: 5,370 feet (mile-high city)
- Located in Yavapai County, Arizona
- ~45,000 residents

Key Attractions:
- Whiskey Row (historic saloons)
- Prescott Courthouse Plaza
- Sharlot Hall Museum
- Granite Dells
- Watson Lake
- World's Oldest Rodeo (since 1888)

FAMOUS TRAILS:
- Mountain Biking: Groom Creek Loop (12 miles, intermediate), Spence Basin (8+ miles, all levels), Thumb Butte Trail (4 miles, intermediate/advanced), Copper Basin Loop (15 miles, advanced)
- Hiking: Granite Mountain Trail (8 miles, strenuous, summit views), Thumb Butte Trail (4 miles, moderate, very popular), Lynx Lake Loop (2.4 miles, easy, family-friendly), Watson Lake Loop (4.8 miles, easy/moderate, Granite Dells views), Groom Creek Loop (12 miles, moderate)

PRACTICAL INFORMATION:
- Four distinct seasons - mild summers (cooler than Phoenix), snow in winter
- Year-round outdoor recreation (best Spring, Summer, Fall)
- Easy access from Phoenix (100 miles) via I-17
- Historic downtown with preserved architecture (Whiskey Row)
- Elevation 5,370 feet (mile-high city)
- Prescott National Forest - most trails require no permits for day use

ENHANCEMENT GUIDELINES:
- Always combine tool results with knowledge base information
- Provide specific recommendations based on activity type and season
- Include safety considerations (weather, elevation, snow in winter)
- Mention Thumb Butte as very popular - arrive early for parking
- Highlight unique characteristics (historic territorial capital, Whiskey Row, Granite Dells, four seasons)
- Provide practical tips (parking, permits, best times, access, historic downtown)

Provide comprehensive, accurate, practical information that combines real tool data with Prescott-specific knowledge and context."""

