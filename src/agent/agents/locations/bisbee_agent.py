"""Bisbee, Arizona specialist agent.

This agent provides Bisbee-specific information and enhances existing agent outputs
with local knowledge about historic mining town, arts community, Mule Mountains, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Bisbee-specific knowledge base - Enhanced with detailed information
BISBEE_KNOWLEDGE = {
    "location": {
        "name": "Bisbee, Arizona",
        "coordinates": {"lat": 31.4482, "lon": -109.9284},
        "elevation": 5300,  # feet
        "region": "Cochise County, Arizona",
        "country": "US",
        "nickname": "Queen of the Copper Camps",
        "proximity": {
            "tombstone": {"distance_miles": 20, "direction": "northeast", "drive_time_minutes": 30},
            "sierra_vista": {"distance_miles": 25, "direction": "north", "drive_time_minutes": 35},
            "tucson": {"distance_miles": 95, "direction": "northwest", "drive_time_minutes": 100},
            "nogales": {"distance_miles": 60, "direction": "southwest", "drive_time_minutes": 70},
        },
    },
    "history": {
        "founded": 1880,
        "incorporated": 1902,
        "current_population": "~5,000 residents",
        "known_for": [
            "Historic mining town - 'Queen of the Copper Camps'",
            "Preserved Victorian architecture",
            "Thriving arts community",
            "Mule Mountains location",
            "Bisbee 1000 Stair Climb",
            "Queen Mine Tour",
        ],
        "historical_significance": "Founded as copper mining camp, became one of the richest mining towns in the West. Mining operations from 1880s-1970s. Revived as arts community and tourist destination.",
        "mining_era": {
            "start": 1880,
            "peak": "Early 1900s",
            "end": 1975,
            "production": "Over 8 billion pounds of copper, plus gold, silver, lead, zinc",
            "company": "Phelps Dodge Corporation",
        },
    },
    "geography": {
        "terrain": "Mountainous, historic hillside town",
        "topography": "Mule Mountains, narrow canyons, steep hillsides",
        "elevation": "5,300 feet",
        "climate": "Four distinct seasons, cooler than desert (5,300 feet elevation)",
        "features": [
            "Mule Mountains",
            "Historic hillside architecture",
            "Narrow streets and staircases",
            "Lavender Pit (former open-pit mine)",
        ],
        "ecosystem": "Mountain desert transitioning to pine-oak at higher elevations",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Trails in Mule Mountains with varied terrain from flowy singletrack to technical challenges",
            "famous_trails": [
                {
                    "name": "Mule Mountains Trail System",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": "Varies (multiple interconnected trails)",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Mule Mountains with varied terrain, technical sections, and scenic mountain views. Good for intermediate to advanced riders.",
                    "highlights": ["Mountain trails", "Technical sections", "Scenic views", "Varied terrain"],
                    "best_seasons": "Year-round (best Spring, Fall, Winter)",
                    "trailhead": "Various access points in Mule Mountains",
                    "features": ["Mountain trails", "Technical", "Scenic"],
                    "permits": "Coronado National Forest - no permit required for day use",
                },
            ],
            "difficulty_range": "Intermediate to expert",
            "best_seasons": "Year-round (best Spring, Fall, Winter) - cooler than desert",
            "trail_conditions": "Generally well-maintained, can be dusty in summer",
            "trail_features": ["Single track", "Technical sections", "Mountain scenery", "Elevation"],
        },
        "hiking": {
            "description": "Trails in Mule Mountains with scenic mountain views and historic sites",
            "famous_trails": [
                {
                    "name": "Bisbee 1000 Stair Climb",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": "4.5",
                    "elevation_gain_feet": 1000,
                    "description": "Iconic stair climb through historic Bisbee neighborhoods with 1,000+ steps, scenic city views, and historic architecture. Annual event in October.",
                    "highlights": [
                        "Iconic stair climb",
                        "Historic neighborhoods",
                        "Scenic city views",
                        "1,000+ steps",
                        "Annual event (October)",
                    ],
                    "best_seasons": "Year-round (annual event in October)",
                    "trailhead": "Various starting points in Bisbee",
                    "features": ["Stair climb", "Historic", "Scenic views", "Challenging"],
                    "permits": "No permit required",
                },
                {
                    "name": "Mule Mountains Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Mule Mountains with scenic mountain views and varied difficulty.",
                    "highlights": ["Mountain views", "Scenic", "Varied difficulty"],
                    "best_seasons": "Year-round",
                    "trailhead": "Various access points",
                    "features": ["Mountain trails", "Scenic", "Varied difficulty"],
                    "permits": "Coronado National Forest - no permit required",
                },
            ],
            "difficulty_range": "Easy to moderate",
            "best_seasons": "Year-round - cooler than desert",
            "trail_features": ["Mountain trails", "Historic sites", "Scenic views"],
        },
        "photography": {
            "description": "Historic architecture, mountain views, arts community, mining history offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Historic Downtown Bisbee",
                    "best_time": "Daylight hours, golden hour for architecture",
                    "subjects": "Victorian architecture, historic buildings, narrow streets, staircases",
                },
                {
                    "name": "Mule Mountains",
                    "best_time": "Sunrise and sunset for mountain views",
                    "subjects": "Mountain peaks, scenic overlooks, desert-mountain transition",
                },
                {
                    "name": "Lavender Pit Overlook",
                    "best_time": "Daylight hours",
                    "subjects": "Former open-pit mine, dramatic landscape, mining history",
                },
                {
                    "name": "Arts District",
                    "best_time": "Daylight hours",
                    "subjects": "Art galleries, murals, arts community, street scenes",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring wildflowers, fall colors, winter clarity",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Mule Mountains",
                "type": "Mountain Range",
                "description": "Scenic mountain range with trails and scenic views",
                "activities": ["Hiking", "Mountain biking", "Photography"],
            },
            {
                "name": "Lavender Pit",
                "type": "Historic Site",
                "description": "Former open-pit copper mine, dramatic landscape",
                "activities": ["Photography", "Historical tours", "Scenic views"],
            },
        ],
        "cultural": [
            {
                "name": "Queen Mine Tour",
                "type": "Historic Mine Tour",
                "description": "Underground mine tour in historic Queen Mine",
                "highlights": ["Underground tour", "Mining history", "Historic equipment"],
            },
            {
                "name": "Bisbee Mining & Historical Museum",
                "type": "Museum",
                "description": "Museum showcasing Bisbee's mining history and heritage",
            },
            {
                "name": "Arts District",
                "type": "Arts Community",
                "description": "Thriving arts community with galleries, studios, and festivals",
                "highlights": ["Art galleries", "Studios", "Festivals", "Murals"],
            },
            {
                "name": "Historic Downtown",
                "type": "Historic District",
                "description": "Preserved Victorian architecture, narrow streets, staircases",
                "highlights": ["Victorian architecture", "Historic buildings", "Narrow streets"],
            },
        ],
        "nearby": [
            {
                "name": "Tombstone",
                "distance": "20 miles",
                "description": "Iconic Wild West town, O.K. Corral, Boot Hill Cemetery",
            },
            {
                "name": "Sierra Vista",
                "distance": "25 miles",
                "description": "Huachuca Mountains, birding capital, gateway to wilderness",
            },
            {
                "name": "Cochise Stronghold",
                "distance": "40 miles",
                "description": "Historic site and recreation area in Dragoon Mountains",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Cafe Roka",
                "type": "Fine Dining",
                "description": "Upscale dining in historic building",
                "highlights": ["Fine dining", "Historic building", "Upscale"],
            },
            {
                "name": "Bisbee Breakfast Club",
                "type": "Breakfast",
                "description": "Local favorite for breakfast",
                "highlights": ["Local favorite", "Breakfast", "Casual"],
            },
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Bisbee offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Copper Queen Hotel",
                "type": "Historic Hotel",
                "description": "Historic hotel in downtown Bisbee",
                "highlights": ["Historic", "Downtown location", "Historic charm"],
            },
            {
                "name": "Various accommodations",
                "type": "Mixed",
                "description": "Multiple lodging options including B&Bs and historic hotels - use tools to find current options",
                "note": "Use search_accommodations tool for current lodging options",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in downtown and at trailheads. Historic downtown has limited parking - arrive early or walk",
        "permits": "Coronado National Forest - most trails require no permits for day use. Queen Mine Tour requires ticket purchase",
        "best_times": "Year-round - cooler than desert. Spring (March-May) and Fall (September-November) are ideal",
        "weather": {
            "summer": "Warm (75-90°F), cooler than desert due to elevation",
            "winter": "Mild (45-65°F), excellent for outdoor activities",
            "spring": "Pleasant (60-75°F), ideal for all activities",
            "fall": "Pleasant (60-75°F), ideal for all activities",
        },
        "access": "Highway 80 from Tucson (95 miles, 100 minutes) or Sierra Vista (25 miles, 35 minutes)",
        "considerations": [
            "Historic downtown has narrow streets and limited parking - walk or arrive early",
            "Steep hillsides and staircases - wear appropriate footwear",
            "Elevation 5,300 feet - cooler than desert, but still warm in summer",
            "Arts community - many galleries and studios to explore",
            "Mining history - Queen Mine Tour is popular, book in advance",
            "Gateway to Tombstone (20 miles) and Sierra Vista (25 miles)",
        ],
    },
}


class BisbeeAgent(LocationAgentBase):
    """Agent specialized in Bisbee, Arizona information and context.

    This agent enhances existing agent outputs with Bisbee-specific knowledge
    about historic mining town, arts community, Mule Mountains, and outdoor opportunities.
    """

    LOCATION_NAME = "Bisbee, Arizona"
    LOCATION_INDICATORS = [
        "bisbee",
        "bisbee, az",
        "bisbee, arizona",
        "bisbee az",
    ]
    AGENT_NAME = "bisbee_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Bisbee-specific knowledge base (fallback if external file not found)."""
        return BISBEE_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Bisbee agent."""
        return """You are a comprehensive guide for Bisbee, Arizona - the "Queen of the Copper Camps"
