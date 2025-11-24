# Trail Enhancement Pattern for Location Agents

## Overview

Location agents should be **trail-focused** and provide comprehensive trail information for all activity types:
- **Hiking** (trails, paths, routes)
- **Mountain Biking** (MTB trails, bike paths)
- **Cycling** (road cycling, gravel, bike paths)
- **Climbing** (rock climbing, bouldering, routes)
- **Paddling** (kayaking, canoeing, paddleboarding routes)

## Knowledge Base Structure

### Trail Data in Knowledge Base

```python
"outdoor_activities": {
    "hiking": {
        "description": "Comprehensive description of hiking opportunities",
        "famous_trails": [
            {
                "name": "Trail Name",
                "difficulty": "Easy/Moderate/Strenuous",
                "length_miles": 8.5,
                "elevation_gain_feet": 1500,
                "description": "Detailed trail description",
                "highlights": ["Scenic views", "Waterfalls", "Wildlife"],
                "best_seasons": "Spring, Fall",
                "trailhead": "Location of trailhead",
                "permits": "Permit requirements if any",
                "features": ["Water sources", "Camping", "Scenic overlooks"]
            }
        ],
        "trail_networks": "Information about trail systems",
        "difficulty_range": "Easy to strenuous",
        "best_seasons": "Year-round or specific seasons"
    },
    "mountain_biking": {
        # Similar structure with MTB-specific details
        "famous_trails": [
            {
                "name": "Trail Name",
                "difficulty": "Green/Blue/Black/Double Black",
                "length_miles": 12.0,
                "elevation_gain_feet": 2000,
                "description": "MTB-specific description",
                "highlights": ["Technical sections", "Flow", "Jumps"],
                "best_seasons": "Spring, Fall",
                "trailhead": "Location",
                "features": ["Single track", "Technical", "Flow sections"]
            }
        ]
    },
    "climbing": {
        "description": "Climbing opportunities",
        "areas": [
            {
                "name": "Climbing Area Name",
                "type": "Sport/Trad/Bouldering",
                "routes": "Number of routes",
                "difficulty_range": "5.5-5.12",
                "description": "Area description",
                "access": "Access information",
                "best_seasons": "Fall, Winter, Spring"
            }
        ]
    },
    "cycling": {
        "description": "Road and gravel cycling",
        "routes": [
            {
                "name": "Route Name",
                "type": "Road/Gravel/Mixed",
                "length_miles": 50.0,
                "elevation_gain_feet": 3000,
                "description": "Route description",
                "highlights": ["Scenic", "Low traffic"],
                "best_seasons": "Year-round"
            }
        ]
    },
    "paddling": {
        "description": "Kayaking, canoeing, paddleboarding",
        "routes": [
            {
                "name": "Route Name",
                "type": "River/Lake/Flatwater",
                "length_miles": 8.0,
                "difficulty": "Class I-IV",
                "description": "Route description",
                "put_in": "Put-in location",
                "take_out": "Take-out location",
                "best_seasons": "Spring, Summer"
            }
        ]
    }
}
```

## System Prompt Enhancement

### Trail-Focused Guidance

Add to system prompts:

```python
TRAIL_FOCUSED_GUIDANCE = """
TRAIL DATA PRIORITY:
Your primary focus is providing comprehensive trail information. Always:

1. USE search_trails TOOL FIRST for any trail-related query
   - For hiking: search_trails(activity_type="hiking")
   - For mountain biking: search_trails(activity_type="mountain_biking")
   - For climbing: search_trails(activity_type="climbing") if available
   - For cycling: search_trails(activity_type="cycling")
   - For paddling: search_trails(activity_type="paddling") if available

2. ENHANCE tool results with knowledge base trail information:
   - Add detailed descriptions from knowledge base
   - Include difficulty ratings, length, elevation gain
   - Add highlights and features
   - Provide seasonal considerations
   - Include trailhead and access information

3. COMBINE multiple sources:
   - Tool data (current conditions, real-time info)
   - Knowledge base (detailed descriptions, historical info)
   - Existing agent outputs (trail_info from trail_agent)

4. PROVIDE comprehensive trail information:
   - Trail names, difficulty, length, elevation
   - Trail descriptions and highlights
   - Best seasons and conditions
   - Trailhead locations and access
   - Permits and regulations
   - Safety considerations
   - Trail connectivity and route planning
"""
```

## Tool Usage Pattern

### For Trail Queries

```python
# Always start with search_trails
trail_data = await search_trails.invoke({
    "location": location,
    "activity_type": activity_type,  # hiking, mountain_biking, climbing, cycling, paddling
    "source": "mtbproject" or "hikingproject" or "osm",
    "difficulty": difficulty,  # Optional filter
    "distance": max_distance  # Optional filter
})

# Enhance with knowledge base
enhanced_trails = enhance_trail_data(trail_data, knowledge_base["outdoor_activities"][activity_type])

# Combine with existing trail_info from other agents
if existing_outputs.get("trail_info"):
    combined = merge_trail_data(enhanced_trails, existing_outputs["trail_info"])
```

## Activity Type Support

### Supported Activity Types

1. **hiking** - Hiking trails, paths, routes
2. **mountain_biking** - MTB trails, bike paths
3. **trail_running** - Running trails
4. **bikepacking** - Multi-day bike routes
5. **climbing** - Rock climbing, bouldering (needs enhancement)
6. **cycling** - Road cycling, gravel (needs enhancement)
7. **paddling** - Kayaking, canoeing, paddleboarding (needs enhancement)

### Adding New Activity Types

1. Update `ACTIVITY_SOURCES` in `trail_agent.py`
2. Add activity-specific knowledge to location agents
3. Update system prompts with activity-specific guidance
4. Ensure tools support the activity type

## Implementation Checklist

For each location agent:

- [ ] Add comprehensive trail data to knowledge base
- [ ] Include all activity types (hiking, MTB, climbing, cycling, paddling)
- [ ] Add detailed trail information (name, difficulty, length, elevation, description)
- [ ] Include trail highlights and features
- [ ] Add seasonal considerations
- [ ] Include trailhead and access information
- [ ] Update system prompt with trail-focused guidance
- [ ] Emphasize search_trails tool usage
- [ ] Add guidance on combining tool data with knowledge base
- [ ] Include trail connectivity and route planning info

## Example: Enhanced Payson Agent

See `payson_agent.py` for complete example with:
- Comprehensive trail data for all activity types
- Detailed trail information (difficulty, length, elevation, descriptions)
- Trail highlights and features
- Seasonal considerations
- Trail-focused system prompt

