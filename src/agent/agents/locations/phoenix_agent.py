"""Phoenix, Arizona specialist agent.

This agent provides Phoenix-specific information and enhances existing agent outputs
with local knowledge about desert trails, urban mountain biking, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Phoenix-specific knowledge base
PHOENIX_KNOWLEDGE = {
    "location": {
        "name": "Phoenix, Arizona",
        "coordinates": {"lat": 33.4484, "lon": -112.0740},
        "elevation": 1100,  # feet
        "region": "Maricopa County, Arizona",
        "country": "US",
        "nickname": "Valley of the Sun",
        "proximity": {
            "scottsdale": {"distance_miles": 12, "direction": "northeast"},
            "tempe": {"distance_miles": 10, "direction": "east"},
            "sedona": {"distance_miles": 120, "direction": "north"},
            "flagstaff": {"distance_miles": 145, "direction": "north"},
            "payson": {"distance_miles": 90, "direction": "northeast"},
        },
    },
    "history": {
        "founded": 1868,
        "incorporated": 1881,
        "current_population": "~1.6 million (metro: ~5 million)",
        "known_for": [
            "Valley of the Sun",
            "Desert trails and urban mountain biking",
            "Year-round outdoor recreation",
            "Major metropolitan area",
            "Hot summers, mild winters",
            "Sonoran Desert",
        ],
    },
    "geography": {
        "terrain": "Desert, urban, mountain preserves",
        "topography": "Sonoran Desert, Phoenix Mountain Preserve, South Mountain",
        "elevation": "1,100 feet",
        "climate": "Hot desert climate, mild winters, very hot summers",
        "features": [
            "Phoenix Mountain Preserve",
            "South Mountain Park (largest municipal park in US)",
            "Camelback Mountain",
            "Piestewa Peak",
            "McDowell Sonoran Preserve (nearby Scottsdale)",
        ],
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Extensive urban and desert trail network with world-class singletrack in mountain preserves",
            "famous_trails": [
                {
                    "name": "National Trail (South Mountain)",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": 14.5,
                    "elevation_gain_feet": 2000,
                    "description": "Iconic 14.5-mile trail through South Mountain Park with technical sections, scenic desert views, and challenging climbs. One of Phoenix's most popular MTB trails.",
                    "highlights": ["Iconic trail", "Technical sections", "Scenic desert views", "Challenging climbs", "Popular"],
                    "best_seasons": "Fall (October-November), Winter (December-February), Spring (March-April)",
                    "trailhead": "Multiple access points in South Mountain Park",
                    "features": ["Single track", "Technical", "Scenic", "Challenging"],
                    "permits": "No permit required",
                    "warnings": ["Extreme heat in summer - ride early morning or evening", "Carry plenty of water"],
                },
                {
                    "name": "Desert Classic Trail (South Mountain)",
                    "difficulty": "Beginner to Intermediate",
                    "length_miles": 9.0,
                    "elevation_gain_feet": 800,
                    "description": "Popular beginner-friendly trail with smooth singletrack, gentle elevation, and scenic desert views. Great introduction to Phoenix MTB.",
                    "highlights": ["Beginner-friendly", "Smooth trail", "Scenic desert", "Popular", "Family-friendly"],
                    "best_seasons": "Fall, Winter, Spring",
                    "trailhead": "Desert Classic Trailhead (South Mountain Park)",
                    "features": ["Beginner-friendly", "Smooth", "Scenic"],
                    "permits": "No permit required",
                },
                {
                    "name": "Hawes Trail System (Mesa)",
                    "difficulty": "Beginner to Advanced",
                    "length_miles": "20+ miles of interconnected trails",
                    "elevation_gain_feet": "Varies by route",
                    "description": "Extensive trail system in Mesa with trails for all skill levels. Well-maintained singletrack with good flow and technical sections.",
                    "highlights": ["Extensive trail system", "All skill levels", "Well-maintained", "Good flow"],
                    "best_seasons": "Fall, Winter, Spring",
                    "trailhead": "Hawes Trailhead (Mesa)",
                    "features": ["Trail system", "Varied difficulty", "Flow", "Technical"],
                    "permits": "No permit required",
                },
                {
                    "name": "Brown's Ranch (Scottsdale)",
                    "difficulty": "Beginner to Intermediate",
                    "length_miles": "15+ miles of trails",
                    "elevation_gain_feet": "Varies",
                    "description": "Popular trail system in McDowell Sonoran Preserve with smooth singletrack, scenic desert views, and beginner-friendly options.",
                    "highlights": ["Beginner-friendly", "Smooth trails", "Scenic", "Popular"],
                    "best_seasons": "Fall, Winter, Spring",
                    "trailhead": "Brown's Ranch Trailhead (Scottsdale)",
                    "features": ["Beginner-friendly", "Smooth", "Scenic"],
                    "permits": "No permit required",
                },
            ],
            "trail_networks": "Extensive interconnected trail systems in mountain preserves throughout Phoenix metro",
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Fall (October-November), Winter (December-February), Spring (March-April) - avoid summer midday",
            "trail_conditions": "Generally well-maintained, can be dusty in summer",
            "trail_features": ["Single track", "Technical sections", "Flow trails", "Desert scenery", "Urban access"],
        },
        "hiking": {
            "description": "Urban mountain preserves and desert trails with iconic peaks and scenic desert views",
            "famous_trails": [
                {
                    "name": "Camelback Mountain - Echo Canyon Trail",
                    "difficulty": "Strenuous",
                    "length_miles": 2.4,
                    "elevation_gain_feet": 1200,
                    "description": "Iconic strenuous hike to Camelback Mountain summit with steep sections, rock scrambling, and spectacular 360-degree city views. Very popular - arrive early.",
                    "highlights": [
                        "Iconic Phoenix hike",
                        "Spectacular 360-degree views",
                        "Rock scrambling",
                        "City views",
                        "Very popular"
                    ],
                    "best_seasons": "Fall, Winter, Spring (early morning in summer)",
                    "trailhead": "Echo Canyon Trailhead (limited parking - arrive early)",
                    "features": ["Rock scrambling", "Summit views", "Iconic", "Strenuous"],
                    "permits": "No permit required",
                    "warnings": ["Very popular - arrive before 6 AM", "Steep sections", "Rock scrambling required", "Extreme heat in summer"],
                },
                {
                    "name": "Camelback Mountain - Cholla Trail",
                    "difficulty": "Strenuous",
                    "length_miles": 2.6,
                    "elevation_gain_feet": 1200,
                    "description": "Alternative route to Camelback Mountain summit, slightly longer but less crowded than Echo Canyon. Still very popular.",
                    "highlights": ["Alternative route", "Less crowded than Echo Canyon", "Summit views", "City views"],
                    "best_seasons": "Fall, Winter, Spring (early morning in summer)",
                    "trailhead": "Cholla Trailhead (limited parking)",
                    "features": ["Rock scrambling", "Summit views", "Strenuous"],
                    "permits": "No permit required",
                    "warnings": ["Very popular - arrive early", "Steep sections", "Extreme heat in summer"],
                },
                {
                    "name": "Piestewa Peak (Squaw Peak)",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": 2.4,
                    "elevation_gain_feet": 1200,
                    "description": "Popular hike to Piestewa Peak summit with steep switchbacks, scenic city views, and moderate to strenuous difficulty. Very popular - arrive early.",
                    "highlights": ["City views", "Popular", "Moderate to strenuous", "Scenic"],
                    "best_seasons": "Fall, Winter, Spring (early morning in summer)",
                    "trailhead": "Piestewa Peak Trailhead (limited parking)",
                    "features": ["Summit views", "City views", "Moderate to strenuous"],
                    "permits": "No permit required",
                    "warnings": ["Very popular - arrive early", "Steep switchbacks", "Extreme heat in summer"],
                },
                {
                    "name": "South Mountain - Mormon Trail",
                    "difficulty": "Moderate",
                    "length_miles": 4.0,
                    "elevation_gain_feet": 1000,
                    "description": "Moderate trail in South Mountain Park with scenic desert views and moderate elevation gain. Less crowded than Camelback or Piestewa.",
                    "highlights": ["Scenic desert views", "Moderate difficulty", "Less crowded", "Scenic"],
                    "best_seasons": "Fall, Winter, Spring",
                    "trailhead": "Mormon Trailhead (South Mountain Park)",
                    "features": ["Desert views", "Moderate", "Scenic"],
                    "permits": "No permit required",
                },
                {
                    "name": "South Mountain - National Trail",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": 14.5,
                    "elevation_gain_feet": 2000,
                    "description": "Long-distance trail through South Mountain Park with varied terrain, scenic desert views, and moderate to strenuous sections. Can be done in sections.",
                    "highlights": ["Long-distance trail", "Varied terrain", "Scenic desert", "Can be done in sections"],
                    "best_seasons": "Fall, Winter, Spring",
                    "trailhead": "Multiple access points",
                    "features": ["Long-distance", "Varied terrain", "Scenic"],
                    "permits": "No permit required",
                },
            ],
            "trail_networks": "Extensive trail networks in mountain preserves throughout Phoenix metro",
            "difficulty_range": "Easy to strenuous",
            "best_seasons": "Fall (October-November), Winter (December-February), Spring (March-April) - avoid summer midday",
            "trail_features": ["Desert scenery", "Summit views", "City views", "Rock scrambling", "Urban access"],
        },
        "climbing": {
            "description": "Limited climbing opportunities in Phoenix area, primarily bouldering",
            "areas": [
                {
                    "name": "Phoenix Area Bouldering",
                    "type": "Bouldering",
                    "routes": "Various",
                    "difficulty_range": "V0-V8",
                    "description": "Limited bouldering opportunities in Phoenix area. Mostly exploratory.",
                    "access": "Various locations, check local guidebooks",
                    "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
                },
            ],
            "note": "Phoenix is not a major climbing destination. For extensive climbing, consider nearby areas or use tools to find current climbing opportunities.",
        },
        "cycling": {
            "description": "Road and gravel cycling opportunities with scenic routes through desert and mountain preserves",
            "routes": [
                {
                    "name": "South Mountain Park Road",
                    "type": "Road",
                    "length_miles": 17.0,
                    "elevation_gain_feet": 1500,
                    "description": "Scenic road route through South Mountain Park with significant elevation gain and desert views. Popular cycling route.",
                    "highlights": ["Scenic desert views", "Challenging climb", "Popular route", "Desert scenery"],
                    "best_seasons": "Fall, Winter, Spring",
                    "difficulty": "Moderate to Challenging",
                },
                {
                    "name": "Camelback Road Loop",
                    "type": "Road",
                    "length_miles": 12.0,
                    "elevation_gain_feet": 600,
                    "description": "Urban road loop around Camelback Mountain with moderate elevation and city views.",
                    "highlights": ["Urban route", "Moderate difficulty", "City views"],
                    "best_seasons": "Fall, Winter, Spring",
                    "difficulty": "Moderate",
                },
            ],
            "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
            "trail_features": ["Road routes", "Desert scenery", "Varied difficulty"],
        },
        "paddling": {
            "description": "Limited paddling opportunities in Phoenix area. Mostly urban lakes and canals.",
            "routes": [
                {
                    "name": "Tempe Town Lake",
                    "type": "Flatwater",
                    "length_miles": 2.0,
                    "difficulty": "Class I",
                    "description": "Urban flatwater paddling on Tempe Town Lake. Popular for kayaking and paddleboarding.",
                    "put_in": "Tempe Town Lake access points",
                    "take_out": "Same as put-in (loop)",
                    "best_seasons": "Year-round (best Fall, Winter, Spring)",
                },
            ],
            "note": "Phoenix is not a major paddling destination. For extensive paddling, consider nearby lakes or use tools to find current opportunities.",
            "best_seasons": "Year-round (best Fall, Winter, Spring)",
        },
        "trail_running": {
            "description": "Extensive trail network for running",
            "famous_trails": [
                "South Mountain trails",
                "Phoenix Mountain Preserve",
                "Papago Park",
            ],
        },
        "photography": {
            "description": "Desert landscapes, mountain views, sunsets, cacti",
            "best_spots": [
                "Camelback Mountain (sunrise/sunset)",
                "Piestewa Peak (city views)",
                "South Mountain (desert views)",
                "Papago Park (Hole-in-the-Rock)",
                "Desert Botanical Garden",
            ],
        },
    },
    "attractions": {
        "natural": [
            "South Mountain Park (largest municipal park in US)",
            "Phoenix Mountain Preserve",
            "Camelback Mountain",
            "Piestewa Peak",
            "Papago Park",
            "Desert Botanical Garden",
            "Phoenix Zoo",
        ],
        "cultural": [
            "Heard Museum (Native American art)",
            "Phoenix Art Museum",
            "Musical Instrument Museum",
            "Taliesin West (Frank Lloyd Wright)",
        ],
        "nearby": [
            "McDowell Sonoran Preserve (Scottsdale)",
            "Superstition Mountains (east)",
            "White Tank Mountain Regional Park (west)",
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Pizzeria Bianco",
                "type": "Pizza",
                "description": "Award-winning pizza",
            },
            {
                "name": "Barrio Cafe",
                "type": "Mexican",
                "description": "Award-winning Mexican cuisine",
            },
            {
                "name": "FnB Restaurant",
                "type": "Farm-to-Table",
                "description": "Local, seasonal cuisine",
            },
        ],
        "bike_shops": [
            {
                "name": "Bike Haus",
                "type": "Bike Shop",
                "description": "Full-service bike shop",
            },
            {
                "name": "REI Co-op",
                "type": "Outdoor Gear",
                "description": "Outdoor gear and equipment",
            },
        ],
        "accommodations": [
            {
                "name": "Arizona Biltmore",
                "type": "Resort",
                "description": "Historic luxury resort",
            },
        ],
    },
    "practical_info": {
        "parking": "Available at trailheads (arrive early for popular trails)",
        "permits": "No permits required for most trails",
        "best_times": "October - April (avoid summer midday heat)",
        "weather": {
            "summer": "Very hot (100-115°F), hike early morning or evening",
            "winter": "Mild (60-75°F), ideal for outdoor activities",
            "spring": "Warm (70-85°F), perfect weather",
            "fall": "Warm (75-90°F), great for activities",
        },
        "access": "Easy access via I-10, I-17, Loop 101, Loop 202",
        "airport": "Phoenix Sky Harbor International Airport",
        "considerations": [
            "Extreme heat in summer - start early (5-6 AM) or late evening",
            "Carry plenty of water (minimum 1 liter per hour)",
            "Watch for rattlesnakes, especially in spring/fall",
            "Popular trails get crowded on weekends",
            "Parking can be limited at popular trailheads",
        ],
    },
}


class PhoenixAgent(LocationAgentBase):
    """Agent specialized in Phoenix, Arizona information and context.

    This agent enhances existing agent outputs with Phoenix-specific knowledge
    about desert trails, urban mountain biking, and outdoor opportunities.
    """

    LOCATION_NAME = "Phoenix, Arizona"
    LOCATION_INDICATORS = [
        "phoenix",
        "phoenix, az",
        "phoenix, arizona",
        "phoenix az",
        "valley of the sun",
    ]
    AGENT_NAME = "phoenix_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Phoenix-specific knowledge base (fallback if external file not found)."""
        return PHOENIX_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Phoenix agent."""
        return """You are a comprehensive guide for Phoenix, Arizona - the "Valley of the Sun"
