# Location Agents Organization

## Directory Structure

Location agents are now organized in a dedicated directory for better scalability:

```
src/agent/agents/
├── locations/                    # Location-specific agents directory
│   ├── __init__.py              # Exports all location agents
│   ├── jerome_agent.py          # Jerome, Arizona
│   ├── sedona_agent.py          # Sedona, Arizona
│   ├── prescott_agent.py        # Prescott, Arizona
│   ├── flagstaff_agent.py       # Flagstaff, Arizona
│   ├── grand_canyon_agent.py    # Grand Canyon (North & South Rim)
│   ├── payson_agent.py          # Payson, Arizona
│   ├── pine_agent.py            # Pine, Arizona
│   ├── strawberry_agent.py      # Strawberry, Arizona
│   ├── pinetop_agent.py          # Pinetop-Lakeside, Arizona
│   └── williams_agent.py        # Williams, Arizona
├── location_agent_base.py       # Base class for all location agents
└── ... (other agents)
```

## Active Location Agents

### Northern Arizona
1. **Flagstaff Agent** - Mountain town, San Francisco Peaks, Grand Canyon gateway
2. **Grand Canyon Agent** - North and South Rim, iconic hiking, one of the Seven Natural Wonders
3. **Williams Agent** - Route 66, Grand Canyon gateway, Grand Canyon Railway
4. **Sedona Agent** - Red rock formations, world-class MTB trails
5. **Prescott Agent** - Historic territorial capital, Whiskey Row
6. **Jerome Agent** - Historic mining town, ghost town revival

### Central Arizona (Mogollon Rim)
7. **Payson Agent** - Mogollon Rim gateway, Tonto National Forest
8. **Pine Agent** - Mogollon Rim community, small mountain town
9. **Strawberry Agent** - Mogollon Rim community, historic buildings

### Eastern Arizona (White Mountains)
10. **Pinetop Agent** - White Mountains, lakes, fishing, outdoor recreation

## Benefits of Organization

1. **Scalability**: Easy to add new location agents without cluttering main agents directory
2. **Clarity**: Clear separation between functional agents and location-specific agents
3. **Maintainability**: All location agents in one place
4. **Consistency**: All location agents follow same pattern via base class

## Adding New Location Agents

1. Create agent file in `src/agent/agents/locations/`
2. Inherit from `LocationAgentBase`
3. Define knowledge base and system prompt
4. Add to `locations/__init__.py`
5. Register in `graph.py`
6. Update `arizona_registry.py`

## Import Pattern

Location agents are imported from the locations subdirectory:

```python
from agent.agents.locations import (
    JeromeAgent,
    SedonaAgent,
    FlagstaffAgent,
    # ... etc
)
```

The base class is imported separately:

```python
from agent.agents.location_agent_base import LocationAgentBase
```

## Registry System

All location agents are registered in:
- `src/agent/arizona_registry.py` - Tracks active agents and planned locations
- `src/agent/graph.py` - Registers agents and creates graph nodes

## Next Locations to Add

High Priority:
- Phoenix
- Tucson

Medium Priority:
- Bisbee
- Page
- Cottonwood

