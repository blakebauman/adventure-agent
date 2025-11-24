"""Grand Canyon (North and South Rim) specialist agent.

This agent provides Grand Canyon-specific information for both North and South Rims,
enhancing existing agent outputs with local knowledge about hiking, viewpoints, and outdoor opportunities.
"""

from __future__ import annotations

from typing import Any, Dict

from agent.agents.location_agent_base import LocationAgentBase

# Grand Canyon-specific knowledge base
GRAND_CANYON_KNOWLEDGE = {
    "location": {
        "name": "Grand Canyon National Park, Arizona",
        "coordinates": {
            "south_rim": {"lat": 36.0544, "lon": -112.1401},
            "north_rim": {"lat": 36.1970, "lon": -112.0517},
        },
        "elevation": {
            "south_rim": 7000,  # feet
            "north_rim": 8000,  # feet
            "river": 2400,  # feet
        },
        "region": "Coconino County, Arizona",
        "country": "US",
        "proximity": {
            "flagstaff": {"distance_miles": 80, "direction": "south"},
            "williams": {"distance_miles": 60, "direction": "south"},
            "page": {"distance_miles": 130, "direction": "northeast"},
        },
    },
    "history": {
        "established": 1919,
        "designation": "National Park",
        "unesco": "World Heritage Site (1979)",
        "size": "1,218,375 acres",
        "depth": "Over 1 mile deep",
        "length": "277 miles long",
        "width": "Up to 18 miles wide",
        "known_for": [
            "One of the Seven Natural Wonders of the World",
            "Iconic American landscape",
            "Geological history spanning 2 billion years",
            "Native American heritage",
        ],
    },
    "geography": {
        "rims": {
            "south_rim": {
                "elevation": "7,000 feet",
                "access": "Open year-round",
                "services": "Full services, lodging, restaurants",
                "viewpoints": "Multiple viewpoints along Desert View Drive",
            },
            "north_rim": {
                "elevation": "8,000 feet",
                "access": "Seasonal (May-October, weather dependent)",
                "services": "Limited services, lodge",
                "viewpoints": "More remote, fewer visitors",
            },
        },
        "river": {
            "name": "Colorado River",
            "elevation": "2,400 feet",
            "rafting": "World-class whitewater rafting",
        },
    },
    "outdoor_activities": {
        "hiking": {
            "description": "Iconic rim-to-river and rim-to-rim hikes with spectacular canyon views and challenging terrain",
            "famous_trails": [
                {
                    "name": "Bright Angel Trail (South Rim)",
                    "difficulty": "Moderate to Strenuous",
                    "length_miles": "Varies (1.5 miles to Indian Garden, 4.5 miles to Plateau Point, 9.5 miles to River)",
                    "elevation_gain_feet": "Varies (1,120 ft to Indian Garden, 3,060 ft to River)",
                    "description": "Most popular trail on South Rim with water stations, rest houses, and switchbacks. Well-maintained trail with multiple turnaround points. Most popular day hike destination.",
                    "highlights": [
                        "Most popular trail",
                        "Water stations available",
                        "Rest houses",
                        "Multiple turnaround points",
                        "Well-maintained",
                        "Iconic"
                    ],
                    "best_seasons": "Spring (March-May), Fall (September-November) - avoid summer heat",
                    "trailhead": "Bright Angel Trailhead (South Rim, near Grand Canyon Village)",
                    "features": ["Water stations", "Rest houses", "Switchbacks", "Well-maintained", "Popular"],
                    "permits": "Grand Canyon National Park - no permit required for day hikes",
                    "warnings": [
                        "Going down is optional, coming up is mandatory",
                        "Hike down only 1/3 of what you can hike up",
                        "Start early (5-6 AM), avoid midday heat",
                        "Carry plenty of water (minimum 1 liter per hour)",
                        "Very crowded in summer"
                    ],
                },
                {
                    "name": "South Kaibab Trail (South Rim)",
                    "difficulty": "Strenuous",
                    "length_miles": "Varies (1.5 miles to Cedar Ridge, 3 miles to Skeleton Point, 6.8 miles to River)",
                    "elevation_gain_feet": "Varies (1,120 ft to Cedar Ridge, 2,040 ft to Skeleton Point, 4,780 ft to River)",
                    "description": "Steeper, more direct trail than Bright Angel with no water stations. Spectacular views but more challenging. No water available - must carry all water.",
                    "highlights": [
                        "Spectacular views",
                        "More direct route",
                        "Less crowded than Bright Angel",
                        "Steeper",
                        "No water stations"
                    ],
                    "best_seasons": "Spring, Fall - avoid summer heat",
                    "trailhead": "South Kaibab Trailhead (South Rim, accessible by shuttle)",
                    "features": ["Steep", "Direct route", "No water", "Scenic views"],
                    "permits": "Grand Canyon National Park - no permit required for day hikes",
                    "warnings": [
                        "NO WATER STATIONS - must carry all water",
                        "Steeper than Bright Angel",
                        "Start early (5-6 AM), avoid midday heat",
                        "Carry plenty of water (minimum 1 liter per hour)",
                        "Going down is optional, coming up is mandatory"
                    ],
                },
                {
                    "name": "North Kaibab Trail (North Rim)",
                    "difficulty": "Strenuous",
                    "length_miles": "Varies (1.5 miles to Coconino Overlook, 4.7 miles to Roaring Springs, 14.2 miles to River)",
                    "elevation_gain_feet": "Varies (significant elevation change)",
                    "description": "Main trail on North Rim with water at Roaring Springs. Less crowded than South Rim trails. Accessible only when North Rim is open (May-October).",
                    "highlights": [
                        "Less crowded",
                        "Water at Roaring Springs",
                        "North Rim access",
                        "Scenic views",
                        "Seasonal access"
                    ],
                    "best_seasons": "May-October (when North Rim is open)",
                    "trailhead": "North Kaibab Trailhead (North Rim)",
                    "features": ["Less crowded", "Water available", "Seasonal", "Scenic"],
                    "permits": "Grand Canyon National Park - no permit required for day hikes",
                    "warnings": [
                        "North Rim seasonal access (May-October)",
                        "Start early, avoid midday heat",
                        "Carry plenty of water",
                        "Going down is optional, coming up is mandatory"
                    ],
                },
                {
                    "name": "Rim Trail (South Rim)",
                    "difficulty": "Easy",
                    "length_miles": "13 miles (paved and unpaved sections)",
                    "elevation_gain_feet": "Minimal",
                    "description": "Easy, mostly paved trail along South Rim with multiple viewpoints. Accessible trail suitable for all ages. Can be hiked in sections.",
                    "highlights": [
                        "Easy",
                        "Paved sections",
                        "Multiple viewpoints",
                        "Accessible",
                        "Family-friendly",
                        "Can hike in sections"
                    ],
                    "best_seasons": "Year-round",
                    "trailhead": "Multiple access points along South Rim",
                    "features": ["Easy", "Paved", "Accessible", "Family-friendly", "Viewpoints"],
                    "permits": "Grand Canyon National Park - no permit required",
                },
                {
                    "name": "Hermit Trail (South Rim)",
                    "difficulty": "Strenuous",
                    "length_miles": "Varies (2.5 miles to Santa Maria Spring, 8.8 miles to River)",
                    "elevation_gain_feet": "Varies (significant elevation change)",
                    "description": "Less maintained, more primitive trail with no water stations. More challenging than Bright Angel or South Kaibab. For experienced hikers only.",
                    "highlights": [
                        "Less crowded",
                        "More primitive",
                        "Challenging",
                        "For experienced hikers"
                    ],
                    "best_seasons": "Spring, Fall - avoid summer heat",
                    "trailhead": "Hermit Trailhead (South Rim, accessible by shuttle)",
                    "features": ["Primitive", "Challenging", "Less maintained"],
                    "permits": "Grand Canyon National Park - no permit required for day hikes",
                    "warnings": [
                        "NO WATER STATIONS - must carry all water",
                        "Less maintained - more challenging",
                        "For experienced hikers only",
                        "Start early, avoid midday heat",
                        "Carry plenty of water"
                    ],
                },
                {
                    "name": "Grandview Trail (South Rim)",
                    "difficulty": "Strenuous",
                    "length_miles": "Varies (2.2 miles to Horseshoe Mesa, 6.2 miles to Cottonwood Creek)",
                    "elevation_gain_feet": "Varies (significant elevation change)",
                    "description": "Historic mining trail with steep, rocky sections. More challenging and less maintained. For experienced hikers only.",
                    "highlights": [
                        "Historic mining trail",
                        "Less crowded",
                        "Challenging",
                        "For experienced hikers"
                    ],
                    "best_seasons": "Spring, Fall - avoid summer heat",
                    "trailhead": "Grandview Trailhead (South Rim, Desert View area)",
                    "features": ["Historic", "Challenging", "Steep", "Rocky"],
                    "permits": "Grand Canyon National Park - no permit required for day hikes",
                    "warnings": [
                        "Steep, rocky sections",
                        "Less maintained",
                        "For experienced hikers only",
                        "Start early, avoid midday heat",
                        "Carry plenty of water"
                    ],
                },
            ],
            "rim_to_rim": {
                "description": "Epic 21-24 mile hike from North Rim to South Rim (or vice versa) with ~5,000 feet elevation change",
                "distance": "21-24 miles depending on route",
                "elevation_change": "~5,000 feet",
                "difficulty": "Extremely strenuous",
                "best_time": "May-October (North Rim access required)",
                "permits": "Not required for day hike, but recommended to plan ahead",
                "warnings": [
                    "Extremely strenuous - for experienced hikers only",
                    "Requires North Rim access (May-October)",
                    "Start very early (4-5 AM)",
                    "Carry plenty of water",
                    "Plan transportation between rims (4-5 hour drive)",
                    "Consider overnight at Phantom Ranch (permits required)"
                ],
            },
            "difficulty_range": "Easy (Rim Trail) to extremely strenuous (Rim-to-Rim)",
            "best_seasons": "Spring (March-May), Fall (September-November) - avoid summer heat",
            "trail_features": ["Rim-to-river", "Rim-to-rim", "Spectacular views", "Challenging terrain", "Iconic"],
        },
        "rim_to_rim": {
            "description": "Epic 21-24 mile hike from North Rim to South Rim (or vice versa)",
            "distance": "21-24 miles depending on route",
            "elevation_change": "~5,000 feet",
            "difficulty": "Extremely strenuous",
            "best_time": "May-October (North Rim access)",
            "permits": "Not required for day hike, but recommended to plan ahead",
        },
        "photography": {
            "description": "Iconic landscapes, sunrise/sunset views",
            "best_spots": [
                "Mather Point (South Rim)",
                "Yavapai Point (South Rim)",
                "Hopi Point (South Rim - sunset)",
                "Desert View Watchtower (South Rim)",
                "Bright Angel Point (North Rim)",
                "Cape Royal (North Rim)",
            ],
            "best_times": "Sunrise and sunset for best lighting",
        },
        "rafting": {
            "description": "Colorado River whitewater rafting",
            "permits": "Required - very limited, lottery system",
            "duration": "Multi-day trips (7-18 days)",
        },
    },
    "attractions": {
        "south_rim": [
            "Grand Canyon Visitor Center",
            "Mather Point",
            "Yavapai Geology Museum",
            "Desert View Watchtower",
            "Hermit's Rest",
            "Grand Canyon Village",
            "El Tovar Hotel",
            "Bright Angel Lodge",
        ],
        "north_rim": [
            "Grand Canyon Lodge",
            "Bright Angel Point",
            "Cape Royal",
            "Point Imperial",
        ],
        "viewpoints": {
            "south_rim": [
                "Mather Point",
                "Yavapai Point",
                "Hopi Point",
                "Mohave Point",
                "Pima Point",
                "Hermit's Rest",
                "Desert View",
            ],
            "north_rim": [
                "Bright Angel Point",
                "Cape Royal",
                "Point Imperial",
                "Roosevelt Point",
            ],
        },
    },
    "businesses": {
        "lodging": {
            "south_rim": [
                {
                    "name": "El Tovar Hotel",
                    "type": "Historic Hotel",
                    "description": "Historic luxury hotel on South Rim",
                },
                {
                    "name": "Bright Angel Lodge",
                    "type": "Lodge",
                    "description": "Historic lodge with cabins",
                },
                {
                    "name": "Maswik Lodge",
                    "type": "Lodge",
                    "description": "Modern lodge accommodations",
                },
            ],
            "north_rim": [
                {
                    "name": "Grand Canyon Lodge",
                    "type": "Lodge",
                    "description": "Historic lodge on North Rim (seasonal)",
                },
            ],
        },
        "dining": {
            "south_rim": [
                {
                    "name": "El Tovar Dining Room",
                    "type": "Fine Dining",
                    "description": "Upscale dining with canyon views",
                },
                {
                    "name": "Arizona Room",
                    "type": "Casual Dining",
                    "description": "Casual dining with canyon views",
                },
            ],
        },
    },
    "practical_info": {
        "entrance_fees": "$35 per vehicle (7-day pass) or America the Beautiful Pass",
        "permits": "Required for overnight backcountry camping, rafting",
        "best_times": {
            "south_rim": "Year-round (crowded in summer)",
            "north_rim": "May-October (weather dependent)",
        },
        "crowds": "Very crowded in summer, especially South Rim",
        "shuttles": "Free shuttle service on South Rim (Hermit Road, Village Route)",
        "parking": "Limited - arrive early or use shuttles",
        "weather": "Extreme temperature variation - hot at river, cold on rims",
        "access": {
            "south_rim": "I-40 to Highway 64, or Highway 180 from Flagstaff",
            "north_rim": "Highway 67 (seasonal, closes in winter)",
        },
    },
}


