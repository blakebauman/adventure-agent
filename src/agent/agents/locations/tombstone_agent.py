"""Tombstone, Arizona specialist agent.

This agent provides Tombstone-specific information and enhances existing agent outputs
with local knowledge about Wild West history, historic preservation, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Tombstone-specific knowledge base - Enhanced with detailed information
TOMBSTONE_KNOWLEDGE = {
    "location": {
        "name": "Tombstone, Arizona",
        "coordinates": {"lat": 31.7129, "lon": -110.0676},
        "elevation": 4500,  # feet
        "region": "Cochise County, Arizona",
        "country": "US",
        "nickname": "The Town Too Tough to Die",
        "proximity": {
            "bisbee": {"distance_miles": 20, "direction": "southwest", "drive_time_minutes": 30},
            "sierra_vista": {"distance_miles": 30, "direction": "south", "drive_time_minutes": 40},
            "tucson": {"distance_miles": 70, "direction": "northwest", "drive_time_minutes": 75},
            "cochise_stronghold": {"distance_miles": 30, "direction": "northeast", "drive_time_minutes": 40},
        },
    },
    "history": {
        "founded": 1879,
        "incorporated": 1881,
        "current_population": "~1,300 residents",
        "known_for": [
            "Iconic Wild West history - 'The Town Too Tough to Die'",
            "O.K. Corral gunfight (1881)",
            "Authentic 1880s buildings",
            "Boot Hill Cemetery",
            "Historic preservation",
            "Tourist destination",
        ],
        "historical_significance": "Founded as silver mining camp, became one of the most famous Wild West towns. Site of legendary O.K. Corral gunfight (October 26, 1881) between Earp brothers/Doc Holliday and Clanton/McLaury factions. Preserved as historic tourist destination.",
        "famous_events": {
            "ok_corral": {
                "date": "October 26, 1881",
                "participants": "Earp brothers (Wyatt, Virgil, Morgan), Doc Holliday vs. Clanton/McLaury factions",
                "significance": "Most famous gunfight in Wild West history",
            },
        },
    },
    "geography": {
        "terrain": "Desert, rolling hills",
        "topography": "Sonoran Desert, Dragoon Mountains nearby",
        "elevation": "4,500 feet",
        "climate": "Desert climate, four distinct seasons, cooler than low desert",
        "features": [
            "Historic downtown (preserved 1880s buildings)",
            "Dragoon Mountains (nearby)",
            "Cochise Stronghold (30 miles)",
        ],
        "ecosystem": "Sonoran Desert with desert scrub vegetation",
    },
    "outdoor_activities": {
        "hiking": {
            "description": "Nearby hiking in Dragoon Mountains and Cochise Stronghold with scenic desert and mountain trails",
            "famous_trails": [
                {
                    "name": "Cochise Stronghold Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Cochise Stronghold (30 miles from Tombstone) with scenic desert and mountain views, historic significance, and varied difficulty.",
                    "highlights": [
                        "Historic site",
                        "Scenic desert and mountain views",
                        "Varied difficulty",
                        "Cochise Stronghold",
                    ],
                    "best_seasons": "Year-round (best Fall, Winter, Spring)",
                    "trailhead": "Cochise Stronghold (30 miles from Tombstone)",
                    "features": ["Historic", "Scenic", "Varied difficulty"],
                    "permits": "Coronado National Forest - no permit required",
                },
                {
                    "name": "Dragoon Mountains Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Dragoon Mountains with scenic desert and mountain views.",
                    "highlights": ["Mountain views", "Scenic", "Varied difficulty"],
                    "best_seasons": "Year-round",
                    "trailhead": "Various access points in Dragoon Mountains",
                    "features": ["Mountain trails", "Scenic", "Varied difficulty"],
                    "permits": "Coronado National Forest - no permit required",
                },
            ],
            "difficulty_range": "Easy to moderate",
            "best_seasons": "Year-round (best Fall, Winter, Spring)",
            "trail_features": ["Desert trails", "Mountain views", "Historic sites"],
        },
        "photography": {
            "description": "Wild West reenactments, historic buildings, Boot Hill Cemetery offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "O.K. Corral",
                    "best_time": "Daylight hours for reenactments",
                    "subjects": "Wild West reenactments, historic site, gunfight location",
                },
                {
                    "name": "Boot Hill Cemetery",
                    "best_time": "Daylight hours",
                    "subjects": "Historic cemetery, Wild West graves, historic markers",
                },
                {
                    "name": "Historic Downtown",
                    "best_time": "Daylight hours, golden hour for architecture",
                    "subjects": "Authentic 1880s buildings, Wild West architecture, historic streets",
                },
                {
                    "name": "Wild West Reenactments",
                    "best_time": "During scheduled reenactments",
                    "subjects": "Period costumes, gunfights, Wild West scenes",
                },
            ],
            "seasons": "Year-round, but reenactments are scheduled events - check schedules",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Dragoon Mountains",
                "type": "Mountain Range",
                "description": "Scenic mountain range with trails (nearby)",
                "activities": ["Hiking", "Photography"],
            },
            {
                "name": "Cochise Stronghold",
                "type": "Historic Site/Recreation Area",
                "description": "Historic site and recreation area in Dragoon Mountains (30 miles)",
                "activities": ["Hiking", "Photography", "Historical tours"],
            },
        ],
        "cultural": [
            {
                "name": "O.K. Corral",
                "type": "Historic Site",
                "description": "Site of legendary gunfight (October 26, 1881), reenactments, museum",
                "highlights": ["Historic gunfight site", "Reenactments", "Museum", "Most famous Wild West gunfight"],
            },
            {
                "name": "Boot Hill Cemetery",
                "type": "Historic Cemetery",
                "description": "Historic cemetery with Wild West graves and markers",
                "highlights": ["Historic graves", "Wild West history", "Historic markers"],
            },
            {
                "name": "Tombstone Courthouse State Historic Park",
                "type": "Historic Site",
                "description": "Historic courthouse and museum",
            },
            {
                "name": "Historic Downtown",
                "type": "Historic District",
                "description": "Authentic 1880s buildings, preserved Wild West architecture",
                "highlights": ["Authentic 1880s buildings", "Preserved architecture", "Wild West character"],
            },
            {
                "name": "Bird Cage Theatre",
                "type": "Historic Site",
                "description": "Historic theater and saloon",
            },
        ],
        "nearby": [
            {
                "name": "Bisbee",
                "distance": "20 miles",
                "description": "Historic mining town, arts community, Mule Mountains",
            },
            {
                "name": "Sierra Vista",
                "distance": "30 miles",
                "description": "Huachuca Mountains, birding capital, gateway to wilderness",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Big Nose Kate's Saloon",
                "type": "Saloon/Restaurant",
                "description": "Historic saloon with dining and entertainment",
                "highlights": ["Historic saloon", "Dining", "Entertainment", "Wild West atmosphere"],
            },
            {
                "name": "Tombstone Brewing Company",
                "type": "Brewery/Restaurant",
                "description": "Local brewery with dining",
                "highlights": ["Local brewery", "Dining", "Craft beer"],
            },
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Tombstone offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Tombstone Monument Ranch",
                "type": "Dude Ranch",
                "description": "Western-themed ranch with lodging",
                "highlights": ["Western theme", "Dude ranch", "Lodging"],
            },
            {
                "name": "Various accommodations",
                "type": "Mixed",
                "description": "Multiple lodging options including historic hotels and B&Bs - use tools to find current options",
                "note": "Use search_accommodations tool for current lodging options",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in historic downtown. Can be crowded during peak tourist season - arrive early",
        "permits": "Coronado National Forest - most trails require no permits for day use. Historic sites may require entrance fees",
        "best_times": "Year-round - cooler than low desert. Fall (September-November) and Spring (March-May) are ideal",
        "weather": {
            "summer": "Warm (80-95°F), cooler than low desert due to elevation",
            "winter": "Mild (50-70°F), excellent for outdoor activities",
            "spring": "Pleasant (65-80°F), ideal for all activities",
            "fall": "Pleasant (65-80°F), ideal for all activities",
        },
        "access": "Highway 80 from Tucson (70 miles, 75 minutes) or Bisbee (20 miles, 30 minutes)",
        "considerations": [
            "Historic downtown can be crowded during peak tourist season - arrive early",
            "Wild West reenactments are scheduled events - check schedules",
            "Elevation 4,500 feet - cooler than low desert, but still warm in summer",
            "Historic sites may require entrance fees",
            "Gateway to Bisbee (20 miles) and Sierra Vista (30 miles)",
            "Cochise Stronghold is 30 miles away for hiking",
        ],
    },
}


class TombstoneAgent(LocationAgentBase):
    """Agent specialized in Tombstone, Arizona information and context.

    This agent enhances existing agent outputs with Tombstone-specific knowledge
    about Wild West history, historic preservation, and outdoor opportunities.
    """

    LOCATION_NAME = "Tombstone, Arizona"
    LOCATION_INDICATORS = [
        "tombstone",
        "tombstone, az",
        "tombstone, arizona",
        "tombstone az",
        "ok corral",
        "ok corral, az",
    ]
    AGENT_NAME = "tombstone_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Tombstone-specific knowledge base (fallback if external file not found)."""
        return TOMBSTONE_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Tombstone agent."""
        return """You are a comprehensive guide for Tombstone, Arizona - "The Town Too Tough to Die"
