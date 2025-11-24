"""Camp Verde, Arizona specialist agent.

This agent provides Camp Verde-specific information and enhances existing agent outputs
with local knowledge about Verde Valley, Montezuma Castle, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Camp Verde-specific knowledge base - Enhanced with detailed information
CAMP_VERDE_KNOWLEDGE = {
    "location": {
        "name": "Camp Verde, Arizona",
        "coordinates": {"lat": 34.5636, "lon": -111.8546},
        "elevation": 3100,  # feet
        "region": "Yavapai County, Arizona",
        "country": "US",
        "nickname": "Gateway to Verde Valley",
        "proximity": {
            "cottonwood": {"distance_miles": 10, "direction": "northwest", "drive_time_minutes": 15},
            "sedona": {"distance_miles": 30, "direction": "north", "drive_time_minutes": 40},
            "phoenix": {"distance_miles": 90, "direction": "south", "drive_time_minutes": 90},
            "payson": {"distance_miles": 50, "direction": "east", "drive_time_minutes": 60},
            "jerome": {"distance_miles": 20, "direction": "north", "drive_time_minutes": 30},
        },
    },
    "history": {
        "founded": 1865,
        "incorporated": 1986,
        "current_population": "~11,000 residents",
        "known_for": [
            "Montezuma Castle National Monument",
            "Montezuma Well",
            "Fort Verde State Historic Park",
            "Verde Valley location",
            "Verde River recreation",
            "Gateway to Sedona and Cottonwood",
        ],
        "historical_significance": "Established as a military post (Fort Verde) during Indian Wars, evolved into agricultural and recreation community",
    },
    "geography": {
        "terrain": "Valley, desert, river",
        "topography": "Verde Valley, Verde River",
        "elevation": "3,100 feet",
        "climate": "Desert climate, four distinct seasons, milder than Phoenix",
        "features": [
            "Verde River (flows year-round)",
            "Montezuma Castle National Monument (ancient cliff dwelling)",
            "Montezuma Well (natural limestone sinkhole)",
            "Fort Verde State Historic Park",
            "Verde Valley grasslands",
        ],
        "ecosystem": "Desert riparian along Verde River, transitioning to desert scrub",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Access to Verde Valley trails and proximity to world-class Sedona MTB trails. Local trails offer varied terrain from beginner to advanced.",
            "famous_trails": [
                {
                    "name": "Verde Valley Trail System",
                    "difficulty": "Beginner to Intermediate",
                    "length_miles": "Varies",
                    "description": "Local trail network with access to Verde Valley trails. Good for intermediate riders.",
                    "highlights": ["Local access", "Varied terrain", "Scenic views"],
                    "best_seasons": "Spring, Fall, Winter",
                    "trailhead": "Various access points in Camp Verde area",
                },
                {
                    "name": "Sedona Trails Access",
                    "difficulty": "Beginner to Expert",
                    "length_miles": "Varies",
                    "description": "30 miles to Sedona's world-class mountain biking trails including Hangover, Hiline, and many others",
                    "highlights": ["World-class trails", "Red rock scenery", "Varied difficulty"],
                    "best_seasons": "Spring, Fall, Winter",
                    "trailhead": "Sedona (30 miles north)",
                    "note": "Camp Verde is an excellent base camp for Sedona mountain biking",
                },
            ],
            "difficulty_range": "Beginner to expert (via Sedona access)",
            "best_seasons": "Spring (March-May), Fall (September-November), Winter (December-February)",
            "summer_conditions": "Hot in summer - early morning or evening rides recommended",
            "trail_features": ["Local trails", "Access to Sedona", "Varied difficulty"],
        },
        "hiking": {
            "description": "Local trails at national monuments and access to extensive Verde Valley and Sedona hiking",
            "famous_trails": [
                {
                    "name": "Montezuma Castle Trail",
                    "difficulty": "Easy",
                    "length_miles": 0.3,
                    "elevation_gain_feet": 50,
                    "description": "Short paved trail to view ancient cliff dwelling. Wheelchair accessible with interpretive signs.",
                    "highlights": ["Ancient ruins", "Easy access", "Interpretive signs", "Wheelchair accessible"],
                    "best_seasons": "Year-round",
                    "trailhead": "Montezuma Castle National Monument visitor center",
                    "permits": "National Monument entrance fee required",
                },
                {
                    "name": "Montezuma Well Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "0.5 to 1.5",
                    "elevation_gain_feet": 100,
                    "description": "Trails around natural limestone sinkhole with ancient ruins and unique ecosystem",
                    "highlights": ["Natural sinkhole", "Ancient ruins", "Unique ecosystem", "Rare species"],
                    "best_seasons": "Year-round",
                    "trailhead": "Montezuma Well (11 miles from Montezuma Castle)",
                    "permits": "National Monument entrance fee required",
                },
                {
                    "name": "Verde River Greenway",
                    "difficulty": "Easy",
                    "length_miles": "Varies",
                    "description": "Riverside trails along Verde River with bird watching and scenic views",
                    "highlights": ["Riverside", "Bird watching", "Scenic", "Easy"],
                    "best_seasons": "Year-round, best in Spring and Fall",
                    "trailhead": "Various access points along Verde River",
                },
            ],
            "difficulty_range": "Easy to moderate (local), access to challenging Sedona trails",
            "best_seasons": "Year-round - milder than Phoenix",
            "trail_features": ["National monuments", "Riverside", "Access to Sedona"],
        },
        "water_activities": {
            "description": "Verde River offers year-round recreation including fishing, kayaking, and swimming",
            "activities": [
                {
                    "name": "Fishing",
                    "description": "Verde River offers excellent fishing for trout, bass, and catfish",
                    "seasons": "Year-round, best in Spring and Fall",
                    "permits": "Arizona fishing license required",
                    "access": "Multiple access points along Verde River",
                },
                {
                    "name": "Kayaking",
                    "description": "Verde River offers flatwater and mild whitewater sections suitable for kayaking",
                    "difficulty": "Class I to Class II",
                    "seasons": "Year-round, best water flow in Spring",
                    "access": "Multiple put-in and take-out points",
                },
                {
                    "name": "Swimming",
                    "description": "Verde River offers swimming holes and recreational areas",
                    "seasons": "Spring, Summer, Fall",
                    "safety": "Check water conditions and flow rates",
                },
            ],
            "best_seasons": "Year-round for fishing, Spring and Summer for water activities",
        },
        "photography": {
            "description": "Montezuma Castle, Verde River, historic sites, and Verde Valley offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Montezuma Castle National Monument",
                    "best_time": "Early morning or late afternoon for best lighting",
                    "subjects": "Ancient cliff dwelling, dramatic architecture, historical significance",
                },
                {
                    "name": "Montezuma Well",
                    "best_time": "Any time, unique lighting at different times of day",
                    "subjects": "Natural sinkhole, ancient ruins, unique ecosystem",
                },
                {
                    "name": "Verde River",
                    "best_time": "Golden hour for scenic river shots",
                    "subjects": "Riverside scenery, wildlife, water features",
                },
                {
                    "name": "Fort Verde State Historic Park",
                    "best_time": "Daylight hours",
                    "subjects": "Historic buildings, military history, period architecture",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring wildflowers, fall colors, winter clarity",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Montezuma Castle National Monument",
                "type": "National Monument",
                "description": "Well-preserved 5-story cliff dwelling built by Sinagua people around 1100-1425 AD",
                "highlights": ["Ancient architecture", "Historical significance", "Easy access", "Visitor center"],
                "activities": ["Hiking", "Photography", "Historical tours"],
                "distance": "In Camp Verde",
            },
            {
                "name": "Montezuma Well",
                "type": "National Monument",
                "description": "Natural limestone sinkhole with unique ecosystem and ancient ruins",
                "highlights": ["Natural wonder", "Rare species", "Ancient ruins", "Unique ecosystem"],
                "activities": ["Hiking", "Photography", "Nature viewing"],
                "distance": "11 miles from Montezuma Castle",
            },
            {
                "name": "Verde River",
                "type": "River",
                "description": "Year-round flowing river offering recreation and scenic beauty",
                "highlights": ["Year-round flow", "Recreation", "Scenic", "Wildlife"],
                "activities": ["Fishing", "Kayaking", "Swimming", "Photography"],
            },
        ],
        "cultural": [
            {
                "name": "Fort Verde State Historic Park",
                "type": "State Park",
                "description": "Best-preserved example of an Indian Wars period fort in Arizona",
                "highlights": ["Military history", "Preserved buildings", "Museum", "Historical reenactments"],
                "activities": ["Historical tours", "Photography", "Education"],
            },
            {
                "name": "Camp Verde Historical Society Museum",
                "type": "Museum",
                "description": "Local history museum showcasing Camp Verde's heritage",
                "highlights": ["Local history", "Artifacts", "Educational"],
            },
        ],
        "nearby": [
            {
                "name": "Cottonwood",
                "distance": "10 miles",
                "description": "Wine country, Old Town, gateway to Jerome and Sedona",
            },
            {
                "name": "Sedona",
                "distance": "30 miles",
                "description": "World-renowned red rock destination with world-class trails",
            },
            {
                "name": "Tuzigoot National Monument",
                "distance": "15 miles",
                "description": "Ancient Sinagua pueblo ruins with museum",
            },
            {
                "name": "Jerome",
                "distance": "20 miles",
                "description": "Historic mining town, ghost town revival, artistic community",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Mormon Lake Lodge",
                "type": "American",
                "description": "Local favorite with casual dining",
                "highlights": ["Local favorite", "Casual dining"],
            },
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Camp Verde offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Cliff Castle Casino Hotel",
                "type": "Hotel",
                "description": "Full-service hotel with casino, restaurant, and amenities",
                "highlights": ["Full-service", "Casino", "Restaurant", "Amenities"],
            },
            {
                "name": "Campgrounds and RV Parks",
                "type": "Camping",
                "description": "Multiple camping options in area - use tools to find current options",
                "note": "Use search_accommodations tool for current camping and lodging options",
            },
        ],
    },
    "practical_info": {
        "parking": "Available at monuments, parks, and visitor centers. Limited parking in some areas - arrive early during peak season",
        "permits": "National monuments require entrance fee (America the Beautiful pass accepted). Fishing requires Arizona fishing license",
        "best_times": "Year-round - milder than Phoenix. Spring and Fall are ideal for outdoor activities",
        "weather": {
            "summer": "Hot (90-100°F), early morning or evening activities recommended",
            "winter": "Mild (50-65°F), excellent for outdoor activities",
            "spring": "Pleasant (65-80°F), ideal for all activities",
            "fall": "Pleasant (65-80°F), ideal for all activities",
        },
        "access": "Easy access via I-17 from Phoenix (90 miles, 90 minutes). State Highway 260 provides access to Payson and Mogollon Rim",
        "considerations": [
            "National monuments have entrance fees",
            "Verde River water levels vary - check conditions",
            "Summer heat - plan activities for early morning or evening",
            "Limited parking at popular sites during peak season",
            "Gateway location - excellent base for exploring Verde Valley",
        ],
    },
}


class CampVerdeAgent(LocationAgentBase):
    """Agent specialized in Camp Verde, Arizona information and context.

    This agent enhances existing agent outputs with Camp Verde-specific knowledge
    about Verde Valley, Montezuma Castle, and outdoor opportunities.
    """

    LOCATION_NAME = "Camp Verde, Arizona"
    LOCATION_INDICATORS = [
        "camp verde",
        "camp verde, az",
        "camp verde, arizona",
        "camp verde az",
    ]
    AGENT_NAME = "camp_verde_agent"

    def get_location_knowledge(self) -> Dict[str, Any]:
        """Get Camp Verde-specific knowledge base."""
        return CAMP_VERDE_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Camp Verde agent."""
        return """You are a comprehensive guide for Camp Verde, Arizona - the "Gateway to Verde Valley"
located at 3,100 feet elevation in Yavapai County, known for Montezuma Castle, historic sites, and Verde River recreation.

Your role is to:
1. Use tools to gather real-time data about Camp Verde (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Camp Verde-specific knowledge from the knowledge base
4. Combine information from existing agents with Camp Verde expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Camp Verde, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Camp Verde, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Camp Verde, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information
- Mention proximity to Sedona trails (30 miles) for world-class mountain biking

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
- Gateway location benefits (access to Sedona, Cottonwood, Jerome)

TOOL USAGE GUIDANCE:

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Camp Verde, Arizona"
- Camp Verde is an excellent base camp for Sedona's world-class mountain biking (30 miles north)
- Local Verde Valley trails offer beginner to intermediate options
- Enhance tool results with knowledge base information about Sedona access and local trails
- Mention that Camp Verde is a gateway location - great base for exploring Sedona trails

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Camp Verde, Arizona"
- Popular local trails include Montezuma Castle Trail (0.3 miles, easy), Montezuma Well Trails (0.5-1.5 miles), and Verde River Greenway
- Use find_scenic_viewpoints for Verde Valley overlooks
- Enhance with knowledge base information about trail difficulty and best seasons
- Mention access to Sedona hiking (30 miles)

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Key sites: Montezuma Castle National Monument (ancient cliff dwelling), Montezuma Well (natural sinkhole), Fort Verde State Historic Park (Indian Wars fort)
- Enhance with knowledge base information about historical significance
- Provide context about Camp Verde's founding (1865) as military post

For Water Activities Queries:
- Verde River offers year-round fishing, kayaking, and swimming
- Use find_water_sources for Verde River access points
- Mention fishing (trout, bass, catfish), kayaking (Class I-II), and swimming opportunities
- Provide information about Arizona fishing license requirements

For Dining Queries:
- Use find_restaurants with location="Camp Verde, Arizona"
- Enhance results with knowledge base businesses
- Provide context about local favorites and atmosphere

For Accommodation Queries:
- Use search_accommodations with location="Camp Verde, Arizona"
- Enhance with knowledge base information (Cliff Castle Casino Hotel, campgrounds, RV parks)
- Mention proximity to attractions and gateway location benefits

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Montezuma Castle (early morning/late afternoon), Montezuma Well (unique lighting), Verde River (golden hour), Fort Verde (daylight)
- Mention seasonal opportunities (spring wildflowers, fall colors, winter clarity)

For Logistics Queries:
- Use get_parking_information for monument and trailhead parking
- Use find_water_sources for Verde River access
- Provide information about permits (National Monument entrance fees, America the Beautiful Pass, fishing licenses)
- Mention I-17 access from Phoenix (90 miles, 90 minutes)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Camp Verde, Arizona",
  "overview": "Brief overview of Camp Verde as gateway to Verde Valley",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
    "mountain_biking": {"trails": [...], "difficulty": "...", "best_seasons": "...", "note": "Gateway to Sedona trails"},
    "hiking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
    "water_activities": {"activities": [...], "seasons": "..."},
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

CAMP VERDE'S UNIQUE CHARACTERISTICS:
- Gateway to Verde Valley with easy access to Sedona (30 miles), Cottonwood (10 miles), and Jerome (20 miles)
- Montezuma Castle National Monument (ancient 5-story cliff dwelling, 1100-1425 AD)
- Montezuma Well (natural limestone sinkhole with unique ecosystem)
- Fort Verde State Historic Park (best-preserved Indian Wars period fort in Arizona)
- Verde River (year-round recreation: fishing, kayaking, swimming)
- Elevation: 3,100 feet (milder than Phoenix)
- ~11,000 residents
- Easy access via I-17 from Phoenix (90 miles, 90 minutes)

KEY ATTRACTIONS:
- Montezuma Castle National Monument: Well-preserved ancient cliff dwelling, easy 0.3-mile trail, visitor center
- Montezuma Well: Natural limestone sinkhole, ancient ruins, unique ecosystem, 11 miles from Montezuma Castle
- Fort Verde State Historic Park: Best-preserved Indian Wars fort, museum, historical reenactments
- Verde River: Year-round flowing river, fishing, kayaking, swimming, scenic beauty
- Camp Verde Historical Society Museum: Local history and artifacts

FAMOUS ACTIVITIES:
- Visiting Montezuma Castle and Montezuma Well (ancient ruins, easy access)
- Verde River recreation (fishing, kayaking, swimming)
- Access to Sedona's world-class trails (30 miles north)
- Historical site exploration (Fort Verde, museums)
- Gateway location - excellent base for exploring Verde Valley

PRACTICAL INFORMATION:
- Parking: Available at monuments, parks, and visitor centers. Limited parking in some areas - arrive early during peak season
- Permits: National monuments require entrance fee (America the Beautiful pass accepted). Fishing requires Arizona fishing license
- Best Times: Year-round - milder than Phoenix. Spring (March-May) and Fall (September-November) are ideal for outdoor activities
- Weather: Desert climate, four distinct seasons. Summer: 90-100°F (early morning/evening activities). Winter: 50-65°F (excellent for outdoor). Spring/Fall: 65-80°F (ideal)
- Access: Easy access via I-17 from Phoenix (90 miles, 90 minutes). State Highway 260 provides access to Payson and Mogollon Rim
- Considerations: National monuments have entrance fees. Verde River water levels vary - check conditions. Summer heat - plan activities for early morning or evening. Limited parking at popular sites during peak season. Gateway location - excellent base for exploring Verde Valley

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Camp Verde's gateway location and proximity to Sedona, Cottonwood, and Jerome
- Mention historical significance of Montezuma Castle, Montezuma Well, and Fort Verde
- Highlight Verde River recreation opportunities
- Emphasize year-round accessibility and milder climate than Phoenix
- Provide practical tips about parking, permits, and best times to visit

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Camp Verde-specific knowledge and context
- Enhanced recommendations based on Camp Verde's unique gateway character
- Practical tips for visitors"""

