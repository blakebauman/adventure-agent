"""Kingman, Arizona specialist agent.

This agent provides Kingman-specific information and enhances existing agent outputs
with local knowledge about Route 66, Grand Canyon West gateway, Hualapai Mountains, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Kingman-specific knowledge base - Enhanced with detailed information
KINGMAN_KNOWLEDGE = {
    "location": {
        "name": "Kingman, Arizona",
        "coordinates": {"lat": 35.1894, "lon": -114.0530},
        "elevation": 3300,  # feet
        "region": "Mohave County, Arizona",
        "country": "US",
        "nickname": "Heart of Historic Route 66",
        "proximity": {
            "grand_canyon_west": {"distance_miles": 70, "direction": "north", "drive_time_minutes": 90},
            "lake_havasu": {"distance_miles": 60, "direction": "south", "drive_time_minutes": 70},
            "las_vegas": {"distance_miles": 100, "direction": "northwest", "drive_time_minutes": 110},
            "flagstaff": {"distance_miles": 150, "direction": "east", "drive_time_minutes": 160},
        },
    },
    "history": {
        "founded": 1882,
        "incorporated": 1952,
        "current_population": "~30,000 residents",
        "known_for": [
            "Historic Route 66",
            "Gateway to Grand Canyon West",
            "Hualapai Mountains",
            "Route 66 Museum",
            "Historic downtown",
            "Mining history",
        ],
        "historical_significance": "Founded as railroad town, became major Route 66 stop and gateway to Grand Canyon West",
    },
    "geography": {
        "terrain": "Desert, mountains",
        "topography": "Mojave Desert, Hualapai Mountains",
        "elevation": "3,300 feet",
        "climate": "Desert climate, hot summers, mild winters",
        "features": [
            "Hualapai Mountains (highest peak: 8,417 ft)",
            "Historic Route 66",
            "Mojave Desert",
        ],
        "ecosystem": "Desert with mountain transition zones",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Trails in Hualapai Mountains and surrounding desert with varied terrain from flowy singletrack to technical challenges",
            "famous_trails": [
                {
                    "name": "Hualapai Mountain Park Trails",
                    "difficulty": "Beginner to Advanced",
                    "length_miles": "Varies (multiple interconnected trails)",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Hualapai Mountain Park with trails for all skill levels. Well-maintained singletrack with scenic mountain and desert views.",
                    "highlights": ["Mountain trails", "All skill levels", "Well-maintained", "Scenic views"],
                    "best_seasons": "Year-round (best Fall, Winter, Spring)",
                    "trailhead": "Hualapai Mountain Park",
                    "features": ["Mountain trails", "Varied difficulty", "Scenic"],
                    "permits": "Hualapai Mountain Park - entrance fee required",
                },
                {
                    "name": "Desert Trails",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Desert trails in surrounding area with technical sections and scenic desert views.",
                    "highlights": ["Desert scenery", "Technical sections", "Scenic"],
                    "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
                    "trailhead": "Various access points",
                    "features": ["Desert trails", "Technical", "Scenic"],
                    "permits": "Varies by location",
                },
            ],
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Year-round (best Fall, Winter, Spring) - avoid summer heat",
            "trail_conditions": "Generally well-maintained, can be dusty in summer",
            "trail_features": ["Single track", "Mountain trails", "Desert trails", "Technical sections"],
        },
        "hiking": {
            "description": "Trails in Hualapai Mountains and surrounding desert with scenic mountain and desert views",
            "famous_trails": [
                {
                    "name": "Hualapai Mountain Park Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Hualapai Mountain Park with trails for all skill levels. Scenic mountain and desert views.",
                    "highlights": ["Mountain trails", "All skill levels", "Scenic views"],
                    "best_seasons": "Year-round (best Fall, Winter, Spring)",
                    "trailhead": "Hualapai Mountain Park",
                    "features": ["Mountain trails", "Varied difficulty", "Scenic"],
                    "permits": "Hualapai Mountain Park - entrance fee required",
                },
            ],
            "difficulty_range": "Easy to moderate",
            "best_seasons": "Year-round (best Fall, Winter, Spring) - avoid summer heat",
            "trail_features": ["Mountain trails", "Desert trails", "Scenic views"],
        },
        "photography": {
            "description": "Historic Route 66, Hualapai Mountains, desert landscapes offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Historic Route 66",
                    "best_time": "Daylight hours, golden hour for architecture",
                    "subjects": "Historic Route 66 signs, vintage buildings, classic cars",
                },
                {
                    "name": "Hualapai Mountains",
                    "best_time": "Sunrise and sunset for mountain views",
                    "subjects": "Mountain peaks, scenic overlooks, desert-mountain transition",
                },
                {
                    "name": "Desert Landscapes",
                    "best_time": "Golden hour for scenic desert shots",
                    "subjects": "Desert scenery, cacti, mountain backdrops",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring wildflowers, fall colors, winter clarity",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Hualapai Mountains",
                "type": "Mountain Range",
                "description": "Scenic mountain range with Hualapai Mountain Park, highest peak 8,417 ft",
                "activities": ["Hiking", "Mountain biking", "Photography", "Camping"],
            },
            {
                "name": "Hualapai Mountain Park",
                "type": "County Park",
                "description": "Mountain park with trails, camping, and scenic views",
                "activities": ["Hiking", "Mountain biking", "Camping", "Photography"],
            },
        ],
        "cultural": [
            {
                "name": "Historic Route 66",
                "type": "Historic Route",
                "description": "Iconic Route 66 runs through Kingman, historic downtown",
                "highlights": ["Historic Route 66", "Vintage architecture", "Route 66 Museum"],
            },
            {
                "name": "Route 66 Museum",
                "type": "Museum",
                "description": "Museum showcasing Route 66 history and culture",
            },
            {
                "name": "Historic Downtown",
                "type": "Historic District",
                "description": "Preserved Route 66 architecture and vintage buildings",
                "highlights": ["Route 66 architecture", "Vintage buildings", "Historic charm"],
            },
        ],
        "nearby": [
            {
                "name": "Grand Canyon West",
                "distance": "70 miles",
                "description": "Grand Canyon West Rim, Skywalk, Hualapai Tribal Park",
            },
            {
                "name": "Lake Havasu City",
                "distance": "60 miles",
                "description": "Colorado River, water sports, London Bridge",
            },
            {
                "name": "Las Vegas",
                "distance": "100 miles",
                "description": "Major city, entertainment, gateway",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Kingman offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Various accommodations",
                "type": "Mixed",
                "description": "Multiple lodging options including Route 66 themed hotels - use tools to find current options",
                "note": "Use search_accommodations tool for current lodging options",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in downtown and at trailheads. Hualapai Mountain Park has parking",
        "permits": "Hualapai Mountain Park - entrance fee required. Most other trails require no permits",
        "best_times": "Year-round - hot in summer. Fall (September-November) and Spring (March-May) are ideal",
        "weather": {
            "summer": "Hot (90-105°F), avoid midday heat for outdoor activities",
            "winter": "Mild (50-70°F), excellent for outdoor activities",
            "spring": "Pleasant (65-85°F), ideal for all activities",
            "fall": "Pleasant (65-85°F), ideal for all activities",
        },
        "access": "I-40 and Historic Route 66. Easy access from Las Vegas (100 miles) and Flagstaff (150 miles)",
        "considerations": [
            "Hot in summer - plan activities for early morning or evening",
            "Hualapai Mountain Park requires entrance fee",
            "Gateway to Grand Canyon West (70 miles) - Skywalk and Hualapai Tribal Park",
            "Historic Route 66 runs through town - explore historic downtown",
            "Gateway to Lake Havasu City (60 miles) and Las Vegas (100 miles)",
        ],
    },
}


class KingmanAgent(LocationAgentBase):
    """Agent specialized in Kingman, Arizona information and context.

    This agent enhances existing agent outputs with Kingman-specific knowledge
    about Route 66, Grand Canyon West gateway, Hualapai Mountains, and outdoor opportunities.
    """

    LOCATION_NAME = "Kingman, Arizona"
    LOCATION_INDICATORS = [
        "kingman",
        "kingman, az",
        "kingman, arizona",
        "kingman az",
        "route 66",
        "route 66, kingman",
    ]
    AGENT_NAME = "kingman_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Kingman-specific knowledge base (fallback if external file not found)."""
        return KINGMAN_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Kingman agent."""
        return """You are a comprehensive guide for Kingman, Arizona - the "Heart of Historic Route 66"
