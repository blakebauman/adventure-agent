"""Payson, Arizona specialist agent.

This agent provides Payson-specific information and enhances existing agent outputs
with local knowledge about Mogollon Rim, Tonto National Forest, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Payson-specific knowledge base - Enhanced with detailed information
PAYSON_KNOWLEDGE = {
    "location": {
        "name": "Payson, Arizona",
        "coordinates": {"lat": 34.2309, "lon": -111.3251},
        "elevation": 5000,  # feet
        "region": "Gila County, Arizona",
        "country": "US",
        "nickname": "Heart of Arizona",
        "proximity": {
            "phoenix": {"distance_miles": 90, "direction": "south", "drive_time_minutes": 90},
            "pinetop": {"distance_miles": 80, "direction": "east", "drive_time_minutes": 90},
            "pine": {"distance_miles": 15, "direction": "southeast", "drive_time_minutes": 20},
            "strawberry": {"distance_miles": 20, "direction": "southeast", "drive_time_minutes": 25},
            "sedona": {"distance_miles": 70, "direction": "northwest", "drive_time_minutes": 90},
        },
    },
    "history": {
        "founded": 1882,
        "incorporated": 1973,
        "current_population": "~16,000 residents",
        "known_for": [
            "Mogollon Rim gateway",
            "Tonto National Forest",
            "Ponderosa pine forests",
            "Cooler climate than Phoenix",
            "Outdoor recreation hub",
            "World's oldest continuous rodeo",
        ],
        "historical_significance": "Founded as a mining and ranching community, evolved into outdoor recreation destination",
    },
    "geography": {
        "terrain": "Mountainous, pine forests",
        "topography": "Mogollon Rim, Tonto National Forest",
        "elevation": "5,000 feet",
        "climate": "Four distinct seasons, cooler than Phoenix",
        "features": [
            "Mogollon Rim (2,000-foot escarpment)",
            "Tonto Creek",
            "Ponderosa pine forests",
            "Mogollon Rim Ranger District",
        ],
        "ecosystem": "Ponderosa pine forest transitioning to mixed conifer at higher elevations",
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Extensive trail network in Tonto National Forest with varied terrain - from flowy singletrack to technical challenges",
            "famous_trails": [
                {
                    "name": "Highline Trail",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": 51.0,
                    "elevation_gain_feet": 8000,
                    "description": "Iconic 51-mile trail along Mogollon Rim with technical sections, scenic overlooks, and challenging terrain. Multiple access points allow for shorter sections.",
                    "highlights": [
                        "Scenic rim views",
                        "Technical sections",
                        "Multiple access points",
                        "Historic trail",
                        "Wildlife viewing"
                    ],
                    "best_seasons": "Spring (March-May), Fall (September-November)",
                    "trailhead": "Multiple access points along Highway 260 and Forest Road 300",
                    "features": ["Single track", "Technical", "Scenic views", "Wildlife"],
                    "permits": "Tonto National Forest - no permit required for day use",
                    "connectivity": "Connects to Mogollon Rim Trail and other forest trails"
                },
                {
                    "name": "Mogollon Rim Trail",
                    "difficulty": "Intermediate",
                    "length_miles": 25.0,
                    "elevation_gain_feet": 3000,
                    "description": "Scenic trail system along the rim with great views of the valley below. Well-maintained singletrack with moderate technical challenges.",
                    "highlights": ["Rim views", "Well-maintained", "Moderate difficulty", "Scenic overlooks"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Various access points along Forest Road 300",
                    "features": ["Single track", "Scenic views", "Moderate technical"],
                },
                {
                    "name": "Pine Trail",
                    "difficulty": "Beginner to Intermediate",
                    "length_miles": 8.0,
                    "elevation_gain_feet": 800,
                    "description": "Accessible trail through pine forests, great for beginners and families. Smooth singletrack with gentle elevation changes.",
                    "highlights": ["Beginner-friendly", "Family-friendly", "Smooth trail", "Pine forests"],
                    "best_seasons": "Year-round",
                    "trailhead": "Pine Trailhead (coordinates available via tools)",
                    "features": ["Single track", "Beginner-friendly", "Smooth"],
                },
                {
                    "name": "Houston Mesa Trail",
                    "difficulty": "Intermediate",
                    "length_miles": 6.5,
                    "elevation_gain_feet": 1200,
                    "description": "Popular trail with good flow, moderate technical sections, and scenic views. Great for intermediate riders.",
                    "highlights": ["Good flow", "Moderate technical", "Popular", "Scenic"],
                    "best_seasons": "Spring, Fall",
                    "trailhead": "Houston Mesa Trailhead",
                    "features": ["Single track", "Flow sections", "Moderate technical"],
                },
            ],
            "trail_networks": "Tonto National Forest offers extensive interconnected trail systems",
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Spring (March-May), Summer (June-August), Fall (September-November)",
            "winter_conditions": "Trails may be snow-covered or muddy December-February",
            "trail_conditions": "Generally well-maintained, can be dusty in summer",
            "trail_features": ["Single track", "Technical sections", "Flow trails", "Scenic views", "Wildlife"],
        },
        "hiking": {
            "description": "Extensive hiking trail network in Tonto National Forest with access to Mogollon Rim, scenic creeks, and pine forests",
            "famous_trails": [
                {
                    "name": "Highline Trail",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": 51.0,
                    "elevation_gain_feet": 8000,
                    "description": "Iconic 51-mile long-distance trail along Mogollon Rim. Multiple access points allow for day hikes or multi-day backpacking. Scenic rim views, pine forests, and varied terrain.",
                    "highlights": [
                        "Long-distance trail (51 miles)",
                        "Multiple access points",
                        "Scenic rim views",
                        "Backpacking opportunities",
                        "Wildlife viewing"
                    ],
                    "best_seasons": "Spring (March-May), Fall (September-November)",
                    "trailhead": "Multiple access points - check Tonto National Forest maps",
                    "features": ["Backpacking", "Scenic views", "Wildlife", "Water sources"],
                    "permits": "No permit required for day hikes, may need permits for overnight",
                    "connectivity": "Connects to Mogollon Rim Trail and other forest trails"
                },
                {
                    "name": "Horton Creek Trail",
                    "difficulty": "Moderate",
                    "length_miles": 8.0,
                    "elevation_gain_feet": 1200,
                    "description": "Popular 8-mile round trip creek-side trail with waterfalls, pools, and scenic forest. Great for day hikes with water features.",
                    "highlights": ["Waterfalls", "Creek crossings", "Swimming holes", "Scenic forest", "Popular trail"],
                    "best_seasons": "Spring (water flow), Summer (swimming), Fall (colors)",
                    "trailhead": "Horton Creek Trailhead (coordinates available via tools)",
                    "features": ["Water features", "Swimming", "Scenic", "Moderate difficulty"],
                    "permits": "No permit required",
                },
                {
                    "name": "Tonto Creek Trail",
                    "difficulty": "Easy to Moderate",
                    "length_miles": 4.0,
                    "elevation_gain_feet": 400,
                    "description": "Family-friendly creek-side trail with gentle elevation. Good for beginners and families. Scenic creek views and forest.",
                    "highlights": ["Family-friendly", "Creek views", "Easy access", "Beginner-friendly"],
                    "best_seasons": "Year-round",
                    "trailhead": "Tonto Creek Trailhead",
                    "features": ["Family-friendly", "Easy", "Creek views"],
                },
                {
                    "name": "Mogollon Rim Trail",
                    "difficulty": "Moderate",
                    "length_miles": 25.0,
                    "elevation_gain_feet": 3000,
                    "description": "Scenic rim trail with dramatic overlooks of the valley below. Well-maintained trail with moderate elevation changes.",
                    "highlights": ["Rim views", "Overlooks", "Well-maintained", "Moderate difficulty"],
                    "best_seasons": "Spring, Summer, Fall",
                    "trailhead": "Various access points along Forest Road 300",
                    "features": ["Scenic views", "Overlooks", "Moderate"],
                },
            ],
            "trail_networks": "Tonto National Forest offers extensive interconnected hiking trail systems",
            "difficulty_range": "Easy to strenuous",
            "best_seasons": "Year-round, but best in Spring and Fall",
            "trail_features": ["Scenic views", "Water features", "Wildlife", "Backpacking", "Day hikes"],
        },
        "climbing": {
            "description": "Limited climbing opportunities in Payson area, primarily bouldering and some sport climbing",
            "areas": [
                {
                    "name": "Mogollon Rim Bouldering",
                    "type": "Bouldering",
                    "routes": "Various",
                    "difficulty_range": "V0-V8",
                    "description": "Bouldering opportunities along Mogollon Rim. Limited developed areas, mostly exploratory.",
                    "access": "Various locations along rim, check local guidebooks",
                    "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
                },
            ],
            "note": "Payson is not a major climbing destination. For extensive climbing, consider nearby areas or use tools to find current climbing opportunities.",
        },
        "cycling": {
            "description": "Road and gravel cycling opportunities with scenic routes through pine forests and along Mogollon Rim",
            "routes": [
                {
                    "name": "Mogollon Rim Scenic Loop",
                    "type": "Road",
                    "length_miles": 45.0,
                    "elevation_gain_feet": 3500,
                    "description": "Scenic road cycling loop along Mogollon Rim with dramatic views. Moderate to challenging with significant elevation gain.",
                    "highlights": ["Scenic rim views", "Challenging climbs", "Low traffic", "Pine forests"],
                    "best_seasons": "Spring, Summer, Fall",
                    "difficulty": "Moderate to Challenging",
                },
                {
                    "name": "Highway 260 to Pine",
                    "type": "Road",
                    "length_miles": 15.0,
                    "elevation_gain_feet": 800,
                    "description": "Scenic road route from Payson to Pine with moderate elevation. Good for intermediate cyclists.",
                    "highlights": ["Scenic", "Moderate difficulty", "Small town destination"],
                    "best_seasons": "Year-round",
                    "difficulty": "Moderate",
                },
                {
                    "name": "Forest Road Gravel Routes",
                    "type": "Gravel",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Extensive network of forest roads suitable for gravel cycling. Routes vary in difficulty and length.",
                    "highlights": ["Gravel roads", "Varied routes", "Forest scenery", "Low traffic"],
                    "best_seasons": "Spring, Fall",
                    "difficulty": "Easy to Challenging",
                },
            ],
            "best_seasons": "Spring, Summer, Fall (avoid winter snow)",
            "trail_features": ["Road routes", "Gravel routes", "Scenic", "Varied difficulty"],
        },
        "paddling": {
            "description": "Limited paddling opportunities in Payson area. Tonto Creek offers some flatwater sections suitable for kayaking and canoeing.",
            "routes": [
                {
                    "name": "Tonto Creek Flatwater",
                    "type": "Flatwater",
                    "length_miles": 5.0,
                    "difficulty": "Class I",
                    "description": "Gentle flatwater section of Tonto Creek suitable for kayaking and canoeing. Best during spring runoff or after rains.",
                    "put_in": "Tonto Creek access points (coordinates available via tools)",
                    "take_out": "Various take-out points downstream",
                    "best_seasons": "Spring (water flow), early Summer",
                    "water_levels": "Dependent on rainfall and snowmelt - check current conditions",
                },
            ],
            "note": "Payson is not a major paddling destination. Water levels are seasonal. For extensive paddling, consider nearby lakes or use tools to find current opportunities.",
            "best_seasons": "Spring (water flow), early Summer",
        },
        "fishing": {
            "description": "Tonto Creek, streams, and lakes offer excellent fishing",
            "locations": [
                {"name": "Tonto Creek", "type": "Stream", "species": "Trout"},
                {"name": "Green Valley Park", "type": "Lake", "species": "Trout, bass"},
                {"name": "Nearby lakes", "type": "Lakes", "description": "Multiple stocked lakes in area"},
            ],
            "seasons": "Year-round, best in Spring and Fall",
            "permits": "Arizona fishing license required",
        },
        "photography": {
            "description": "Mogollon Rim views, pine forests, Tonto Creek offer excellent photo opportunities",
            "best_spots": [
                {
                    "name": "Mogollon Rim overlooks",
                    "best_time": "Sunrise and sunset",
                    "subjects": "Panoramic views, dramatic escarpment",
                },
                {
                    "name": "Tonto Creek",
                    "best_time": "Golden hour",
                    "subjects": "Water features, forest scenes",
                },
                {
                    "name": "Ponderosa pine forests",
                    "best_time": "Any time, especially with morning mist",
                    "subjects": "Forest landscapes, wildlife",
                },
            ],
            "seasons": "All seasons offer unique opportunities - fall colors, winter snow, spring wildflowers",
        },
        "camping": {
            "description": "Multiple campgrounds in Tonto National Forest",
            "options": [
                "Developed campgrounds with amenities",
                "Dispersed camping in designated areas",
                "RV parks in town",
            ],
            "permits": "Some areas require permits, check Tonto National Forest regulations",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Mogollon Rim",
                "description": "2,000-foot escarpment with dramatic views",
                "activities": ["Hiking", "Mountain biking", "Photography", "Camping"],
            },
            {
                "name": "Tonto National Forest",
                "description": "3 million acres of public land with extensive trail network",
                "activities": ["All outdoor activities"],
            },
            {
                "name": "Tonto Creek",
                "description": "Scenic creek with fishing and hiking opportunities",
            },
            {
                "name": "Green Valley Park",
                "description": "Community park with lake, fishing, and recreation facilities",
            },
        ],
        "cultural": [
            {
                "name": "Rim Country Museum",
                "description": "Local history museum showcasing Payson's heritage",
                "hours": "Check current hours",
            },
            {
                "name": "Payson Rodeo",
                "description": "World's oldest continuous rodeo, held annually in August",
                "significance": "Historic event dating back to 1884",
            },
            {
                "name": "Tonto Natural Bridge State Park",
                "description": "Natural travertine bridge, largest in the world",
                "distance": "10 miles from Payson",
                "activities": ["Hiking", "Photography", "Nature viewing"],
            },
        ],
        "nearby": [
            {
                "name": "Pine",
                "distance": "15 miles",
                "description": "Small mountain town with additional trails and amenities",
            },
            {
                "name": "Strawberry",
                "distance": "20 miles",
                "description": "Historic town with pie shop and local charm",
            },
            {
                "name": "Tonto Natural Bridge",
                "distance": "10 miles",
                "description": "State park with natural bridge",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Macky's Grill",
                "type": "American",
                "description": "Local favorite for casual dining",
                "highlights": ["Family-friendly", "Local atmosphere"],
            },
            {
                "name": "Crosswinds Restaurant",
                "type": "American",
                "description": "Full-service restaurant",
            },
            {
                "name": "Fargo's Steakhouse",
                "type": "Steakhouse",
                "description": "Upscale dining",
            },
        ],
        "accommodations": [
            {
                "name": "Majestic Mountain Inn",
                "type": "Hotel",
                "description": "Full-service hotel in town center",
                "highlights": ["Convenient location", "All amenities"],
            },
            {
                "name": "Various RV Parks",
                "type": "RV Park",
                "description": "Multiple RV parks available",
            },
            {
                "name": "Cabins and Vacation Rentals",
                "type": "Vacation Rental",
                "description": "Various cabin rentals available",
            },
        ],
        "services": [
            {
                "name": "Bike Shops",
                "type": "Retail",
                "description": "Local bike shops for repairs and gear",
            },
            {
                "name": "Grocery Stores",
                "type": "Retail",
                "description": "Full-service grocery stores for resupply",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in town and at trailheads. Popular trailheads may fill up on weekends - arrive early.",
        "permits": "Tonto National Forest - some areas may require permits. Check current regulations. America the Beautiful Pass accepted.",
        "best_times": "Year-round - cooler than Phoenix. Spring (March-May) and Fall (September-November) are ideal. Summer is warm but manageable. Winter may have snow.",
        "weather": {
            "spring": "Mild (50-75°F), perfect for outdoor activities",
            "summer": "Warm (70-90°F), cooler than Phoenix, afternoon thunderstorms possible",
            "fall": "Mild to cool (45-70°F), excellent conditions",
            "winter": "Cool to cold (30-55°F), snow possible at higher elevations",
        },
        "access": "Highway 87 (Beeline Highway) from Phoenix - scenic 90-mile drive. Easy access from I-17.",
        "cell_service": "Variable - may be limited in remote areas",
        "water_sources": "Carry water - streams may be seasonal. Check current conditions.",
        "wildlife": "Black bears, mountain lions, elk present. Store food properly, be aware of surroundings.",
        "fire_restrictions": "Check current fire restrictions - may affect camping and campfires",
        "considerations": [
            "Elevation is 5,000 feet - sun protection important",
            "Weather can change quickly in mountains",
            "Some trails may be closed seasonally",
            "Respect private property boundaries",
            "Leave no trace principles",
        ],
    },
}


class PaysonAgent(LocationAgentBase):
    """Agent specialized in Payson, Arizona information and context.

    This agent enhances existing agent outputs with Payson-specific knowledge
    about Mogollon Rim, Tonto National Forest, and outdoor opportunities.
    """

    LOCATION_NAME = "Payson, Arizona"
    LOCATION_INDICATORS = [
        "payson",
        "payson, az",
        "payson, arizona",
        "payson az",
    ]
    AGENT_NAME = "payson_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Payson-specific knowledge base (fallback if external file not found)."""
        return PAYSON_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Payson agent."""
        return """You are a comprehensive guide for Payson, Arizona - the "Heart of Arizona"