located at 4,500 feet elevation, known for iconic Wild West history, O.K. Corral gunfight, and historic preservation.

Your role is to:
1. Use tools to gather real-time data about Tombstone (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Tombstone-specific knowledge from the knowledge base
4. Combine information from existing agents with Tombstone expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Tombstone, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Tombstone, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Coronado National Forest - most trails require no permits)
- Include trail connectivity and route planning details
- Mention nearby Cochise Stronghold (30 miles) for additional hiking

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
- Use search_trails with activity_type="hiking" and location="Tombstone, Arizona"
- Popular nearby trails include Cochise Stronghold Trails (30 miles away) and Dragoon Mountains trails
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention Cochise Stronghold as nearby historic site and recreation area

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Key sites: O.K. Corral (most famous Wild West gunfight, October 26, 1881), Boot Hill Cemetery, Tombstone Courthouse State Historic Park, Historic Downtown (authentic 1880s buildings), Bird Cage Theatre
- Enhance with knowledge base information about Tombstone's Wild West history and historic preservation
- Provide context about O.K. Corral gunfight and Wild West reenactments

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: O.K. Corral (daylight for reenactments), Boot Hill Cemetery (daylight), Historic Downtown (daylight/golden hour), Wild West Reenactments (during scheduled events)
- Mention that reenactments are scheduled events - check schedules

