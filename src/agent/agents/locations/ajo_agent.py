"""Ajo, Arizona specialist agent.

This agent provides Ajo-specific information and enhances existing agent outputs
with local knowledge about Organ Pipe Cactus National Monument, desert wilderness, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Ajo-specific knowledge base - Enhanced with detailed information
AJO_KNOWLEDGE = {
    "location": {
        "name": "Ajo, Arizona",
        "coordinates": {"lat": 32.3717, "lon": -112.8606},
        "elevation": 1700,  # feet
        "region": "Pima County, Arizona",
        "country": "US",
        "nickname": "Gateway to Organ Pipe Cactus National Monument",
        "proximity": {
            "organ_pipe": {"distance_miles": 15, "direction": "south", "drive_time_minutes": 20},
            "tucson": {"distance_miles": 120, "direction": "east", "drive_time_minutes": 130},
            "phoenix": {"distance_miles": 140, "direction": "northeast", "drive_time_minutes": 150},
        },
    },
    "history": {
        "founded": 1847,
        "current_population": "~3,000 residents",
        "known_for": [
            "Organ Pipe Cactus National Monument gateway",
            "Desert wilderness",
            "Historic mining town",
            "Sonoran Desert",
            "Border region",
        ],
        "historical_significance": "Founded as mining town, now gateway to Organ Pipe Cactus National Monument",
    },
    "geography": {
        "terrain": "Desert",
        "topography": "Sonoran Desert, Organ Pipe Cactus National Monument",
        "elevation": "1,700 feet",
        "climate": "Hot desert climate, very hot summers, mild winters",
        "features": [
            "Organ Pipe Cactus National Monument",
            "Sonoran Desert",
            "Desert wilderness",
        ],
        "ecosystem": "Sonoran Desert with unique cacti and desert wildlife",
    },
    "outdoor_activities": {
        "hiking": {
            "description": "Trails in Organ Pipe Cactus National Monument and surrounding desert with scenic desert views",
            "famous_trails": [
                {
                    "name": "Organ Pipe Cactus National Monument Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Organ Pipe Cactus National Monument with scenic desert views and unique cacti.",
                    "highlights": ["Desert scenery", "Organ Pipe Cactus", "Unique cacti", "Desert wildlife"],
                    "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
                    "trailhead": "Organ Pipe Cactus National Monument Visitor Center",
                    "features": ["Desert trails", "Scenic", "Unique cacti"],
                    "permits": "Organ Pipe Cactus National Monument - entrance fee required",
                },
            ],
            "difficulty_range": "Easy to moderate",
            "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
            "trail_features": ["Desert trails", "Scenic views", "Unique cacti"],
        },
        "photography": {
            "description": "Organ Pipe Cactus, Sonoran Desert, desert landscapes offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Organ Pipe Cactus National Monument",
                    "best_time": "Daylight hours, golden hour for scenic shots",
                    "subjects": "Organ Pipe Cactus, desert landscapes, unique cacti",
                },
                {
                    "name": "Sonoran Desert",
                    "best_time": "Golden hour for scenic desert shots",
                    "subjects": "Desert scenery, cacti, desert wildlife",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring wildflowers, winter clarity",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Organ Pipe Cactus National Monument",
                "type": "National Monument",
                "description": "330,000 acres of Sonoran Desert with unique Organ Pipe Cactus",
                "activities": ["Hiking", "Photography", "Wildlife viewing", "Desert exploration"],
            },
            {
                "name": "Sonoran Desert",
                "type": "Desert",
                "description": "Unique desert ecosystem with diverse cacti and wildlife",
                "activities": ["All desert activities"],
            },
        ],
        "cultural": [
            {
                "name": "Historic Downtown",
                "type": "Historic District",
                "description": "Small historic mining town with preserved architecture",
                "highlights": ["Historic architecture", "Mining history", "Small town charm"],
            },
        ],
        "nearby": [
            {
                "name": "Tucson",
                "distance": "120 miles",
                "description": "Major city, Sonoran Desert, Saguaro National Park",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Ajo offers several local dining options - use tools to find current restaurants",
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
        "parking": "Available in downtown and at Organ Pipe Cactus National Monument Visitor Center",
        "permits": "Organ Pipe Cactus National Monument - entrance fee required. Most trails require no additional permits",
        "best_times": "Fall (September-November), Winter (December-February), Spring (March-May) - avoid summer heat",
        "weather": {
            "summer": "Very hot (95-115°F), avoid midday heat for outdoor activities",
            "winter": "Mild (60-75°F), excellent for outdoor activities",
            "spring": "Pleasant (75-90°F), ideal for all activities",
            "fall": "Pleasant (75-90°F), ideal for all activities",
        },
        "access": "Highway 85 from Tucson (120 miles) or Phoenix (140 miles)",
        "considerations": [
            "Very hot in summer - plan activities for early morning or evening",
            "Organ Pipe Cactus National Monument requires entrance fee",
            "Desert wilderness - carry plenty of water, be prepared",
            "Border region - be aware of border security",
            "Gateway to Organ Pipe Cactus National Monument (15 miles)",
        ],
    },
}


class AjoAgent(LocationAgentBase):
    """Agent specialized in Ajo, Arizona information and context.

    This agent enhances existing agent outputs with Ajo-specific knowledge
    about Organ Pipe Cactus National Monument, desert wilderness, and outdoor opportunities.
    """

    LOCATION_NAME = "Ajo, Arizona"
    LOCATION_INDICATORS = [
        "ajo",
        "ajo, az",
        "ajo, arizona",
        "ajo az",
        "organ pipe",
        "organ pipe cactus",
    ]
    AGENT_NAME = "ajo_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Ajo-specific knowledge base (fallback if external file not found)."""
        return AJO_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Ajo agent."""
        return """You are a comprehensive guide for Ajo, Arizona - the "Gateway to Organ Pipe Cactus National Monument"
