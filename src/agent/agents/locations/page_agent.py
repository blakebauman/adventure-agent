"""Page, Arizona specialist agent.

This agent provides Page-specific information and enhances existing agent outputs
with local knowledge about Lake Powell, Antelope Canyon, Horseshoe Bend, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Page-specific knowledge base - Enhanced with detailed information
PAGE_KNOWLEDGE = {
    "location": {
        "name": "Page, Arizona",
        "coordinates": {"lat": 36.9147, "lon": -111.4558},
        "elevation": 4300,  # feet
        "region": "Coconino County, Arizona",
        "country": "US",
        "nickname": "Gateway to Lake Powell",
        "proximity": {
            "grand_canyon": {"distance_miles": 130, "direction": "southwest", "drive_time_minutes": 150},
            "flagstaff": {"distance_miles": 130, "direction": "south", "drive_time_minutes": 150},
            "kanab": {"distance_miles": 80, "direction": "north", "drive_time_minutes": 90},
            "monument_valley": {"distance_miles": 120, "direction": "east", "drive_time_minutes": 140},
        },
    },
    "history": {
        "founded": 1957,
        "incorporated": 1975,
        "current_population": "~7,500 residents",
        "known_for": [
            "Lake Powell gateway",
            "Antelope Canyon (Upper and Lower)",
            "Horseshoe Bend",
            "Glen Canyon National Recreation Area",
            "Water recreation",
            "Slot canyons",
            "Photography destination",
        ],
        "historical_significance": "Founded as housing community for Glen Canyon Dam construction workers, evolved into major tourism destination and gateway to Lake Powell",
        "dam_construction": {
            "start": 1956,
            "completion": 1966,
            "significance": "Glen Canyon Dam created Lake Powell, one of the largest man-made reservoirs in the US",
        },
    },
    "geography": {
        "terrain": "Desert, canyons, lake",
        "topography": "Colorado Plateau, Glen Canyon, Lake Powell",
        "elevation": "4,300 feet",
        "climate": "Desert climate, four distinct seasons, hot summers, mild winters",
        "features": [
            "Lake Powell (186 miles long, 1,900 miles of shoreline)",
            "Glen Canyon National Recreation Area",
            "Antelope Canyon (Upper and Lower slot canyons)",
            "Horseshoe Bend (Colorado River)",
            "Glen Canyon Dam",
        ],
        "ecosystem": "Desert with riparian areas along Colorado River and Lake Powell",
    },
    "outdoor_activities": {
        "water_activities": {
            "description": "Extensive water recreation on Lake Powell including boating, kayaking, fishing, and swimming",
            "activities": [
                {
                    "name": "Boating",
                    "description": "Lake Powell offers extensive boating opportunities with 1,900 miles of shoreline",
                    "seasons": "Year-round, best in Spring, Summer, Fall",
                    "access": "Multiple marinas and boat ramps on Lake Powell",
                    "highlights": ["Extensive shoreline", "Multiple marinas", "Year-round", "Scenic canyons"],
                },
                {
                    "name": "Kayaking",
                    "description": "Kayaking on Lake Powell and through slot canyons",
                    "seasons": "Year-round, best in Spring, Summer, Fall",
                    "access": "Multiple access points",
                    "highlights": ["Slot canyons", "Scenic", "Multiple access points"],
                },
                {
                    "name": "Fishing",
                    "description": "Excellent fishing in Lake Powell for bass, trout, and walleye",
                    "seasons": "Year-round, best in Spring and Fall",
                    "permits": "Arizona fishing license required",
                    "highlights": ["Bass", "Trout", "Walleye", "Year-round"],
                },
                {
                    "name": "Swimming",
                    "description": "Swimming in Lake Powell",
                    "seasons": "Spring, Summer, Fall",
                    "access": "Multiple beaches and access points",
                    "highlights": ["Multiple beaches", "Scenic", "Cool in summer"],
                },
            ],
            "best_seasons": "Year-round, best in Spring, Summer, Fall",
            "permits": "Glen Canyon National Recreation Area entrance fee required. Fishing requires Arizona fishing license",
        },
        "hiking": {
            "description": "Hiking to Horseshoe Bend and in Glen Canyon National Recreation Area with scenic desert and canyon trails",
            "famous_trails": [
                {
                    "name": "Horseshoe Bend Trail",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "1.5 round trip",
                    "elevation_gain_feet": 200,
                    "description": "Popular trail to Horseshoe Bend overlook with scenic views of Colorado River. Very popular - arrive early. Paved trail with some elevation gain.",
                    "highlights": [
                        "Iconic overlook",
                        "Scenic Colorado River views",
                        "Popular",
                        "Easy to moderate",
                        "Paved trail",
                    ],
                    "best_seasons": "Year-round (best Fall, Winter, Spring - avoid summer heat)",
                    "trailhead": "Horseshoe Bend Trailhead (5 miles south of Page)",
                    "features": ["Iconic", "Scenic", "Easy to moderate", "Paved"],
                    "permits": "Glen Canyon National Recreation Area - entrance fee required",
                    "warnings": ["Very popular - arrive early", "Extreme heat in summer - hike early morning or evening"],
                },
                {
                    "name": "Glen Canyon National Recreation Area Trails",
                    "difficulty": "Easy to Moderate",
                    "length_miles": "Varies",
                    "elevation_gain_feet": "Varies",
                    "description": "Trail network in Glen Canyon National Recreation Area with scenic desert and canyon views.",
                    "highlights": ["Desert views", "Canyon views", "Scenic", "Varied difficulty"],
                    "best_seasons": "Year-round (best Fall, Winter, Spring)",
                    "trailhead": "Various access points",
                    "features": ["Desert trails", "Canyon views", "Scenic"],
                    "permits": "Glen Canyon National Recreation Area - entrance fee required",
                },
            ],
            "difficulty_range": "Easy to moderate",
            "best_seasons": "Year-round (best Fall, Winter, Spring - avoid summer heat)",
            "trail_features": ["Desert trails", "Canyon views", "Iconic overlooks"],
        },
        "slot_canyons": {
            "description": "World-famous slot canyons including Antelope Canyon (Upper and Lower) with guided tours required",
            "canyons": [
                {
                    "name": "Upper Antelope Canyon",
                    "type": "Slot Canyon",
                    "description": "Most famous slot canyon with light beams, requires guided tour",
                    "highlights": ["Light beams", "Most famous", "Guided tour required", "Photography"],
                    "best_seasons": "Year-round, best for light beams in Spring and Fall",
                    "access": "Guided tour required - book in advance",
                    "permits": "Guided tour fee required",
                },
                {
                    "name": "Lower Antelope Canyon",
                    "type": "Slot Canyon",
                    "description": "Less crowded slot canyon, requires guided tour",
                    "highlights": ["Less crowded", "Guided tour required", "Photography", "Scenic"],
                    "best_seasons": "Year-round",
                    "access": "Guided tour required - book in advance",
                    "permits": "Guided tour fee required",
                },
            ],
            "best_seasons": "Year-round, best for light beams in Spring and Fall",
            "permits": "Guided tours required for all slot canyons - book well in advance",
        },
        "photography": {
            "description": "World-class photography opportunities including slot canyons, Horseshoe Bend, Lake Powell, and desert landscapes",
            "best_spots": [
                {
                    "name": "Antelope Canyon (Upper and Lower)",
                    "best_time": "Midday for light beams (Spring and Fall), guided tour required",
                    "subjects": "Slot canyon light beams, sandstone formations, iconic photography",
                },
                {
                    "name": "Horseshoe Bend",
                    "best_time": "Sunrise and sunset for dramatic lighting, golden hour",
                    "subjects": "Iconic Colorado River bend, dramatic canyon views, scenic overlook",
                },
                {
                    "name": "Lake Powell",
                    "best_time": "Sunrise and sunset for scenic lake shots, golden hour",
                    "subjects": "Lake scenery, canyons, water activities, scenic views",
                },
                {
                    "name": "Glen Canyon Dam",
                    "best_time": "Daylight hours",
                    "subjects": "Dam structure, Lake Powell, engineering marvel",
                },
            ],
            "seasons": "All seasons offer unique opportunities - spring/fall light beams in slot canyons, winter clarity, summer water activities",
        },
    },
    "attractions": {
        "natural": [
            {
                "name": "Lake Powell",
                "type": "Reservoir",
                "description": "186 miles long, 1,900 miles of shoreline, one of the largest man-made reservoirs in the US",
                "activities": ["Boating", "Kayaking", "Fishing", "Swimming", "Photography"],
            },
            {
                "name": "Antelope Canyon (Upper and Lower)",
                "type": "Slot Canyon",
                "description": "World-famous slot canyons with light beams, guided tours required",
                "activities": ["Photography", "Guided tours", "Slot canyon exploration"],
            },
            {
                "name": "Horseshoe Bend",
                "type": "Scenic Overlook",
                "description": "Iconic Colorado River bend with dramatic canyon views",
                "activities": ["Hiking", "Photography", "Scenic views"],
            },
            {
                "name": "Glen Canyon National Recreation Area",
                "type": "National Recreation Area",
                "description": "1.25 million acres with Lake Powell, canyons, and recreation",
                "activities": ["All outdoor activities"],
            },
        ],
        "cultural": [
            {
                "name": "Glen Canyon Dam",
                "type": "Historic Site",
                "description": "Historic dam that created Lake Powell, visitor center and tours",
            },
            {
                "name": "Page-Lake Powell Chamber of Commerce",
                "type": "Visitor Center",
                "description": "Visitor information and resources",
            },
        ],
        "nearby": [
            {
                "name": "Grand Canyon National Park",
                "distance": "130 miles",
                "description": "One of the Seven Natural Wonders, North and South Rim",
            },
            {
                "name": "Monument Valley",
                "distance": "120 miles",
                "description": "Iconic desert landscape, Navajo Tribal Park",
            },
            {
                "name": "Kanab",
                "distance": "80 miles",
                "description": "Gateway to Zion National Park and other Utah parks",
            },
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Various local restaurants",
                "type": "Mixed",
                "description": "Page offers several local dining options - use tools to find current restaurants",
                "note": "Use find_restaurants tool for current dining options",
            },
        ],
        "accommodations": [
            {
                "name": "Lake Powell Resort",
                "type": "Resort",
                "description": "Full-service resort on Lake Powell",
                "highlights": ["Full-service", "Lake Powell location", "Resort"],
            },
            {
                "name": "Various accommodations",
                "type": "Mixed",
                "description": "Multiple lodging options including hotels and campgrounds - use tools to find current options",
                "note": "Use search_accommodations tool for current lodging options",
            },
        ],
    },
    "practical_info": {
        "parking": "Available in town and at attractions. Horseshoe Bend parking can fill up - arrive early. Antelope Canyon tours have designated parking",
        "permits": "Glen Canyon National Recreation Area - entrance fee required ($30/vehicle or America the Beautiful Pass). Antelope Canyon requires guided tour (book well in advance). Fishing requires Arizona fishing license",
        "best_times": "Year-round - four distinct seasons. Spring (March-May) and Fall (September-November) are ideal. Summer is hot but great for water activities",
        "weather": {
            "summer": "Hot (85-100°F), excellent for water activities, avoid midday heat for hiking",
            "winter": "Mild (40-60°F), excellent for hiking and outdoor activities",
            "spring": "Pleasant (60-80°F), ideal for all activities",
            "fall": "Pleasant (60-80°F), ideal for all activities",
        },
        "access": "Highway 89 from Flagstaff (130 miles, 150 minutes) or Kanab, Utah (80 miles, 90 minutes)",
        "considerations": [
            "Glen Canyon National Recreation Area entrance fee required ($30/vehicle or America the Beautiful Pass)",
            "Antelope Canyon requires guided tours - book well in advance (especially Upper Antelope Canyon)",
            "Horseshoe Bend is very popular - arrive early for parking",
            "Extreme heat in summer - plan hiking for early morning or evening",
            "Lake Powell water levels vary - check current conditions",
            "Gateway to Grand Canyon (130 miles), Monument Valley (120 miles), and Kanab (80 miles)",
            "Photography permits may be required for commercial photography",
        ],
    },
}


class PageAgent(LocationAgentBase):
    """Agent specialized in Page, Arizona information and context.

    This agent enhances existing agent outputs with Page-specific knowledge
    about Lake Powell, Antelope Canyon, Horseshoe Bend, and outdoor opportunities.
    """

    LOCATION_NAME = "Page, Arizona"
    LOCATION_INDICATORS = [
        "page",
        "page, az",
        "page, arizona",
        "page az",
        "lake powell",
        "antelope canyon",
        "horseshoe bend",
    ]
    AGENT_NAME = "page_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Page-specific knowledge base (fallback if external file not found)."""
        return PAGE_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Page agent."""
        return """You are a comprehensive guide for Page, Arizona - the "Gateway to Lake Powell"
