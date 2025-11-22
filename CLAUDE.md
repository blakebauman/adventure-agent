# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Adventure Agent is an intelligent adventure planning system built with LangChain, LangGraph, and LangSmith. It uses a multi-agent architecture with 17 specialized agents plus orchestrator to plan mountain bike adventures, bikepacking trips, and outdoor adventures across the US and Canada.

## Development Commands

### Setup & Dependencies
- `uv venv` - Create virtual environment
- `source .venv/bin/activate` - Activate virtual environment  
- `uv pip install -e .` - Install project dependencies
- `./run.sh install` - Install/update all dependencies including LangGraph CLI

### Development Server
- `./run.sh dev` - Run LangGraph development server (default port 8123)
- `./run.sh dev --port 8000` - Run with custom port
- `./run.sh dev-tunnel` - Run with public tunnel (Cloudflare)
- `langgraph dev` - Direct command (equivalent to ./run.sh dev)

### Testing
- `./run.sh test` - Run all tests
- `./run.sh test tests/unit_tests/` - Run unit tests only
- `./run.sh test tests/integration_tests/` - Run integration tests only
- `pytest` - Direct pytest command (after installing dev dependencies)

### Code Quality
- `./run.sh lint` - Run ruff linting
- `./run.sh typecheck` - Run MyPy type checking
- `ruff check .` - Direct ruff command
- `mypy src/` - Direct MyPy command

### Important Development Notes
- **ALWAYS run lint and typecheck after making changes** - Use `./run.sh lint` and `./run.sh typecheck` before committing
- **Use uv for package management** - Never use pip directly, always use `uv pip install`
- **Environment variables** - See Environment Setup section for required API keys

### Build & Deploy
- `./run.sh build` - Build Docker image via LangGraph
- `./run.sh clean` - Clean build artifacts
- `langgraph build` - Direct build command

## Architecture Overview

### Multi-Agent System
The system uses a **hub-and-spoke architecture** with an Orchestrator agent managing 17 specialized agents:

1. **Orchestrator Agent** (`src/agent/agents/orchestrator.py`) - Routes requests using LLM analysis and structured output (Pydantic models) for text-to-adventure generation
2. **Core Planning**: Geo, Trail, Route Planning, Bikepacking, Planning agents
3. **Land Management**: BLM, Advocacy, Permits agents  
4. **Safety & Conditions**: Weather, Safety agents
5. **Logistics**: Accommodation, Transportation, Food agents
6. **Enhancement**: Gear, Photography, Community, Historical agents

### Key Components

**State Management** (`src/agent/state.py`):
- `AdventureState` - Main graph state with typed dictionaries
- `UserPreferences` - User input preferences  
- `AdventurePlan` - Final structured output
- Additional fields: `route_planning_info`, `bikepacking_info`, `advocacy_info` for new agents

**Graph Definition** (`src/agent/graph.py`):
- StateGraph with conditional routing based on required agents
- Priority-based agent execution order
- Human-in-the-loop checkpoints for complex plans
- Retry policies for external API calls

**Configuration** (`src/agent/config.py`):
- Environment-based configuration with .env support
- Checkpointer configuration (memory/sqlite/postgres/none)
- OpenAI, LangSmith, Tavily API settings
- Default model: `gpt-4o-mini` (configurable via OPENAI_MODEL)
- Temperature: 0.7 (configurable via OPENAI_TEMPERATURE)

**Tools** (`src/agent/tools.py`):
- 60+ tools for external integrations
- Trail data from MTB Project, Hiking Project, Trail Run Project
- Route planning from RideWithGPS, Strava
- Bikepacking routes from Bikepacking.com, Bikepacking Roots
- IMBA trail networks, Adventure Cycling Association routes
- BLM lands, accommodations, weather, safety, gear recommendations

### Text-to-Adventure Feature
The system supports **natural language input processing**:
- Users describe adventures in plain text
- Orchestrator uses LLM + structured output to extract intent, activity type, location, duration, skill level
- Automatically populates UserPreferences from extracted data
- No need for structured JSON input - just describe your adventure

### Agent Execution Flow
1. Orchestrator analyzes user input and determines required agents
2. Agents execute in priority order: geo → weather → permits → safety → trail → route_planning → bikepacking → blm → advocacy → transportation → accommodation → food → gear → community → planning → photography → historical
3. Planning agent synthesizes all information into comprehensive itinerary
4. Human review checkpoint (if needed for complex/expensive plans)
5. Final adventure plan returned

### Specialized Agent Capabilities
- **Route Planning Agent**: RideWithGPS routes, Strava community routes and segments
- **Bikepacking Agent**: Multi-day bikepacking routes from Bikepacking.com and Bikepacking Roots
- **Advocacy Agent**: IMBA trail networks, Adventure Cycling Association long-distance routes, trail access information

### Testing Strategy
- **Unit tests** (`tests/unit_tests/`) - Individual agent and component testing
- **Integration tests** (`tests/integration_tests/`) - Full graph execution testing
- Use pytest with fixtures for agent testing (`tests/conftest.py` configures asyncio backend)
- Mock external APIs for consistent testing
- Dev dependencies include pytest 8.3.5+ with anyio backend support

### Key Dependencies
- **LangGraph** - Multi-agent orchestration and state management
- **LangChain** - LLM integrations and tools
- **Pydantic** - Type-safe structured output from LLMs
- **OpenAI** - Default LLM provider (gpt-4o-mini)
- **Tavily** - Web search capabilities (optional)

## Environment Setup

Required environment variables:
```bash
OPENAI_API_KEY=your_key_here

# Optional
LANGSMITH_API_KEY=your_key_here  # For observability
TAVILY_API_KEY=your_key_here     # For web search
CHECKPOINTER_TYPE=memory         # memory/sqlite/postgres/none
```

## Important Notes

- Main graph entry point: `src/agent/graph.py:graph`
- Default model: `gpt-4o-mini` (configurable via OPENAI_MODEL)
- Use uv for package management (not pip) - **Never use pip directly**
- LangGraph API handles checkpointing automatically when deployed
- Human-in-the-loop interrupts for plan review/approval
- Graph uses priority-based agent execution with conditional routing
- Retry policies implemented for external API calls (3 retries with exponential backoff)
- All agent nodes have error handling and graceful fallbacks