and gateway to the Mogollon Rim, located at 5,000 feet elevation in Gila County.

Your role is to:
1. Use tools to gather real-time data about Payson (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Payson-specific knowledge from the knowledge base
4. Combine information from existing agents with Payson expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Payson, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Payson, Arizona")
- For climbing: search_trails(activity_type="climbing", location="Payson, Arizona") if available
- For cycling: search_trails(activity_type="cycling", location="Payson, Arizona")
- For paddling: search_trails(activity_type="paddling", location="Payson, Arizona") if available
- For trail running: search_trails(activity_type="trail_running", location="Payson, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information
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
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Payson, Arizona"
- Payson has extensive trails in Tonto National Forest including Highline Trail, Mogollon Rim Trail, Pine Trail, and Houston Mesa Trail
- Enhance tool results with knowledge base information about trail difficulty, length, and conditions
- Mention seasonal considerations (winter snow, summer dust)

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Payson, Arizona"
- Popular trails include Highline Trail (51 miles, multiple access points), Mogollon Rim Trail, Horton Creek Trail (8 miles, waterfalls), and Tonto Creek Trail
- Use find_scenic_viewpoints for Mogollon Rim overlooks
- Enhance with knowledge base information about trail difficulty and best seasons

For Dining Queries:
- Use find_restaurants with location="Payson, Arizona"
- Enhance results with knowledge base businesses (Macky's Grill, Crosswinds, Fargo's Steakhouse)
- Provide context about local favorites and atmosphere

For Accommodation Queries:
- Use search_accommodations with location="Payson, Arizona"
- Enhance with knowledge base information (Majestic Mountain Inn, RV parks, cabin rentals)
- Mention proximity to trails and attractions

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Enhance with knowledge base information about Rim Country Museum, Payson Rodeo (world's oldest continuous rodeo since 1884), and Tonto Natural Bridge State Park
- Provide historical context about Payson's founding (1882) and evolution

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Mogollon Rim overlooks (sunrise/sunset), Tonto Creek (golden hour), Ponderosa pine forests
- Mention seasonal opportunities (fall colors, winter snow, spring wildflowers)

For Logistics Queries:
- Use get_parking_information for trailhead parking
- Use find_water_sources for water availability
- Provide information about permits (Tonto National Forest, America the Beautiful Pass)
- Mention Highway 87 access from Phoenix (90 miles, scenic drive)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Payson, Arizona",
  "overview": "Brief overview of Payson as gateway to Mogollon Rim",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
    "mountain_biking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
    "hiking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
    "climbing": {"areas": [...], "difficulty_range": "...", "best_seasons": "..."},
    "cycling": {"routes": [...], "type": "...", "best_seasons": "..."},
    "paddling": {"routes": [...], "type": "...", "best_seasons": "..."},
    "fishing": {"locations": [...], "seasons": "..."},
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

PAYSON'S UNIQUE CHARACTERISTICS:
- Gateway to Mogollon Rim (2,000-foot escarpment with dramatic views)
- Tonto National Forest (3 million acres, extensive trail network)
- Ponderosa pine forests (elevation 5,000 feet)
- Cooler climate than Phoenix (four distinct seasons)
- World's oldest continuous rodeo (since 1884, held in August)
- ~16,000 residents, outdoor recreation hub
- Easy access from Phoenix via Highway 87 (90 miles, scenic Beeline Highway)
- Gateway to nearby Pine (15 miles) and Strawberry (20 miles)

KEY ATTRACTIONS:
- Mogollon Rim: 2,000-foot escarpment with hiking, biking, camping, photography
- Tonto National Forest: 3 million acres with extensive trail network
- Tonto Creek: Fishing, hiking, scenic beauty
- Green Valley Park: Community park with lake and fishing
- Rim Country Museum: Local history and heritage
- Payson Rodeo: World's oldest continuous rodeo (August)
- Tonto Natural Bridge State Park: 10 miles away, largest natural travertine bridge

FAMOUS TRAILS:
- Highline Trail: 51-mile long-distance trail along Mogollon Rim (multiple access points, moderate to strenuous)
- Mogollon Rim Trail: Scenic rim trail with overlooks (intermediate)
- Horton Creek Trail: 8-mile round trip, popular creek-side trail with waterfalls (moderate)
- Tonto Creek Trail: Creek-side trail, good for families (easy to moderate)
- Pine Trail: ~8 miles, accessible through pine forests (beginner to intermediate)
- Houston Mesa Trail: Popular trail with good flow (intermediate)

PRACTICAL INFORMATION:
- Parking: Available in town and at trailheads. Popular trailheads may fill on weekends - arrive early.
- Permits: Tonto National Forest - some areas require permits. America the Beautiful Pass accepted.
- Best Times: Year-round but Spring (March-May) and Fall (September-November) are ideal. Summer is warm but manageable. Winter may have snow at higher elevations.
- Weather: Four distinct seasons. Spring: 50-75°F. Summer: 70-90°F with afternoon thunderstorms. Fall: 45-70°F. Winter: 30-55°F with possible snow.
- Access: Highway 87 (Beeline Highway) from Phoenix - scenic 90-mile drive. Easy access from I-17.
- Considerations: Elevation 5,000 feet - sun protection important. Weather changes quickly. Some trails closed seasonally. Respect private property. Leave no trace. Wildlife present (bears, mountain lions, elk).

ENHANCEMENT GUIDELINES:
- Always combine tool results with knowledge base information
- Provide specific recommendations based on activity type and season
- Include safety considerations (wildlife, weather, elevation)
- Mention nearby attractions (Pine, Strawberry, Tonto Natural Bridge)
- Highlight unique characteristics (Mogollon Rim gateway, rodeo history)
- Provide practical tips (parking, permits, best times, access)

Provide comprehensive, accurate, practical information that combines real tool data with Payson-specific knowledge and context."""

