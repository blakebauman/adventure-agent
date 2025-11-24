"""Sierra Vista, Arizona specialist agent.

This agent provides Sierra Vista-specific information and enhances existing agent outputs
with local knowledge about Huachuca Mountains, birding capital, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Sierra Vista-specific knowledge base - Enhanced with detailed information
SIERRA_VISTA_KNOWLEDGE = {
    "location": {
        "name": "Sierra Vista, Arizona",
        "coordinates": {"lat": 31.5545, "lon": -110.3037},
        "elevation": 4600,  # feet
        "region": "Cochise County, Arizona",
        "country": "US",
        "nickname": "Hummingbird Capital of the United States",
        "proximity": {
            "bisbee": {"distance_miles": 25, "direction": "south", "drive_time_minutes": 35},
            "tombstone": {"distance_miles": 30, "direction": "north", "drive_time_minutes": 40},
            "tucson": {"distance_miles": 75, "direction": "northwest", "drive_time_minutes": 80},
            "patagonia": {"distance_miles": 40, "direction": "southwest", "drive_time_minutes": 50},
        },
    },
    "history": {
        "founded": 1956,
        "incorporated": 1956,
        "current_population": "~45,000 residents",
        "known_for": [
            "Huachuca Mountains location",
            "Birding capital - 'Hummingbird Capital of the United States'",
            "Coronado National Forest gateway",
            "Miller Peak (9,466 ft)",
            "Ramsey Canyon Preserve",
            "San Pedro Riparian Area",
        ],
        "historical_significance": "Founded as military community (Fort Huachuca), evolved into major recreation hub and birding destination",
    },
    "geography": {
        "terrain": "Mountainous, desert",
        "topography": "Huachuca Mountains, Coronado National Forest, San Pedro River",
        "elevation": "4,600 feet",
        "climate": "Four distinct seasons, cooler than desert (4,600 feet elevation)",
        "features": [
            "Huachuca Mountains (Miller Peak - 9,466 ft)",
            "Coronado National Forest (1.78 million acres)",
            "San Pedro Riparian National Conservation Area",
            "Ramsey Canyon Preserve",
        ],
        "ecosystem": "Mountain desert transitioning to pine-oak at higher elevations, riparian areas along San Pedro River",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Trails in Huachuca Mountains and Coronado National Forest with varied terrain from flowy singletrack to technical challenges",
            "famous_trails": [
                {
                    "name": "Carr Canyon Trails",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Carr Canyon with technical sections, significant elevation gain, and scenic mountain views. Popular with advanced riders.",
                    "highlights": ["Technical sections", "Challenging", "Scenic mountain views", "Elevation gain"],
                    "best_seasons": "Year-round (best Spring, Fall, Winter)",
                    "trailhead": "Carr Canyon Trailhead",
                    "features": ["Mountain trails", "Technical", "Challenging", "Scenic"],
                    "permits": "Coronado National Forest - no permit required for day use",
                },
                {
                    "name": "Miller Peak Trails",
                    "difficulty": "Advanced",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Significant (to 9,466 ft summit)",
                    "description": "Challenging trails to Miller Peak summit (9,466 ft) with significant elevation gain, technical sections, and spectacular views.",
                    "highlights": ["Summit views", "Challenging", "Significant elevation", "Spectacular views"],
                    "best_seasons": "Spring, Fall, Winter (snow in winter at higher elevations)",
                    "trailhead": "Various access points",
                    "features": ["Summit trail", "Technical", "Challenging", "Scenic"],
                    "permits": "Coronado National Forest - no permit required",
                },
            ],
            "difficulty_range": "Intermediate to expert",
            "best_seasons": "Year-round (best Spring, Fall, Winter)",
            "trail_conditions": "Generally well-maintained, can be dusty in summer",
            "trail_features": ["Single track", "Technical sections", "Mountain scenery", "Elevation"],
        },
        "hiking": {
            "description": "Trails in Huachuca Mountains and Coronado National Forest with scenic mountain views, birding opportunities, and varied difficulty",
            "famous_trails": [
                {
                    "name": "Ramsey Canyon Preserve Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Ramsey Canyon Preserve with easy to moderate difficulty, excellent birding opportunities, and scenic canyon views. World-renowned birding destination.",
                    "highlights": [
                        "World-renowned birding",
                        "Scenic canyon",
                        "Easy to moderate",
                        "Birding opportunities",
                        "Ramsey Canyon Preserve",
                    ],
                    "best_seasons": "Year-round (best Spring, Fall for birding)",
                    "trailhead": "Ramsey Canyon Preserve",
                    "features": ["Birding", "Scenic", "Easy to moderate"],
                    "permits": "Ramsey Canyon Preserve - entrance fee required",
                },
                {
                    "name": "Miller Peak Trail",
                    "difficulty": "Strenuous",
                    "length_miles": "10.0",
                    "elevation_gain_feet": 4000,
                    "description": "Challenging trail to Miller Peak summit (9,466 ft) with significant elevation gain (4,000 ft) and spectacular views. One of the most challenging hikes in area.",
                    "highlights": ["Summit views", "Challenging", "Significant elevation", "Spectacular views", "9,466 ft summit"],
                    "best_seasons": "Spring, Fall, Winter (snow in winter at higher elevations)",
                    "trailhead": "Miller Peak Trailhead",
                    "features": ["Summit hike", "Challenging", "Scenic"],
                    "permits": "Coronado National Forest - no permit required",
                },
                {
                    "name": "Carr Peak Trail",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": "6.0",
                    "elevation_gain_feet": 2500,
                    "description": "Trail to Carr Peak with moderate to strenuous difficulty, significant elevation gain, and scenic mountain views.",
                    "highlights": ["Summit views", "Moderate to strenuous", "Scenic mountain views"],
                    "best_seasons": "Spring, Fall, Winter",
                    "trailhead": "Carr Peak Trailhead",
                    "features": ["Summit hike", "Moderate to strenuous", "Scenic"],
                    "permits": "Coronado National Forest - no permit required",
                },
            ],
            "difficulty_range": "Easy to strenuous",
            "best_seasons": "Year-round (best Spring, Fall, Winter)",
            "trail_features": ["Mountain peaks", "Birding", "Scenic views", "Riparian areas"],
        },
        "birding": {
            "description": "World-class birding in Ramsey Canyon Preserve, San Pedro Riparian Area, and Huachuca Mountains",
            "locations": [
                {
                    "name": "Ramsey Canyon Preserve",
                    "type": "Preserve",
                    "species": "Hummingbirds, trogons, warblers, tanagers",
                    "description": "World-renowned birding destination with excellent hummingbird viewing and diverse bird species",
                    "seasons": "Year-round, best in Spring and Fall migration",
                    "highlights": ["Hummingbirds", "Trogons", "World-renowned", "Diverse species"],
                },
                {
                    "name": "San Pedro Riparian National Conservation Area",
                    "type": "Riparian Area",
                    "species": "Waterfowl, warblers, flycatchers, riparian birds",
                    "description": "Riparian area along San Pedro River with excellent birding opportunities",
                    "seasons": "Year-round, best in Spring and Fall migration",
                    "highlights": ["Riparian birds", "Waterfowl", "Migration stopover"],
                },
                {
                    "name": "Huachuca Mountains",
                    "type": "Mountains",
                    "species": "Mountain birds, warblers, tanagers",
                    "description": "Mountain habitat with diverse bird species",
                    "seasons": "Year-round, best in Spring and Fall",
                    "highlights": ["Mountain birds", "Diverse species"],
                },
            ],
            "seasons": "Year-round, best in Spring and Fall migration",
            "permits": "Ramsey Canyon Preserve - entrance fee required. San Pedro Riparian Area - no permit required",
        },
        "photography": {
            "description": "Wildlife, mountain views, birding, riparian areas offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Ramsey Canyon Preserve",
                    "best_time": "Early morning for birding, golden hour for scenic shots",
                    "subjects": "Hummingbirds, birds, wildlife, canyon scenery",
                },
                {
                    "name": "Huachuca Mountains",
                    "best_time": "Sunrise and sunset for mountain views",
                    "subjects": "Mountain peaks, scenic overlooks, wildlife",
                },
                {
                    "name": "San Pedro Riparian Area",
                    "best_time": "Early morning for birding, golden hour for scenic shots",
                    "subjects": "Riparian birds, wildlife, river scenery",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring migration, fall colors, winter clarity",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Huachuca Mountains",
                "type": "Mountain Range",
                "description": "Scenic mountain range with Miller Peak (9,466 ft), trails, and wildlife",
                "activities": ["Hiking", "Mountain biking", "Photography", "Wildlife viewing"],
            },
            {
                "name": "Ramsey Canyon Preserve",
                "type": "Preserve",
                "description": "World-renowned birding destination with excellent hummingbird viewing",
                "activities": ["Birding", "Hiking", "Photography", "Wildlife viewing"],
            },
            {
                "name": "San Pedro Riparian National Conservation Area",
                "type": "Riparian Area",
                "description": "Riparian area along San Pedro River with excellent birding and wildlife viewing",
                "activities": ["Birding", "Hiking", "Photography", "Wildlife viewing"],
            },
            {
                "name": "Coronado National Forest",
                "type": "National Forest",
                "description": "1.78 million acres with extensive trail network",
                "activities": ["All outdoor activities"],
            },
        ],
        "cultural": [
            {
                "name": "Fort Huachuca",
                "type": "Military Base",
                "description": "Historic military base with museum",
            },
        ],
        "nearby": [
            {
                "name": "Bisbee",
                "distance": "25 miles",
                "description": "Historic mining town, arts community, Mule Mountains",
            },
            {
                "name": "Tombstone",
                "distance": "30 miles",
                "description": "Iconic Wild West town, O.K. Corral, Boot Hill Cemetery",
            },
            {
                "name": "Patagonia",
                "distance": "40 miles",
                "description": "Birding destination, small town charm, Sonoita Creek",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Sierra Vista offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Various accommodations",
                "type": "Mixed",
                "description": "Multiple lodging options in area - use tools to find current options",
                "note": "Use search_accommodations tool for current lodging options",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in town and at trailheads. Popular trailheads like Ramsey Canyon may fill up - arrive early",
        "permits": "Coronado National Forest - most trails require no permits for day use. Ramsey Canyon Preserve requires entrance fee. San Pedro Riparian Area - no permit required",
        "best_times": "Year-round - cooler than desert. Spring (March-May) and Fall (September-November) are ideal for birding and outdoor activities",
        "weather": {
            "summer": "Warm (75-90°F), cooler than desert due to elevation",
            "winter": "Mild (45-65°F), excellent for outdoor activities",
            "spring": "Pleasant (60-75°F), ideal for all activities and birding",
            "fall": "Pleasant (60-75°F), ideal for all activities and birding",
        },
        "access": "Highway 90 from Tucson (75 miles, 80 minutes) or Bisbee (25 miles, 35 minutes)",
        "considerations": [
            "Elevation 4,600 feet - cooler than desert, but still warm in summer",
            "World-class birding - bring binoculars and field guides",
            "Ramsey Canyon Preserve requires entrance fee - check hours",
            "Popular trailheads may fill up on weekends - arrive early",
            "Gateway to Bisbee (25 miles), Tombstone (30 miles), and Patagonia (40 miles)",
            "Miller Peak is challenging - be prepared for significant elevation gain",
        ],
    },
}


class SierraVistaAgent(LocationAgentBase):
    """Agent specialized in Sierra Vista, Arizona information and context.

    This agent enhances existing agent outputs with Sierra Vista-specific knowledge
    about Huachuca Mountains, birding capital, and outdoor opportunities.
    """

    LOCATION_NAME = "Sierra Vista, Arizona"
    LOCATION_INDICATORS = [
        "sierra vista",
        "sierra vista, az",
        "sierra vista, arizona",
        "sierra vista az",
    ]
    AGENT_NAME = "sierra_vista_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Sierra Vista-specific knowledge base (fallback if external file not found)."""
        return SIERRA_VISTA_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Sierra Vista agent."""
        return """You are a comprehensive guide for Sierra Vista, Arizona - the "Hummingbird Capital of the United States"
