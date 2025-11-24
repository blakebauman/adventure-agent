"""Lake Havasu City, Arizona specialist agent.

This agent provides Lake Havasu City-specific information and enhances existing agent outputs
with local knowledge about Colorado River, water sports, London Bridge, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Lake Havasu City-specific knowledge base - Enhanced with detailed information
LAKE_HAVASU_KNOWLEDGE = {
    "location": {
        "name": "Lake Havasu City, Arizona",
        "coordinates": {"lat": 34.4839, "lon": -114.3225},
        "elevation": 750,  # feet
        "region": "Mohave County, Arizona",
        "country": "US",
        "nickname": "Arizona's Playground",
        "proximity": {
            "kingman": {"distance_miles": 60, "direction": "north", "drive_time_minutes": 70},
            "parker": {"distance_miles": 30, "direction": "south", "drive_time_minutes": 35},
            "phoenix": {"distance_miles": 200, "direction": "east", "drive_time_minutes": 200},
            "las_vegas": {"distance_miles": 150, "direction": "northwest", "drive_time_minutes": 160},
        },
    },
    "history": {
        "founded": 1963,
        "incorporated": 1978,
        "current_population": "~57,000 residents",
        "known_for": [
            "London Bridge (relocated from London, England)",
            "Colorado River recreation",
            "Water sports hub",
            "Desert trails",
            "Spring break destination",
            "Boaters' paradise",
        ],
        "historical_significance": "Founded as planned community, became major recreation destination. London Bridge purchased and relocated in 1968-1971.",
        "london_bridge": {
            "purchased": 1968,
            "relocated": 1968-1971,
            "significance": "Original London Bridge from London, England, relocated to Lake Havasu City",
        },
    },
    "geography": {
        "terrain": "Desert, lake, river",
        "topography": "Colorado River, Lake Havasu, Sonoran Desert",
        "elevation": "750 feet",
        "climate": "Hot desert climate, very hot summers, mild winters",
        "features": [
            "Lake Havasu (45 miles long, part of Colorado River)",
            "London Bridge",
            "Colorado River",
            "Sonoran Desert",
        ],
        "ecosystem": "Desert with riparian areas along Colorado River",
    },
    "outdoor_activities": {
        "water_activities": {
            "description": "Extensive water recreation on Lake Havasu and Colorado River including boating, jet skiing, fishing, and swimming",
            "activities": [
                {
                    "name": "Boating",
                    "description": "Lake Havasu offers extensive boating opportunities with 45 miles of lake and Colorado River access",
                    "seasons": "Year-round, best in Spring, Summer, Fall",
                    "access": "Multiple marinas and boat ramps",
                    "highlights": ["45 miles of lake", "Multiple marinas", "Year-round", "Popular destination"],
                },
                {
                    "name": "Jet Skiing",
                    "description": "Popular jet skiing on Lake Havasu",
                    "seasons": "Year-round, best in Spring, Summer, Fall",
                    "access": "Multiple access points",
                    "highlights": ["Popular", "Year-round", "Multiple access points"],
                },
                {
                    "name": "Fishing",
                    "description": "Excellent fishing in Lake Havasu for bass, catfish, and other species",
                    "seasons": "Year-round, best in Spring and Fall",
                    "permits": "Arizona fishing license required",
                    "highlights": ["Bass", "Catfish", "Year-round"],
                },
                {
                    "name": "Swimming",
                    "description": "Swimming in Lake Havasu",
                    "seasons": "Spring, Summer, Fall",
                    "access": "Multiple beaches and access points",
                    "highlights": ["Multiple beaches", "Scenic", "Cool in summer"],
                },
            ],
            "best_seasons": "Year-round, best in Spring, Summer, Fall",
            "permits": "Fishing requires Arizona fishing license",
        },
        "mountain_biking": {
            "description": "Desert trails in surrounding area with varied terrain",
            "famous_trails": [
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
            "difficulty_range": "Intermediate to expert",
            "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
            "trail_conditions": "Desert trails, can be dusty",
            "trail_features": ["Desert trails", "Technical sections"],
        },
        "hiking": {
            "description": "Desert trails in surrounding area with scenic desert views",
            "famous_trails": [
                {
                    "name": "Desert Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Desert trails in surrounding area with scenic desert views.",
                    "highlights": ["Desert scenery", "Scenic", "Varied difficulty"],
                    "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
                    "trailhead": "Various access points",
                    "features": ["Desert trails", "Scenic"],
                    "permits": "Varies by location",
                },
            ],
            "difficulty_range": "Easy to moderate",
            "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
            "trail_features": ["Desert trails", "Scenic views"],
        },
        "photography": {
            "description": "London Bridge, Lake Havasu, Colorado River, desert landscapes offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "London Bridge",
                    "best_time": "Daylight hours, golden hour for architecture",
                    "subjects": "London Bridge, lake views, architecture",
                },
                {
                    "name": "Lake Havasu",
                    "best_time": "Sunrise and sunset for scenic lake shots",
                    "subjects": "Lake scenery, water activities, scenic views",
                },
                {
                    "name": "Desert Landscapes",
                    "best_time": "Golden hour for scenic desert shots",
                    "subjects": "Desert scenery, cacti, mountain backdrops",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring wildflowers, winter clarity",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Lake Havasu",
                "type": "Lake",
                "description": "45 miles long, part of Colorado River, major recreation destination",
                "activities": ["Boating", "Jet Skiing", "Fishing", "Swimming", "Photography"],
            },
            {
                "name": "Colorado River",
                "type": "River",
                "description": "Major river with extensive recreation opportunities",
                "activities": ["All water activities"],
            },
        ],
        "cultural": [
            {
                "name": "London Bridge",
                "type": "Historic Site",
                "description": "Original London Bridge from London, England, relocated 1968-1971",
                "highlights": ["Historic bridge", "Relocated from London", "Iconic landmark"],
            },
            {
                "name": "Historic Downtown",
                "type": "Historic District",
                "description": "Downtown area with shops, restaurants, and London Bridge views",
                "highlights": ["London Bridge views", "Shopping", "Dining"],
            },
        ],
        "nearby": [
            {
                "name": "Kingman",
                "distance": "60 miles",
                "description": "Route 66, gateway to Grand Canyon West, Hualapai Mountains",
            },
            {
                "name": "Parker",
                "distance": "30 miles",
                "description": "Colorado River recreation, water sports",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Lake Havasu City offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Various accommodations",
                "type": "Mixed",
                "description": "Multiple lodging options including resorts and hotels - use tools to find current options",
                "note": "Use search_accommodations tool for current lodging options",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in downtown and at marinas. Popular areas may fill up on weekends - arrive early",
        "permits": "Fishing requires Arizona fishing license. Most trails require no permits",
        "best_times": "Year-round - very hot in summer. Fall (September-November) and Spring (March-May) are ideal",
        "weather": {
            "summer": "Very hot (95-115°F), excellent for water activities, avoid midday heat for hiking",
            "winter": "Mild (60-75°F), excellent for outdoor activities",
            "spring": "Pleasant (75-90°F), ideal for all activities",
            "fall": "Pleasant (75-90°F), ideal for all activities",
        },
        "access": "Highway 95 from Kingman (60 miles) or Parker (30 miles). Easy access from Phoenix (200 miles) and Las Vegas (150 miles)",
        "considerations": [
            "Very hot in summer - plan hiking for early morning or evening, water activities are great",
            "Popular water recreation destination - can be crowded on weekends",
            "London Bridge is iconic landmark - visit for photos",
            "Gateway to Kingman (60 miles) and Parker (30 miles)",
            "Multiple marinas and boat ramps available",
        ],
    },
}


class LakeHavasuAgent(LocationAgentBase):
    """Agent specialized in Lake Havasu City, Arizona information and context.

    This agent enhances existing agent outputs with Lake Havasu City-specific knowledge
    about Colorado River, water sports, London Bridge, and outdoor opportunities.
    """

    LOCATION_NAME = "Lake Havasu City, Arizona"
    LOCATION_INDICATORS = [
        "lake havasu",
        "lake havasu city",
        "lake havasu, az",
        "lake havasu, arizona",
        "lake havasu az",
        "london bridge",
        "london bridge, arizona",
    ]
    AGENT_NAME = "lake_havasu_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Lake Havasu City-specific knowledge base (fallback if external file not found)."""
        return LAKE_HAVASU_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Lake Havasu agent."""
        return """You are a comprehensive guide for Lake Havasu City, Arizona - "Arizona's Playground"
