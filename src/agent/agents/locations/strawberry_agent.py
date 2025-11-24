"""Strawberry, Arizona specialist agent.

This agent provides Strawberry-specific information and enhances existing agent outputs
with local knowledge about Mogollon Rim, Tonto National Forest, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Strawberry-specific knowledge base
STRAWBERRY_KNOWLEDGE = {
    "location": {
        "name": "Strawberry, Arizona",
        "coordinates": {"lat": 34.4078, "lon": -111.4925},
        "elevation": 5600,  # feet
        "region": "Gila County, Arizona",
        "country": "US",
        "proximity": {
            "pine": {"distance_miles": 5, "direction": "northwest"},
            "payson": {"distance_miles": 20, "direction": "northwest"},
            "phoenix": {"distance_miles": 110, "direction": "south"},
        },
    },
    "history": {
        "founded": "Late 1800s",
        "current_population": "~1,000 residents",
        "known_for": [
            "Mogollon Rim community",
            "Ponderosa pine forests",
            "Small mountain town",
            "Historic buildings",
        ],
    },
    "geography": {
        "terrain": "Mountainous, pine forests",
        "topography": "Mogollon Rim, Tonto National Forest",
        "elevation": "5,600 feet",
        "climate": "Four distinct seasons, cooler than Phoenix",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Trails in Tonto National Forest with access to Mogollon Rim and scenic forest terrain",
            "famous_trails": [
                {
                    "name": "Highline Trail",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": "50+ miles (can be done in sections)",
                    "elevation_gain_feet": "Varies by section",
                    "description": "Long-distance trail along Mogollon Rim with scenic views, technical sections, and varied terrain. Can be done in sections or as multi-day adventure.",
                    "highlights": ["Long-distance", "Mogollon Rim views", "Technical sections", "Scenic", "Can do in sections"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Various access points along trail",
                    "features": ["Long-distance", "Technical", "Scenic", "Mogollon Rim"],
                    "permits": "Tonto National Forest - no permit required for day use",
                },
                {
                    "name": "Mogollon Rim Trail",
                    "difficulty": "Intermediate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail along Mogollon Rim with scenic rim views and moderate difficulty.",
                    "highlights": ["Rim views", "Scenic", "Moderate difficulty"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Various access points",
                    "features": ["Rim views", "Moderate", "Scenic"],
                    "permits": "Tonto National Forest - no permit required",
                },
            ],
            "trail_networks": "Trails in Tonto National Forest",
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Spring, Summer, Fall (cooler than Phoenix)",
            "trail_features": ["Single track", "Forest scenery", "Rim views"],
        },
        "hiking": {
            "description": "Access to Mogollon Rim and Tonto National Forest with scenic rim and forest trails",
            "famous_trails": [
                {
                    "name": "Highline Trail",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": "50+ miles (can be done in sections)",
                    "elevation_gain_feet": "Varies by section",
                    "description": "Long-distance trail along Mogollon Rim with scenic views, varied terrain, and moderate to strenuous difficulty. Can be done in sections or as multi-day adventure.",
                    "highlights": ["Long-distance", "Mogollon Rim views", "Scenic", "Can do in sections", "Moderate to strenuous"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Various access points along trail",
                    "features": ["Long-distance", "Rim views", "Scenic", "Moderate to strenuous"],
                    "permits": "Tonto National Forest - no permit required",
                },
                {
                    "name": "Mogollon Rim Trail",
                    "difficulty": "Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail along Mogollon Rim with scenic rim views and moderate difficulty.",
                    "highlights": ["Rim views", "Scenic", "Moderate difficulty"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Various access points",
                    "features": ["Rim views", "Moderate", "Scenic"],
                    "permits": "Tonto National Forest - no permit required",
                },
            ],
            "trail_networks": "Trails in Tonto National Forest",
            "difficulty_range": "Easy to strenuous",
            "best_seasons": "Spring, Summer, Fall (cooler than Phoenix)",
            "trail_features": ["Forest trails", "Rim views", "Scenic views"],
        },
        "climbing": {
            "description": "Limited climbing opportunities in Strawberry area",
            "note": "Strawberry is not a major climbing destination. For extensive climbing, consider nearby areas or use tools to find current climbing opportunities.",
        },
        "cycling": {
            "description": "Road cycling opportunities with scenic routes through pine forests",
            "routes": [
                {
                    "name": "Mogollon Rim Area Roads",
                    "type": "Road",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Scenic road routes through Tonto National Forest with forest and rim views.",
                    "highlights": ["Forest scenery", "Rim views", "Scenic"],
                    "best_seasons": "Spring, Summer, Fall",
                    "difficulty": "Varies",
                },
            ],
            "best_seasons": "Spring, Summer, Fall",
        },
        "paddling": {
            "description": "Limited paddling opportunities in Strawberry area",
            "note": "Strawberry is not a major paddling destination. For extensive paddling, consider nearby lakes or use tools to find current opportunities.",
        },
    },
    "attractions": {
        "natural": [
            "Mogollon Rim",
            "Tonto National Forest",
        ],
        "cultural": [
            "Historic buildings",
        ],
        "nearby": [
            "Pine (5 miles)",
            "Payson (20 miles)",
        ],
    },
    "practical_info": {
        "parking": "Available at trailheads",
        "permits": "Tonto National Forest - some areas may require permits",
        "best_times": "Year-round - cooler than Phoenix",
        "weather": "Four distinct seasons",
        "access": "Highway 87, then Highway 260",
    },
}


class StrawberryAgent(LocationAgentBase):
    """Agent specialized in Strawberry, Arizona information and context."""

    LOCATION_NAME = "Strawberry, Arizona"
    LOCATION_INDICATORS = [
        "strawberry",
        "strawberry, az",
        "strawberry, arizona",
        "strawberry az",
    ]
    AGENT_NAME = "strawberry_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Strawberry-specific knowledge base (fallback if external file not found)."""
        return STRAWBERRY_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Strawberry agent."""
        return """You are a comprehensive guide for Strawberry, Arizona - a small mountain town
