"""Cottonwood, Arizona specialist agent.

This agent provides Cottonwood-specific information and enhances existing agent outputs
with local knowledge about Verde Valley, wine country, Old Town, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Cottonwood-specific knowledge base - Enhanced with detailed information
COTTONWOOD_KNOWLEDGE = {
    "location": {
        "name": "Cottonwood, Arizona",
        "coordinates": {"lat": 34.7392, "lon": -112.0099},
        "elevation": 3300,  # feet
        "region": "Yavapai County, Arizona",
        "country": "US",
        "nickname": "Heart of Verde Valley Wine Country",
        "proximity": {
            "jerome": {"distance_miles": 8, "direction": "northeast", "drive_time_minutes": 15},
            "sedona": {"distance_miles": 20, "direction": "northeast", "drive_time_minutes": 30},
            "prescott": {"distance_miles": 50, "direction": "southwest", "drive_time_minutes": 60},
            "camp_verde": {"distance_miles": 10, "direction": "southeast", "drive_time_minutes": 15},
            "phoenix": {"distance_miles": 100, "direction": "south", "drive_time_minutes": 100},
        },
    },
    "history": {
        "founded": 1879,
        "incorporated": 1960,
        "current_population": "~12,000 residents",
        "known_for": [
            "Verde Valley wine country hub",
            "Historic Old Town with preserved architecture",
            "Gateway to Jerome (8 miles) and Sedona (20 miles)",
            "Verde River recreation",
            "Dead Horse Ranch State Park",
            "Tuzigoot National Monument proximity",
        ],
        "historical_significance": "Founded as a mining and agricultural community, evolved into wine country destination and gateway to Verde Valley attractions",
    },
    "geography": {
        "terrain": "Valley, desert, river",
        "topography": "Verde Valley, Verde River",
        "elevation": "3,300 feet",
        "climate": "Desert climate, four distinct seasons, milder than Phoenix",
        "features": [
            "Verde River (flows year-round)",
            "Dead Horse Ranch State Park (324 acres)",
            "Tuzigoot National Monument (5 miles away)",
            "Verde Valley wine country",
        ],
        "ecosystem": "Desert riparian along Verde River, transitioning to desert scrub",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Local trails at Dead Horse Ranch State Park and excellent base camp for Sedona's world-class mountain biking (20 miles northeast)",
            "famous_trails": [
                {
                    "name": "Dead Horse Ranch State Park Trails",
                    "difficulty": "Beginner to Intermediate",
                    "length_miles": "Varies (multiple interconnected trails)",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network within state park with varied difficulty. Good for beginners and intermediate riders.",
                    "highlights": ["State park trails", "Varied difficulty", "Scenic", "Beginner-friendly"],
                    "best_seasons": "Year-round (best Spring, Fall, Winter)",
                    "trailhead": "Dead Horse Ranch State Park",
                    "features": ["State park", "Varied difficulty", "Scenic"],
                    "permits": "State park entrance fee required",
                },
                {
                    "name": "Sedona Trails Access",
                    "difficulty": "Beginner to Expert",
                    "length_miles": "Varies",
                    "description": "20 miles to Sedona's world-class mountain biking trails including Hiline, Hangover, Highline, and many others",
                    "highlights": ["World-class trails", "Red rock scenery", "Varied difficulty", "20 miles away"],
                    "best_seasons": "Spring, Fall, Winter",
                    "trailhead": "Sedona (20 miles northeast)",
                    "note": "Cottonwood is an excellent base camp for Sedona mountain biking",
                },
            ],
            "difficulty_range": "Beginner to expert (via Sedona access)",
            "best_seasons": "Year-round (best Spring, Fall, Winter)",
            "summer_conditions": "Hot in summer - early morning or evening rides recommended",
            "trail_features": ["Local trails", "Access to Sedona", "Varied difficulty"],
        },
        "hiking": {
            "description": "Local trails at Dead Horse Ranch State Park and Tuzigoot National Monument, plus access to Sedona hiking",
            "famous_trails": [
                {
                    "name": "Dead Horse Ranch State Park Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies (multiple trail options)",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network within state park with easy to moderate difficulty. Good for families and casual hikers.",
                    "highlights": ["State park trails", "Family-friendly", "Easy to moderate", "Scenic"],
                    "best_seasons": "Year-round",
                    "trailhead": "Dead Horse Ranch State Park",
                    "features": ["State park", "Family-friendly", "Scenic"],
                    "permits": "State park entrance fee required",
                },
                {
                    "name": "Tuzigoot National Monument Trails",
                    "difficulty": "Easy",
                    "length_miles": "0.5 to 1.0",
                    "elevation_gain_feet": 100,
                    "description": "Easy trails around ancient Sinagua pueblo ruins with interpretive signs and scenic views",
                    "highlights": ["Ancient ruins", "Easy access", "Interpretive signs", "Scenic views"],
                    "best_seasons": "Year-round",
                    "trailhead": "Tuzigoot National Monument (5 miles from Cottonwood)",
                    "features": ["Historic site", "Easy", "Interpretive"],
                    "permits": "National Monument entrance fee required",
                },
            ],
            "difficulty_range": "Easy to moderate (local), access to challenging Sedona trails",
            "best_seasons": "Year-round - milder than Phoenix",
            "trail_features": ["State park", "National monument", "Access to Sedona"],
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
            "description": "Historic Old Town, Verde River, wine country vineyards, and scenic Verde Valley offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Historic Old Town Cottonwood",
                    "best_time": "Daylight hours, golden hour for architecture",
                    "subjects": "Historic buildings, wine tasting rooms, street scenes",
                },
                {
                    "name": "Verde River",
                    "best_time": "Golden hour for scenic river shots",
                    "subjects": "Riverside scenery, wildlife, water features",
                },
                {
                    "name": "Wine Country Vineyards",
                    "best_time": "Golden hour, sunrise/sunset",
                    "subjects": "Vineyard rows, mountain backdrops, seasonal changes",
                },
                {
                    "name": "Tuzigoot National Monument",
                    "best_time": "Daylight hours",
                    "subjects": "Ancient ruins, scenic views, historical significance",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring wildflowers, fall colors, winter clarity",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Dead Horse Ranch State Park",
                "type": "State Park",
                "description": "324-acre state park with trails, fishing, and recreation",
                "highlights": ["Trails", "Fishing", "Recreation", "Family-friendly"],
                "activities": ["Hiking", "Mountain biking", "Fishing", "Camping"],
                "distance": "In Cottonwood",
            },
            {
                "name": "Verde River",
                "type": "River",
                "description": "Year-round flowing river offering recreation and scenic beauty",
                "highlights": ["Year-round flow", "Recreation", "Scenic", "Wildlife"],
                "activities": ["Fishing", "Kayaking", "Swimming", "Photography"],
            },
            {
                "name": "Tuzigoot National Monument",
                "type": "National Monument",
                "description": "Ancient Sinagua pueblo ruins with museum and trails",
                "highlights": ["Ancient ruins", "Museum", "Trails", "Historical significance"],
                "activities": ["Hiking", "Photography", "Historical tours"],
                "distance": "5 miles from Cottonwood",
            },
        ],
        "cultural": [
            {
                "name": "Historic Old Town Cottonwood",
                "type": "Historic District",
                "description": "Preserved historic downtown with wine tasting rooms, restaurants, and shops",
                "highlights": ["Historic architecture", "Wine tasting", "Shopping", "Dining"],
            },
            {
                "name": "Verde Valley Wine Country",
                "type": "Wine Region",
                "description": "Multiple wineries and tasting rooms in Old Town and surrounding area",
                "highlights": ["Wine tasting", "Multiple wineries", "Scenic vineyards"],
            },
            {
                "name": "Blazin' M Ranch",
                "type": "Entertainment",
                "description": "Western-themed entertainment and dining",
                "highlights": ["Western theme", "Entertainment", "Dining"],
            },
        ],
        "nearby": [
            {
                "name": "Jerome",
                "distance": "8 miles",
                "description": "Historic mining town, ghost town revival, artistic community",
            },
            {
                "name": "Sedona",
                "distance": "20 miles",
                "description": "World-renowned red rock destination with world-class trails",
            },
            {
                "name": "Camp Verde",
                "distance": "10 miles",
                "description": "Montezuma Castle, Montezuma Well, Fort Verde",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Crema Craft Kitchen",
                "type": "American",
                "description": "Local favorite with craft cocktails and American cuisine",
                "highlights": ["Local favorite", "Craft cocktails", "American cuisine"],
            },
            {
                "name": "Nic's Italian Steak & Crab House",
                "type": "Italian/Steakhouse",
                "description": "Upscale dining with Italian and steakhouse options",
                "highlights": ["Upscale", "Italian cuisine", "Steakhouse"],
            },
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Old Town offers several dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "wineries": [
            {
                "name": "Arizona Stronghold Vineyards",
                "type": "Winery",
                "description": "Wine tasting room in Old Town",
                "highlights": ["Wine tasting", "Old Town location"],
            },
            {
                "name": "Pillsbury Wine Company",
                "type": "Winery",
                "description": "Wine tasting room",
                "highlights": ["Wine tasting"],
            },
            {
                "name": "Multiple wineries",
                "type": "Winery",
                "description": "Verde Valley wine country offers multiple wineries and tasting rooms - use tools to find current options",
                "note": "Use find_restaurants or search for wineries to find current tasting rooms",
            },
        ],
        "accommodations": [
            {
                "name": "Tavern Hotel",
                "type": "Boutique Hotel",
                "description": "Historic boutique hotel in Old Town",
                "highlights": ["Historic", "Boutique", "Old Town location"],
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
        "parking": "Available in Old Town and at parks. Old Town parking can be limited during peak times - arrive early",
        "permits": "State parks require entrance fee (America the Beautiful pass accepted). National monuments require entrance fee. Fishing requires Arizona fishing license",
        "best_times": "Year-round - milder than Phoenix. Spring and Fall are ideal for outdoor activities",
        "weather": {
            "summer": "Hot (90-100°F), early morning or evening activities recommended",
            "winter": "Mild (50-65°F), excellent for outdoor activities",
            "spring": "Pleasant (65-80°F), ideal for all activities",
            "fall": "Pleasant (65-80°F), ideal for all activities",
        },
        "access": "Easy access via Highway 89A from Sedona (20 miles) and Jerome (8 miles). Highway 260 provides access from Phoenix (100 miles, 100 minutes)",
        "considerations": [
            "State parks have entrance fees",
            "Verde River water levels vary - check conditions",
            "Summer heat - plan activities for early morning or evening",
            "Old Town parking can be limited during peak times",
            "Gateway location - excellent base for exploring Verde Valley",
            "Wine country - many tasting rooms in Old Town",
        ],
    },
}


class CottonwoodAgent(LocationAgentBase):
    """Agent specialized in Cottonwood, Arizona information and context.

    This agent enhances existing agent outputs with Cottonwood-specific knowledge
    about Verde Valley, wine country, and outdoor opportunities.
    """

    LOCATION_NAME = "Cottonwood, Arizona"
    LOCATION_INDICATORS = [
        "cottonwood",
        "cottonwood, az",
        "cottonwood, arizona",
        "cottonwood az",
    ]
    AGENT_NAME = "cottonwood_agent"

    def get_location_knowledge(self) -> Dict[str, Any]:
        """Get Cottonwood-specific knowledge base."""
        return COTTONWOOD_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Cottonwood agent."""
        return """You are a comprehensive guide for Cottonwood, Arizona - the "Heart of Verde Valley Wine Country"
located at 3,300 feet elevation in Yavapai County, known for historic Old Town, wine country, and gateway location.

Your role is to:
1. Use tools to gather real-time data about Cottonwood (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Cottonwood-specific knowledge from the knowledge base
4. Combine information from existing agents with Cottonwood expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Cottonwood, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Cottonwood, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Cottonwood, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (state park entrance fees)
- Mention proximity to Sedona trails (20 miles) for world-class mountain biking

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
- Proximity to Sedona trails (20 miles) for world-class mountain biking
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Cottonwood, Arizona"
- Cottonwood is an excellent base camp for Sedona's world-class mountain biking (20 miles northeast)
- Local trails at Dead Horse Ranch State Park offer beginner to intermediate options
- Enhance tool results with knowledge base information about Sedona proximity and local trails
- Mention that Cottonwood is a gateway location - great base for exploring Sedona trails

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Cottonwood, Arizona"
- Popular local trails include Dead Horse Ranch State Park trails and Tuzigoot National Monument trails (5 miles)
- Access to Sedona hiking (20 miles) and Jerome area trails (8 miles)
- Use find_scenic_viewpoints for Verde Valley overlooks
- Enhance with knowledge base information about trail difficulty and best seasons

For Wine Country Queries:
- Cottonwood is the heart of Verde Valley wine country with multiple tasting rooms in Old Town
- Use find_restaurants to locate wine tasting rooms (many are listed as restaurants)
- Key wineries: Arizona Stronghold Vineyards, Pillsbury Wine Company, and many others
- Enhance with knowledge base information about wine country character

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Key sites: Historic Old Town Cottonwood (preserved architecture), Tuzigoot National Monument (ancient Sinagua pueblo ruins, 5 miles)
- Enhance with knowledge base information about Cottonwood's history and wine country evolution
- Provide context about gateway location to Jerome and Sedona

For Water Activities Queries:
- Verde River offers year-round fishing, kayaking, and swimming
- Use find_water_sources for Verde River access points
- Mention fishing (trout, bass, catfish), kayaking (Class I-II), and swimming opportunities
- Provide information about Arizona fishing license requirements

For Dining Queries:
- Use find_restaurants with location="Cottonwood, Arizona"
- Enhance results with knowledge base businesses (Crema Craft Kitchen, Nic's Italian Steak & Crab House)
- Many wine tasting rooms also serve food
- Provide context about Old Town atmosphere and wine country character

For Accommodation Queries:
- Use search_accommodations with location="Cottonwood, Arizona"
- Enhance with knowledge base information (Tavern Hotel, various options)
- Mention proximity to attractions and gateway location benefits

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Historic Old Town (daylight/golden hour), Verde River (golden hour), wine country vineyards (sunrise/sunset), Tuzigoot National Monument (daylight)
- Mention seasonal opportunities (spring wildflowers, fall colors, winter clarity)

For Logistics Queries:
- Use get_parking_information (Old Town parking can be limited during peak times)
- Use find_water_sources for Verde River access
- Provide information about permits (state park entrance fees, America the Beautiful Pass, fishing licenses)
- Mention Highway 89A access from Sedona (20 miles) and Jerome (8 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Cottonwood, Arizona",
  "overview": "Brief overview of Cottonwood as heart of Verde Valley wine country",
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

COTTONWOOD'S UNIQUE CHARACTERISTICS:
- Heart of Verde Valley wine country with multiple tasting rooms in Old Town
- Historic Old Town with preserved architecture and wine tasting rooms
- Gateway to Jerome (8 miles northeast) and Sedona (20 miles northeast)
- Dead Horse Ranch State Park (324 acres with trails and recreation)
- Tuzigoot National Monument (5 miles - ancient Sinagua pueblo ruins)
- Verde River (year-round recreation: fishing, kayaking, swimming)
- Elevation: 3,300 feet (milder than Phoenix)
- ~12,000 residents
- Easy access via Highway 89A from Sedona and Jerome

KEY ATTRACTIONS:
- Historic Old Town Cottonwood: Preserved historic downtown with wine tasting rooms, restaurants, and shops
- Verde Valley Wine Country: Multiple wineries and tasting rooms in Old Town and surrounding area
- Dead Horse Ranch State Park: 324-acre state park with trails, fishing, and recreation
- Verde River: Year-round flowing river offering fishing, kayaking, swimming, and scenic beauty
- Tuzigoot National Monument: Ancient Sinagua pueblo ruins with museum and trails (5 miles away)
- Blazin' M Ranch: Western-themed entertainment and dining

FAMOUS ACTIVITIES:
- Wine tasting (multiple tasting rooms in Old Town - Arizona Stronghold, Pillsbury, and many others)
- Verde River recreation (fishing, kayaking, swimming)
- Access to Sedona's world-class trails (20 miles northeast)
- Gateway to Jerome (8 miles) - historic mining town
- Historical site exploration (Tuzigoot National Monument, Old Town)

PRACTICAL INFORMATION:
- Parking: Available in Old Town and at parks. Old Town parking can be limited during peak times - arrive early
- Permits: State parks require entrance fee (America the Beautiful pass accepted). National monuments require entrance fee. Fishing requires Arizona fishing license
- Best Times: Year-round - milder than Phoenix. Spring (March-May) and Fall (September-November) are ideal for outdoor activities
- Weather: Desert climate, four distinct seasons. Summer: 90-100°F (early morning/evening activities). Winter: 50-65°F (excellent for outdoor). Spring/Fall: 65-80°F (ideal)
- Access: Easy access via Highway 89A from Sedona (20 miles) and Jerome (8 miles). Highway 260 provides access from Phoenix (100 miles, 100 minutes)
- Considerations: State parks have entrance fees. Verde River water levels vary - check conditions. Summer heat - plan activities for early morning or evening. Old Town parking can be limited during peak times. Gateway location - excellent base for exploring Verde Valley. Wine country - many tasting rooms in Old Town

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Cottonwood's gateway location and proximity to Sedona, Jerome, and Camp Verde
- Mention wine country character and Old Town atmosphere
- Highlight Verde River recreation opportunities
- Emphasize year-round accessibility and milder climate than Phoenix
- Provide practical tips about parking, permits, and best times to visit

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Cottonwood-specific knowledge and context
- Enhanced recommendations based on Cottonwood's unique wine country and gateway character
- Practical tips for visitors"""

