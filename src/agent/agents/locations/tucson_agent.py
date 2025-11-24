"""Tucson, Arizona specialist agent.

This agent provides Tucson-specific information and enhances existing agent outputs
with local knowledge about Sonoran Desert, Saguaro National Park, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Tucson-specific knowledge base
TUCSON_KNOWLEDGE = {
    "location": {
        "name": "Tucson, Arizona",
        "coordinates": {"lat": 32.2226, "lon": -110.9747},
        "elevation": 2400,  # feet
        "region": "Pima County, Arizona",
        "country": "US",
        "nickname": "Old Pueblo",
        "proximity": {
            "phoenix": {"distance_miles": 115, "direction": "north"},
            "bisbee": {"distance_miles": 95, "direction": "southeast"},
            "nogales": {"distance_miles": 65, "direction": "south"},
            "mount_lemmon": {"distance_miles": 30, "direction": "northeast"},
        },
    },
    "history": {
        "founded": 1775,
        "incorporated": 1877,
        "current_population": "~550,000 (metro: ~1 million)",
        "known_for": [
            "Sonoran Desert",
            "Saguaro National Park",
            "University of Arizona",
            "Desert trails and mountain biking",
            "Historic Old Pueblo",
            "Mount Lemmon (sky island)",
        ],
    },
    "geography": {
        "terrain": "Desert, mountains, sky islands",
        "topography": "Sonoran Desert, Santa Catalina Mountains, Saguaro National Park",
        "elevation": "2,400 feet",
        "climate": "Hot desert climate, mild winters, hot summers (cooler than Phoenix)",
        "features": [
            "Saguaro National Park (East and West units)",
            "Santa Catalina Mountains (Mount Lemmon - 9,157 ft)",
            "Tucson Mountains",
            "Rincon Mountains",
            "Sonoran Desert",
        ],
    },
    "outdoor_activities": {
        "mountain_biking": {
            "description": "Extensive desert and mountain trail network with world-class singletrack in desert preserves and mountain terrain",
            "famous_trails": [
                {
                    "name": "50 Year Trail (Tucson Mountain Park)",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": 8.0,
                    "elevation_gain_feet": 1000,
                    "description": "Popular intermediate to advanced trail in Tucson Mountain Park with technical sections, scenic desert views, and challenging terrain. One of Tucson's most popular MTB trails.",
                    "highlights": ["Technical sections", "Scenic desert", "Popular", "Challenging", "Intermediate-friendly"],
                    "best_seasons": "Fall (October-November), Winter (December-February), Spring (March-April)",
                    "trailhead": "50 Year Trailhead (Tucson Mountain Park)",
                    "features": ["Single track", "Technical", "Desert scenery", "Challenging"],
                    "permits": "Tucson Mountain Park - no permit required",
                    "warnings": ["Extreme heat in summer - ride early morning or evening"],
                },
                {
                    "name": "Sweetwater Preserve Trails",
                    "difficulty": "Beginner to Intermediate",
                    "length_miles": "10+ miles of interconnected trails",
                    "elevation_gain_feet": "Varies by route",
                    "description": "Extensive trail system in Sweetwater Preserve with trails for all skill levels. Well-maintained singletrack with good flow and scenic desert views.",
                    "highlights": ["Trail system", "All skill levels", "Well-maintained", "Good flow", "Scenic desert"],
                    "best_seasons": "Fall, Winter, Spring",
                    "trailhead": "Sweetwater Preserve Trailhead",
                    "features": ["Trail system", "Varied difficulty", "Flow", "Desert scenery"],
                    "permits": "No permit required",
                },
                {
                    "name": "Starr Pass Trails",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": "15+ miles of trails",
                    "elevation_gain_feet": "Varies",
                    "description": "Challenging trail system with technical sections, significant elevation gain, and scenic desert views. Popular with advanced riders.",
                    "highlights": ["Technical", "Challenging", "Scenic", "Advanced", "Popular"],
                    "best_seasons": "Fall, Winter, Spring",
                    "trailhead": "Starr Pass Trailhead",
                    "features": ["Technical", "Challenging", "Desert scenery"],
                    "permits": "No permit required",
                },
                {
                    "name": "Fantasy Island (Tucson Mountain Park)",
                    "difficulty": "Beginner to Intermediate",
                    "length_miles": "8+ miles of trails",
                    "elevation_gain_feet": "Varies",
                    "description": "Beginner-friendly trail system with smooth singletrack, gentle elevation, and scenic desert views. Great for families and beginners.",
                    "highlights": ["Beginner-friendly", "Smooth trails", "Family-friendly", "Scenic desert"],
                    "best_seasons": "Fall, Winter, Spring",
                    "trailhead": "Fantasy Island Trailhead (Tucson Mountain Park)",
                    "features": ["Beginner-friendly", "Smooth", "Family-friendly"],
                    "permits": "Tucson Mountain Park - no permit required",
                },
                {
                    "name": "Mount Lemmon Trails (Seasonal)",
                    "difficulty": "Intermediate to Advanced",
                    "length_miles": "Varies by trail",
                    "elevation_gain_feet": "Varies",
                    "description": "Mountain trails on Mount Lemmon (9,157 ft) accessible in summer when desert is too hot. Cooler temperatures and mountain terrain. Accessible via Catalina Highway.",
                    "highlights": ["Cooler in summer", "Mountain terrain", "Sky island", "Seasonal access"],
                    "best_seasons": "Summer (June-August) - escape desert heat",
                    "trailhead": "Various trailheads on Mount Lemmon (30 miles from Tucson)",
                    "features": ["Mountain terrain", "Cooler temperatures", "Seasonal"],
                    "permits": "Coronado National Forest - no permit required for day use",
                    "note": "Mount Lemmon provides cool escape in summer when desert trails are too hot",
                },
            ],
            "trail_networks": "Extensive interconnected trail systems in desert preserves and mountain terrain",
            "difficulty_range": "Beginner to expert",
            "best_seasons": "Fall (October-November), Winter (December-February), Spring (March-April) - Mount Lemmon in summer",
            "trail_conditions": "Generally well-maintained, can be dusty in summer",
            "trail_features": ["Single track", "Technical sections", "Desert scenery", "Mountain terrain", "Sky island access"],
        },
        "hiking": {
            "description": "Desert trails, mountain hikes, and Saguaro National Park with iconic saguaro cacti and scenic desert landscapes",
            "famous_trails": [
                {
                    "name": "Mount Lemmon Trails",
                    "difficulty": "Easy to Strenuous",
                    "length_miles": "Varies by trail (multiple trails available)",
                    "elevation_gain_feet": "Varies",
                    "description": "Multiple hiking trails on Mount Lemmon (9,157 ft peak) ranging from easy to strenuous. Cooler temperatures in summer make this a great escape from desert heat. Accessible via scenic Catalina Highway.",
                    "highlights": [
                        "Sky island (9,157 ft)",
                        "Cooler in summer",
                        "Multiple trails",
                        "Mountain terrain",
                        "Scenic views"
                    ],
                    "best_seasons": "Summer (June-August) - escape desert heat, also Spring and Fall",
                    "trailhead": "Various trailheads on Mount Lemmon (30 miles from Tucson via Catalina Highway)",
                    "features": ["Mountain terrain", "Cooler temperatures", "Multiple trails", "Sky island"],
                    "permits": "Coronado National Forest - no permit required for day use",
                    "note": "Mount Lemmon provides cool escape in summer (70-80°F vs 100°F in Tucson)",
                },
                {
                    "name": "Saguaro National Park Trails (East and West units)",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies by trail (multiple trails in both units)",
                    "elevation_gain_feet": "Varies",
                    "description": "Iconic trails through Saguaro National Park with spectacular saguaro cacti, desert wildlife, and scenic desert landscapes. Park has East and West units with separate entrances.",
                    "highlights": [
                        "Iconic saguaro cacti",
                        "Desert wildlife",
                        "Scenic desert landscapes",
                        "Multiple trails",
                        "National Park"
                    ],
                    "best_seasons": "Fall (October-November), Winter (December-February), Spring (March-April)",
                    "trailhead": "Various trailheads in East and West units (separate entrances)",
                    "features": ["Saguaro cacti", "Desert wildlife", "Scenic", "National Park"],
                    "permits": "Saguaro National Park requires entrance fee ($25/vehicle or America the Beautiful Pass)",
                    "warnings": ["Extreme heat in summer - hike early morning or evening", "Park has East and West units - separate entrances"],
                },
                {
                    "name": "Wasson Peak (Tucson Mountains)",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": 7.0,
                    "elevation_gain_feet": 1800,
                    "description": "Challenging hike to Wasson Peak summit with significant elevation gain, scenic desert views, and moderate to strenuous difficulty. Popular summit hike.",
                    "highlights": ["Summit views", "Scenic desert", "Challenging", "Popular", "Moderate to strenuous"],
                    "best_seasons": "Fall, Winter, Spring (early morning in summer)",
                    "trailhead": "Wasson Peak Trailhead (Tucson Mountain Park)",
                    "features": ["Summit hike", "Challenging", "Desert scenery"],
                    "permits": "Tucson Mountain Park - no permit required",
                    "warnings": ["Extreme heat in summer - hike early morning or evening"],
                },
                {
                    "name": "Seven Falls (Bear Canyon)",
                    "difficulty": "Moderate",
                    "length_miles": 8.0,
                    "elevation_gain_feet": 1000,
                    "description": "Popular moderate trail to Seven Falls with multiple creek crossings, scenic canyon views, and seasonal water flow. Very popular - arrive early.",
                    "highlights": ["Seven waterfalls", "Creek crossings", "Scenic canyon", "Popular", "Seasonal water"],
                    "best_seasons": "Spring (water flow), Fall, Winter",
                    "trailhead": "Bear Canyon Trailhead (Sabino Canyon area)",
                    "features": ["Waterfalls", "Creek crossings", "Canyon views", "Scenic"],
                    "permits": "Coronado National Forest - no permit required",
                    "warnings": ["Very popular - arrive early", "Seasonal water flow", "Extreme heat in summer"],
                },
                {
                    "name": "Romero Pools",
                    "difficulty": "Moderate",
                    "length_miles": 5.5,
                    "elevation_gain_feet": 1200,
                    "description": "Moderate trail to Romero Pools with scenic canyon views, seasonal pools, and moderate elevation gain. Popular day hike.",
                    "highlights": ["Swimming pools", "Scenic canyon", "Moderate difficulty", "Popular", "Seasonal pools"],
                    "best_seasons": "Spring (water flow), Fall, Winter",
                    "trailhead": "Romero Canyon Trailhead",
                    "features": ["Swimming pools", "Canyon views", "Moderate", "Scenic"],
                    "permits": "Coronado National Forest - no permit required",
                    "warnings": ["Seasonal pools", "Extreme heat in summer"],
                },
            ],
            "trail_networks": "Extensive trail networks in desert preserves, Saguaro National Park, and mountain terrain",
            "difficulty_range": "Easy to strenuous",
            "best_seasons": "Fall (October-November), Winter (December-February), Spring (March-April) - Mount Lemmon in summer",
            "trail_features": ["Desert scenery", "Saguaro cacti", "Mountain terrain", "Sky island", "Water features"],
        },
        "climbing": {
            "description": "Limited climbing opportunities in Tucson area, primarily bouldering and some sport climbing",
            "areas": [
                {
                    "name": "Tucson Area Bouldering",
                    "type": "Bouldering",
                    "routes": "Various",
                    "difficulty_range": "V0-V8",
                    "description": "Limited bouldering opportunities in Tucson area. Mostly exploratory.",
                    "access": "Various locations, check local guidebooks",
                    "best_seasons": "Fall, Winter, Spring (avoid summer heat)",
                },
            ],
            "note": "Tucson is not a major climbing destination. For extensive climbing, consider nearby areas or use tools to find current climbing opportunities.",
        },
        "cycling": {
            "description": "Road and gravel cycling opportunities with scenic routes through desert and mountain terrain",
            "routes": [
                {
                    "name": "Catalina Highway to Mount Lemmon",
                    "type": "Road",
                    "length_miles": 28.0,
                    "elevation_gain_feet": 6000,
                    "description": "Challenging road route up Catalina Highway to Mount Lemmon summit with significant elevation gain (6,000 ft) and spectacular mountain views. One of the most challenging road climbs in Arizona.",
                    "highlights": ["Challenging climb", "Mountain views", "Significant elevation", "Iconic route", "Scenic"],
                    "best_seasons": "Spring, Summer, Fall",
                    "difficulty": "Very Challenging",
                },
                {
                    "name": "Gates Pass Road",
                    "type": "Road",
                    "length_miles": 8.0,
                    "elevation_gain_feet": 800,
                    "description": "Scenic road route through Gates Pass with moderate elevation and spectacular desert sunset views. Popular cycling route.",
                    "highlights": ["Desert views", "Sunset views", "Moderate difficulty", "Scenic", "Popular"],
                    "best_seasons": "Fall, Winter, Spring",
                    "difficulty": "Moderate",
                },
            ],
            "best_seasons": "Fall, Winter, Spring (Mount Lemmon route in summer for cooler temps)",
            "trail_features": ["Road routes", "Desert scenery", "Mountain routes", "Varied difficulty"],
        },
        "paddling": {
            "description": "Limited paddling opportunities in Tucson area. Mostly nearby lakes and reservoirs.",
            "routes": [
                {
                    "name": "Patagonia Lake",
                    "type": "Flatwater",
                    "length_miles": "Varies",
                    "difficulty": "Class I",
                    "description": "Flatwater paddling on Patagonia Lake. Popular for kayaking and canoeing.",
                    "put_in": "Patagonia Lake access points",
                    "take_out": "Same as put-in",
                    "best_seasons": "Year-round (best Fall, Winter, Spring)",
                    "distance": "60 miles from Tucson",
                },
            ],
            "note": "Tucson is not a major paddling destination. For extensive paddling, consider nearby lakes or use tools to find current opportunities.",
            "best_seasons": "Year-round (best Fall, Winter, Spring)",
        },
        "trail_running": {
            "description": "Extensive trail network for running",
            "famous_trails": [
                "Saguaro National Park trails",
                "Tucson Mountain Park",
                "Sweetwater Preserve",
            ],
        },
        "sky_island": {
            "description": "Mount Lemmon - escape summer heat",
            "elevation": "9,157 feet",
            "activities": ["Hiking", "Mountain biking", "Camping", "Cooler temperatures"],
            "access": "Catalina Highway (scenic drive)",
        },
        "photography": {
            "description": "Saguaro cacti, desert landscapes, mountain views, sunsets",
            "best_spots": [
                "Saguaro National Park (sunrise/sunset)",
                "Mount Lemmon (mountain views)",
                "Gates Pass (sunset)",
                "Tucson Mountain Park",
            ],
        },
    },
    "attractions": {
        "natural": [
            "Saguaro National Park (East and West units)",
            "Mount Lemmon (Santa Catalina Mountains)",
            "Tucson Mountain Park",
            "Catalina State Park",
            "Sabino Canyon",
            "Arizona-Sonora Desert Museum",
        ],
        "cultural": [
            "Mission San Xavier del Bac",
            "Pima Air & Space Museum",
            "University of Arizona",
            "Historic downtown Tucson",
            "Old Tucson Studios",
        ],
        "nearby": [
            "Mount Lemmon (30 miles)",
            "Bisbee (95 miles)",
            "Mexico border (65 miles to Nogales)",
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "El Charro Cafe",
                "type": "Mexican",
                "description": "Oldest Mexican restaurant in US (founded 1922)",
            },
            {
                "name": "Cafe Poca Cosa",
                "type": "Mexican",
                "description": "Award-winning Mexican cuisine",
            },
            {
                "name": "The Parish",
                "type": "Southern",
                "description": "Southern comfort food",
            },
        ],
        "bike_shops": [
            {
                "name": "Fair Wheel Bikes",
                "type": "Bike Shop",
                "description": "Full-service bike shop",
            },
            {
                "name": "Tucson Mountain Biking",
                "type": "Bike Shop",
                "description": "Mountain bike specialty shop",
            },
        ],
        "accommodations": [
            {
                "name": "Arizona Inn",
                "type": "Historic Hotel",
                "description": "Historic boutique hotel",
            },
        ],
    },
    "practical_info": {
        "parking": "Available at trailheads (arrive early for popular trails)",
        "permits": "Saguaro National Park requires entrance fee ($25/vehicle or America the Beautiful Pass)",
        "best_times": "October - April (avoid summer midday heat)",
        "weather": {
            "summer": "Hot (95-105°F), but cooler than Phoenix. Mount Lemmon much cooler (70-80°F)",
            "winter": "Mild (60-75°F), ideal for outdoor activities",
            "spring": "Warm (70-85°F), perfect weather",
            "fall": "Warm (75-90°F), great for activities",
        },
        "access": "Easy access via I-10, I-19",
        "airport": "Tucson International Airport",
        "considerations": [
            "Hot in summer - start early (5-6 AM) or late evening",
            "Mount Lemmon provides cool escape in summer (9,157 ft elevation)",
            "Carry plenty of water (minimum 1 liter per hour)",
            "Watch for rattlesnakes, especially in spring/fall",
            "Saguaro National Park has East and West units (separate entrances)",
            "Popular trails get crowded on weekends",
        ],
    },
}


class TucsonAgent(LocationAgentBase):
    """Agent specialized in Tucson, Arizona information and context.

    This agent enhances existing agent outputs with Tucson-specific knowledge
    about Sonoran Desert, Saguaro National Park, and outdoor opportunities.
    """

    LOCATION_NAME = "Tucson, Arizona"
    LOCATION_INDICATORS = [
        "tucson",
        "tucson, az",
        "tucson, arizona",
        "tucson az",
        "old pueblo",
    ]
    AGENT_NAME = "tucson_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Tucson-specific knowledge base (fallback if external file not found)."""
        return TUCSON_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Tucson agent."""
        return """You are a comprehensive guide for Tucson, Arizona - the "Old Pueblo"