located in the Huachuca Mountains at 4,600 feet elevation, known for world-class birding, mountain recreation, and gateway to wilderness.

Your role is to:
1. Use tools to gather real-time data about Sierra Vista (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Sierra Vista-specific knowledge from the knowledge base
4. Combine information from existing agents with Sierra Vista expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Sierra Vista, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Sierra Vista, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Sierra Vista, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Coronado National Forest - most trails require no permits, Ramsey Canyon Preserve requires entrance fee)
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

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Sierra Vista, Arizona"
- Sierra Vista has trails in Huachuca Mountains including Carr Canyon Trails (intermediate/advanced) and Miller Peak Trails (advanced, to 9,466 ft summit)
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- Mention seasonal considerations (snow in winter at higher elevations)

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Sierra Vista, Arizona"
- Popular trails include Ramsey Canyon Preserve Trails (easy/moderate, world-renowned birding), Miller Peak Trail (10 miles, strenuous, 9,466 ft summit), and Carr Peak Trail (6 miles, moderate/strenuous)
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention world-class birding opportunities in Ramsey Canyon Preserve

For Birding Queries:
- Sierra Vista is "Hummingbird Capital of the United States" with world-class birding
- Key locations: Ramsey Canyon Preserve (world-renowned, entrance fee required), San Pedro Riparian National Conservation Area (no permit required), Huachuca Mountains
- Best seasons: Year-round, best in Spring and Fall migration
- Mention bringing binoculars and field guides

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Ramsey Canyon Preserve (early morning for birding, golden hour for scenic), Huachuca Mountains (sunrise/sunset), San Pedro Riparian Area (early morning for birding, golden hour)
- Mention seasonal opportunities (spring migration, fall colors, winter clarity)