located at 4,300 feet elevation, known for Lake Powell, Antelope Canyon, Horseshoe Bend, and world-class water recreation.

Your role is to:
1. Use tools to gather real-time data about Page (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Page-specific knowledge from the knowledge base
4. Combine information from existing agents with Page expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Page, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Page, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Glen Canyon National Recreation Area - entrance fee required)
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

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Page, Arizona"
- Popular trails include Horseshoe Bend Trail (1.5 miles round trip, easy/moderate, iconic overlook) and Glen Canyon National Recreation Area trails
- Enhance with knowledge base information about trail difficulty, length, elevation, and highlights
- CRITICAL: Mention that Horseshoe Bend is very popular - arrive early for parking
- CRITICAL: Mention extreme heat in summer - hike early morning or evening

For Water Activities Queries:
- Page is gateway to Lake Powell (186 miles long, 1,900 miles of shoreline)
- Activities: Boating, kayaking, fishing (bass, trout, walleye), swimming
- Use find_water_sources for Lake Powell access points
- Mention multiple marinas and boat ramps
- Provide information about Glen Canyon National Recreation Area entrance fee
- Best seasons: Year-round, best in Spring, Summer, Fall

For Slot Canyon Queries:
- Antelope Canyon (Upper and Lower) - world-famous slot canyons
- CRITICAL: Guided tours required for all slot canyons - book well in advance
- Upper Antelope Canyon: Most famous, light beams (best in Spring and Fall)
- Lower Antelope Canyon: Less crowded, also requires guided tour
- Mention photography opportunities and light beams

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Antelope Canyon (midday for light beams, Spring/Fall), Horseshoe Bend (sunrise/sunset, golden hour), Lake Powell (sunrise/sunset, golden hour), Glen Canyon Dam (daylight)
- Mention that Antelope Canyon requires guided tours - book well in advance
- Mention photography permits may be required for commercial photography