located in the Sonoran Desert at 2,400 feet elevation.

Your role is to:
1. Use tools to gather real-time data about Tucson (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Tucson-specific knowledge from the knowledge base
4. Combine information from existing agents with Tucson expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Tucson, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Tucson, Arizona")
- For climbing: search_trails(activity_type="climbing", location="Tucson, Arizona") if available
- For cycling: search_trails(activity_type="cycling", location="Tucson, Arizona")
- For paddling: search_trails(activity_type="paddling", location="Tucson, Arizona") if available
- For trail running: search_trails(activity_type="trail_running", location="Tucson, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Saguaro National Park requires entrance fee)
- Include trail connectivity and route planning details
- Highlight Mount Lemmon as summer escape option

COMBINE multiple sources:
- Tool data (current conditions, real-time info from search_trails)
- Knowledge base (detailed trail descriptions, historical info)
- Existing agent outputs (trail_info from trail_agent if available)

PROVIDE comprehensive trail information:
- Trail names, difficulty ratings, length, elevation gain
- Detailed trail descriptions and highlights
- Best seasons and current conditions
- Trailhead locations and access
- Permits and regulations (Saguaro National Park: $25/vehicle or America the Beautiful Pass)
- Safety considerations (extreme heat, water, rattlesnakes, Mount Lemmon escape)
- Trail connectivity and route planning
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Tucson, Arizona"
- Tucson has extensive MTB trails including 50 Year Trail (8 miles, intermediate/advanced), Sweetwater Preserve (10+ miles, all levels), Starr Pass (15+ miles, intermediate/advanced), Fantasy Island (8+ miles, beginner/intermediate), and Mount Lemmon trails (summer escape)
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, and features
- Mention Mount Lemmon as summer escape option when desert is too hot

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Tucson, Arizona"
- Popular trails include Mount Lemmon trails (multiple trails, sky island, cool in summer), Saguaro National Park trails (East and West units, iconic saguaro cacti), Wasson Peak (7 miles, moderate/strenuous), Seven Falls (8 miles, moderate), and Romero Pools (5.5 miles, moderate)
- Use find_scenic_viewpoints for desert views and saguaro cacti
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- CRITICAL: Mention Mount Lemmon as summer escape (70-80°F vs 100°F in Tucson)
- CRITICAL: Mention extreme heat in summer - hike early morning (5-6 AM) or evening

For Dining Queries:
- Use find_restaurants with location="Tucson, Arizona"
- Enhance results with knowledge base businesses (El Charro Cafe - oldest Mexican restaurant in US, Cafe Poca Cosa, The Parish)
- Provide context about local favorites

For Accommodation Queries:
- Use search_accommodations with location="Tucson, Arizona"
- Enhance with knowledge base information (Arizona Inn)
- Mention proximity to trails and attractions

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Saguaro National Park (sunrise/sunset, iconic saguaro cacti), Mount Lemmon (mountain views), Gates Pass (sunset), Tucson Mountain Park
- Mention seasonal opportunities and best times

For Logistics Queries:
- Use get_parking_information for trailhead parking
- Provide information about permits (Saguaro National Park: $25/vehicle or America the Beautiful Pass, most other trails require no permits)
- Mention I-10 and I-19 access
- Tucson International Airport for air access

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

Tucson's Highlights:
- Old Pueblo - historic desert city
- Saguaro National Park (East and West units)
- Mount Lemmon (9,157 ft - sky island, cool escape in summer)
- Sonoran Desert trails
- University of Arizona
- Cooler than Phoenix (2,400 ft elevation)
- ~550,000 residents (metro: ~1 million)

Key Attractions:
- Saguaro National Park (East and West units)
- Mount Lemmon (Santa Catalina Mountains - 9,157 ft)
- Tucson Mountain Park
- Catalina State Park
- Sabino Canyon
- Arizona-Sonora Desert Museum
- Mission San Xavier del Bac

FAMOUS TRAILS:
- Hiking: Mount Lemmon trails (multiple trails, sky island, 9,157 ft, cool in summer), Saguaro National Park trails (East and West units, iconic saguaro cacti), Wasson Peak (7 miles, moderate/strenuous), Seven Falls (8 miles, moderate, waterfalls), Romero Pools (5.5 miles, moderate, swimming pools)
- Mountain Biking: 50 Year Trail (8 miles, intermediate/advanced), Sweetwater Preserve (10+ miles, all levels), Starr Pass (15+ miles, intermediate/advanced), Fantasy Island (8+ miles, beginner/intermediate), Mount Lemmon trails (summer escape)
- Trail Running: Saguaro National Park, Tucson Mountain Park, Sweetwater Preserve

SKY ISLAND FEATURE - Mount Lemmon:
- Elevation: 9,157 feet - 30 miles from Tucson via scenic Catalina Highway
- Much cooler in summer (70-80°F vs 100°F in Tucson)
- Great escape from summer heat
- Multiple trails for hiking and mountain biking
- Accessible year-round (check conditions in winter)

CRITICAL Safety Information:
- Hot in summer (95-105°F) - hike/ride early morning (5-6 AM) or evening
- Mount Lemmon provides cool escape in summer (70-80°F vs 100°F in Tucson)
- Carry plenty of water (minimum 1 liter per hour)
- Watch for rattlesnakes, especially in spring/fall
- Saguaro National Park requires entrance fee ($25/vehicle or America the Beautiful Pass)
- Popular trails get crowded on weekends
- Saguaro National Park has East and West units (separate entrances)

Practical Information:
- Best times: October - April (avoid summer midday heat)
- Winter: Mild (60-75°F) - ideal for outdoor activities
- Spring: Warm (70-85°F) - perfect weather
- Fall: Warm (75-90°F) - great for activities
- Summer: Hot (95-105°F) but Mount Lemmon much cooler (70-80°F) - use Mount Lemmon for summer activities
- Easy access via I-10 and I-19
- Tucson International Airport for air access

ENHANCEMENT GUIDELINES:
- Always combine tool results with knowledge base information
- Provide specific recommendations based on activity type and season
- Include critical safety considerations (extreme heat, water, rattlesnakes, Mount Lemmon escape)
- Emphasize Mount Lemmon as summer escape option
- Mention Saguaro National Park entrance fee and separate East/West units
- Highlight unique characteristics (sky island, saguaro cacti, desert scenery)
- Provide practical tips (parking, permits, best times, access, Mount Lemmon escape)

Provide comprehensive, accurate, practical information that combines real tool data with Tucson-specific knowledge and context."""

