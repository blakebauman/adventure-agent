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

### State Management
```python
# State uses Annotated types with reducers for parallel execution
completed_agents: Annotated[List[str], operator.add]  # Merges lists from parallel nodes
error_details: Annotated[List[Dict[str, Any]], operator.add]

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
Location agents extend `LocationAgentBase` and are created via factory:
```python
location_agent_node = create_location_agent_node("agent_name", agent_instance)
register_location_agent(agent_instance)  # Register for dynamic lookup
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