located at 1,700 feet elevation, known for Organ Pipe Cactus National Monument, desert wilderness, and Sonoran Desert.

Your role is to:
1. Use tools to gather real-time data about Ajo (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Ajo-specific knowledge from the knowledge base
4. Combine information from existing agents with Ajo expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Ajo, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Ajo, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Organ Pipe Cactus National Monument requires entrance fee)
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
- Safety considerations (extreme heat in summer, desert wilderness)
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Ajo, Arizona"
- Popular trails include Organ Pipe Cactus National Monument trails
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- CRITICAL: Mention extreme heat in summer - hike early morning or evening only
- Mention Organ Pipe Cactus National Monument entrance fee requirement

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Organ Pipe Cactus National Monument (daylight/golden hour), Sonoran Desert (golden hour)
- Mention unique Organ Pipe Cactus and desert wildlife photography opportunities

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Key sites: Historic Downtown (preserved mining town architecture), Historic Mining Sites
- Enhance with knowledge base information about Ajo's mining history

For Dining Queries:
- Use find_restaurants with location="Ajo, Arizona"
- Provide context about small town charm

For Accommodation Queries:
- Use search_accommodations with location="Ajo, Arizona"
- Mention proximity to Organ Pipe Cactus National Monument

For Logistics Queries:
- Use get_parking_information (Organ Pipe Cactus National Monument Visitor Center has parking)
- Provide information about permits (Organ Pipe Cactus National Monument - entrance fee required)
- Mention Highway 85 access from Tucson (120 miles) and Phoenix (140 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Ajo, Arizona",
  "overview": "Brief overview of Ajo as Organ Pipe Cactus National Monument gateway",
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

AJO'S UNIQUE CHARACTERISTICS:
- Gateway to Organ Pipe Cactus National Monument (15 miles) - 330,000 acres of Sonoran Desert
- Desert wilderness - unique Organ Pipe Cactus and desert wildlife
- Historic mining town - preserved architecture
- Sonoran Desert - unique desert ecosystem
- Elevation: 1,700 feet (very hot in summer)
- ~3,000 residents
- Gateway to Tucson (120 miles) and Phoenix (140 miles)

KEY ATTRACTIONS:
- Organ Pipe Cactus National Monument: 330,000 acres of Sonoran Desert with unique Organ Pipe Cactus
- Sonoran Desert: Unique desert ecosystem with diverse cacti and wildlife
- Historic Downtown: Small historic mining town with preserved architecture

FAMOUS ACTIVITIES:
- Hiking in Organ Pipe Cactus National Monument (easy to moderate)
- Photography (Organ Pipe Cactus, Sonoran Desert, desert landscapes)
- Desert exploration and wildlife viewing

PRACTICAL INFORMATION:
- Parking: Available in downtown and at Organ Pipe Cactus National Monument Visitor Center
- Permits: Organ Pipe Cactus National Monument - entrance fee required. Most trails require no additional permits
- Best Times: Fall (September-November), Winter (December-February), Spring (March-May) - avoid summer heat
- Weather: Hot desert climate. Summer: 95-115°F (avoid midday heat for outdoor activities). Winter: 60-75°F (excellent for outdoor). Spring/Fall: 75-90°F (ideal)
- Access: Highway 85 from Tucson (120 miles) or Phoenix (140 miles)
- Considerations: Very hot in summer - plan activities for early morning or evening. Organ Pipe Cactus National Monument requires entrance fee. Desert wilderness - carry plenty of water, be prepared. Border region - be aware of border security. Gateway to Organ Pipe Cactus National Monument (15 miles)

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Ajo's Organ Pipe Cactus National Monument gateway character
- Mention unique Organ Pipe Cactus and desert wildlife
- Highlight desert wilderness opportunities
- Emphasize seasonal considerations (extreme summer heat)
- Provide practical tips about parking, permits, best times, access, and desert safety

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Ajo-specific knowledge and context
- Enhanced recommendations based on Ajo's unique Organ Pipe Cactus National Monument gateway character
- Practical tips for visitors"""

