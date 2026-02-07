# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Adventure Agent is an intelligent adventure planning system built with LangChain, LangGraph, and LangSmith. It uses a hub-and-spoke multi-agent architecture with 17+ specialized agents plus an orchestrator to plan mountain bike adventures, bikepacking trips, hiking, and trail running. Specializes in Arizona adventures with 28+ location-specific agents.

## Development Commands

### Setup & Dependencies
```bash
uv venv && source .venv/bin/activate
uv pip install -e .                    # Install project
./run.sh install                       # Install all deps including LangGraph CLI
```

### Development Server
```bash
./run.sh dev                           # Default port 8123
./run.sh dev --port 8000               # Custom port
./run.sh dev-tunnel                    # With public Cloudflare tunnel
langgraph dev                          # Direct LangGraph API server
```

### Testing
```bash
./run.sh test                          # All tests
./run.sh test tests/unit_tests/        # Unit tests only
./run.sh test tests/integration_tests/ # Integration tests only
pytest tests/unit_tests/test_file.py   # Single test file
pytest tests/unit_tests/test_file.py::test_name  # Single test
```

### Code Quality (ALWAYS run before committing)
```bash
./run.sh lint                          # Ruff linting
./run.sh typecheck                     # MyPy type checking
ruff format .                          # Auto-format code
```

### Build & Deploy
```bash
./run.sh build                         # Build Docker image
./run.sh clean                         # Clean build artifacts
```

**Package management**: Always use `uv pip install`, never use pip directly.

## Architecture Overview

### Hub-and-Spoke Multi-Agent System
The orchestrator (`src/agent/agents/orchestrator.py`) manages specialized agents:

- **Core Planning**: Geo, Trail, Route Planning, Bikepacking, Planning
- **Land Management**: BLM, Advocacy, Permits
- **Safety & Conditions**: Weather, Safety
- **Logistics**: Accommodation, Transportation, Food
- **Enhancement**: Gear, Photography, Community, Historical
- **Arizona Locations**: 28+ agents (Jerome, Sedona, Prescott, Flagstaff, Phoenix, Tucson, etc.)

### Key Files

| Component | File | Description |
|-----------|------|-------------|
| State | `src/agent/state.py` | `AdventureState`, `UserPreferences`, `AdventurePlan` TypedDicts |
| Graph | `src/agent/graph.py` | StateGraph with conditional routing, parallel execution, entry point is `graph` |
| Config | `src/agent/config.py` | Environment config, model settings, checkpointer |
| Tools | `src/agent/tools.py` | 60+ tools for external integrations |
| Utils | `src/agent/utils.py` | Helper functions for state extraction and agent node creation |
| Cache | `src/agent/cache.py` | API caching and rate limiting utilities |
| Agents | `src/agent/agents/` | All agent implementations |

### Agent Execution Flow
1. Orchestrator analyzes input using structured output → determines required agents
2. **Parallel execution** of independent agents (dependencies tracked via `AGENT_DEPENDENCIES`)
3. Priority order when sequential: geo → weather → permits → safety → trail → route_planning → bikepacking → blm → advocacy → transportation → accommodation → food → gear → community → planning → photography → historical
4. Early synthesis when core agents (geo, trail, weather) complete
5. Human review checkpoint (if complex/expensive)
6. Archive and return final `AdventurePlan`

### Agent Node Pattern
All agent nodes follow this structure:
```python
async def agent_name_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    try:
        context = state.get("agent_context", {}).get("agent_name", state.get("user_input", ""))
        result = await agent.method(...)
        return {
            "agent_output": result,
            "completed_agents": ["agent_name"],  # List with single item - merged via operator.add
        }
    except Exception as e:
        # Use handle_agent_error for categorized error handling
        error_result = handle_agent_error(e, "agent_name", state, fallback_value)
        if isinstance(error_result, Command):
            return error_result  # Routes to orchestrator for LLM-recoverable errors
        error_result["agent_output"] = fallback_value
        return error_result
```

### Utility Functions (`src/agent/utils.py`)
Use these helpers to reduce boilerplate and ensure consistency:

```python
from agent.utils import (
    extract_activity_type,  # Get activity with backward compatibility
    extract_location,       # Get location with cascading fallbacks
    extract_context,        # Get agent-specific context
    extract_route_info,     # Get trail info for dependent agents
    create_agent_node,      # Factory for standardized agent nodes
    invoke_tool_async,      # Async wrapper for sync tools
)

# extract_activity_type - handles deprecated adventure_type field
activity = extract_activity_type(state.get("user_preferences"))  # Returns "mountain_biking" etc.

# extract_location - cascading fallbacks: geo_info → user_preferences → user_input
location = extract_location(state, default="Arizona")

# extract_context - agent-specific context with user_input fallback
context = extract_context(state, "trail_agent")

# extract_route_info - get trail info for safety, food, photography agents
route_info = extract_route_info(state)  # Returns {"trails": [...]}

# create_agent_node - factory for consistent agent nodes with error handling
async def invoke_blm(state, context):
    location = extract_location(state)
    activity = extract_activity_type(state.get("user_preferences"))
    return await blm_agent.get_blm_information(location, activity, context)

blm_agent_node = create_agent_node(
    agent_name="blm_agent",
    output_field="blm_info",
    invoke_fn=invoke_blm,
    fallback_value=[],
)
```