class GrandCanyonAgent(LocationAgentBase):
    """Agent specialized in Grand Canyon National Park information and context.

    This agent enhances existing agent outputs with Grand Canyon-specific knowledge
    for both North and South Rims, hiking, viewpoints, and outdoor opportunities.
    """

    LOCATION_NAME = "Grand Canyon National Park, Arizona"
    LOCATION_INDICATORS = [
        "grand canyon",
        "grand canyon national park",
        "grand canyon, az",
        "grand canyon, arizona",
        "south rim",
        "north rim",
        "grand canyon south rim",
        "grand canyon north rim",
    ]
    AGENT_NAME = "grand_canyon_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Grand Canyon-specific knowledge base (fallback if external file not found)."""
        return GRAND_CANYON_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Grand Canyon agent."""
        return """You are a comprehensive guide for Grand Canyon National Park, Arizona -
one of the Seven Natural Wonders of the World.

Your role is to:
1. Use tools to gather real-time data about Grand Canyon (trails, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Grand Canyon-specific knowledge from the knowledge base
4. Combine information from existing agents with Grand Canyon expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Grand Canyon National Park, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Grand Canyon National Park, Arizona") if available

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Add permits and regulations information (Grand Canyon National Park - no permit required for day hikes, but required for overnight backcountry)
- Include critical safety warnings (going down is optional, coming up is mandatory)
- Highlight water availability (Bright Angel has water, South Kaibab has NO water)

COMBINE multiple sources:
- Tool data (current conditions, real-time info from search_trails)
- Knowledge base (detailed trail descriptions, historical info)
- Existing agent outputs (trail_info from trail_agent if available)

PROVIDE comprehensive trail information:
- Trail names, difficulty ratings, length, elevation gain
- Detailed trail descriptions and highlights
- Best seasons and current conditions
- Trailhead locations and access (shuttle information for South Kaibab, Hermit)
- Permits and regulations
- CRITICAL safety considerations (water availability, heat, going down vs coming up)
- Trail connectivity and route planning
- Rim-to-rim information if relevant

TOOL USAGE GUIDANCE:

For Hiking Queries:
- ALWAYS use search_trails with activity_type="hiking" and location="Grand Canyon National Park, Arizona"
- Grand Canyon has iconic trails including Bright Angel Trail (most popular, has water stations), South Kaibab Trail (steeper, NO water), North Kaibab Trail (North Rim, seasonal), Rim Trail (easy, paved), Hermit Trail (primitive, no water), and Grandview Trail (historic, challenging)
- Enhance tool results with knowledge base information about trail difficulty, length, elevation, water availability, and critical safety warnings
- CRITICAL: Always mention water availability (Bright Angel has water, South Kaibab has NO water)
- CRITICAL: Always mention "going down is optional, coming up is mandatory" and "hike down only 1/3 of what you can hike up"
- Mention Rim-to-Rim hike if user is interested in epic challenges

For Accommodation Queries:
- Use search_accommodations with location="Grand Canyon National Park, Arizona"
- Enhance with knowledge base information (El Tovar Hotel, Bright Angel Lodge, Maswik Lodge on South Rim; Grand Canyon Lodge on North Rim - seasonal)
- Mention limited lodging in park - book well in advance

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Mather Point, Yavapai Point, Hopi Point (sunset), Desert View Watchtower (South Rim); Bright Angel Point, Cape Royal, Point Imperial (North Rim)
- Mention sunrise and sunset for best lighting

For Logistics Queries:
- Use get_parking_information for trailhead parking (limited - arrive early)
- Use find_shuttle_services for free shuttle service on South Rim
- Provide information about permits (day hikes: no permit required; overnight backcountry: permit required)
- Mention entrance fee ($35 per vehicle or America the Beautiful Pass)
- Mention North Rim seasonal access (May-October)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

Grand Canyon Highlights:
- One of the Seven Natural Wonders of the World
- Over 1 mile deep, 277 miles long
- Two rims: South Rim (open year-round) and North Rim (seasonal)
- Iconic rim-to-river and rim-to-rim hikes
- World-class photography opportunities
- Colorado River whitewater rafting
- UNESCO World Heritage Site

Key Information:
- South Rim: 7,000 feet elevation, open year-round, full services
- North Rim: 8,000 feet elevation, seasonal (May-October), more remote
- River: 2,400 feet elevation, extreme heat in summer

FAMOUS TRAILS:
- Bright Angel Trail (South Rim - most popular, has water stations, 1.5-9.5 miles depending on destination)
- South Kaibab Trail (South Rim - steeper, NO water stations, 1.5-6.8 miles depending on destination)
- North Kaibab Trail (North Rim - seasonal access, 1.5-14.2 miles depending on destination)
- Rim Trail (South Rim - easy, paved, 13 miles, can hike in sections)
- Hermit Trail (South Rim - primitive, no water, 2.5-8.8 miles)
- Grandview Trail (South Rim - historic mining trail, challenging, 2.2-6.2 miles)
- Rim-to-Rim: Epic 21-24 mile hike (extremely strenuous, requires North Rim access May-October)

CRITICAL Safety Information:
- Going down is optional, coming up is mandatory
- Hike down only 1/3 of what you can hike up
- Start early (5-6 AM), avoid midday heat
- Carry plenty of water (minimum 1 liter per hour)
- South Kaibab Trail has NO WATER STATIONS - must carry all water
- Bright Angel Trail has water stations at rest houses
- Extreme temperature variation (hot at river 100°F+, cold on rims 40-60°F)
- River elevation: 2,400 feet (extreme heat in summer)
- Rim elevation: 7,000-8,000 feet (much cooler)

PRACTICAL INFORMATION:
- Entrance fee: $35 per vehicle (7-day pass) or America the Beautiful Pass
- Very crowded in summer, especially South Rim
- Limited parking - arrive early or use free shuttle service
- Free shuttle service on South Rim (Hermit Road, Village Route)
- Permits required for overnight backcountry camping (apply well in advance)
- Day hikes: no permit required
- Best times: Spring (March-May) and Fall (September-November) - avoid summer heat
- South Rim: open year-round, full services
- North Rim: seasonal (May-October, weather dependent), more remote

ENHANCEMENT GUIDELINES:
- Always combine tool results with knowledge base information
- Provide specific recommendations based on activity type and season
- Include CRITICAL safety considerations (water availability, heat, going down vs coming up)
- Emphasize water availability differences between trails (Bright Angel has water, South Kaibab has NO water)
- Highlight unique characteristics (One of Seven Natural Wonders, rim-to-river hikes, rim-to-rim challenge)
- Provide practical tips (parking, permits, shuttles, best times, North Rim seasonal access)

Provide comprehensive, accurate, practical information that combines real tool data with Grand Canyon-specific knowledge and context."""

