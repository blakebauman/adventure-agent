"""Jerome, Arizona specialist agent.

This agent provides Jerome-specific information and enhances existing agent outputs
with local knowledge about Jerome's history, culture, and outdoor opportunities.
Only activated when location is Jerome, Arizona.
"""

from __future__ import annotations

import json
from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage

from agent.agents.location_agent_base import LocationAgentBase

# Jerome-specific knowledge base
JEROME_KNOWLEDGE = {
    "location": {
        "name": "Jerome, Arizona",
        "coordinates": {"lat": 34.7531, "lon": -112.1139},
        "elevation": 5000,  # feet
        "region": "Yavapai County, Arizona",
        "country": "US",
        "proximity": {
            "sedona": {"distance_miles": 30, "direction": "northeast"},
            "prescott": {"distance_miles": 45, "direction": "southwest"},
            "flagstaff": {"distance_miles": 50, "direction": "north"},
            "phoenix": {"distance_miles": 100, "direction": "south"},
        },
    },
    "history": {
        "founded": 1875,
        "incorporated": 1899,
        "peak_population": 15000,
        "current_population": 444,
        "nickname": "Wickedest Town in The West",
        "mining_era": {
            "start": 1883,
            "end": 1953,
            "company": "United Verde Copper Company",
            "founder": "Frederick Tritle",
            "major_owner": "William Clark",
            "production": "Nearly $1 billion in copper",
        },
        "decline": {
            "major_mining_ceased": 1953,
            "population_drop": "Under 100 by late 1950s",
            "factors": [
                "Lack of high-grade ores",
                "Great Depression",
                "Severe landslides",
                "Smelter fumes killed vegetation",
                "Large blasting operations",
            ],
        },
        "revival": {
            "historical_society_founded": "March 15, 1953",
            "founder_inspiration": "Jimmy Brewer (Tuzigoot National Monument curator)",
            "slogan_creator": "Jimmy Brewer - 'America's Largest Ghost City'",
            "phelps_dodge_negotiation": 1956,
            "main_street_purchase": 1956,
            "artistic_community": "Early 1950s - Verde Valley Art Association",
            "current_character": "Bustling artistic community",
            "annual_visitation": "~1 million visitors",
        },
        "postal_history": {
            "established": 1883,
            "first_postmaster": "Frederick E. Thomas (salary $18.53/year)",
            "mail_carrier": "Virgil Earp (Wyatt's brother) 1897-1902 by horseback",
            "fires": "Multiple fires destroyed post office buildings",
            "slides": "Post office collapsed due to mining blasts, town slid 3/8 inch/month",
            "jail_slide": "Jail slid 300 feet before tipping over",
            "tunnels": "84 miles of tunnels beneath the town",
            "protest": "1975 - residents protested post office closure, kept it open",
        },
    },
    "attractions": {
        "historical_sites": [
            "Jerome State Historic Park (Douglas Mansion, built 1916)",
            "Jerome Historical Society & Mine Museum",
            "Sliding Jail (built 1905, slid 225 feet, stabilized 2017)",
            "Little Daisy Hotel (built 1918, now private residence)",
            "Jerome Grand Hotel",
            "Spook Hall Venue",
            "New State Motor Building",
            "Audrey Headframe Park (largest wooden headframe in Arizona)",
            "Art Park",
            "Scenic Overlook",
            "Gold King Mine & Ghost Town (nearby in Haynes)",
        ],
        "museums": [
            "Jerome Historical Society Mine Museum (1899 building)",
            "Jerome State Historic Park Museum (Douglas Mansion)",
        ],
        "cultural": [
            "Jerome Historical Society",
            "Jerome Chamber of Commerce",
            "Jerome Public Library",
            "The Old Book Room",
            "Art galleries and studios throughout town",
        ],
        "events": [
            "Ghost Walk (annual October event with reenactments)",
            "Art Walks (monthly events)",
            "Community Arts Program",
            "Home Tours (annual events)",
        ],
        "nearby_attractions": [
            "Tuzigoot National Monument (Jimmy Brewer was curator)",
            "Sharlot Hall Museum (Prescott - regional history)",
        ],
    },
    "geography": {
        "terrain": "Hillside town on Cleopatra Hill",
        "topography": "Black Hills of Arizona",
        "viewpoints": "Overlooks Verde Valley and Mogollon Rim",
        "red_rock_cliffs": "Spectacular views of red rock formations",
        "san_francisco_peaks": "13,000-foot peaks visible 50 miles to the north",
    },
    "outdoor_activities": {
        "hiking": "Access to trails in Verde Valley and surrounding areas",
        "mountain_biking": "Proximity to Sedona's world-class MTB trails",
        "scenic_drives": "State Highway 89A through Jerome",
        "photography": "Historic architecture, mining ruins, scenic overlooks",
        "cultural_tourism": "Ghost town tours, historical sites, art galleries",
    },
    "resources": {
        "historical_society": {
            "website": "https://www.jeromehistoricalsociety.com/",
            "phone": "928-634-1066",
            "address": "PO Box 156, Jerome, AZ 86331",
            "hours": "Monday-Friday: 10:00am-4:00pm",
            "founded": "March 15, 1953",
            "founders": ["John Moore", "James Haskins", "Laura Williams"],
            "archives": "Over 12,000 photographs and documents",
            "services": [
                "Research services",
                "Photo archive",
                "Jerome resident video interviews (28+ interviews)",
                "Museum tours",
            ],
            "sitemap": "https://www.jeromehistoricalsociety.com/wp-sitemap.xml",
        },
        "town_website": "https://jerome.az.gov/",
        "arizona_memory_project": {
            "url": "https://azmemory.azlibrary.gov/nodes/view/124",
            "collections": [
                "Jerome Postal History (46 images, 15 documents)",
                "Men, Mines and Money",
            ],
        },
        "arizona_historical_society": {
            "url": "https://arizonahistoricalsociety.org/",
            "digital_archives": "https://azhsarchives.contentdm.oclc.org/",
            "jerome_collections": [
                "Jannette Kimble Drawings",
                "Lollesgard Postcard Collection",
                "Douglas Dr. James Collection",
                "ADMMR Colvocoresses Collection",
                "ADMMR Tucson Office Mining Collection",
            ],
        },
        "wikipedia": [
            "https://en.wikipedia.org/wiki/Jerome_Historic_District",
            "https://en.wikipedia.org/wiki/Jerome_State_Historic_Park",
        ],
    },
    "local_context": {
        "nearby_towns": {
            "sedona": {
                "description": "World-renowned red rock destination",
                "activities": "Mountain biking, hiking, spiritual retreats",
                "distance": "30 miles northeast",
            },
            "prescott": {
                "description": "Historic territorial capital",
                "activities": "Mountain biking, hiking, Whiskey Row",
                "distance": "45 miles southwest",
            },
        },
        "access": {
            "highway": "State Highway 89A",
            "parking": "Limited parking, shuttle service available",
            "shuttle": "Free shuttle service for visitors",
        },
        "considerations": [
            "Historic buildings and mining ruins",
            "Steep hillside terrain",
            "Limited parking - use shuttle service",
            "Respect private property",
            "Ghost town atmosphere - many abandoned buildings",
        ],
    },
    "businesses": {
        "restaurants": [
            {
                "name": "Haunted Hamburger",
                "type": "Casual Dining",
                "description": "Burgers and American fare with scenic views",
                "highlights": ["Scenic views", "Popular with visitors", "Historic building"],
            },
            {
                "name": "The Asylum Restaurant",
                "type": "Fine Dining",
                "location": "Jerome Grand Hotel",
                "description": "Fine dining with historical ambiance",
                "highlights": ["Historic hotel setting", "Upscale dining", "Ghost town atmosphere"],
            },
            {
                "name": "Bobby D's BBQ",
                "type": "Barbecue",
                "description": "Classic barbecue in historic building",
                "highlights": ["Historic building", "BBQ specialties"],
            },
            {
                "name": "Flatiron Cafe",
                "type": "Cafe",
                "description": "Local cafe with coffee and light meals",
            },
            {
                "name": "Grapes Restaurant & Bar",
                "type": "Restaurant & Bar",
                "description": "Wine bar and restaurant",
            },
            {
                "name": "Mile High Grill & Inn",
                "type": "Restaurant",
                "description": "Restaurant with inn accommodations",
            },
        ],
        "shops_and_galleries": [
            {
                "name": "Nellie Bly Kaleidoscopes",
                "type": "Art Gallery/Shop",
                "description": "Kaleidoscope gallery and shop",
            },
            {
                "name": "Jerome Artists Cooperative Gallery",
                "type": "Art Gallery",
                "description": "Cooperative gallery featuring local artists",
            },
            {
                "name": "Pura Vida Gallery",
                "type": "Art Gallery",
                "description": "Art gallery showcasing local and regional artists",
            },
            {
                "name": "Raku Gallery",
                "type": "Art Gallery",
                "description": "Ceramics and pottery gallery",
            },
            {
                "name": "Jerome Winery",
                "type": "Winery",
                "description": "Local winery and tasting room",
            },
            {
                "name": "Jerome Pottery",
                "type": "Pottery Shop",
                "description": "Handmade pottery and ceramics",
            },
            {
                "name": "Mile High Sweets & Treats",
                "type": "Candy Shop",
                "description": "Candy and sweets shop",
            },
            {
                "name": "Jerome Rocks & Minerals",
                "type": "Rock Shop",
                "description": "Minerals, rocks, and gemstones",
            },
            {
                "name": "Spirit Room",
                "type": "Bar/Live Music",
                "description": "Historic bar with live music",
            },
        ],
        "accommodations": [
            {
                "name": "Jerome Grand Hotel",
                "type": "Hotel",
                "description": "Historic hotel with fine dining (The Asylum Restaurant)",
                "highlights": ["Historic building", "Haunted reputation", "Fine dining"],
            },
            {
                "name": "Mile High Grill & Inn",
                "type": "Inn",
                "description": "Inn with restaurant",
            },
            {
                "name": "Connor Hotel",
                "type": "Historic Hotel",
                "description": "Historic hotel in downtown Jerome",
            },
            {
                "name": "Surgeon's House Bed & Breakfast",
                "type": "Bed & Breakfast",
                "description": "Historic B&B",
            },
        ],
        "places_to_see": [
            {
                "name": "Jerome State Historic Park",
                "type": "Historic Site/Museum",
                "description": "Douglas Mansion (1916) with mining history exhibits",
                "highlights": ["Mining history", "Panoramic views", "Museum exhibits"],
            },
            {
                "name": "Jerome Historical Society Mine Museum",
                "type": "Museum",
                "location": "Main Street",
                "description": "Mining artifacts, equipment, and historical photographs",
                "highlights": ["1899 building", "Mining equipment", "12,000+ photos"],
            },
            {
                "name": "Sliding Jail",
                "type": "Historic Landmark",
                "description": "Jail that slid 225 feet down the hillside (1905-1938)",
                "highlights": ["Stabilized 2017", "Historic significance"],
            },
            {
                "name": "Audrey Headframe Park",
                "type": "Park",
                "description": "Largest wooden headframe still standing in Arizona",
                "highlights": ["Mining history", "Scenic views"],
            },
            {
                "name": "Art Park",
                "type": "Park",
                "description": "Public art space and park",
            },
            {
                "name": "Scenic Overlook",
                "type": "Viewpoint",
                "description": "Panoramic views of Verde Valley and Mogollon Rim",
                "highlights": ["Red rock views", "San Francisco Peaks", "Sunset viewing"],
            },
            {
                "name": "Gold King Mine & Ghost Town",
                "type": "Attraction",
                "location": "Nearby in Haynes",
                "description": "Historic ghost town with petting zoo, antique equipment, walk-in mine",
                "highlights": ["Petting zoo", "Mining equipment", "Ghost town atmosphere"],
            },
            {
                "name": "Little Daisy Hotel",
                "type": "Historic Building",
                "description": "Built 1918, now private residence (exterior viewing)",
            },
            {
                "name": "Spook Hall",
                "type": "Historic Venue",
                "description": "Historic venue available for events",
            },
            {
                "name": "New State Motor Building",
                "type": "Historic Building",
                "description": "Preserved historic building",
            },
        ],
        "entertainment": [
            {
                "name": "Spirit Room",
                "type": "Bar/Live Music",
                "description": "Historic bar with live music and entertainment",
            },
            {
                "name": "Ghost Walk",
                "type": "Event",
                "description": "Annual October event with historical reenactments",
                "highlights": ["Historical reenactments", "Haunted stories", "Annual event"],
            },
            {
                "name": "Art Walks",
                "type": "Event",
                "description": "Monthly events where galleries open to visitors",
            },
        ],
    },
}