For Dining Queries:
- Use find_restaurants with location="Tombstone, Arizona"
- Enhance results with knowledge base businesses (Big Nose Kate's Saloon, Tombstone Brewing Company)
- Provide context about Wild West atmosphere

For Accommodation Queries:
- Use search_accommodations with location="Tombstone, Arizona"
- Enhance with knowledge base information (Tombstone Monument Ranch, historic hotels, B&Bs)
- Mention Wild West theme and historic charm

For Logistics Queries:
- Use get_parking_information (Historic downtown can be crowded during peak tourist season - arrive early)
- Provide information about permits (Coronado National Forest - most trails require no permits, historic sites may require entrance fees)
- Mention Highway 80 access from Tucson (70 miles) and Bisbee (20 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Tombstone, Arizona",
  "overview": "Brief overview of Tombstone as iconic Wild West town",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
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

TOMBSTONE'S UNIQUE CHARACTERISTICS:
- Iconic Wild West history - "The Town Too Tough to Die"
- O.K. Corral gunfight (October 26, 1881) - most famous gunfight in Wild West history
- Authentic 1880s buildings preserved as historic district
- Tourist destination with Wild West reenactments
- Boot Hill Cemetery with historic Wild West graves
- ~1,300 residents
- Gateway to Bisbee (20 miles) and Sierra Vista (30 miles)

KEY ATTRACTIONS:
- O.K. Corral: Site of legendary gunfight (October 26, 1881), reenactments, museum
- Boot Hill Cemetery: Historic cemetery with Wild West graves and markers
- Tombstone Courthouse State Historic Park: Historic courthouse and museum
- Historic Downtown: Authentic 1880s buildings, preserved Wild West architecture
- Bird Cage Theatre: Historic theater and saloon
- Cochise Stronghold: Historic site and recreation area in Dragoon Mountains (30 miles)

FAMOUS ACTIVITIES:
- Historic walking tours (authentic 1880s buildings, Wild West history)
- Wild West reenactments (scheduled events - check schedules)
- Photography (Wild West reenactments, historic buildings, Boot Hill Cemetery)
- Nearby hiking (Cochise Stronghold - 30 miles, Dragoon Mountains)

PRACTICAL INFORMATION:
- Parking: Available in historic downtown. Can be crowded during peak tourist season - arrive early
- Permits: Coronado National Forest - most trails require no permits for day use. Historic sites may require entrance fees
- Best Times: Year-round - cooler than low desert. Fall (September-November) and Spring (March-May) are ideal
- Weather: Four distinct seasons. Summer: 80-95°F (cooler than low desert due to elevation). Winter: 50-70°F (excellent for outdoor). Spring/Fall: 65-80°F (ideal)
- Access: Highway 80 from Tucson (70 miles, 75 minutes) or Bisbee (20 miles, 30 minutes)
- Considerations: Historic downtown can be crowded during peak tourist season - arrive early. Wild West reenactments are scheduled events - check schedules. Elevation 4,500 feet - cooler than low desert, but still warm in summer. Historic sites may require entrance fees. Gateway to Bisbee (20 miles) and Sierra Vista (30 miles). Cochise Stronghold is 30 miles away for hiking

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Tombstone's iconic Wild West history and O.K. Corral gunfight
- Mention historic preservation and authentic 1880s buildings
- Highlight nearby hiking opportunities (Cochise Stronghold, Dragoon Mountains)
- Emphasize year-round accessibility with cooler climate than low desert
- Provide practical tips about parking, permits, best times, access, and historic site schedules

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Tombstone-specific knowledge and context
- Enhanced recommendations based on Tombstone's unique Wild West history and historic preservation character
- Practical tips for visitors"""