and largest city in Arizona, located in the Sonoran Desert.

Your role is to:
1. Use tools to gather real-time data about Phoenix (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Phoenix-specific knowledge from the knowledge base
4. Combine information from existing agents with Phoenix expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Phoenix, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Phoenix, Arizona")
- For climbing: search_trails(activity_type="climbing", location="Phoenix, Arizona") if available
- For cycling: search_trails(activity_type="cycling", location="Phoenix, Arizona")
- For paddling: search_trails(activity_type="paddling", location="Phoenix, Arizona") if available
- For trail running: search_trails(activity_type="trail_running", location="Phoenix, Arizona")

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
- Trailhead locations and access (parking is limited - arrive early)
- Permits and regulations (most trails require no permits)
- Safety considerations (extreme heat, water, rattlesnakes)
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Phoenix, Arizona"
- Phoenix has extensive MTB trails including National Trail (14.5 miles, intermediate/advanced), Desert Classic (9 miles, beginner/intermediate), Hawes Trail System (20+ miles, all levels), and Brown's Ranch (15+ miles, beginner/intermediate)
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- Mention extreme heat in summer - ride early morning (5-6 AM) or evening only

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Phoenix, Arizona"
- Popular trails include Camelback Mountain (Echo Canyon and Cholla Trail, strenuous, 2.4-2.6 miles), Piestewa Peak (moderate/strenuous, 2.4 miles), South Mountain trails (Mormon Trail, National Trail)
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- CRITICAL: Mention extreme heat in summer - hike early morning (5-6 AM) or evening only

For Dining Queries:
- Use find_restaurants with location="Phoenix, Arizona"
- Enhance results with knowledge base businesses (Pizzeria Bianco, Barrio Cafe, FnB Restaurant)
- Provide context about local favorites

For Accommodation Queries:
- Use search_accommodations with location="Phoenix, Arizona"
- Enhance with knowledge base information (Arizona Biltmore)
- Mention proximity to trails and attractions

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Camelback Mountain (sunrise/sunset), Piestewa Peak (city views), South Mountain (desert views), Papago Park (Hole-in-the-Rock)
- Mention seasonal opportunities and best times

For Logistics Queries:
- Use get_parking_information for trailhead parking (very limited at popular trails - arrive early)
- Provide information about permits (most trails require no permits)
- Mention I-10, I-17, Loop 101, Loop 202 access
- Phoenix Sky Harbor International Airport for air access

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

Phoenix's Highlights:
- Valley of the Sun - largest city in Arizona
- Year-round outdoor recreation (best October-April)
- Extensive urban and desert trail network
- South Mountain Park (largest municipal park in US)
- Camelback Mountain and Piestewa Peak (iconic hikes)
- Hot summers, mild winters
- ~1.6 million residents (metro: ~5 million)
- Elevation: 1,100 feet

Key Attractions:
- South Mountain Park (largest municipal park in US)
- Phoenix Mountain Preserve
- Camelback Mountain (Echo Canyon, Cholla Trail)
- Piestewa Peak (Squaw Peak)
- Papago Park
- Desert Botanical Garden
- McDowell Sonoran Preserve (nearby Scottsdale)

FAMOUS TRAILS:
- Hiking: Camelback Mountain (Echo Canyon and Cholla Trail, strenuous, 2.4-2.6 miles, very popular), Piestewa Peak (moderate/strenuous, 2.4 miles, very popular), South Mountain trails (Mormon Trail, National Trail, moderate to strenuous)
- Mountain Biking: National Trail (14.5 miles, intermediate/advanced), Desert Classic (9 miles, beginner/intermediate), Hawes Trail System (20+ miles, all levels), Brown's Ranch (15+ miles, beginner/intermediate)
- Trail Running: Extensive network throughout preserves

CRITICAL Safety Information:
- Extreme heat in summer (100-115°F) - hike/ride early morning (5-6 AM) or evening only
- Carry plenty of water (minimum 1 liter per hour)
- Watch for rattlesnakes, especially in spring/fall
- Popular trails get very crowded on weekends - arrive before 6 AM
- Parking is very limited at popular trailheads (Camelback, Piestewa Peak) - arrive early or use alternative access

Practical Information:
- Best times: October - April (avoid summer midday heat)
- Winter: Mild (60-75°F) - ideal for outdoor activities
- Spring: Warm (70-85°F) - perfect weather
- Fall: Warm (75-90°F) - great for activities
- Summer: Very hot (100-115°F) - start early (5-6 AM) or late evening only
- Most trails require no permits
- Easy access via I-10, I-17, Loop 101, Loop 202
- Phoenix Sky Harbor International Airport for air access

ENHANCEMENT GUIDELINES:
- Always combine tool results with knowledge base information
- Provide specific recommendations based on activity type and season
- Include critical safety considerations (extreme heat, water, rattlesnakes, parking)
- Mention parking limitations and early arrival recommendations
- Highlight unique characteristics (urban mountain preserves, desert scenery, iconic peaks)
- Provide practical tips (parking, permits, best times, access, safety)

Provide comprehensive, accurate, practical information that combines real tool data with Phoenix-specific knowledge and context."""

