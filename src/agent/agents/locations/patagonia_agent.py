"""Patagonia, Arizona specialist agent.

This agent provides Patagonia-specific information and enhances existing agent outputs
with local knowledge about birding destination, Sonoita Creek, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Patagonia-specific knowledge base - Enhanced with detailed information
PATAGONIA_KNOWLEDGE = {
    "location": {
        "name": "Patagonia, Arizona",
        "coordinates": {"lat": 31.5401, "lon": -110.7501},
        "elevation": 4000,  # feet
        "region": "Santa Cruz County, Arizona",
        "country": "US",
        "nickname": "Birding Capital of Arizona",
        "proximity": {
            "nogales": {"distance_miles": 18, "direction": "south", "drive_time_minutes": 25},
            "sierra_vista": {"distance_miles": 40, "direction": "east", "drive_time_minutes": 50},
            "tucson": {"distance_miles": 60, "direction": "north", "drive_time_minutes": 70},
            "sonoita": {"distance_miles": 10, "direction": "north", "drive_time_minutes": 15},
        },
    },
    "history": {
        "founded": "Late 1800s",
        "current_population": "~900 residents",
        "known_for": [
            "World-renowned birding destination",
            "Patagonia-Sonoita Creek Preserve",
            "Small town charm",
            "Artsy community",
            "Sonoita Creek riparian area",
            "Patagonia Lake State Park",
        ],
        "historical_significance": "Founded as ranching and mining community, evolved into birding destination and small artsy town",
    },
    "geography": {
        "terrain": "Desert, riparian, rolling hills",
        "topography": "Sonoran Desert, Sonoita Creek, Patagonia Mountains",
        "elevation": "4,000 feet",
        "climate": "Desert climate, four distinct seasons, cooler than low desert",
        "features": [
            "Sonoita Creek (riparian area)",
            "Patagonia-Sonoita Creek Preserve",
            "Patagonia Lake State Park",
            "Patagonia Mountains",
        ],
        "ecosystem": "Sonoran Desert with riparian areas along Sonoita Creek, important bird habitat",
    },
    "outdoor_activities": {
        "hiking": {
            "description": "Trails in Patagonia-Sonoita Creek Preserve and Patagonia Lake State Park with scenic riparian and desert trails",
            "famous_trails": [
                {
                    "name": "Patagonia-Sonoita Creek Preserve Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Patagonia-Sonoita Creek Preserve with easy to moderate difficulty, excellent birding opportunities, and scenic riparian views. World-renowned birding destination.",
                    "highlights": [
                        "World-renowned birding",
                        "Riparian area",
                        "Easy to moderate",
                        "Birding opportunities",
                        "Scenic riparian views",
                    ],
                    "best_seasons": "Year-round (best Spring, Fall for birding)",
                    "trailhead": "Patagonia-Sonoita Creek Preserve",
                    "features": ["Birding", "Riparian", "Scenic", "Easy to moderate"],
                    "permits": "Patagonia-Sonoita Creek Preserve - entrance fee required",
                },
                {
                    "name": "Patagonia Lake State Park Trails",
                    "difficulty": "Easy",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Minimal",
                    "description": "Easy trails in Patagonia Lake State Park with scenic lake views and birding opportunities.",
                    "highlights": ["Lake views", "Easy", "Birding opportunities", "Scenic"],
                    "best_seasons": "Year-round",
                    "trailhead": "Patagonia Lake State Park",
                    "features": ["Lake trails", "Easy", "Scenic"],
                    "permits": "Patagonia Lake State Park - entrance fee required",
                },
            ],
            "difficulty_range": "Easy to moderate",
            "best_seasons": "Year-round (best Spring, Fall for birding)",
            "trail_features": ["Riparian trails", "Birding", "Scenic views", "Lake trails"],
        },
        "birding": {
            "description": "World-renowned birding in Patagonia-Sonoita Creek Preserve, Patagonia Lake State Park, and Sonoita Creek riparian area",
            "locations": [
                {
                    "name": "Patagonia-Sonoita Creek Preserve",
                    "type": "Preserve",
                    "species": "Trogons, warblers, tanagers, flycatchers, riparian birds",
                    "description": "World-renowned birding destination with excellent riparian bird viewing and diverse bird species",
                    "seasons": "Year-round, best in Spring and Fall migration",
                    "highlights": ["Trogons", "World-renowned", "Riparian birds", "Diverse species"],
                },
                {
                    "name": "Patagonia Lake State Park",
                    "type": "State Park",
                    "species": "Waterfowl, warblers, flycatchers, riparian birds",
                    "description": "Lake and riparian area with excellent birding opportunities",
                    "seasons": "Year-round, best in Spring and Fall migration",
                    "highlights": ["Waterfowl", "Riparian birds", "Migration stopover"],
                },
                {
                    "name": "Sonoita Creek Riparian Area",
                    "type": "Riparian Area",
                    "species": "Riparian birds, warblers, flycatchers",
                    "description": "Riparian area along Sonoita Creek with excellent birding",
                    "seasons": "Year-round, best in Spring and Fall",
                    "highlights": ["Riparian birds", "Diverse species"],
                },
            ],
            "seasons": "Year-round, best in Spring and Fall migration",
            "permits": "Patagonia-Sonoita Creek Preserve - entrance fee required. Patagonia Lake State Park - entrance fee required",
        },
        "mountain_biking": {
            "description": "Limited mountain biking opportunities in Patagonia area. Nearby trails in Patagonia Mountains and Coronado National Forest",
            "famous_trails": [
                {
                    "name": "Nearby Patagonia Mountains Trails",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in nearby Patagonia Mountains and Coronado National Forest with varied terrain.",
                    "highlights": ["Mountain trails", "Varied terrain", "Nearby"],
                    "best_seasons": "Year-round",
                    "trailhead": "Various access points in Patagonia Mountains",
                    "features": ["Mountain trails", "Varied difficulty"],
                    "permits": "Coronado National Forest - no permit required",
                    "note": "Use tools to find current mountain biking opportunities",
                },
            ],
            "difficulty_range": "Intermediate to expert",
            "best_seasons": "Year-round",
            "note": "Patagonia is primarily a birding destination. For extensive mountain biking, consider nearby areas or use tools to find current opportunities.",
        },
        "photography": {
            "description": "Wildlife, birding, riparian areas, lake scenery offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Patagonia-Sonoita Creek Preserve",
                    "best_time": "Early morning for birding, golden hour for scenic shots",
                    "subjects": "Birds, wildlife, riparian scenery, trogons",
                },
                {
                    "name": "Patagonia Lake State Park",
                    "best_time": "Early morning for birding, golden hour for lake shots",
                    "subjects": "Lake scenery, waterfowl, riparian birds, wildlife",
                },
                {
                    "name": "Sonoita Creek Riparian Area",
                    "best_time": "Early morning for birding, golden hour for scenic shots",
                    "subjects": "Riparian birds, wildlife, creek scenery",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring migration, fall colors, winter clarity",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Patagonia-Sonoita Creek Preserve",
                "type": "Preserve",
                "description": "World-renowned birding destination with excellent riparian bird viewing",
                "activities": ["Birding", "Hiking", "Photography", "Wildlife viewing"],
            },
            {
                "name": "Patagonia Lake State Park",
                "type": "State Park",
                "description": "Lake and riparian area with excellent birding and recreation",
                "activities": ["Birding", "Hiking", "Photography", "Fishing", "Boating"],
            },
            {
                "name": "Sonoita Creek",
                "type": "Riparian Area",
                "description": "Riparian area with excellent birding and wildlife viewing",
                "activities": ["Birding", "Hiking", "Photography", "Wildlife viewing"],
            },
            {
                "name": "Patagonia Mountains",
                "type": "Mountain Range",
                "description": "Scenic mountain range with trails (nearby)",
                "activities": ["Hiking", "Mountain biking", "Photography"],
            },
        ],
        "cultural": [
            {
                "name": "Historic Downtown",
                "type": "Historic District",
                "description": "Small town with artsy community, galleries, and shops",
                "highlights": ["Artsy community", "Galleries", "Small town charm"],
            },
        ],
        "nearby": [
            {
                "name": "Nogales",
                "distance": "18 miles",
                "description": "Border town, international border with Mexico",
            },
            {
                "name": "Sierra Vista",
                "distance": "40 miles",
                "description": "Huachuca Mountains, birding capital, gateway to wilderness",
            },
            {
                "name": "Sonoita",
                "distance": "10 miles",
                "description": "Wine country, rolling hills, scenic beauty",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Patagonia offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Various accommodations",
                "type": "Mixed",
                "description": "Multiple lodging options including B&Bs - use tools to find current options",
                "note": "Use search_accommodations tool for current lodging options",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in town and at preserves/parks. Popular birding areas may fill up - arrive early",
        "permits": "Patagonia-Sonoita Creek Preserve - entrance fee required. Patagonia Lake State Park - entrance fee required. Coronado National Forest - no permit required",
        "best_times": "Year-round - cooler than low desert. Spring (March-May) and Fall (September-November) are ideal for birding",
        "weather": {
            "summer": "Warm (75-90°F), cooler than low desert due to elevation",
            "winter": "Mild (50-70°F), excellent for outdoor activities",
            "spring": "Pleasant (60-75°F), ideal for all activities and birding",
            "fall": "Pleasant (60-75°F), ideal for all activities and birding",
        },
        "access": "Highway 82 from Nogales (18 miles, 25 minutes) or Tucson (60 miles, 70 minutes)",
        "considerations": [
            "World-renowned birding - bring binoculars and field guides",
            "Patagonia-Sonoita Creek Preserve requires entrance fee - check hours",
            "Patagonia Lake State Park requires entrance fee",
            "Popular birding areas may fill up - arrive early",
            "Small town - limited services, plan accordingly",
            "Gateway to Nogales (18 miles), Sierra Vista (40 miles), and Sonoita (10 miles)",
        ],
    },
}


class PatagoniaAgent(LocationAgentBase):
    """Agent specialized in Patagonia, Arizona information and context.

    This agent enhances existing agent outputs with Patagonia-specific knowledge
    about birding destination, Sonoita Creek, and outdoor opportunities.
    """

    LOCATION_NAME = "Patagonia, Arizona"
    LOCATION_INDICATORS = [
        "patagonia",
        "patagonia, az",
        "patagonia, arizona",
        "patagonia az",
    ]
    AGENT_NAME = "patagonia_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Patagonia-specific knowledge base (fallback if external file not found)."""
        return PATAGONIA_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Patagonia agent."""
        return """You are a comprehensive guide for Patagonia, Arizona - the "Birding Capital of Arizona"