class JeromeAgent(LocationAgentBase):
    """Agent specialized in Jerome, Arizona information and context.

    This agent enhances existing agent outputs with Jerome-specific knowledge
    about the town's history, culture, geography, and outdoor opportunities.
    Only activated when location is Jerome, Arizona.
    """

    LOCATION_NAME = "Jerome, Arizona"
    LOCATION_INDICATORS = [
        "jerome",
        "jerome, az",
        "jerome, arizona",
        "jerome az",
    ]
    AGENT_NAME = "jerome_agent"

    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Get Jerome-specific knowledge base (fallback if external file not found)."""
        return JEROME_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Jerome agent."""
        return """You are a comprehensive guide for Jerome, Arizona - a historic mining town
turned artistic community perched on a hillside at 5,000 feet elevation, known as "America's Largest Ghost City"
and the "Wickedest Town in The West."

Your role is to:
1. Use tools to gather real-time data about Jerome (trails, restaurants, accommodations, etc.)
2. Select which tools are most relevant based on the user's query and activity type
3. Enhance tool results with Jerome-specific knowledge from the knowledge base
4. Combine information from existing agents with Jerome expertise
5. Provide a complete, practical guide for visitors

TRAIL DATA PRIORITY - Your primary focus is comprehensive trail information:

ALWAYS USE search_trails TOOL FIRST for any trail-related query:
- For hiking: search_trails(activity_type="hiking", location="Jerome, Arizona")
- For mountain biking: search_trails(activity_type="mountain_biking", location="Jerome, Arizona")
- For trail running: search_trails(activity_type="trail_running", location="Jerome, Arizona")

ENHANCE tool results with knowledge base trail information:
- Add detailed descriptions, difficulty, length, elevation from knowledge base
- Include highlights, features, and seasonal considerations
- Provide trailhead locations and access information
- Mention proximity to Sedona's world-class trails (30 miles northeast)
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
- Proximity to Sedona trails (30 miles) for world-class mountain biking
- Activity-specific recommendations

TOOL USAGE GUIDANCE:

For Mountain Biking Queries:
- ALWAYS use search_trails with activity_type="mountain_biking" and location="Jerome, Arizona"
- Jerome is 30 miles from Sedona's world-class mountain biking trails (Hiline, Hangover, Highline, etc.)
- Local Verde Valley trails offer additional options
- Enhance tool results with knowledge base information about Sedona proximity and local trails
- Mention that Jerome is an excellent base camp for exploring Sedona trails

For Hiking Queries:
- Use search_trails with activity_type="hiking" and location="Jerome, Arizona"
- Local trails in surrounding Black Hills and Verde Valley
- Access to Sedona hiking (30 miles) and Prescott trails (45 miles)
- Use find_scenic_viewpoints for Verde Valley and Mogollon Rim overlooks
- Enhance with knowledge base information about trail difficulty and best seasons

For Historical/Cultural Queries:
- Use find_historical_sites and get_local_history
- Key sites: Jerome State Historic Park (Douglas Mansion, 1916), Jerome Historical Society & Mine Museum (1899 building, 12,000+ photos/documents), Sliding Jail (1905, slid 225 feet), Audrey Headframe Park
- Enhance with knowledge base information about Jerome's rich mining history and revival
- Provide context about Jerome's transformation from mining town to artistic community

For Dining Queries:
- Use find_restaurants with location="Jerome, Arizona"
- Enhance results with knowledge base businesses (Haunted Hamburger, The Asylum, Flatiron Cafe, etc.)
- Provide context about local favorites and historic atmosphere

For Accommodation Queries:
- Use search_accommodations with location="Jerome, Arizona"
- Enhance with knowledge base information (Jerome Grand Hotel, Connor Hotel, etc.)
- Mention proximity to Sedona, Prescott, and Flagstaff

For Photography Queries:
- Use find_photo_spots and find_scenic_viewpoints
- Key spots: Historic architecture, mining ruins, scenic overlooks (Verde Valley, Mogollon Rim, San Francisco Peaks visible 50 miles north), Audrey Headframe Park
- Mention best times (golden hour, sunrise/sunset) and seasonal opportunities

For Logistics Queries:
- Use get_parking_information (LIMITED PARKING - emphasize free shuttle service)
- Use find_shuttle_services (free shuttle service available for visitors)
- Provide information about State Highway 89A access
- Mention proximity to Sedona (30 miles), Prescott (45 miles), Flagstaff (50 miles), Phoenix (100 miles)

TOOL SELECTION RULES:
- Only call tools relevant to the user's query - be selective, not exhaustive
- Start with get_coordinates to verify location if location is unclear
- Combine tool results with knowledge base information for comprehensive answers
- If tool results are incomplete, supplement with knowledge base data

Jerome's History:
- Founded in 1875 as a mining camp, incorporated in 1899
- Peak population of 15,000 during mining boom (early 1900s)
- Known as "Wickedest Town in The West" (30+ nationalities, saloons, brothels)
- Major copper mining operations from 1883-1953 (United Verde Copper Company)
- Big Mine closed: January 30, 1953
- Population dropped to under 100 by late 1950s
- Historical Society founded: March 15, 1953 (saved the town from demolition)
- Revived as artistic community starting in 1950s
- Current population: ~444 residents, ~1 million annual visitors

Location & Geography:
- Located in Yavapai County, Arizona
- Elevation: 5,000 feet on Cleopatra Hill (Black Hills of Arizona)
- 30 miles northeast of Sedona (world-class MTB trails)
- 45 miles southwest of Prescott (historic territorial capital)
- 50 miles south of Flagstaff
- 100 miles north of Phoenix
- Overlooks Verde Valley and Mogollon Rim
- Spectacular views of red rock cliffs and San Francisco Peaks (13,000 ft, 50 miles north)

Key Attractions:
- Jerome State Historic Park (Douglas Mansion, 1916)
- Jerome Historical Society & Mine Museum (1899 building, 12,000+ photos/documents)
- Sliding Jail (1905, slid 225 feet, stabilized 2017)
- Little Daisy Hotel (1918, now private residence)
- Audrey Headframe Park (largest wooden headframe in Arizona)
- Art galleries and studios throughout town
- Scenic overlooks with panoramic views
- Ghost Walk (annual October event)

Outdoor Opportunities:
- Access to Verde Valley trails
- Proximity to Sedona's world-class mountain biking (30 miles)
- Hiking in surrounding Black Hills
- Photography of historic architecture, mining ruins, scenic views
- Cultural and historical tourism
- State Highway 89A scenic drive

Practical Information:
- Limited parking - use free shuttle service
- Steep hillside terrain - wear appropriate footwear
- Historic buildings - respect private property
- Many abandoned buildings - ghost town atmosphere
- Best photography: historic architecture, mining ruins, scenic overlooks

Provide comprehensive, accurate, practical information that combines:
- Real tool data (trails, restaurants, accommodations, etc.)
- Jerome-specific knowledge and context
- Enhanced recommendations based on Jerome's unique character
- Practical tips for visitors"""

    def is_jerome_location(self, location: str) -> bool:
        """Check if location string refers to Jerome, Arizona."""
        location_lower = location.lower()
        jerome_indicators = [
            "jerome",
            "jerome, az",
            "jerome, arizona",
            "jerome az",
        ]
        return any(indicator in location_lower for indicator in jerome_indicators)

    async def get_jerome_info(
        self,
        location: str,
        existing_agent_outputs: Dict[str, Any] | None = None,
        context: str = "",
        activity_type: str = "mountain_biking",
    ) -> Dict[str, Any]:
        """Get comprehensive Jerome-specific information using existing tools and agents.

        This method acts as a comprehensive guide for Jerome, using existing tools
        to gather real data and enhancing it with Jerome-specific knowledge.

        Args:
            location: Location name (should be Jerome, Arizona)
            existing_agent_outputs: Outputs from other agents to enhance
            context: Additional context from orchestrator
            activity_type: Type of activity (mountain_biking, hiking, etc.)

        Returns:
            Dictionary with Jerome-specific information and enhancements
        """
        # Verify this is Jerome
        if not self.is_jerome_location(location):
            return {
                "location": location,
                "is_jerome": False,
                "message": "Location is not Jerome, Arizona",
            }

        existing_outputs = existing_agent_outputs or {}

        # Build the query for the agent
        query_parts = [
            f"Location: {location}",
            f"Activity Type: {activity_type}",
        ]
        if context:
            query_parts.append(f"Context: {context}")

        # Add information about what other agents have found
        if existing_outputs:
            query_parts.append("\nExisting agent outputs to enhance:")
            if existing_outputs.get("geo_info"):
                query_parts.append(f"- Geo info: {json.dumps(existing_outputs['geo_info'])}")
            if existing_outputs.get("trail_info"):
                query_parts.append(f"- Trail info: {json.dumps(existing_outputs['trail_info'])}")
            if existing_outputs.get("historical_info"):
                query_parts.append(f"- Historical info: {json.dumps(existing_outputs['historical_info'])}")
            if existing_outputs.get("accommodation_info"):
                query_parts.append(f"- Accommodation info: {json.dumps(existing_outputs['accommodation_info'])}")
            if existing_outputs.get("food_info"):
                query_parts.append(f"- Food info: {json.dumps(existing_outputs['food_info'])}")

        query_parts.append(
            f"\nJerome Knowledge Base:\n{json.dumps(JEROME_KNOWLEDGE, indent=2)}"
        )

        query_parts.append(
            "\nYour task: Use tools to gather relevant information about Jerome, then provide a comprehensive guide. "
            "Select which tools are most relevant based on the activity type and context. "
            "Enhance tool results with Jerome-specific knowledge from the knowledge base above. "
            "Provide a complete guide covering location, history, attractions, businesses, outdoor activities, "
            "and practical tips. Return your response as structured JSON."
        )

        user_query = "\n".join(query_parts)

        try:
            # Use the agent to dynamically select and call tools
            response = await self.agent.ainvoke({
                "messages": [
                    SystemMessage(content=self._get_system_prompt()),
                    HumanMessage(content=user_query),
                ],
            })

            # Extract the final response from the agent
            messages = response.get("messages", [])
            final_message = messages[-1] if messages else None
            content = final_message.content if final_message else ""

            # Parse enhanced data
            import re

            json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
            if json_match:
                enhanced = json.loads(json_match.group(1))
            else:
                json_match = re.search(r"\{.*\}", content, re.DOTALL)
                if json_match:
                    enhanced = json.loads(json_match.group(0))
                else:
                    # If no JSON found, create a structured response from the content
                    enhanced = {
                        "guide": content,
                        "location": location,
                        "activity_type": activity_type,
                    }

            # Extract tool calls from agent response for debugging/transparency
            tool_calls = []
            if messages:
                for msg in messages:
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        tool_calls.extend([tc.get("name", "unknown") for tc in msg.tool_calls])

            return {
                "location": location,
                "is_jerome": True,
                "jerome_knowledge": JEROME_KNOWLEDGE,
                "jerome_guide": enhanced,  # Comprehensive guide from agent
                "enhanced_info": enhanced,  # For backward compatibility
                "tools_used": tool_calls,  # Tools the agent selected to use
                "historical_context": {
                    "mining_era": JEROME_KNOWLEDGE["history"]["mining_era"],
                    "decline": JEROME_KNOWLEDGE["history"]["decline"],
                    "revival": JEROME_KNOWLEDGE["history"]["revival"],
                },
                "attractions": JEROME_KNOWLEDGE["attractions"],
                "geography": JEROME_KNOWLEDGE["geography"],
                "outdoor_activities": JEROME_KNOWLEDGE["outdoor_activities"],
                "local_context": JEROME_KNOWLEDGE["local_context"],
                "resources": JEROME_KNOWLEDGE["resources"],
                "proximity": JEROME_KNOWLEDGE["location"]["proximity"],
                "businesses": JEROME_KNOWLEDGE["businesses"],  # Complete business directory
            }

        except Exception as e:
            print(f"Error in Jerome agent: {e}")
            return {
                "location": location,
                "is_jerome": True,
                "jerome_knowledge": JEROME_KNOWLEDGE,
                "enhanced_info": {},
                "error": str(e),
            }

