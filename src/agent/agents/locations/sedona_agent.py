"""Sedona, Arizona specialist agent.

This agent provides Sedona-specific information and enhances existing agent outputs
with local knowledge about Sedona's red rock formations, trails, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Sedona-specific knowledge base
SEDONA_KNOWLEDGE = {
    "location": {
        "name": "Sedona, Arizona",
        "coordinates": {"lat": 34.8697, "lon": -111.7610},
        "elevation": 4500,  # feet
        "region": "Coconino County, Arizona",
        "country": "US",
        "proximity": {
            "jerome": {"distance_miles": 30, "direction": "southwest"},
            "prescott": {"distance_miles": 60, "direction": "southwest"},
            "flagstaff": {"distance_miles": 30, "direction": "north"},
            "phoenix": {"distance_miles": 120, "direction": "south"},
        },
    },
    "history": {
        "founded": "Early 1900s",
        "incorporated": 1988,
        "current_population": "~10,000 residents",
        "tourism": "~3 million annual visitors",
        "known_for": [
            "Red rock formations",
            "Spiritual vortex sites",
            "World-class mountain biking",
            "Hiking and outdoor recreation",
            "Art galleries and New Age culture",
        ],
    },
    "geography": {
        "terrain": "Red rock canyons and mesas",
        "topography": "Oak Creek Canyon, Verde Valley",
        "red_rock_formations": [
            "Cathedral Rock",
            "Bell Rock",
            "Courthouse Butte",
            "Coffee Pot Rock",
            "Snoopy Rock",
            "Thunder Mountain",
        ],
        "creeks": "Oak Creek runs through Sedona",
        "climate": "High desert, 4 seasons",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "World-class MTB destination with 200+ miles of world-renowned singletrack through red rock country",
            "famous_trails": [
                {
                    "name": "Hiline Trail",
                    "difficulty": "Advanced to Expert",
                    "length_miles": 11.0,
                    "elevation_gain_feet": 1500,
                    "description": "Iconic advanced/expert trail with technical rock sections, exposure, and stunning red rock views. Not for beginners. Requires advanced bike handling skills.",
                    "highlights": [
                        "Technical rock sections",
                        "Exposure and cliff edges",
                        "Stunning red rock views",
                        "World-famous trail",
                        "Advanced riders only"
                    ],
                    "best_seasons": "Spring (March-May), Fall (September-November), Winter",
                    "trailhead": "Hiline Trailhead (coordinates available via tools)",
                    "features": ["Technical", "Exposure", "Scenic views", "Advanced"],
                    "permits": "Red Rock Pass required ($5/day or $15/week)",
                    "warnings": ["Advanced/expert only", "Exposure", "Technical sections", "Not for beginners"],
                },
                {
                    "name": "Hangover Trail",
                    "difficulty": "Expert",
                    "length_miles": 3.5,
                    "elevation_gain_feet": 800,
                    "description": "Extremely technical expert trail with significant exposure, technical rock moves, and narrow ledges. One of Sedona's most challenging trails.",
                    "highlights": ["Extreme technical", "Significant exposure", "Narrow ledges", "Expert only", "Iconic challenge"],
                    "best_seasons": "Spring, Fall, Winter",
                    "trailhead": "Hangover Trailhead",
                    "features": ["Extreme technical", "Exposure", "Expert"],
                    "permits": "Red Rock Pass required",
                    "warnings": ["Expert only", "Significant exposure", "Extremely technical", "Not for intermediate riders"],
                },
                {
                    "name": "Highline Trail",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": 8.5,
                    "elevation_gain_feet": 1200,
                    "description": "Popular intermediate to advanced trail with flow sections, technical challenges, and scenic red rock views. Great for intermediate riders looking to progress.",
                    "highlights": ["Flow sections", "Technical challenges", "Scenic views", "Popular", "Intermediate-friendly"],
                    "best_seasons": "Spring, Fall, Winter",
                    "trailhead": "Highline Trailhead",
                    "features": ["Flow", "Technical", "Scenic"],
                    "permits": "Red Rock Pass required",
                },
                {
                    "name": "Mescal Trail",
                    "difficulty": "Beginner to Intermediate",
                    "length_miles": 2.5,
                    "elevation_gain_feet": 300,
                    "description": "Beginner-friendly trail with smooth singletrack, gentle elevation, and scenic red rock views. Great introduction to Sedona riding.",
                    "highlights": ["Beginner-friendly", "Smooth trail", "Scenic views", "Family-friendly"],
                    "best_seasons": "Year-round (best Spring, Fall, Winter)",
                    "trailhead": "Mescal Trailhead",
                    "features": ["Beginner-friendly", "Smooth", "Scenic"],
                    "permits": "Red Rock Pass required",
                },
                {
                    "name": "Aerie Trail",
                    "difficulty": "Intermediate",
                    "length_miles": 4.0,
                    "elevation_gain_feet": 600,
                    "description": "Intermediate trail with good flow, moderate technical sections, and scenic overlooks. Popular with intermediate riders.",
                    "highlights": ["Good flow", "Moderate technical", "Scenic overlooks", "Popular"],
                    "best_seasons": "Spring, Fall, Winter",
                    "trailhead": "Aerie Trailhead",
                    "features": ["Flow", "Moderate technical", "Scenic"],
                    "permits": "Red Rock Pass required",
                },
                {
                    "name": "Baldwin Trail",
                    "difficulty": "Beginner",
                    "length_miles": 2.0,
                    "elevation_gain_feet": 200,
                    "description": "Easy beginner trail with smooth singletrack, minimal elevation, and scenic Oak Creek views. Perfect for families and beginners.",
                    "highlights": ["Beginner-friendly", "Family-friendly", "Smooth", "Oak Creek views"],
                    "best_seasons": "Year-round",
                    "trailhead": "Baldwin Trailhead",
                    "features": ["Beginner-friendly", "Smooth", "Family-friendly"],
                    "permits": "Red Rock Pass required",
                },
            ],
            "trail_networks": "Sedona has 200+ miles of interconnected singletrack trails",
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Spring (March-May), Fall (September-November), Winter (December-February)",
            "trail_conditions": "Generally well-maintained, can be dusty in summer",
            "trail_features": ["Single track", "Technical sections", "Flow trails", "Red rock scenery", "Exposure"],
        },
        "hiking": {
            "description": "Extensive hiking trail network through iconic red rock country with world-famous formations and scenic vistas",
            "famous_trails": [
                {
                    "name": "Cathedral Rock Trail",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": 1.5,
                    "elevation_gain_feet": 600,
                    "description": "Iconic trail to Cathedral Rock summit with steep sections, rock scrambling, and spectacular 360-degree views. One of Sedona's most popular hikes.",
                    "highlights": [
                        "Iconic Cathedral Rock",
                        "Spectacular 360-degree views",
                        "Rock scrambling",
                        "Sunrise/sunset views",
                        "Vortex site"
                    ],
                    "best_seasons": "Spring, Fall, Winter (early morning in summer)",
                    "trailhead": "Cathedral Rock Trailhead (limited parking)",
                    "features": ["Rock scrambling", "Summit views", "Iconic", "Vortex site"],
                    "permits": "Red Rock Pass required",
                    "warnings": ["Steep sections", "Rock scrambling required", "Very popular - arrive early"],
                },
                {
                    "name": "Devil's Bridge Trail",
                    "difficulty": "Moderate",
                    "length_miles": 4.2,
                    "elevation_gain_feet": 400,
                    "description": "Popular trail to natural sandstone arch (Devil's Bridge) with moderate elevation gain and stunning views. Very popular - expect crowds.",
                    "highlights": ["Natural sandstone arch", "Scenic views", "Popular photo spot", "Moderate difficulty"],
                    "best_seasons": "Spring, Fall, Winter (early morning in summer)",
                    "trailhead": "Devil's Bridge Trailhead (limited parking, use shuttle)",
                    "features": ["Natural arch", "Scenic views", "Photo opportunity"],
                    "permits": "Red Rock Pass required",
                    "warnings": ["Very popular - expect crowds", "Limited parking - use shuttle", "Arrive early"],
                },
                {
                    "name": "West Fork Trail",
                    "difficulty": "Easy to Moderate",
                    "length_miles": 6.4,
                    "elevation_gain_feet": 200,
                    "description": "Scenic creek-side trail through Oak Creek Canyon with multiple creek crossings, fall colors, and canyon views. One of Arizona's most popular hikes.",
                    "highlights": ["Creek crossings", "Fall colors", "Canyon views", "Scenic", "Popular"],
                    "best_seasons": "Spring (water flow), Fall (colors), Winter",
                    "trailhead": "West Fork Trailhead (limited parking)",
                    "features": ["Creek crossings", "Canyon views", "Scenic"],
                    "permits": "Red Rock Pass required",
                    "warnings": ["Very popular - arrive early", "Limited parking", "Creek crossings may be wet"],
                },
                {
                    "name": "Boynton Canyon Trail",
                    "difficulty": "Moderate",
                    "length_miles": 6.1,
                    "elevation_gain_feet": 800,
                    "description": "Scenic trail through Boynton Canyon with red rock views, vortex site, and moderate elevation gain. Less crowded than some trails.",
                    "highlights": ["Canyon views", "Vortex site", "Less crowded", "Scenic", "Moderate difficulty"],
                    "best_seasons": "Spring, Fall, Winter",
                    "trailhead": "Boynton Canyon Trailhead",
                    "features": ["Canyon views", "Vortex site", "Scenic"],
                    "permits": "Red Rock Pass required",
                },
                {
                    "name": "Fay Canyon Trail",
                    "difficulty": "Easy",
                    "length_miles": 2.4,
                    "elevation_gain_feet": 200,
                    "description": "Easy family-friendly trail through Fay Canyon with minimal elevation gain and scenic red rock views. Great for beginners and families.",
                    "highlights": ["Family-friendly", "Easy", "Scenic", "Beginner-friendly"],
                    "best_seasons": "Year-round",
                    "trailhead": "Fay Canyon Trailhead",
                    "features": ["Family-friendly", "Easy", "Scenic"],
                    "permits": "Red Rock Pass required",
                },
            ],
            "trail_networks": "Extensive interconnected hiking trail network through red rock country",
            "difficulty_range": "Easy to strenuous",
            "best_seasons": "Spring (March-May), Fall (September-November), Winter (December-February)",
            "trail_features": ["Red rock scenery", "Scenic views", "Vortex sites", "Canyon views", "Creek crossings"],
        },
        "climbing": {
            "description": "Limited climbing opportunities in Sedona area, primarily bouldering and some sport climbing",
            "areas": [
                {
                    "name": "Sedona Bouldering Areas",
                    "type": "Bouldering",
                    "routes": "Various",
                    "difficulty_range": "V0-V10",
                    "description": "Various bouldering areas in Sedona with sandstone boulders. Limited developed areas.",
                    "access": "Various locations, check local guidebooks",
                    "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
                },
            ],
            "note": "Sedona is not a major climbing destination. For extensive climbing, consider nearby areas or use tools to find current climbing opportunities.",
        },
        "cycling": {
            "description": "Road and gravel cycling opportunities with scenic routes through red rock country",
            "routes": [
                {
                    "name": "Oak Creek Canyon Scenic Drive",
                    "type": "Road",
                    "length_miles": 14.0,
                    "elevation_gain_feet": 2000,
                    "description": "Scenic road route through Oak Creek Canyon with significant elevation gain and stunning canyon views. Popular cycling route.",
                    "highlights": ["Scenic canyon views", "Challenging climb", "Popular route", "Stunning scenery"],
                    "best_seasons": "Spring, Fall, Winter",
                    "difficulty": "Moderate to Challenging",
                },
                {
                    "name": "Red Rock Loop Road",
                    "type": "Road",
                    "length_miles": 7.0,
                    "elevation_gain_feet": 400,
                    "description": "Scenic road loop with red rock views and moderate elevation. Popular with cyclists.",
                    "highlights": ["Red rock views", "Moderate difficulty", "Scenic loop"],
                    "best_seasons": "Year-round (best Spring, Fall, Winter)",
                    "difficulty": "Moderate",
                },
            ],
            "best_seasons": "Spring, Fall, Winter (avoid summer heat)",
            "trail_features": ["Road routes", "Scenic", "Varied difficulty"],
        },
        "paddling": {
            "description": "Limited paddling opportunities in Sedona. Oak Creek offers some sections suitable for kayaking and paddleboarding, but water levels are seasonal.",
            "routes": [
                {
                    "name": "Oak Creek Paddling",
                    "type": "Flatwater/River",
                    "length_miles": "Varies",
                    "difficulty": "Class I-II",
                    "description": "Seasonal paddling on Oak Creek. Water levels dependent on rainfall and snowmelt. Best during spring runoff.",
                    "put_in": "Various access points along Oak Creek (coordinates available via tools)",
                    "take_out": "Various take-out points downstream",
                    "best_seasons": "Spring (water flow), early Summer",
                    "water_levels": "Dependent on rainfall and snowmelt - check current conditions",
                },
            ],
            "note": "Sedona is not a major paddling destination. Water levels are seasonal. For extensive paddling, consider nearby lakes or use tools to find current opportunities.",
            "best_seasons": "Spring (water flow), early Summer",
        },
        "photography": {
            "description": "Iconic red rock formations, sunrise/sunset views",
            "best_spots": [
                "Airport Mesa (sunset)",
                "Cathedral Rock (sunrise)",
                "Bell Rock",
                "Red Rock Crossing",
                "Chapel of the Holy Cross",
            ],
        },
        "spiritual": {
            "description": "Known for vortex sites and spiritual energy",
            "vortex_locations": [
                "Airport Mesa",
                "Cathedral Rock",
                "Bell Rock",
                "Boynton Canyon",
            ],
        },
    },
    "attractions": {
        "natural": [
            "Red Rock State Park",
            "Slide Rock State Park",
            "Oak Creek Canyon",
            "Tlaquepaque Arts & Shopping Village",
            "Chapel of the Holy Cross",
        ],
        "cultural": [
            "Sedona Arts Center",
            "Tlaquepaque Arts & Shopping Village",
            "Sedona Heritage Museum",
            "Sedona International Film Festival",
        ],
        "recreation": [
            "Pink Jeep Tours",
            "Sedona Stargazing Tours",
            "Hot air balloon rides",
            "ATV tours",
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Elote Cafe",
                "type": "Southwestern",
                "description": "Award-winning Southwestern cuisine",
            },
            {
                "name": "Mariposa Latin Inspired Grill",
                "type": "Fine Dining",
                "description": "Upscale Latin-inspired cuisine with red rock views",
            },
            {
                "name": "The Hudson",
                "type": "American",
                "description": "Modern American cuisine with scenic views",
            },
        ],
        "shops": [
            {
                "name": "Tlaquepaque Arts & Shopping Village",
                "type": "Shopping Village",
                "description": "Art galleries, shops, restaurants in Spanish-style architecture",
            },
        ],
        "accommodations": [
            {
                "name": "Enchantment Resort",
                "type": "Resort",
                "description": "Luxury resort in Boynton Canyon",
            },
            {
                "name": "L'Auberge de Sedona",
                "type": "Resort",
                "description": "Luxury resort on Oak Creek",
            },
        ],
    },
    "practical_info": {
        "parking": "Limited parking at trailheads - arrive early or use shuttles",
        "shuttles": "Sedona Shuttle service available for popular trailheads",
        "permits": "Red Rock Pass required for some areas ($5/day or $15/week)",
        "best_times": "Spring (March-May) and Fall (September-November)",
        "crowds": "Very popular - expect crowds at popular trails",
        "weather": "Hot summers (100+ F), mild winters, can snow",
    },
}


class SedonaAgent(LocationAgentBase):
    """Agent specialized in Sedona, Arizona information and context.

    This agent enhances existing agent outputs with Sedona-specific knowledge
    about red rock formations, world-class trails, and outdoor opportunities.
    """

    LOCATION_NAME = "Sedona, Arizona"
    LOCATION_INDICATORS = [
        "sedona",
        "sedona, az",
        "sedona, arizona",
        "sedona az",
    ]
    AGENT_NAME = "sedona_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Sedona-specific knowledge base (fallback if external file not found)."""
        return SEDONA_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Sedona agent."""
        return """You are a comprehensive guide for Sedona, Arizona - a world-renowned