located at 750 feet elevation, known for Colorado River, water sports, London Bridge, and desert recreation.

Your role is to:
1. Use tools to gather real-time data about Lake Havasu City (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Lake Havasu City-specific knowledge from the knowledge base
4. Combine information from existing agents with Lake Havasu City expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Lake Havasu City, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Lake Havasu City, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Lake Havasu City, Arizona")

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
- Trailhead locations and access
- Permits and regulations
- Safety considerations (extreme heat in summer)
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Water Activities Queries:
- Lake Havasu City is major water recreation destination
- Activities: Boating, jet skiing, fishing (bass, catfish), swimming
- Use find_water_sources for Lake Havasu access points
- Mention multiple marinas and boat ramps
- Provide information about Arizona fishing license requirements
- Best seasons: Year-round, best in Spring, Summer, Fall

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Lake Havasu City, Arizona"
- Lake Havasu City has desert trails with intermediate to advanced difficulty
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- CRITICAL: Mention extreme heat in summer - ride early morning or evening only

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Lake Havasu City, Arizona"
- Popular trails include desert trails (easy/moderate)
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- CRITICAL: Mention extreme heat in summer - hike early morning or evening only

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: London Bridge (daylight/golden hour), Lake Havasu (sunrise/sunset), Desert landscapes (golden hour)
- Mention iconic London Bridge as photography destination

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Key sites: London Bridge (original from London, England, relocated 1968-1971), Historic Downtown
- Enhance with knowledge base information about London Bridge relocation and recreation destination history

For Dining Queries:
- Use find_restaurants with location="Lake Havasu City, Arizona"
- Provide context about recreation destination

For Accommodation Queries:
- Use search_accommodations with location="Lake Havasu City, Arizona"
- Mention resorts and hotels, proximity to Lake Havasu

For Logistics Queries:
- Use get_parking_information (Popular areas may fill up on weekends - arrive early)
- Provide information about permits (Fishing requires Arizona fishing license, most trails require no permits)
- Mention Highway 95 access from Kingman (60 miles) and Parker (30 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Lake Havasu City, Arizona",
  "overview": "Brief overview of Lake Havasu City as water recreation destination",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
    "water_activities": {"activities": [...], "seasons": "..."},
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

LAKE HAVASU CITY'S UNIQUE CHARACTERISTICS:
- "Arizona's Playground" - major water recreation destination
- London Bridge (original from London, England, relocated 1968-1971)
- Lake Havasu (45 miles long, part of Colorado River)
- Colorado River recreation
- Elevation: 750 feet (very hot in summer)
- ~57,000 residents
- Gateway to Kingman (60 miles) and Parker (30 miles)

KEY ATTRACTIONS:
- London Bridge: Original London Bridge from London, England, relocated 1968-1971, iconic landmark
- Lake Havasu: 45 miles long, part of Colorado River, major recreation destination
- Colorado River: Major river with extensive recreation opportunities
- Historic Downtown: Downtown area with shops, restaurants, and London Bridge views

FAMOUS ACTIVITIES:
- Water recreation (boating, jet skiing, fishing, swimming) on Lake Havasu - year-round, best in Spring, Summer, Fall
- Desert trails (mountain biking, hiking) - Fall, Winter, Spring (avoid summer heat)
- Photography (London Bridge, Lake Havasu, desert landscapes)

PRACTICAL INFORMATION:
- Parking: Available in downtown and at marinas. Popular areas may fill up on weekends - arrive early
- Permits: Fishing requires Arizona fishing license. Most trails require no permits
- Best Times: Year-round - very hot in summer. Fall (September-November) and Spring (March-May) are ideal
- Weather: Hot desert climate. Summer: 95-115°F (excellent for water activities, avoid midday heat for hiking). Winter: 60-75°F (excellent for outdoor). Spring/Fall: 75-90°F (ideal)
- Access: Highway 95 from Kingman (60 miles) or Parker (30 miles). Easy access from Phoenix (200 miles) and Las Vegas (150 miles)
- Considerations: Very hot in summer - plan hiking for early morning or evening, water activities are great. Popular water recreation destination - can be crowded on weekends. London Bridge is iconic landmark - visit for photos. Gateway to Kingman (60 miles) and Parker (30 miles). Multiple marinas and boat ramps available

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Lake Havasu City's water recreation character and London Bridge landmark
- Mention Lake Havasu as major recreation destination
- Highlight desert trail opportunities (with summer heat warnings)
- Emphasize year-round water recreation with summer heat considerations for land activities
- Provide practical tips about parking, permits, best times, access, and water recreation

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Lake Havasu City-specific knowledge and context
- Enhanced recommendations based on Lake Havasu City's unique water recreation and London Bridge character
- Practical tips for visitors"""