### API Caching (`src/agent/cache.py`)
Use `cached_api_call()` for all external API requests:
```python
from agent.cache import cached_api_call

def _fetch_data() -> dict:
    with httpx.Client() as client:
        response = client.get(url, params=params, timeout=10.0)
        return response.json() if response.status_code == 200 else {}

result = cached_api_call(
    endpoint="api_name",           # Rate limiter key
    params={"lat": lat, "lon": lon},  # Cache key params
    api_func=_fetch_data,          # Function to call on cache miss
    ttl=3600.0,                    # Cache TTL in seconds
)
```

Cache TTL guidelines:
- **30 min - 1 hr**: Time-sensitive data (weather alerts, fire data)
- **2-6 hours**: Frequently changing (weather forecasts, restaurant availability)
- **12-24 hours**: Stable data (locations, trails, permits, regulations)

### State Management
```python
# State uses Annotated types with reducers for parallel execution
completed_agents: Annotated[List[str], operator.add]  # Merges lists from parallel nodes
error_details: Annotated[List[Dict[str, Any]], operator.add]  # Merges error lists

# IMPORTANT: With reducers, only return NEW items - reducer handles merging
# CORRECT:
return {"error_details": [new_error], "completed_agents": ["agent_name"]}
# WRONG (causes duplicates in parallel execution):
return {"error_details": state.get("error_details", []) + [new_error]}

# Safe access patterns
location = state.get("geo_info", {}).get("location", "") if state.get("geo_info") else ""

# Activity type with backward compatibility
activity = state.get("user_preferences", {}).get("activity_type") or \
           state.get("user_preferences", {}).get("adventure_type", "mountain_biking")
```

### Structured Output with Pydantic
Use `with_structured_output()` for type-safe LLM responses:
```python
from pydantic import BaseModel, Field

class AnalysisModel(BaseModel):
    activity_type: str = Field(description="Type of activity")
    required_agents: List[str] = Field(description="Required agents")

llm_structured = llm.with_structured_output(AnalysisModel)
result = await llm_structured.ainvoke(messages)  # Returns AnalysisModel instance
```

### Location Agent Pattern
Location agents extend `LocationAgentBase` and use structured output for consistent responses:

```python
# Location agents use Pydantic schemas (see location_response_schemas.py)
from agent.agents.location_response_schemas import (
    LocationGuideResponse,  # Main response schema
    LocationOverview,       # Coordinates, elevation, region, proximity
    OutdoorActivity,        # Activity type, trails, difficulty, seasons
    Attraction,             # Name, type, description, highlights
    Business,               # Restaurants, accommodations, shops
    PracticalInfo,          # Parking, permits, weather, access
)

# LocationAgentBase uses structured output internally:
self.structured_llm = self.llm.with_structured_output(
    LocationGuideResponse, method="function_calling"
)

# Response is normalized and validated automatically via field_validators
```

Location agent registration and lookup:
```python
location_agent_node = create_location_agent_node("agent_name", agent_instance)
register_location_agent(agent_instance)  # Register for dynamic lookup

# Find agent for a location
agent = find_location_agent_for_location("Sedona, Arizona")  # Returns sedona_agent
```

### Activity Types & Skill Mapping
- **Types**: `mountain_biking`, `hiking`, `trail_running`, `bikepacking`
- **Skill levels**: beginner, intermediate, advanced, expert
- **Difficulty mapping**:
  - MTB: beginner→green, intermediate→blue, advanced→black, expert→double_black
  - Hiking: beginner→easy, intermediate→intermediate, advanced→difficult, expert→expert

## Configuration

### Required Environment Variables
```bash
OPENAI_API_KEY=your_key_here
# Or use Anthropic
ANTHROPIC_API_KEY=your_key_here
```

### Optional Configuration
```bash
LANGSMITH_API_KEY=your_key_here       # Observability
TAVILY_API_KEY=your_key_here          # Web search
CHECKPOINTER_TYPE=memory              # memory/sqlite/postgres/none
OPENAI_MODEL=gpt-4o-mini              # Default model
OPENAI_TEMPERATURE=0.7                # Default temperature
MAX_CONCURRENCY=10                    # Parallel agent execution limit

# Agent Timeouts (seconds)
TIMEOUT_DEFAULT=60.0                  # Default for all agents
TIMEOUT_GEO_AGENT=30.0                # Geo lookups
TIMEOUT_TRAIL_AGENT=45.0              # Trail search + LLM
TIMEOUT_SYNTHESIZE=45.0               # Plan synthesis
```

### Per-Agent Model Configuration
Override models for specific agents (see `docs/PER_AGENT_MODEL_ASSIGNMENT.md`):
```bash
AGENT_MODEL_ORCHESTRATOR=claude-sonnet-3.5  # High-complexity
AGENT_MODEL_TRAIL=claude-haiku-3            # Medium-complexity
AGENT_MODEL_GEO=gpt-4o-mini                 # Low-complexity
```

## Key Patterns

- **Error handling**: Return empty/default values on errors, don't raise exceptions in agents. Use `handle_agent_error()` for categorized handling with Command-based recovery.
- **Retry policies**: 3 retries with exponential backoff for external API calls via `RetryPolicy`
- **Human-in-the-loop**: Use `interrupt()` for review checkpoints on complex plans
- **Parallel execution**: Return agent lists from `route_to_agents()` for concurrent execution
- **Tools**: Return JSON strings, use try/except, return empty results on failure
- **State updates**: Return only changed fields, `completed_agents` uses reducer to merge parallel results
- **Timeouts**: Use `asyncio.wait_for()` with `Config.get_timeout("agent_name")` for configurable timeouts
- **Agent normalization**: Use `normalize_agent_name()` for consistent agent name handling