on the Mogollon Rim at 5,600 feet elevation.

Your role is to:
1. Use tools to gather real-time data about Strawberry (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Strawberry-specific knowledge from the knowledge base
4. Combine information from existing agents with Strawberry expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Strawberry, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Strawberry, Arizona")
- For climbing: search_trails(activity_type="climbing", location="Strawberry, Arizona") if available
- For cycling: search_trails(activity_type="cycling", location="Strawberry, Arizona")
- For paddling: search_trails(activity_type="paddling", location="Strawberry, Arizona") if available
- For trail running: search_trails(activity_type="trail_running", location="Strawberry, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Tonto National Forest - most trails require no permits)
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
- Safety considerations (weather, elevation)
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Strawberry, Arizona"
- Strawberry has trails including Highline Trail (50+ miles, intermediate/advanced, can be done in sections) and Mogollon Rim Trail
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Strawberry, Arizona"
- Popular trails include Highline Trail (50+ miles, moderate/strenuous, can be done in sections) and Mogollon Rim Trail
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights

For Dining Queries:
- Use find_restaurants with location="Strawberry, Arizona"
- Provide context about small mountain town character

For Accommodation Queries:
- Use search_accommodations with location="Strawberry, Arizona"
- Mention proximity to Mogollon Rim and Tonto National Forest

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Mogollon Rim, Tonto National Forest, Historic buildings
- Mention seasonal opportunities

For Logistics Queries:
- Use get_parking_information for trailhead parking
- Provide information about permits (Tonto National Forest - most trails require no permits)
- Mention Highway 87/260 access from Phoenix

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

Strawberry's Highlights:
- Small mountain town on Mogollon Rim
- Ponderosa pine forests
- Tonto National Forest access
- Historic buildings
- Cooler climate than Phoenix
- ~1,000 residents
- Close to Pine and Payson

KEY ATTRACTIONS:
- Mogollon Rim
- Tonto National Forest
- Historic buildings
- Highline Trail access (50+ miles, can be done in sections)

FAMOUS TRAILS:
- Mountain Biking: Highline Trail (50+ miles, intermediate/advanced), Mogollon Rim Trail
- Hiking: Highline Trail (50+ miles, moderate/strenuous), Mogollon Rim Trail

PRACTICAL INFORMATION:
- Four distinct seasons
- Year-round outdoor recreation (best Spring, Summer, Fall)
- Access via Highway 87/260 from Phoenix (110 miles)
- Elevation 5,600 feet (cooler than Phoenix)
- Tonto National Forest - most trails require no permits for day use
- Close to Pine (5 miles) and Payson (20 miles)

ENHANCEMENT GUIDELINES:
- Always combine tool results with knowledge base information
- Provide specific recommendations based on activity type and season
- Include safety considerations (weather, elevation)
- Highlight unique characteristics (Mogollon Rim, small mountain town, historic buildings, cooler than Phoenix)
- Provide practical tips (parking, permits, best times, access)

Provide comprehensive, accurate, practical information that combines real tool data with Strawberry-specific knowledge and context."""

