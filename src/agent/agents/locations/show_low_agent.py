"""Show Low, Arizona specialist agent.

This agent provides Show Low-specific information and enhances existing agent outputs
with local knowledge about White Mountains, Ponderosa pine forests, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Show Low-specific knowledge base - Enhanced with detailed information
SHOW_LOW_KNOWLEDGE = {
    "location": {
        "name": "Show Low, Arizona",
        "coordinates": {"lat": 34.2542, "lon": -110.0298},
        "elevation": 6400,  # feet
        "region": "Navajo County, Arizona",
        "country": "US",
        "nickname": "Home of the World's Smallest International Airport",
        "proximity": {
            "pinetop": {"distance_miles": 5, "direction": "north", "drive_time_minutes": 10},
            "payson": {"distance_miles": 80, "direction": "west", "drive_time_minutes": 90},
            "phoenix": {"distance_miles": 180, "direction": "southwest", "drive_time_minutes": 180},
            "springerville": {"distance_miles": 30, "direction": "east", "drive_time_minutes": 35},
        },
    },
    "history": {
        "founded": 1870,
        "incorporated": 1953,
        "current_population": "~11,000 residents",
        "known_for": [
            "White Mountains location",
            "Ponderosa pine forests",
            "Cooler climate (6,400 feet elevation)",
            "Summer retreat from Phoenix",
            "Outdoor recreation",
            "Arizona Trail access",
        ],
        "historical_significance": "Founded as logging and ranching community, evolved into recreation destination and summer retreat",
    },
    "geography": {
        "terrain": "Mountainous, pine forests",
        "topography": "White Mountains, Apache-Sitgreaves National Forest",
        "elevation": "6,400 feet",
        "climate": "Four distinct seasons, snow in winter (December-April), mild summers (70-85°F)",
        "features": [
            "White Mountains (highest peaks in Arizona outside San Francisco Peaks)",
            "Apache-Sitgreaves National Forest (2.76 million acres)",
            "Show Low Lake",
            "Ponderosa pine forests",
            "Arizona Trail segments",
        ],
        "ecosystem": "Ponderosa pine forest transitioning to mixed conifer at higher elevations",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Trails in Apache-Sitgreaves National Forest with access to Arizona Trail segments and White Mountain terrain",
            "famous_trails": [
                {
                    "name": "Arizona Trail Segments",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": "Varies by segment",
                    "elevation_gain_feet": "Varies",
                    "description": "Segments of the 800-mile Arizona Trail pass through Show Low area, offering long-distance trail opportunities with varied terrain.",
                    "highlights": ["Long-distance trail", "Arizona Trail", "Varied difficulty", "Scenic", "Can do in sections"],
                    "best_seasons": "Spring (May-June), Summer (July-August), Fall (September-October)",
                    "trailhead": "Various access points",
                    "features": ["Long-distance", "Varied difficulty", "Scenic"],
                    "permits": "Apache-Sitgreaves National Forest - no permit required for day use",
                },
                {
                    "name": "White Mountain Trail System",
                    "difficulty": "Beginner to Advanced",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Apache-Sitgreaves National Forest with trails for all skill levels. Well-maintained singletrack with forest scenery.",
                    "highlights": ["Trail system", "All skill levels", "Well-maintained", "Forest scenery"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Various access points",
                    "features": ["Trail system", "Varied difficulty", "Forest scenery"],
                    "permits": "Apache-Sitgreaves National Forest - no permit required",
                },
            ],
            "trail_networks": "Trails in Apache-Sitgreaves National Forest with Arizona Trail access",
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Spring (May-June), Summer (July-August), Fall (September-October) - snow in winter",
            "trail_conditions": "Generally well-maintained, can be muddy in spring, snow-covered in winter",
            "trail_features": ["Single track", "Forest scenery", "Mountain views", "Arizona Trail"],
        },
        "hiking": {
            "description": "Access to White Mountains and Apache-Sitgreaves National Forest with scenic mountain and forest trails, including Arizona Trail segments",
            "famous_trails": [
                {
                    "name": "Arizona Trail Segments",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": "Varies by segment",
                    "elevation_gain_feet": "Varies",
                    "description": "Segments of the 800-mile Arizona Trail pass through Show Low area, offering long-distance hiking opportunities with varied terrain.",
                    "highlights": ["Long-distance trail", "Arizona Trail", "Varied difficulty", "Scenic", "Can do in sections"],
                    "best_seasons": "Spring (May-June), Summer (July-August), Fall (September-October)",
                    "trailhead": "Various access points",
                    "features": ["Long-distance", "Varied difficulty", "Scenic"],
                    "permits": "Apache-Sitgreaves National Forest - no permit required",
                },
                {
                    "name": "White Mountain Trails",
                    "difficulty": "Easy to Strenuous",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Apache-Sitgreaves National Forest with trails for all skill levels. Scenic forest and mountain views.",
                    "highlights": ["Trail system", "All skill levels", "Scenic", "Forest and mountain views"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Various access points",
                    "features": ["Trail system", "Varied difficulty", "Scenic"],
                    "permits": "Apache-Sitgreaves National Forest - no permit required",
                },
            ],
            "trail_networks": "Trails in Apache-Sitgreaves National Forest with Arizona Trail access",
            "difficulty_range": "Easy to strenuous",
            "best_seasons": "Spring (May-June), Summer (July-August), Fall (September-October) - snow in winter",
            "trail_features": ["Mountain peaks", "Forest trails", "Arizona Trail", "Scenic views"],
        },
        "fishing": {
            "description": "Excellent fishing in Show Low Lake and White Mountain streams",
            "locations": [
                {
                    "name": "Show Low Lake",
                    "type": "Lake",
                    "species": "Trout, bass",
                    "description": "Popular fishing lake with good trout and bass fishing",
                    "seasons": "Year-round, best in Spring and Fall",
                },
                {
                    "name": "White Mountain Streams",
                    "type": "Streams",
                    "species": "Trout",
                    "description": "Mountain streams with trout fishing",
                    "seasons": "Year-round, best in Spring and Fall",
                },
            ],
            "seasons": "Year-round, best in Spring and Fall",
            "permits": "Arizona fishing license required",
        },
        "winter_sports": {
            "description": "Snow activities in winter including snowshoeing and cross-country skiing",
            "activities": [
                {
                    "name": "Snowshoeing",
                    "description": "Snowshoeing opportunities in Apache-Sitgreaves National Forest",
                    "seasons": "December-April (snow dependent)",
                },
                {
                    "name": "Cross-country Skiing",
                    "description": "Cross-country skiing on forest roads and trails",
                    "seasons": "December-April (snow dependent)",
                },
            ],
            "season": "December-April (snow dependent)",
            "note": "Sunrise Ski Resort is 30 miles away for downhill skiing",
        },
        "photography": {
            "description": "Mountain views, lakes, pine forests offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "White Mountains",
                    "best_time": "Sunrise and sunset for mountain views",
                    "subjects": "Mountain peaks, forest landscapes",
                },
                {
                    "name": "Show Low Lake",
                    "best_time": "Golden hour for scenic lake shots",
                    "subjects": "Lake scenery, reflections, wildlife",
                },
                {
                    "name": "Ponderosa Pine Forests",
                    "best_time": "Any time, especially with morning mist or snow",
                    "subjects": "Forest landscapes, wildlife, seasonal changes",
                },
            ],
            "seasons": "All seasons offer unique opportunities - fall colors, winter snow, spring wildflowers, summer greenery",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "White Mountains",
                "type": "Mountain Range",
                "description": "Highest peaks in Arizona outside San Francisco Peaks, scenic mountain views",
                "activities": ["Hiking", "Mountain biking", "Photography", "Scenic drives"],
            },
            {
                "name": "Apache-Sitgreaves National Forest",
                "type": "National Forest",
                "description": "2.76 million acres of public land with extensive trail network",
                "activities": ["All outdoor activities"],
            },
            {
                "name": "Show Low Lake",
                "type": "Lake",
                "description": "Popular fishing and recreation lake",
                "activities": ["Fishing", "Boating", "Kayaking", "Photography"],
            },
        ],
        "cultural": [
            {
                "name": "Show Low Historical Society Museum",
                "type": "Museum",
                "description": "Local history museum showcasing Show Low's heritage",
            },
        ],
        "nearby": [
            {
                "name": "Pinetop-Lakeside",
                "distance": "5 miles",
                "description": "Larger recreation hub with additional lakes and amenities",
            },
            {
                "name": "Sunrise Ski Resort",
                "distance": "30 miles",
                "description": "Downhill skiing and snowboarding in winter",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "The House",
                "type": "American",
                "description": "Local favorite with American cuisine",
                "highlights": ["Local favorite", "American cuisine"],
            },
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Show Low offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Quality Inn Show Low",
                "type": "Hotel",
                "description": "Full-service hotel",
                "highlights": ["Full-service", "Hotel"],
            },
            {
                "name": "Various accommodations",
                "type": "Mixed",
                "description": "Multiple lodging options in area - use tools to find current options",
                "note": "Use search_accommodations tool for current lodging options",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in town and at trailheads. Popular trailheads may fill up on weekends - arrive early",
        "permits": "Apache-Sitgreaves National Forest - most trails require no permits for day use. Fishing requires Arizona fishing license",
        "best_times": "Year-round - four distinct seasons. Spring (May-June) and Fall (September-October) are ideal for outdoor activities",
        "weather": {
            "summer": "Mild (70-85°F), perfect for outdoor activities",
            "winter": "Cold with snow (30-50°F), excellent for winter sports",
            "spring": "Pleasant (50-70°F), ideal for all activities",
            "fall": "Pleasant (50-70°F), ideal for all activities",
        },
        "access": "Highway 260 from Payson (80 miles, 90 minutes) or I-40. Highway 60 provides access from Phoenix (180 miles, 180 minutes)",
        "considerations": [
            "Elevation is 6,400 feet - cooler than Phoenix, snow in winter",
            "Weather can change quickly in mountains",
            "Some trails may be closed seasonally due to snow",
            "Fishing requires Arizona fishing license",
            "Summer retreat from Phoenix - popular in summer",
            "Gateway to White Mountains recreation",
            "Close to Pinetop-Lakeside (5 miles) for additional recreation",
        ],
    },
}


class ShowLowAgent(LocationAgentBase):
    """Agent specialized in Show Low, Arizona information and context.

    This agent enhances existing agent outputs with Show Low-specific knowledge
    about White Mountains, Ponderosa pine forests, and outdoor opportunities.
    """

    LOCATION_NAME = "Show Low, Arizona"
    LOCATION_INDICATORS = [
        "show low",
        "show low, az",
        "show low, arizona",
        "show low az",
    ]
    AGENT_NAME = "show_low_agent"

    def get_location_knowledge(self) -> Dict[str, Any]:
        """Get Show Low-specific knowledge base."""
        return SHOW_LOW_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Show Low agent."""
        return """You are a comprehensive guide for Show Low, Arizona - a mountain town
in the White Mountains at 6,400 feet elevation, known as "Home of the World's Smallest International Airport"
and a summer retreat from Phoenix.

Your role is to:
1. Use tools to gather real-time data about Show Low (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Show Low-specific knowledge from the knowledge base
4. Combine information from existing agents with Show Low expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Show Low, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Show Low, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Show Low, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Apache-Sitgreaves National Forest - most trails require no permits)
- Include trail connectivity and route planning details
- Mention Arizona Trail segments if relevant

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
- Safety considerations (weather, elevation, snow in winter)
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Show Low, Arizona"
- Show Low has access to Arizona Trail segments and White Mountain trail systems
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- Mention seasonal considerations (snow in winter, mud in spring)

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Show Low, Arizona"
- Popular trails include Arizona Trail segments and White Mountain trails
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- Mention seasonal considerations (snow in winter)

For Fishing Queries:
- Show Low offers excellent fishing in Show Low Lake and White Mountain streams
- Mention trout and bass fishing opportunities
- Provide information about Arizona fishing license requirements
- Best seasons: Year-round, best in Spring and Fall

For Winter Sports Queries:
- Snowshoeing and cross-country skiing opportunities in Apache-Sitgreaves National Forest
- Season: December-April (snow dependent)
- Sunrise Ski Resort is 30 miles away for downhill skiing

For Dining Queries:
- Use find_restaurants with location="Show Low, Arizona"
- Enhance results with knowledge base businesses (The House)
- Provide context about small mountain town character

For Accommodation Queries:
- Use search_accommodations with location="Show Low, Arizona"
- Enhance with knowledge base information (Quality Inn Show Low)
- Mention proximity to lakes and trails

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: White Mountains (sunrise/sunset), Show Low Lake (golden hour), Ponderosa pine forests (any time)
- Mention seasonal opportunities (fall colors, winter snow, spring wildflowers)

For Logistics Queries:
- Use get_parking_information for trailhead parking
- Provide information about permits (Apache-Sitgreaves National Forest - most trails require no permits, fishing license required)
- Mention Highway 260 access from Payson (80 miles) and I-40

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Show Low, Arizona",
  "overview": "Brief overview of Show Low as White Mountains mountain town",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
    "mountain_biking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
    "hiking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
    "fishing": {"locations": [...], "seasons": "..."},
    "winter_sports": {"activities": [...], "seasons": "..."},
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

SHOW LOW'S UNIQUE CHARACTERISTICS:
- White Mountains location (highest peaks in Arizona outside San Francisco Peaks)
- Show Low Lake with excellent fishing
- Arizona Trail segments pass through area
- Elevation: 6,400 feet (cooler than Phoenix, snow in winter)
- Summer retreat from Phoenix (popular in summer)
- Ponderosa pine forests
- ~11,000 residents
- Close to Pinetop-Lakeside (5 miles) for additional recreation

KEY ATTRACTIONS:
- White Mountains: Highest peaks in Arizona outside San Francisco Peaks, scenic mountain views
- Apache-Sitgreaves National Forest: 2.76 million acres with extensive trail network
- Show Low Lake: Popular fishing and recreation lake
- Arizona Trail segments: Long-distance trail opportunities
- Show Low Historical Society Museum: Local history and heritage

FAMOUS ACTIVITIES:
- Fishing in Show Low Lake and streams (trout, bass) - year-round, best in Spring and Fall
- Mountain biking and hiking (Arizona Trail segments, White Mountain trails)
- Winter sports (snowshoeing, cross-country skiing) - December-April
- Lake recreation (boating, kayaking)
- Photography (mountain views, lakes, pine forests)

PRACTICAL INFORMATION:
- Parking: Available in town and at trailheads. Popular trailheads may fill up on weekends - arrive early
- Permits: Apache-Sitgreaves National Forest - most trails require no permits for day use. Fishing requires Arizona fishing license
- Best Times: Year-round - four distinct seasons. Spring (May-June) and Fall (September-October) are ideal for outdoor activities
- Weather: Four distinct seasons. Summer: 70-85°F (mild, perfect for outdoor). Winter: 30-50°F with snow (excellent for winter sports). Spring/Fall: 50-70°F (ideal)
- Access: Highway 260 from Payson (80 miles, 90 minutes) or I-40. Highway 60 provides access from Phoenix (180 miles, 180 minutes)
- Considerations: Elevation 6,400 feet - cooler than Phoenix, snow in winter. Weather changes quickly in mountains. Some trails closed seasonally due to snow. Fishing requires Arizona fishing license. Summer retreat from Phoenix - popular in summer. Gateway to White Mountains recreation. Close to Pinetop-Lakeside (5 miles) for additional recreation

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Show Low's White Mountains location and lake recreation
- Mention Arizona Trail access and segments
- Highlight fishing opportunities in Show Low Lake
- Emphasize year-round accessibility with seasonal considerations (snow in winter)
- Provide practical tips about parking, permits, best times, access, and weather

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Show Low-specific knowledge and context
- Enhanced recommendations based on Show Low's unique White Mountains and lake character
- Practical tips for visitors"""