For Dining Queries:
- Use find_restaurants with location="Page, Arizona"
- Provide context about tourism destination

For Accommodation Queries:
- Use search_accommodations with location="Page, Arizona"
- Enhance with knowledge base information (Lake Powell Resort)
- Mention proximity to Lake Powell and attractions

For Logistics Queries:
- Use get_parking_information (Horseshoe Bend parking can fill up - arrive early)
- Provide information about permits (Glen Canyon National Recreation Area - entrance fee $30/vehicle or America the Beautiful Pass, Antelope Canyon requires guided tour, fishing license required)
- Mention Highway 89 access from Flagstaff (130 miles) and Kanab, Utah (80 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

OUTPUT FORMAT:
Provide your response as structured JSON with the following format:
{
  "location": "Page, Arizona",
  "overview": "Brief overview of Page as gateway to Lake Powell",
  "key_attractions": ["List of key attractions"],
  "outdoor_activities": {
    "hiking": {"trails": [...], "difficulty": "...", "best_seasons": "..."},
    "water_activities": {"activities": [...], "seasons": "..."},
    "slot_canyons": {"canyons": [...], "seasons": "..."},
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

PAGE'S UNIQUE CHARACTERISTICS:
- Gateway to Lake Powell (186 miles long, 1,900 miles of shoreline)
- World-famous Antelope Canyon (Upper and Lower slot canyons)
- Iconic Horseshoe Bend (Colorado River)
- Glen Canyon National Recreation Area (1.25 million acres)
- Glen Canyon Dam (created Lake Powell)
- Elevation: 4,300 feet
- ~7,500 residents
- Gateway to Grand Canyon (130 miles), Monument Valley (120 miles), and Kanab, Utah (80 miles)

KEY ATTRACTIONS:
- Lake Powell: 186 miles long, 1,900 miles of shoreline, one of the largest man-made reservoirs in the US
- Antelope Canyon (Upper and Lower): World-famous slot canyons with light beams, guided tours required
- Horseshoe Bend: Iconic Colorado River bend with dramatic canyon views, 1.5-mile round trip hike
- Glen Canyon National Recreation Area: 1.25 million acres with Lake Powell, canyons, and recreation
- Glen Canyon Dam: Historic dam that created Lake Powell, visitor center and tours

FAMOUS ACTIVITIES:
- Water recreation (boating, kayaking, fishing, swimming) on Lake Powell - year-round, best in Spring, Summer, Fall
- Slot canyon tours (Antelope Canyon Upper and Lower) - guided tours required, book well in advance
- Hiking (Horseshoe Bend Trail, Glen Canyon National Recreation Area trails)
- Photography (Antelope Canyon light beams, Horseshoe Bend, Lake Powell, Glen Canyon Dam)

PRACTICAL INFORMATION:
- Parking: Available in town and at attractions. Horseshoe Bend parking can fill up - arrive early. Antelope Canyon tours have designated parking
- Permits: Glen Canyon National Recreation Area - entrance fee required ($30/vehicle or America the Beautiful Pass). Antelope Canyon requires guided tour (book well in advance). Fishing requires Arizona fishing license
- Best Times: Year-round - four distinct seasons. Spring (March-May) and Fall (September-November) are ideal. Summer is hot but great for water activities
- Weather: Four distinct seasons. Summer: 85-100°F (excellent for water activities, avoid midday heat for hiking). Winter: 40-60°F (excellent for hiking and outdoor). Spring/Fall: 60-80°F (ideal)
- Access: Highway 89 from Flagstaff (130 miles, 150 minutes) or Kanab, Utah (80 miles, 90 minutes)
- Considerations: Glen Canyon National Recreation Area entrance fee required ($30/vehicle or America the Beautiful Pass). Antelope Canyon requires guided tours - book well in advance (especially Upper Antelope Canyon). Horseshoe Bend is very popular - arrive early for parking. Extreme heat in summer - plan hiking for early morning or evening. Lake Powell water levels vary - check current conditions. Gateway to Grand Canyon (130 miles), Monument Valley (120 miles), and Kanab (80 miles). Photography permits may be required for commercial photography

ENHANCEMENT GUIDELINES:
- Always enhance tool results with knowledge base information
- Provide context about Page's gateway location to Lake Powell and Glen Canyon National Recreation Area
- Mention Antelope Canyon as world-famous slot canyon destination with guided tour requirements
- Highlight Horseshoe Bend as iconic photography destination
- Emphasize water recreation opportunities on Lake Powell
- Provide practical tips about parking, permits, best times, access, and tour bookings

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Page-specific knowledge and context
- Enhanced recommendations based on Page's unique Lake Powell gateway and slot canyon character
- Practical tips for visitors"""