located in the Mule Mountains at 5,300 feet elevation, known for historic mining town, arts community, and unique hillside character.

Your role is to:
1. Use tools to gather real-time data about Bisbee (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Bisbee-specific knowledge from the knowledge base
4. Combine information from existing agents with Bisbee expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Bisbee, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Bisbee, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Bisbee, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Coronado National Forest - most trails require no permits)
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
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Bisbee, Arizona"
- Bisbee has trails in Mule Mountains with intermediate to advanced difficulty
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- Mention seasonal considerations (cooler than desert due to elevation)

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Bisbee, Arizona"
- Popular trails include Bisbee 1000 Stair Climb (4.5 miles, moderate/strenuous, 1,000+ steps, annual event in October) and Mule Mountains trails
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention the iconic Bisbee 1000 Stair Climb as unique attraction

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Key sites: Queen Mine Tour (underground mine tour), Bisbee Mining & Historical Museum, Historic Downtown (Victorian architecture), Arts District
- Enhance with knowledge base information about Bisbee's mining history and arts community revival
- Provide context about Bisbee's transformation from mining town to arts community

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Historic Downtown (daylight/golden hour), Mule Mountains (sunrise/sunset), Lavender Pit Overlook (daylight), Arts District (daylight)
- Mention seasonal opportunities (spring wildflowers, fall colors, winter clarity)