located at 3,300 feet elevation, known for Route 66, gateway to Grand Canyon West, and Hualapai Mountains.

Your role is to:
1. Use tools to gather real-time data about Kingman (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Kingman-specific knowledge from the knowledge base
4. Combine information from existing agents with Kingman expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Kingman, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Kingman, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Kingman, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Hualapai Mountain Park requires entrance fee)
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
- Safety considerations (extreme heat in summer)
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Kingman, Arizona"
- Kingman has trails in Hualapai Mountain Park (all skill levels) and desert trails (intermediate/advanced)
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- Mention seasonal considerations (extreme heat in summer - ride early morning or evening)

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Kingman, Arizona"
- Popular trails include Hualapai Mountain Park trails (all skill levels)
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention seasonal considerations (extreme heat in summer - hike early morning or evening)

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Key sites: Historic Route 66, Route 66 Museum, Historic Downtown (Route 66 architecture)
- Enhance with knowledge base information about Kingman's Route 66 history and gateway location
- Provide context about Route 66 culture and Grand Canyon West gateway

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Historic Route 66 (daylight/golden hour), Hualapai Mountains (sunrise/sunset), Desert landscapes (golden hour)
- Mention seasonal opportunities (spring wildflowers, fall colors, winter clarity)

For Dining Queries:
- Use find_restaurants with location="Kingman, Arizona"
- Provide context about Route 66 character