located at 4,000 feet elevation, known for world-renowned birding, Sonoita Creek, and small town charm.

Your role is to:
1. Use tools to gather real-time data about Patagonia (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Patagonia-specific knowledge from the knowledge base
4. Combine information from existing agents with Patagonia expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Patagonia, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Patagonia, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Patagonia, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Patagonia-Sonoita Creek Preserve and Patagonia Lake State Park require entrance fees)
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

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Patagonia, Arizona"
- Popular trails include Patagonia-Sonoita Creek Preserve Trails (easy/moderate, world-renowned birding) and Patagonia Lake State Park Trails (easy, lake views)
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention world-class birding opportunities in Patagonia-Sonoita Creek Preserve

For Birding Queries:
- Patagonia is "Birding Capital of Arizona" with world-renowned birding
- Key locations: Patagonia-Sonoita Creek Preserve (world-renowned, entrance fee required), Patagonia Lake State Park (entrance fee required), Sonoita Creek riparian area
- Best seasons: Year-round, best in Spring and Fall migration
- Mention bringing binoculars and field guides
- Highlight trogons, warblers, tanagers, and other riparian birds

For Mountain Biking Queries:
- Use search_trails with activity_type="mountain_biking" and location="Patagonia, Arizona"
- Patagonia is primarily a birding destination - limited mountain biking opportunities in town
- Nearby trails in Patagonia Mountains and Coronado National Forest
- Mention that for extensive mountain biking, consider nearby areas or use tools to find current opportunities

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Patagonia-Sonoita Creek Preserve (early morning for birding, golden hour for scenic), Patagonia Lake State Park (early morning for birding, golden hour for lake shots), Sonoita Creek riparian area (early morning for birding, golden hour)
- Mention seasonal opportunities (spring migration, fall colors, winter clarity)

