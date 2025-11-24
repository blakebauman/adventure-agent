# Arizona Adventure Agentic Workflow

An intelligent adventure planning system built with LangChain, LangGraph, and LangSmith. **Specializing in Arizona adventures** - from Sedona's red rock trails to Jerome's historic mining town, from Flagstaff's mountain peaks to Tucson's Sonoran Desert.

Built by Arizonans, for Arizonans, and anyone who loves exploring the Grand Canyon State.

## Features

- **Arizona-First Design**: Specializes in Arizona adventures with location-specific agents for cities and towns
- **Text-to-Adventure AI Generation**: Natural language input processing - simply describe your Arizona adventure in plain text and the AI generates a complete plan
- **Multi-Agent Architecture**: 17+ specialized agents plus location-specific agents for Arizona cities/towns
- **Location Agents**: Specialized agents for Jerome, Sedona, Prescott, and more Arizona destinations
- **Orchestrator Agent**: Intelligently routes requests to appropriate specialized agents using LLM analysis, automatically detects Arizona locations
- **Core Planning Agents**:
  - **Geographic Agent**: Location data, coordinates, and geographic information
  - **Trail Agent**: Expert on trails for multiple activity types:
    - Mountain biking ([MTB Project](https://www.mtbproject.com))
    - Hiking ([Hiking Project](https://www.hikingproject.com))
    - Trail running ([Trail Run Project](https://www.trailrunproject.com))
  - **Planning Agent**: Creates detailed day-by-day itineraries and logistics
- **Land Management & Regulations**:
  - **BLM Agent**: Expert on Bureau of Land Management lands, access points, and regulations
  - **Permits Agent**: Permit requirements, regulations, and access restrictions
- **Safety & Conditions**:
  - **Weather Agent**: Real-time weather forecasts, trail conditions, and seasonal information
  - **Safety Agent**: Safety information, emergency contacts, and risk assessment
- **Logistics & Services**:
  - **Accommodation Agent**: Finds hotels, campgrounds, and lodging options
  - **Transportation Agent**: Parking, shuttles, public transit, and transportation logistics
  - **Food Agent**: Food options, resupply points, water sources, and local recommendations
- **Community & Culture**:
  - **Community Agent**: Local clubs, events, and community resources
  - **Historical Agent**: Historical sites, cultural significance, and local history
- **Enhancement Agents**:
  - **Gear Agent**: Recommends gear and products with affiliate links (revenue model)
  - **Photography Agent**: Best photo spots, scenic viewpoints, and media resources
- **Human-in-the-Loop**: Checkpoints for review and approval
- **API Access**: RESTful API exposed via LangGraph CLI (development) or LangSmith (production)

## Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

## Setup

1. **Create a virtual environment:**
   ```bash
   uv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Install the LangGraph CLI:**
   ```bash
   uv pip install -U "langgraph-cli[inmem]"
   ```

4. **Install project dependencies:**
   ```bash
   uv pip install -e .
   ```

## Development

### Quick Start with Run Script

Use the provided `run.sh` script for common tasks:

```bash
# Run development server
./run.sh dev

# Run development server with custom port
./run.sh dev --port 8000

# Run tests
./run.sh test

# Run linting
./run.sh lint

# Run type checking
./run.sh typecheck

# Install/update dependencies
./run.sh install

# Build Docker image
./run.sh build

# Clean build artifacts
./run.sh clean
```

### Running the Development Server

Start the LangGraph API server in development mode with hot reloading:

```bash
langgraph dev
```

Or use the run script:

```bash
./run.sh dev
```

This will:
- Start the API server on `http://localhost:2024` (default port)
- Enable hot reloading when code changes are detected
- Expose REST API endpoints for threads, runs, and assistants
- Provide OpenAPI documentation at `/docs`
- Connect to LangGraph Studio for visualization and debugging

### Available Commands

- `langgraph dev` - Run the development server
- `langgraph build` - Build a Docker image for the LangGraph API server
- `langgraph up` - Launch the LangGraph API server
- `langgraph dockerfile` - Generate a Dockerfile

### Project Structure

```
adventure-agent/
├── langgraph.json          # LangGraph configuration
├── pyproject.toml          # Project dependencies and configuration
├── main.py                 # Main entry point
├── run.sh                  # Development script
├── src/
│   └── agent/
│       ├── __init__.py
│       ├── graph.py        # Main agent graph definition
│       ├── state.py        # State schema for adventure planning
│       ├── tools.py        # Tools for all agents
│       ├── config.py       # Configuration management
│       └── agents/         # Agent modules
│           ├── __init__.py
│           ├── orchestrator.py         # Main orchestrator agent
│           ├── geo_agent.py            # Geographic information specialist
│           ├── trail_agent.py          # Trail specialist (MTB, Hiking, Trail Running)
│           ├── blm_agent.py            # BLM land specialist
│           ├── permits_agent.py        # Permits and regulations specialist
│           ├── weather_agent.py        # Weather and conditions specialist
│           ├── safety_agent.py         # Safety and emergency specialist
│           ├── accommodation_agent.py   # Accommodation specialist
│           ├── transportation_agent.py # Transportation and logistics specialist
│           ├── food_agent.py           # Food and resupply specialist
│           ├── gear_agent.py           # Gear recommendation specialist
│           ├── planning_agent.py       # Planning and itinerary specialist
│           ├── community_agent.py      # Community and social specialist
│           ├── photography_agent.py   # Photography and media specialist
│           ├── historical_agent.py     # Historical and cultural specialist
│           ├── route_planning_agent.py # Route planning specialist (RideWithGPS, Strava)
│           ├── bikepacking_agent.py   # Bikepacking route specialist
│           └── advocacy_agent.py      # Trail advocacy and long-distance routes specialist
└── tests/
    ├── conftest.py
    ├── integration_tests/  # Integration tests
    └── unit_tests/         # Unit tests
```

## Configuration

The agent is configured in `langgraph.json`. The main graph is defined in `src/agent/graph.py` and exported as `graph`.

### Environment Variables

Create a `.env` file in the project root for environment-specific configuration:

```bash
# Copy the template file
cp env.template .env

# Then edit .env with your actual API keys
```

**Quick Start - Minimum Required:**
```bash
# At minimum, you need at least one LLM provider API key
OPENAI_API_KEY=your_openai_api_key_here

# Required if using Anthropic models (Claude)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Full Configuration:**
See [`env.template`](env.template) for a complete list of all available environment variables, including:

- **LLM Configuration**: OpenAI and Anthropic API keys, default models, temperature
- **Per-Agent Model Assignments**: Override models for specific agents (e.g., `AGENT_MODEL_ORCHESTRATOR=claude-sonnet-3.5`)
- **LangSmith**: Observability and tracing configuration
- **External APIs**: Tavily, OpenCage, OpenWeather, Google Places, Recreation.gov
- **System Configuration**: Checkpointing, caching, rate limiting, archiving

**Per-Agent Model Configuration:**
The system supports assigning specific LLM models to each agent for cost optimization and performance tuning. By default:
- **High-complexity agents** (orchestrator, planning, synthesis): Use `claude-sonnet-3.5`
- **Medium-complexity agents** (trail, route planning, location agents): Use `claude-haiku-3`
- **Low-complexity agents** (geo, weather, accommodation, etc.): Use `claude-haiku-3`

Override defaults via environment variables:
```bash
AGENT_MODEL_ORCHESTRATOR=claude-sonnet-3.5
AGENT_MODEL_TRAIL=claude-haiku-3
AGENT_MODEL_GEO=gpt-4o-mini
```

See [`docs/PER_AGENT_MODEL_ASSIGNMENT.md`](docs/PER_AGENT_MODEL_ASSIGNMENT.md) for detailed model assignment strategy.

## Supported Activity Types

The adventure agent supports multiple outdoor activity types:

- **Mountain Biking** (`mountain_biking`) - Uses [MTB Project](https://www.mtbproject.com) for trail data
- **Hiking** (`hiking`) - Uses [Hiking Project](https://www.hikingproject.com) for trail data
- **Trail Running** (`trail_running`) - Uses [Trail Run Project](https://www.trailrunproject.com) for trail data
- **Bikepacking** (`bikepacking`) - Multi-day bike adventures

> **Note**: We're starting with the current trail data sources listed above and will be adding more data sources in the near future.

Specify the activity type in your user preferences:

```python
"user_preferences": {
    "activity_type": "hiking",  # or "mountain_biking", "trail_running", "bikepacking"
    "skill_level": "intermediate",
    "region": "Colorado"
}
```

## Architecture

### Agent System

The adventure agent uses a multi-agent architecture with 17 specialized agents (plus orchestrator) organized by function:

#### Core Planning Agents

1. **Orchestrator Agent**: Analyzes user requests and determines which specialized agents to call, manages workflow
2. **Geo Agent**: Provides geographic information, coordinates, location data, and regional context
3. **Trail Agent**: Specializes in trail data for multiple activity types:
   - Mountain biking from [MTB Project](https://www.mtbproject.com)
   - Hiking from [Hiking Project](https://www.hikingproject.com)
   - Trail running from [Trail Run Project](https://www.trailrunproject.com)
4. **Route Planning Agent**: Expert on route planning tools:
   - [RideWithGPS](https://ridewithgps.com) - Route planning, navigation, large route library
   - [Strava](https://www.strava.com) - Popular routes, segments, community-driven data
5. **Bikepacking Agent**: Expert on bikepacking routes:
   - [Bikepacking.com](https://bikepacking.com) - Curated bikepacking routes worldwide
   - [Bikepacking Roots](https://bikepackingroots.org) - Conservation-focused route development
6. **Planning Agent**: Creates detailed day-by-day itineraries, logistics, and trip planning

#### Land Management & Regulations

7. **BLM Agent**: Expert on Bureau of Land Management lands, access points, and regulations
8. **Advocacy Agent**: Expert on trail advocacy and long-distance routes:
   - [IMBA](https://www.imba.com) - Trail networks, access, advocacy
   - [Adventure Cycling Association](https://www.adventurecycling.org) - Long-distance cycling routes
9. **Permits Agent**: Permit requirements, regulations, access restrictions, and application processes

#### Safety & Conditions

10. **Weather Agent**: Real-time weather forecasts, trail conditions, seasonal information, and safety considerations
11. **Safety Agent**: Safety information, emergency contacts, risk assessment, and wildlife alerts

#### Logistics & Services

12. **Accommodation Agent**: Finds hotels, campgrounds, hostels, and lodging options
13. **Transportation Agent**: Parking information, shuttle services, public transit, and bike transport
14. **Food Agent**: Food options, resupply points, water sources, and local restaurant recommendations

#### Community & Culture

15. **Community Agent**: Local clubs, events, group rides, and community resources
16. **Historical Agent**: Historical sites, cultural significance, and local history

#### Enhancement Agents

17. **Gear Agent**: Recommends gear and products with affiliate links (revenue model)
18. **Photography Agent**: Best photo spots, scenic viewpoints, sunrise/sunset locations, and media resources

### Workflow

The agent workflow follows a priority-based routing system with AI-powered natural language understanding:

1. **User Request**: User submits natural language text describing their adventure (text-to-adventure) or structured preferences
2. **AI Analysis**: Orchestrator uses LLM to analyze the text, extract intent, activity type, location, duration, and preferences
3. **Orchestration**: Orchestrator determines which specialized agents are needed based on the analyzed request
4. **Agent Execution** (in priority order):
   - Geographic information (geo_agent)
   - Weather and conditions (weather_agent)
   - Permits and regulations (permits_agent)
   - Safety information (safety_agent)
   - Trail data (trail_agent)
   - Route planning (route_planning_agent)
   - Bikepacking routes (bikepacking_agent)
   - Land management (blm_agent)
   - Trail advocacy (advocacy_agent)
   - Transportation (transportation_agent)
   - Accommodations (accommodation_agent)
   - Food and resupply (food_agent)
   - Gear recommendations (gear_agent)
   - Community resources (community_agent)
   - Itinerary planning (planning_agent)
   - Photography spots (photography_agent)
   - Historical context (historical_agent)
5. **Information Gathering**: Each agent gathers information using tools, web search, and LLM analysis
6. **Synthesis**: Planning agent and orchestrator synthesize all information into a comprehensive itinerary
7. **Human Review**: Checkpoint for human review (if needed based on complexity, cost, or errors)
8. **Final Plan**: Complete adventure plan is returned with all relevant information

### Human-in-the-Loop

The system includes checkpoints for human review when:
- Complex multi-day adventures (>7 days)
- High-cost recommendations
- Errors occur during processing
- User preferences are unclear

## API Usage

Once the server is running, you can interact with the agent via the LangGraph API. The system supports **text-to-adventure generation** - you can provide natural language descriptions and the AI will understand and generate a complete adventure plan.

> **📚 For complete API documentation, see [docs/API_DEPLOYMENT.md](docs/API_DEPLOYMENT.md)**

### Using the Python Client (Recommended)

The easiest way to interact with the API is using the provided Python client:

```python
from agent.api_client import AdventureAgentClient

# Initialize client
client = AdventureAgentClient(base_url="http://localhost:2024")

# Create a thread
thread_id = client.create_thread(user_id="user123", session_id="session456")

# Create an adventure plan from natural language
run = client.create_adventure_plan(
    thread_id,
    "I want to plan a 3-day mountain bike trip in Colorado for intermediate riders. I prefer camping and want to explore some challenging trails with great views."
)

# Wait for completion
state = client.wait_for_completion(thread_id, run["run_id"])
adventure_plan = state["adventure_plan"]
print(f"Plan: {adventure_plan['title']}")
```

### Simple One-Line Usage

For quick testing, use the convenience function:

```python
from agent.api_client import create_adventure_plan_simple

plan = create_adventure_plan_simple(
    "Plan a 3-day mountain bike trip in Colorado"
)
print(plan["adventure_plan"]["title"])
```

### Direct REST API Usage

You can also use the REST API directly with `requests` or any HTTP client:

```python
import requests

# Start a new thread
response = requests.post(
    "http://localhost:2024/threads",
    json={"config": {"configurable": {"user_id": "user123", "session_id": "session456"}}}
)
thread_id = response.json()["thread_id"]

# Submit a natural language adventure request
response = requests.post(
    f"http://localhost:2024/threads/{thread_id}/runs",
    json={
        "assistant_id": "agent",
        "input": {
            "user_input": "I want to plan a 3-day mountain bike trip in Colorado for intermediate riders. I prefer camping and want to explore some challenging trails with great views."
        }
    }
)

# Get the result
run_id = response.json()["run_id"]
result = requests.get(f"http://localhost:2024/threads/{thread_id}/runs/{run_id}/state")
adventure_plan = result.json()["values"]["adventure_plan"]
```

### Example with Structured Preferences (Optional)

You can also provide structured preferences alongside or instead of natural language:

```python
from agent.api_client import AdventureAgentClient

client = AdventureAgentClient()
thread_id = client.create_thread()

run = client.create_adventure_plan(
    thread_id,
    "Plan a 3-day mountain bike adventure in Colorado",
    user_preferences={
        "skill_level": "intermediate",
        "activity_type": "mountain_biking",
        "duration_days": 3,
        "region": "Colorado",
        "accommodation_preference": "camping"
    }
)

state = client.wait_for_completion(thread_id, run["run_id"])
adventure_plan = state["adventure_plan"]
```

### How Text-to-Adventure Works

1. **Natural Language Processing**: The orchestrator agent uses an LLM with structured output to analyze your text input
2. **Structured Intent Extraction**: Uses Pydantic models for type-safe extraction of:
   - Activity type (mountain biking, hiking, trail running, bikepacking)
   - Location/region (automatically extracted from text)
   - Duration in days (if mentioned)
   - Skill level (beginner, intermediate, advanced, expert)
   - Required specialized agents
   - Context for each agent
   - Priority order for agent execution
3. **Automatic Preference Population**: Extracted information is automatically added to user preferences, so you don't need to provide structured data
4. **Agent Routing**: Determines which specialized agents are needed based on the analyzed request
5. **Plan Generation**: Coordinates all agents to gather information and synthesize a complete adventure plan

**Technical Implementation**: The system uses LangChain's `with_structured_output()` feature with Pydantic models to ensure reliable, validated extraction of information from natural language. This eliminates the need for manual JSON parsing and provides type safety.

### Example with cURL

```bash
# Create a thread
curl -X POST http://127.0.0.1:8123/threads \
  -H "Content-Type: application/json" \
  -d '{"config": {"configurable": {"user_id": "user123"}}}'

# Submit a natural language request (text-to-adventure)
curl -X POST http://127.0.0.1:8123/threads/{thread_id}/runs \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent",
    "input": {
      "user_input": "I need a challenging 5-day hiking adventure in Arizona near Sedona. I want scenic trails with good camping options and prefer advanced difficulty."
    }
  }'

# Or with structured preferences
curl -X POST http://127.0.0.1:8123/threads/{thread_id}/runs \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent",
    "input": {
      "user_input": "Find hiking trails near Sedona, Arizona",
      "user_preferences": {
        "skill_level": "advanced",
        "activity_type": "hiking",
        "region": "Arizona"
      }
    }
  }'
```

## Testing

Run tests using the run script:

```bash
# Run all tests
./run.sh test

# Run specific test files (pass arguments to pytest)
./run.sh test tests/unit_tests/
./run.sh test tests/integration_tests/
```

Or manually:

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run all tests
pytest

# Run specific test files
pytest tests/unit_tests/
pytest tests/integration_tests/
```

## Code Quality

This project uses:
- **Ruff** for linting and formatting
- **MyPy** for type checking

Run using the run script:

```bash
# Run linting
./run.sh lint

# Run type checking
./run.sh typecheck
```

Or manually:

```bash
# Run linting
ruff check .

# Run type checking
mypy src/
```

## Building for Production

Build a Docker image:

```bash
langgraph build
```

Or use the run script:

```bash
./run.sh build
```

### Production Considerations

For production deployment, consider:

1. **Persistent Checkpointer**: Replace `MemorySaver` with `PostgresSaver` or `SqliteSaver` for state persistence
2. **Environment Variables**: Ensure all required API keys are set in your production environment
3. **Rate Limiting**: Implement rate limiting for external API calls
4. **Error Handling**: Monitor and handle errors gracefully
5. **Logging**: Configure comprehensive logging and monitoring via LangSmith

> **📚 For complete deployment instructions, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)**

See `docs/BEST_PRACTICES.md` for detailed best practices and compliance information.

## API Integrations

The adventure agent uses real API integrations with fallbacks:

### Geocoding
- **Primary**: OpenCage Geocoding API (if `OPENCAGE_API_KEY` is set)
- **Fallback**: Nominatim (OpenStreetMap) - free, no key required
- **Used by**: `get_coordinates` tool

### Weather
- **Primary**: OpenWeatherMap API (if `OPENWEATHER_API_KEY` is set)
- **Fallback**: Weather.gov API (free, no key, US locations only)
- **Used by**: `get_weather_forecast` tool

### Trail Data
- **Primary**: OpenStreetMap Overpass API (free, no key required)
- **Fallback**: Placeholder data
- **Used by**: `search_trails` tool
- **Note**: Adventure Projects (MTB Project, Hiking Project, Trail Run Project) don't have public APIs, so we use OpenStreetMap data

### Distance Calculation
- **Implementation**: Haversine formula (great-circle distance)
- **Used by**: `calculate_distance` tool

### BLM Land Data
- **Primary**: Recreation.gov API (free, no key required)
- **Fallback**: Web search via Tavily (if API key available)
- **Used by**: `search_blm_lands` tool
- **Note**: Searches for Bureau of Land Management recreation areas

### Accommodations
- **Campgrounds**: Recreation.gov API (free, no key required)
- **Hotels/Lodging**: Google Places API (if `GOOGLE_PLACES_API_KEY` is set)
- **Fallback**: Placeholder data
- **Used by**: `search_accommodations` tool

All tools include error handling and fallback to placeholder data if APIs fail, ensuring the system continues to function even when external services are unavailable.

## Additional Documentation

- **docs/AGENT_RECOMMENDATIONS.md**: Agent implementation status and available resources
- **docs/BEST_PRACTICES.md**: LangChain/LangGraph best practices compliance
- **docs/TRAIL_DATA_SOURCES.md**: Detailed information on trail data sources and integration methods

## Contributing

This project follows LangChain/LangGraph best practices. When contributing:

1. Follow the existing code structure and patterns
2. Add tests for new features
3. Run linting and type checking before submitting
4. Update documentation as needed

## License

MIT