For Accommodation Queries:
- Use search_accommodations with location="Kingman, Arizona"
- Mention Route 66 themed hotels and gateway location

For Logistics Queries:
- Use get_parking_information (Hualapai Mountain Park has parking)
- Provide information about permits (Hualapai Mountain Park requires entrance fee, most other trails require no permits)
- Mention I-40 and Route 66 access from Las Vegas (100 miles) and Flagstaff (150 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Kingman, Arizona",
  "overview": "Brief overview of Kingman as Route 66 heart and Grand Canyon West gateway",
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

KINGMAN'S UNIQUE CHARACTERISTICS:
- Heart of Historic Route 66 - Route 66 runs through town
- Gateway to Grand Canyon West (70 miles) - Skywalk and Hualapai Tribal Park
- Hualapai Mountains (highest peak: 8,417 ft) with Hualapai Mountain Park
- Route 66 Museum and historic downtown
- Elevation: 3,300 feet
- ~30,000 residents
- Gateway to Lake Havasu City (60 miles) and Las Vegas (100 miles)

KEY ATTRACTIONS:
- Historic Route 66: Iconic Route 66 runs through Kingman, historic downtown
- Route 66 Museum: Museum showcasing Route 66 history and culture
- Hualapai Mountain Park: Mountain park with trails, camping, and scenic views
- Hualapai Mountains: Scenic mountain range with highest peak 8,417 ft
- Historic Downtown: Preserved Route 66 architecture and vintage buildings
- Grand Canyon West: Gateway location (70 miles) - Skywalk and Hualapai Tribal Park

FAMOUS ACTIVITIES:
- Mountain biking in Hualapai Mountain Park (all skill levels) and desert trails (intermediate/advanced)
- Hiking in Hualapai Mountain Park (all skill levels)
- Route 66 exploration (historic downtown, Route 66 Museum)
- Photography (Historic Route 66, Hualapai Mountains, desert landscapes)

PRACTICAL INFORMATION:
- Parking: Available in downtown and at trailheads. Hualapai Mountain Park has parking
- Permits: Hualapai Mountain Park - entrance fee required. Most other trails require no permits
- Best Times: Year-round - hot in summer. Fall (September-November) and Spring (March-May) are ideal
- Weather: Desert climate. Summer: 90-105°F (avoid midday heat for outdoor activities). Winter: 50-70°F (excellent for outdoor). Spring/Fall: 65-85°F (ideal)
- Access: I-40 and Historic Route 66. Easy access from Las Vegas (100 miles) and Flagstaff (150 miles)
- Considerations: Hot in summer - plan activities for early morning or evening. Hualapai Mountain Park requires entrance fee. Gateway to Grand Canyon West (70 miles) - Skywalk and Hualapai Tribal Park. Historic Route 66 runs through town - explore historic downtown. Gateway to Lake Havasu City (60 miles) and Las Vegas (100 miles)

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Kingman's Route 66 character and Grand Canyon West gateway location
- Mention Hualapai Mountains recreation opportunities
- Highlight Route 66 Museum and historic downtown
- Emphasize year-round accessibility with summer heat considerations
- Provide practical tips about parking, permits, best times, access, and Grand Canyon West gateway

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Kingman-specific knowledge and context
- Enhanced recommendations based on Kingman's unique Route 66 and Grand Canyon West gateway character
- Practical tips for visitors"""