red rock destination and outdoor recreation paradise.

Your role is to:
1. Use tools to gather real-time data about Sedona (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Sedona-specific knowledge from the knowledge base
4. Combine information from existing agents with Sedona expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Sedona, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Sedona, Arizona")
- For climbing: search_trails(activity_type="climbing", location="Sedona, Arizona") if available
- For cycling: search_trails(activity_type="cycling", location="Sedona, Arizona")
- For paddling: search_trails(activity_type="paddling", location="Sedona, Arizona") if available
- For trail running: search_trails(activity_type="trail_running", location="Sedona, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Red Rock Pass required)
- Include trail connectivity and route planning details

COMBINE multiple sources:
- Tool data (current conditions, real-time info from search_trails)
- Knowledge base (detailed trail descriptions, historical info)
- Existing agent outputs (trail_info from trail_agent if available)

PROVIDE comprehensive trail information:
- Trail names, difficulty ratings, length, elevation gain
- Detailed trail descriptions and highlights
- Best seasons and current conditions
- Trailhead locations and access (parking is limited - mention shuttles)
- Permits and regulations (Red Rock Pass: $5/day or $15/week)
- Safety considerations (exposure, technical sections, crowds)
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Sedona, Arizona"
- Sedona has 200+ miles of world-class MTB trails including Hiline (advanced/expert), Hangover (expert), Highline (intermediate/advanced), Mescal (beginner), Aerie (intermediate), and Baldwin (beginner)
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and technical features
- Mention Red Rock Pass requirement and parking limitations
- Highlight exposure and technical sections for advanced trails

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Sedona, Arizona"
- Popular trails include Cathedral Rock (moderate/strenuous, iconic), Devil's Bridge (moderate, very popular), West Fork (easy/moderate, scenic), Boynton Canyon (moderate, vortex site), and Fay Canyon (easy, family-friendly)
- Use find_scenic_viewpoints for red rock formations and overlooks
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention Red Rock Pass requirement and parking limitations (use shuttles for popular trails)

For Dining Queries:
- Use find_restaurants with location="Sedona, Arizona"
- Enhance results with knowledge base businesses (Elote Cafe, Mariposa, The Hudson)
- Provide context about local favorites and atmosphere

For Accommodation Queries:
- Use search_accommodations with location="Sedona, Arizona"
- Enhance with knowledge base information (Enchantment Resort, L'Auberge de Sedona)
- Mention proximity to trails and attractions

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Airport Mesa (sunset), Cathedral Rock (sunrise), Bell Rock, Red Rock Crossing, Chapel of the Holy Cross
- Mention seasonal opportunities and best times

For Logistics Queries:
- Use get_parking_information for trailhead parking (very limited - emphasize shuttles)
- Use find_shuttle_services (Sedona Shuttle available for popular trailheads)
- Provide information about Red Rock Pass ($5/day or $15/week)
- Mention Highway 89A access and proximity to Flagstaff (30 miles) and Phoenix (120 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

Sedona's Highlights:
- World-class mountain biking destination (200+ miles of trails)
- Iconic red rock formations (Cathedral Rock, Bell Rock, etc.)
- Extensive hiking trail network
- Spiritual vortex sites
- Art galleries and New Age culture
- ~3 million annual visitors
- Elevation: 4,500 feet
- Located in Coconino County, Arizona

Key Attractions:
- Red Rock State Park
- Slide Rock State Park
- Oak Creek Canyon
- Tlaquepaque Arts & Shopping Village
- Chapel of the Holy Cross
- Cathedral Rock
- Bell Rock

FAMOUS TRAILS:
- Mountain Biking: Hiline (advanced/expert, 11 miles), Hangover (expert, 3.5 miles), Highline (intermediate/advanced, 8.5 miles), Mescal (beginner, 2.5 miles), Aerie (intermediate, 4 miles), Baldwin (beginner, 2 miles)
- Hiking: Cathedral Rock (moderate/strenuous, 1.5 miles, iconic), Devil's Bridge (moderate, 4.2 miles, very popular), West Fork (easy/moderate, 6.4 miles, scenic), Boynton Canyon (moderate, 6.1 miles, vortex site), Fay Canyon (easy, 2.4 miles, family-friendly)

PRACTICAL INFORMATION:
- Red Rock Pass required for most areas ($5/day or $15/week)
- Limited parking at trailheads - arrive early (before 7 AM) or use Sedona Shuttle service
- Very popular - expect crowds at popular trails, especially Cathedral Rock and Devil's Bridge
- Best times: Spring (March-May) and Fall (September-November). Winter is also good. Summer is hot - hike early morning or evening
- Weather: Hot summers (100+ F), mild winters, can snow
- Shuttles: Sedona Shuttle service available for popular trailheads - highly recommended

ENHANCEMENT GUIDELINES:
- Always combine tool results with knowledge base information
- Provide specific recommendations based on activity type and season
- Include safety considerations (exposure on advanced trails, crowds, parking)
- Mention Red Rock Pass requirement and shuttle services
- Highlight unique characteristics (red rock formations, vortex sites, world-class MTB)
- Provide practical tips (parking, permits, best times, access, shuttles)

Provide comprehensive, accurate, practical information that combines real tool data with Sedona-specific knowledge and context."""

