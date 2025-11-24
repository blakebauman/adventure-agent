# Location Agents Architecture

## Overview

The location agents system provides a scalable architecture for adding location-specific agents (cities, towns, regions) that enhance adventure planning with local knowledge.

## Architecture

### Base Class: `LocationAgentBase`

All location agents inherit from `LocationAgentBase`, which provides:
- Common tool access (trails, restaurants, accommodations, etc.)
- Dynamic tool selection via `create_agent`
- Standardized interface for location-specific knowledge
- Automatic location matching

### Registry System

Location agents are registered in a global registry, allowing:
- Dynamic discovery of available location agents
- Automatic routing based on location detection
- Easy addition of new location agents

## Current Location Agents

1. **Jerome Agent** (`jerome_agent`)
   - Location: Jerome, Arizona
   - Specializes in: Historic mining town, ghost town revival, artistic community

2. **Sedona Agent** (`sedona_agent`)
   - Location: Sedona, Arizona
   - Specializes in: Red rock formations, world-class MTB trails, spiritual vortex sites

3. **Prescott Agent** (`prescott_agent`)
   - Location: Prescott, Arizona
   - Specializes in: Historic territorial capital, Whiskey Row, mountain biking

## How to Add a New Location Agent

### Step 1: Create the Agent File

Create a new file `src/agent/agents/{location}_agent.py`:

```python
"""{Location} specialist agent."""

from __future__ import annotations
from typing import Any, Dict
from agent.agents.location_agent_base import LocationAgentBase

# Location-specific knowledge base
{LOCATION}_KNOWLEDGE = {
    "location": {
        "name": "{Location Name}",
        "coordinates": {"lat": 0.0, "lon": 0.0},
        "elevation": 0,  # feet
        "region": "County, State",
        "country": "US",
        "proximity": {
            "nearby_town": {"distance_miles": 0, "direction": "north"},
        },
    },
    "history": {
        # Historical information
    },
    "attractions": {
        # Local attractions
    },
    "businesses": {
        # Restaurants, shops, accommodations
    },
    # ... more knowledge
}

class {Location}Agent(LocationAgentBase):
    LOCATION_NAME = "{Location Name}"
    LOCATION_INDICATORS = [
        "{location}",
        "{location}, az",
        "{location}, arizona",
    ]
    AGENT_NAME = "{location}_agent"

    def get_location_knowledge(self) -> Dict[str, Any]:
        return {LOCATION}_KNOWLEDGE

    def _get_system_prompt(self) -> str:
        return """Your system prompt here..."""
```

### Step 2: Register the Agent

In `src/agent/graph.py`, add:

```python
from agent.agents.{location}_agent import {Location}Agent

# Initialize and register
{location}_agent = {Location}Agent()
register_location_agent({location}_agent)
```

### Step 3: Add to Graph

The graph will automatically detect and route to location agents based on location matching.

### Step 4: Update Exports

Add to `src/agent/agents/__init__.py`:

```python
from agent.agents.{location}_agent import {Location}Agent

__all__ = [
    # ... existing agents
    "{Location}Agent",
]
```

## How It Works

### 1. Location Detection

The orchestrator analyzes user input and extracts the location. It then:
- Calls `find_location_agent_for_location(location)` 
- If a match is found, adds the location agent to `required_agents`
- Provides context for the location agent

### 2. Agent Execution

When a location agent is called:
1. Verifies location match
2. Uses tools to gather real-time data (trails, restaurants, etc.)
3. Enhances tool results with location-specific knowledge
4. Combines with outputs from other agents
5. Returns comprehensive location guide

### 3. Dynamic Tool Selection

Location agents use `create_agent` which allows the LLM to:
- Select relevant tools based on query
- Call tools dynamically
- Synthesize results with knowledge base

## Knowledge Base Structure

Each location agent maintains a knowledge base with:

```python
{
    "location": {
        "name": str,
        "coordinates": {"lat": float, "lon": float},
        "elevation": int,  # feet
        "region": str,
        "country": str,
        "proximity": {
            "nearby_town": {"distance_miles": int, "direction": str},
        },
    },
    "history": {
        # Historical context
    },
    "geography": {
        # Geographic features
    },
    "outdoor_activities": {
        # Trail info, activities
    },
    "attractions": {
        # Points of interest
    },
    "businesses": {
        "restaurants": [...],
        "shops": [...],
        "accommodations": [...],
    },
    "practical_info": {
        # Parking, permits, best times, etc.
    },
}
```

## Benefits

1. **Scalability**: Easy to add new locations
2. **Consistency**: All location agents follow same pattern
3. **Maintainability**: Base class handles common functionality
4. **Flexibility**: Each agent can customize knowledge and prompts
5. **Dynamic**: Automatic detection and routing

## Future Enhancements

- Load knowledge bases from external sources (JSON, database)
- Support for regions (not just cities)
- Multi-location support (e.g., "Sedona to Prescott route")
- Knowledge base versioning and updates
- Community-contributed location agents