For Dining Queries:
- Use find_restaurants with location="Patagonia, Arizona"
- Provide context about small town with limited services

For Accommodation Queries:
- Use search_accommodations with location="Patagonia, Arizona"
- Mention small town with limited lodging options, B&Bs available

For Logistics Queries:
- Use get_parking_information (Popular birding areas may fill up - arrive early)
- Provide information about permits (Patagonia-Sonoita Creek Preserve and Patagonia Lake State Park require entrance fees)
- Mention Highway 82 access from Nogales (18 miles) and Tucson (60 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Patagonia, Arizona",
  "overview": "Brief overview of Patagonia as birding capital and small town",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
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

PATAGONIA'S UNIQUE CHARACTERISTICS:
- World-renowned birding destination - "Birding Capital of Arizona"
- Patagonia-Sonoita Creek Preserve (world-renowned birding)
- Small town charm (~900 residents)
- Artsy community with galleries and shops
- Sonoita Creek riparian area (important bird habitat)
- Patagonia Lake State Park
- Elevation: 4,000 feet (cooler than low desert)
- Gateway to Nogales (18 miles), Sierra Vista (40 miles), and Sonoita (10 miles)

KEY ATTRACTIONS:
- Patagonia-Sonoita Creek Preserve: World-renowned birding destination with excellent riparian bird viewing
- Patagonia Lake State Park: Lake and riparian area with excellent birding and recreation
- Sonoita Creek: Riparian area with excellent birding and wildlife viewing
- Historic Downtown: Small town with artsy community, galleries, and shops
- Patagonia Mountains: Scenic mountain range with trails (nearby)

FAMOUS ACTIVITIES:
- Birding (world-renowned - Patagonia-Sonoita Creek Preserve, Patagonia Lake State Park, Sonoita Creek)
- Hiking (Patagonia-Sonoita Creek Preserve, Patagonia Lake State Park)
- Wildlife photography (birds, wildlife, riparian areas, lake scenery)

PRACTICAL INFORMATION:
- Parking: Available in town and at preserves/parks. Popular birding areas may fill up - arrive early
- Permits: Patagonia-Sonoita Creek Preserve - entrance fee required. Patagonia Lake State Park - entrance fee required. Coronado National Forest - no permit required
- Best Times: Year-round - cooler than low desert. Spring (March-May) and Fall (September-November) are ideal for birding
- Weather: Four distinct seasons. Summer: 75-90°F (cooler than low desert due to elevation). Winter: 50-70°F (excellent for outdoor). Spring/Fall: 60-75°F (ideal)
- Access: Highway 82 from Nogales (18 miles, 25 minutes) or Tucson (60 miles, 70 minutes)
- Considerations: World-renowned birding - bring binoculars and field guides. Patagonia-Sonoita Creek Preserve requires entrance fee - check hours. Patagonia Lake State Park requires entrance fee. Popular birding areas may fill up - arrive early. Small town - limited services, plan accordingly. Gateway to Nogales (18 miles), Sierra Vista (40 miles), and Sonoita (10 miles)

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Patagonia's world-renowned birding status and "Birding Capital of Arizona" designation
- Mention Patagonia-Sonoita Creek Preserve as world-renowned birding destination
- Highlight Sonoita Creek riparian area as important bird habitat
- Emphasize small town charm and artsy community
- Provide practical tips about parking, permits, best times, access, and birding preparation

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Patagonia-specific knowledge and context
- Enhanced recommendations based on Patagonia's unique birding capital and small town character
- Practical tips for visitors"""