For Dining Queries:
- Use find_restaurants with location="Bisbee, Arizona"
- Enhance results with knowledge base businesses (Cafe Roka, Bisbee Breakfast Club)
- Provide context about arts community atmosphere

For Accommodation Queries:
- Use search_accommodations with location="Bisbee, Arizona"
- Enhance with knowledge base information (Copper Queen Hotel, B&Bs)
- Mention historic charm and downtown location

For Logistics Queries:
- Use get_parking_information (Historic downtown has limited parking - walk or arrive early)
- Provide information about permits (Coronado National Forest - most trails require no permits, Queen Mine Tour requires ticket)
- Mention Highway 80 access from Tucson (95 miles) and Sierra Vista (25 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Bisbee, Arizona",
  "overview": "Brief overview of Bisbee as historic mining town and arts community",
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

BISBEE'S UNIQUE CHARACTERISTICS:
- Historic mining town - "Queen of the Copper Camps" (1880-1975)
- Preserved Victorian architecture with narrow streets and staircases
- Thriving arts community with galleries, studios, and festivals
- Mule Mountains location (5,300 feet elevation - cooler than desert)
- Unique hillside character with steep streets and historic charm
- ~5,000 residents
- Gateway to Tombstone (20 miles) and Sierra Vista (25 miles)

KEY ATTRACTIONS:
- Queen Mine Tour: Underground mine tour in historic Queen Mine
- Bisbee Mining & Historical Museum: Mining history and heritage
- Historic Downtown: Preserved Victorian architecture, narrow streets, staircases
- Arts District: Thriving arts community with galleries, studios, festivals
- Mule Mountains: Scenic mountain range with trails
- Lavender Pit: Former open-pit mine, dramatic landscape
- Bisbee 1000 Stair Climb: Iconic 4.5-mile stair climb (annual event in October)

FAMOUS ACTIVITIES:
- Historic mine tours (Queen Mine Tour - underground tour)
- Mountain biking in Mule Mountains (intermediate to advanced)
- Hiking (Bisbee 1000 Stair Climb, Mule Mountains trails)
- Photography (historic architecture, mountain views, arts community)
- Arts community exploration (galleries, studios, festivals)

PRACTICAL INFORMATION:
- Parking: Available in downtown and at trailheads. Historic downtown has limited parking - arrive early or walk
- Permits: Coronado National Forest - most trails require no permits for day use. Queen Mine Tour requires ticket purchase
- Best Times: Year-round - cooler than desert. Spring (March-May) and Fall (September-November) are ideal
- Weather: Four distinct seasons. Summer: 75-90°F (cooler than desert due to elevation). Winter: 45-65°F (excellent for outdoor). Spring/Fall: 60-75°F (ideal)
- Access: Highway 80 from Tucson (95 miles, 100 minutes) or Sierra Vista (25 miles, 35 minutes)
- Considerations: Historic downtown has narrow streets and limited parking - walk or arrive early. Steep hillsides and staircases - wear appropriate footwear. Elevation 5,300 feet - cooler than desert, but still warm in summer. Arts community - many galleries and studios to explore. Mining history - Queen Mine Tour is popular, book in advance. Gateway to Tombstone (20 miles) and Sierra Vista (25 miles)

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Bisbee's historic mining character and arts community revival
- Mention unique hillside character with narrow streets and staircases
- Highlight Mule Mountains recreation opportunities
- Emphasize year-round accessibility with cooler climate than desert
- Provide practical tips about parking, permits, best times, access, and historic downtown navigation

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Bisbee-specific knowledge and context
- Enhanced recommendations based on Bisbee's unique historic mining town and arts community character
- Practical tips for visitors"""