For Dining Queries:
- Use find_restaurants with location="Sierra Vista, Arizona"
- Provide context about major recreation hub

For Accommodation Queries:
- Use search_accommodations with location="Sierra Vista, Arizona"
- Mention proximity to trails and birding areas

For Logistics Queries:
- Use get_parking_information (Popular trailheads like Ramsey Canyon may fill up - arrive early)
- Provide information about permits (Coronado National Forest - most trails require no permits, Ramsey Canyon Preserve requires entrance fee)
- Mention Highway 90 access from Tucson (75 miles) and Bisbee (25 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Sierra Vista, Arizona",
  "overview": "Brief overview of Sierra Vista as birding capital and mountain recreation hub",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
    "mountain_biking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
    "hiking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
    "birding": {"locations": [...], "seasons": "..."},
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

SIERRA VISTA'S UNIQUE CHARACTERISTICS:
- Birding capital - "Hummingbird Capital of the United States"
- Huachuca Mountains location (Miller Peak - 9,466 ft)
- Coronado National Forest gateway (1.78 million acres)
- World-class birding in Ramsey Canyon Preserve and San Pedro Riparian Area
- Elevation: 4,600 feet (cooler than desert)
- ~45,000 residents
- Gateway to Bisbee (25 miles), Tombstone (30 miles), and Patagonia (40 miles)

KEY ATTRACTIONS:
- Ramsey Canyon Preserve: World-renowned birding destination with excellent hummingbird viewing
- San Pedro Riparian National Conservation Area: Riparian area with excellent birding and wildlife viewing
- Huachuca Mountains: Scenic mountain range with Miller Peak (9,466 ft), trails, and wildlife
- Coronado National Forest: 1.78 million acres with extensive trail network
- Fort Huachuca: Historic military base with museum

FAMOUS ACTIVITIES:
- Birding (world-class - Ramsey Canyon Preserve, San Pedro Riparian Area, Huachuca Mountains)
- Mountain biking (Carr Canyon Trails, Miller Peak Trails)
- Hiking (Ramsey Canyon Preserve, Miller Peak Trail - 9,466 ft summit, Carr Peak Trail)
- Wildlife photography (birds, wildlife, mountain views)

PRACTICAL INFORMATION:
- Parking: Available in town and at trailheads. Popular trailheads like Ramsey Canyon may fill up - arrive early
- Permits: Coronado National Forest - most trails require no permits for day use. Ramsey Canyon Preserve requires entrance fee. San Pedro Riparian Area - no permit required
- Best Times: Year-round - cooler than desert. Spring (March-May) and Fall (September-November) are ideal for birding and outdoor activities
- Weather: Four distinct seasons. Summer: 75-90°F (cooler than desert due to elevation). Winter: 45-65°F (excellent for outdoor). Spring/Fall: 60-75°F (ideal)
- Access: Highway 90 from Tucson (75 miles, 80 minutes) or Bisbee (25 miles, 35 minutes)
- Considerations: Elevation 4,600 feet - cooler than desert, but still warm in summer. World-class birding - bring binoculars and field guides. Ramsey Canyon Preserve requires entrance fee - check hours. Popular trailheads may fill up on weekends - arrive early. Gateway to Bisbee (25 miles), Tombstone (30 miles), and Patagonia (40 miles). Miller Peak is challenging - be prepared for significant elevation gain

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Sierra Vista's birding capital status and world-class birding opportunities
- Mention Huachuca Mountains recreation and Miller Peak (9,466 ft)
- Highlight Ramsey Canyon Preserve as world-renowned birding destination
- Emphasize year-round accessibility with cooler climate than desert
- Provide practical tips about parking, permits, best times, access, and birding preparation

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Sierra Vista-specific knowledge and context
- Enhanced recommendations based on Sierra Vista's unique birding capital and mountain recreation character
- Practical tips for visitors"""

