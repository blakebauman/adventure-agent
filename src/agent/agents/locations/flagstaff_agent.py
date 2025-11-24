"""Flagstaff, Arizona specialist agent.

This agent provides Flagstaff-specific information and enhances existing agent outputs
with local knowledge about Flagstaff's mountain trails, San Francisco Peaks, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Flagstaff-specific knowledge base
FLAGSTAFF_KNOWLEDGE = {
    "location": {
        "name": "Flagstaff, Arizona",
        "coordinates": {"lat": 35.1983, "lon": -111.6513},
        "elevation": 7000,  # feet
        "region": "Coconino County, Arizona",
        "country": "US",
        "nickname": "City of Seven Wonders",
        "proximity": {
            "grand_canyon": {"distance_miles": 80, "direction": "north"},
            "sedona": {"distance_miles": 30, "direction": "south"},
            "prescott": {"distance_miles": 95, "direction": "southwest"},
            "phoenix": {"distance_miles": 145, "direction": "south"},
        },
    },
    "history": {
        "founded": 1876,
        "incorporated": 1928,
        "current_population": "~75,000 residents",
        "known_for": [
            "Gateway to Grand Canyon",
            "San Francisco Peaks (highest point in Arizona)",
            "Route 66",
            "Northern Arizona University",
            "Lowell Observatory",
            "Four distinct seasons",
            "Mountain town atmosphere",
        ],
    },
    "geography": {
        "terrain": "Mountainous, pine forests",
        "topography": "San Francisco Peaks, Coconino National Forest",
        "elevation": "7,000 feet - mile-high city",
        "climate": "Four distinct seasons, snow in winter, mild summers",
        "peaks": [
            "Humphreys Peak (12,633 ft - highest in Arizona)",
            "Agassiz Peak (12,356 ft)",
            "Fremont Peak (11,969 ft)",
        ],
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Extensive trail network in Coconino National Forest with varied terrain from flowy singletrack to technical challenges",
            "famous_trails": [
                {
                    "name": "Schultz Creek Trail",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": 8.0,
                    "elevation_gain_feet": 1200,
                    "description": "Popular intermediate to advanced trail with good flow, technical sections, and scenic forest views. One of Flagstaff's most popular MTB trails.",
                    "highlights": ["Good flow", "Technical sections", "Scenic forest", "Popular", "Intermediate-friendly"],
                    "best_seasons": "Spring (May-June), Summer (July-August), Fall (September-October)",
                    "trailhead": "Schultz Creek Trailhead",
                    "features": ["Single track", "Flow", "Technical", "Scenic"],
                    "permits": "Coconino National Forest - no permit required for day use",
                },
                {
                    "name": "Mount Elden Lookout Trail",
                    "difficulty": "Advanced",
                    "length_miles": 5.5,
                    "elevation_gain_feet": 2300,
                    "description": "Challenging advanced trail to Mount Elden summit with significant elevation gain, technical sections, and spectacular views. Strenuous climb.",
                    "highlights": ["Summit views", "Challenging climb", "Technical", "Spectacular views", "Advanced"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Mount Elden Trailhead",
                    "features": ["Summit trail", "Technical", "Challenging", "Scenic"],
                    "permits": "Coconino National Forest - no permit required",
                    "warnings": ["Strenuous climb", "Advanced only", "Significant elevation gain"],
                },
                {
                    "name": "Fort Valley Trail System",
                    "difficulty": "Beginner to Intermediate",
                    "length_miles": "15+ miles of interconnected trails",
                    "elevation_gain_feet": "Varies by route",
                    "description": "Extensive trail system with trails for all skill levels. Well-maintained singletrack with good flow and scenic forest views.",
                    "highlights": ["Trail system", "All skill levels", "Well-maintained", "Good flow", "Scenic"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Fort Valley Trailhead",
                    "features": ["Trail system", "Varied difficulty", "Flow", "Scenic"],
                    "permits": "Coconino National Forest - no permit required",
                },
                {
                    "name": "Little Elden Trail",
                    "difficulty": "Beginner to Intermediate",
                    "length_miles": 6.0,
                    "elevation_gain_feet": 600,
                    "description": "Beginner-friendly trail with smooth singletrack, gentle elevation, and scenic forest views. Great for families and beginners.",
                    "highlights": ["Beginner-friendly", "Smooth trail", "Family-friendly", "Scenic"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Little Elden Trailhead",
                    "features": ["Beginner-friendly", "Smooth", "Family-friendly"],
                    "permits": "Coconino National Forest - no permit required",
                },
            ],
            "trail_networks": "Extensive interconnected trail systems in Coconino National Forest",
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Spring (May-June), Summer (July-August), Fall (September-October) - snow in winter",
            "trail_conditions": "Generally well-maintained, can be muddy in spring, snow-covered in winter",
            "trail_features": ["Single track", "Technical sections", "Flow trails", "Forest scenery", "Mountain views"],
        },
        "hiking": {
            "description": "Access to San Francisco Peaks (highest point in Arizona), Grand Canyon, and extensive forest trails in Coconino National Forest",
            "famous_trails": [
                {
                    "name": "Humphreys Peak Trail",
                    "difficulty": "Strenuous",
                    "length_miles": 10.0,
                    "elevation_gain_feet": 3300,
                    "description": "Iconic trail to Humphreys Peak, the highest point in Arizona at 12,633 feet. Strenuous hike with significant elevation gain, alpine terrain, and spectacular 360-degree views. Weather can change quickly at elevation.",
                    "highlights": [
                        "Highest point in Arizona (12,633 ft)",
                        "Spectacular 360-degree views",
                        "Alpine terrain",
                        "Iconic hike",
                        "Challenging"
                    ],
                    "best_seasons": "Summer (July-September) - snow-free conditions",
                    "trailhead": "Humphreys Peak Trailhead (Arizona Snowbowl area)",
                    "features": ["Summit hike", "Alpine terrain", "High elevation", "Strenuous"],
                    "permits": "Coconino National Forest - no permit required",
                    "warnings": ["Strenuous", "Weather can change quickly", "High elevation", "Start early", "Check weather"],
                },
                {
                    "name": "Mount Elden Lookout Trail",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": 5.5,
                    "elevation_gain_feet": 2300,
                    "description": "Challenging trail to Mount Elden summit with significant elevation gain, switchbacks, and spectacular views of Flagstaff and surrounding area.",
                    "highlights": ["Summit views", "City views", "Challenging", "Scenic", "Moderate to strenuous"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Mount Elden Trailhead",
                    "features": ["Summit hike", "Challenging", "Scenic views"],
                    "permits": "Coconino National Forest - no permit required",
                    "warnings": ["Strenuous climb", "Significant elevation gain"],
                },
                {
                    "name": "Kachina Trail",
                    "difficulty": "Moderate",
                    "length_miles": 10.0,
                    "elevation_gain_feet": 1500,
                    "description": "Scenic moderate trail through pine forests with good elevation gain, forest scenery, and moderate difficulty. Popular day hike.",
                    "highlights": ["Scenic forest", "Moderate difficulty", "Popular", "Forest scenery"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Kachina Trailhead",
                    "features": ["Forest trail", "Moderate", "Scenic"],
                    "permits": "Coconino National Forest - no permit required",
                },
                {
                    "name": "Weatherford Trail",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": 8.0,
                    "elevation_gain_feet": 2000,
                    "description": "Scenic trail with significant elevation gain, forest scenery, and moderate to strenuous difficulty. Good training for Humphreys Peak.",
                    "highlights": ["Good training", "Significant elevation", "Forest scenery", "Moderate to strenuous"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Weatherford Trailhead",
                    "features": ["Training trail", "Challenging", "Scenic"],
                    "permits": "Coconino National Forest - no permit required",
                },
            ],
            "trail_networks": "Extensive interconnected hiking trail network in Coconino National Forest",
            "difficulty_range": "Easy to strenuous",
            "best_seasons": "Spring (May-June), Summer (July-August), Fall (September-October) - snow in winter",
            "trail_features": ["Mountain peaks", "Forest trails", "Alpine terrain", "Summit hikes", "Scenic views"],
        },
        "climbing": {
            "description": "Limited climbing opportunities in Flagstaff area, primarily bouldering and some sport climbing",
            "areas": [
                {
                    "name": "Flagstaff Area Bouldering",
                    "type": "Bouldering",
                    "routes": "Various",
                    "difficulty_range": "V0-V10",
                    "description": "Various bouldering areas in Flagstaff area with granite boulders. Limited developed areas.",
                    "access": "Various locations, check local guidebooks",
                    "best_seasons": "Spring, Summer, Fall (avoid winter snow)",
                },
            ],
            "note": "Flagstaff is not a major climbing destination. For extensive climbing, consider nearby areas or use tools to find current climbing opportunities.",
        },
        "cycling": {
            "description": "Road and gravel cycling opportunities with scenic routes through pine forests and mountain terrain",
            "routes": [
                {
                    "name": "San Francisco Peaks Scenic Loop",
                    "type": "Road",
                    "length_miles": 45.0,
                    "elevation_gain_feet": 4000,
                    "description": "Challenging road route around San Francisco Peaks with significant elevation gain and spectacular mountain views.",
                    "highlights": ["Mountain views", "Challenging", "Scenic", "Significant elevation"],
                    "best_seasons": "Spring, Summer, Fall",
                    "difficulty": "Challenging",
                },
                {
                    "name": "Fort Valley Road",
                    "type": "Road/Gravel",
                    "length_miles": 20.0,
                    "elevation_gain_feet": 1500,
                    "description": "Scenic road/gravel route through Fort Valley with moderate elevation and forest scenery.",
                    "highlights": ["Forest scenery", "Moderate difficulty", "Scenic"],
                    "best_seasons": "Spring, Summer, Fall",
                    "difficulty": "Moderate",
                },
            ],
            "best_seasons": "Spring, Summer, Fall (avoid winter snow)",
            "trail_features": ["Road routes", "Gravel routes", "Mountain scenery", "Varied difficulty"],
        },
        "paddling": {
            "description": "Limited paddling opportunities in Flagstaff area. Mostly nearby lakes and reservoirs.",
            "routes": [
                {
                    "name": "Lake Mary",
                    "type": "Flatwater",
                    "length_miles": "Varies",
                    "difficulty": "Class I",
                    "description": "Flatwater paddling on Lake Mary. Popular for kayaking and canoeing.",
                    "put_in": "Lake Mary access points",
                    "take_out": "Same as put-in",
                    "best_seasons": "Spring, Summer, Fall",
                },
            ],
            "note": "Flagstaff is not a major paddling destination. For extensive paddling, consider nearby lakes or use tools to find current opportunities.",
            "best_seasons": "Spring, Summer, Fall",
        },
        "winter_sports": {
            "description": "Skiing and snowboarding at Arizona Snowbowl",
            "facilities": "Arizona Snowbowl (San Francisco Peaks)",
            "season": "December - April",
        },
        "photography": {
            "description": "Mountain peaks, pine forests, Route 66, historic downtown",
            "best_spots": [
                "San Francisco Peaks",
                "Lowell Observatory",
                "Historic Route 66",
                "Downtown Flagstaff",
                "Sunset Crater National Monument",
            ],
        },
    },
    "attractions": {
        "natural": [
            "San Francisco Peaks",
            "Arizona Snowbowl",
            "Sunset Crater National Monument",
            "Wupatki National Monument",
            "Walnut Canyon National Monument",
            "Coconino National Forest",
        ],
        "cultural": [
            "Lowell Observatory",
            "Museum of Northern Arizona",
            "Riordan Mansion State Historic Park",
            "Route 66",
            "Northern Arizona University",
        ],
        "nearby": [
            "Grand Canyon National Park (80 miles)",
            "Sedona (30 miles)",
            "Meteor Crater (40 miles)",
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Brix Restaurant & Wine Bar",
                "type": "Fine Dining",
                "description": "Upscale dining with wine selection",
            },
            {
                "name": "Diablo Burger",
                "type": "Casual",
                "description": "Local burger joint",
            },
            {
                "name": "MartAnne's Burrito Palace",
                "type": "Mexican",
                "description": "Local favorite for breakfast and Mexican cuisine",
            },
        ],
        "accommodations": [
            {
                "name": "Little America Hotel",
                "type": "Hotel",
                "description": "Full-service hotel with mountain views",
            },
            {
                "name": "Hotel Monte Vista",
                "type": "Historic Hotel",
                "description": "Historic Route 66 hotel",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in downtown and at trailheads",
        "permits": "Coconino National Forest - some areas may require permits",
        "best_times": "Year-round - four distinct seasons",
        "weather": "Snow in winter, mild summers, spring and fall ideal",
        "access": "Easy access via I-40 and Route 66",
        "airport": "Flagstaff Pulliam Airport",
    },
}


class FlagstaffAgent(LocationAgentBase):
    """Agent specialized in Flagstaff, Arizona information and context.

    This agent enhances existing agent outputs with Flagstaff-specific knowledge
    about the mountain town, San Francisco Peaks, and outdoor opportunities.
    """

    LOCATION_NAME = "Flagstaff, Arizona"
    LOCATION_INDICATORS = [
        "flagstaff",
        "flagstaff, az",
        "flagstaff, arizona",
        "flagstaff az",
    ]
    AGENT_NAME = "flagstaff_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Flagstaff-specific knowledge base (fallback if external file not found)."""
        return FLAGSTAFF_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Flagstaff agent."""
        return """You are a comprehensive guide for Flagstaff, Arizona - the "City of Seven Wonders"
and gateway to the Grand Canyon, located at 7,000 feet elevation.

Your role is to:
1. Use tools to gather real-time data about Flagstaff (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Flagstaff-specific knowledge from the knowledge base
4. Combine information from existing agents with Flagstaff expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Flagstaff, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Flagstaff, Arizona")
- For climbing: search_trails(activity_type="climbing", location="Flagstaff, Arizona") if available
- For cycling: search_trails(activity_type="cycling", location="Flagstaff, Arizona")
- For paddling: search_trails(activity_type="paddling", location="Flagstaff, Arizona") if available
- For trail running: search_trails(activity_type="trail_running", location="Flagstaff, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Coconino National Forest - most trails require no permits)
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
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Flagstaff, Arizona"
- Flagstaff has extensive MTB trails including Schultz Creek (8 miles, intermediate/advanced), Mount Elden Lookout (5.5 miles, advanced), Fort Valley Trail System (15+ miles, all levels), and Little Elden (6 miles, beginner/intermediate)
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- Mention seasonal considerations (snow in winter, mud in spring)

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Flagstaff, Arizona"
- Popular trails include Humphreys Peak (10 miles, strenuous, highest point in Arizona), Mount Elden Lookout (5.5 miles, moderate/strenuous), Kachina Trail (10 miles, moderate), and Weatherford Trail (8 miles, moderate/strenuous)
- Use find_scenic_viewpoints for San Francisco Peaks and mountain views
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- CRITICAL: Mention weather considerations at high elevation and snow in winter

For Dining Queries:
- Use find_restaurants with location="Flagstaff, Arizona"
- Enhance results with knowledge base businesses (Brix Restaurant, Diablo Burger, MartAnne's Burrito Palace)
- Provide context about local favorites

For Accommodation Queries:
- Use search_accommodations with location="Flagstaff, Arizona"
- Enhance with knowledge base information (Little America Hotel, Hotel Monte Vista)
- Mention proximity to trails and attractions

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: San Francisco Peaks, Lowell Observatory, Historic Route 66, Downtown Flagstaff
- Mention seasonal opportunities

For Logistics Queries:
- Use get_parking_information for trailhead parking
- Provide information about permits (Coconino National Forest - most trails require no permits)
- Mention I-40 and Route 66 access
- Flagstaff Pulliam Airport for air access

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

Flagstaff's Highlights:
- Gateway to Grand Canyon (80 miles north)
- San Francisco Peaks (Humphreys Peak - 12,633 ft, highest in Arizona)
- Mountain town at 7,000 feet elevation
- Four distinct seasons (snow in winter)
- Extensive trail network in Coconino National Forest
- Route 66 historic downtown
- Northern Arizona University
- Lowell Observatory
- ~75,000 residents

Key Attractions:
- San Francisco Peaks (Humphreys, Agassiz, Fremont peaks)
- Arizona Snowbowl (winter sports)
- Lowell Observatory
- Museum of Northern Arizona
- Route 66 historic downtown
- Sunset Crater National Monument
- Wupatki National Monument

FAMOUS TRAILS:
- Hiking: Humphreys Peak Trail (10 miles, strenuous, highest point in Arizona at 12,633 ft), Mount Elden Lookout (5.5 miles, moderate/strenuous), Kachina Trail (10 miles, moderate), Weatherford Trail (8 miles, moderate/strenuous)
- Mountain Biking: Schultz Creek (8 miles, intermediate/advanced), Mount Elden Lookout (5.5 miles, advanced), Fort Valley Trail System (15+ miles, all levels), Little Elden (6 miles, beginner/intermediate)
- Arizona Trail segments pass through Flagstaff area

PRACTICAL INFORMATION:
- Four distinct seasons - snow in winter (December-April), mild summers
- Year-round outdoor recreation (best Spring, Summer, Fall)
- Easy access via I-40 and Route 66
- Gateway to Grand Canyon (80 miles north) and other northern Arizona destinations
- Elevation 7,000 feet - weather can change quickly, especially at higher elevations
- Coconino National Forest - most trails require no permits for day use
- Flagstaff Pulliam Airport for air access

ENHANCEMENT GUIDELINES:
- Always combine tool results with knowledge base information
- Provide specific recommendations based on activity type and season
- Include safety considerations (weather at elevation, snow in winter, high elevation)
- Mention Humphreys Peak as highest point in Arizona and weather considerations
- Highlight unique characteristics (mountain town, San Francisco Peaks, gateway to Grand Canyon)
- Provide practical tips (parking, permits, best times, access, weather)

Provide comprehensive, accurate, practical information that combines real tool data with Flagstaff-specific knowledge and context."""

