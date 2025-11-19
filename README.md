# Adventure Agent

An intelligent adventure planning agent built with LangChain, LangGraph, and LangSmith. This system helps plan mountain bike adventures, bikepacking trips, and outdoor adventures across the United States and Canada.

## Features

- **Text-to-Adventure AI Generation**: Natural language input processing - simply describe your adventure in plain text and the AI generates a complete plan
- **Multi-Agent Architecture**: 14 specialized agents for comprehensive adventure planning
- **Orchestrator Agent**: Intelligently routes requests to appropriate specialized agents using LLM analysis
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
- **API Access**: RESTful API exposed via LangGraph Cloud

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
- Start the API server on `http://127.0.0.1:8123` (default port)
- Enable hot reloading when code changes are detected
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
│           └── historical_agent.py     # Historical and cultural specialist
│           # Note: route_planning_agent.py, bikepacking_agent.py, and advocacy_agent.py
│           # exist but are not currently wired into the graph
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
# OpenAI API Key (required for LLM functionality)
OPENAI_API_KEY=your_openai_api_key_here

# OpenAI Model Configuration (optional)
OPENAI_MODEL=gpt-4o-mini  # Default model
OPENAI_TEMPERATURE=0.7     # Default temperature

# LangSmith Configuration (optional, for observability)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=adventure-agent

# Tavily API Key (optional, for web search)
TAVILY_API_KEY=your_tavily_api_key_here

# Affiliate Partner URLs (for gear recommendations)
AFFILIATE_BASE_URL=https://example.com/affiliate
```

## Supported Activity Types

The adventure agent supports multiple outdoor activity types:

- **Mountain Biking** (`mountain_biking`) - Uses [MTB Project](https://www.mtbproject.com) for trail data
- **Hiking** (`hiking`) - Uses [Hiking Project](https://www.hikingproject.com) for trail data
- **Trail Running** (`trail_running`) - Uses [Trail Run Project](https://www.trailrunproject.com) for trail data
- **Bikepacking** (`bikepacking`) - Multi-day bike adventures

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

The adventure agent uses a multi-agent architecture with 14 specialized agents organized by function:

#### Core Planning Agents

1. **Orchestrator Agent**: Analyzes user requests and determines which specialized agents to call, manages workflow
2. **Geo Agent**: Provides geographic information, coordinates, location data, and regional context
3. **Trail Agent**: Specializes in trail data for multiple activity types:
   - Mountain biking from [MTB Project](https://www.mtbproject.com)
   - Hiking from [Hiking Project](https://www.hikingproject.com)
   - Trail running from [Trail Run Project](https://www.trailrunproject.com)
4. **Planning Agent**: Creates detailed day-by-day itineraries, logistics, and trip planning

#### Land Management & Regulations

7. **BLM Agent**: Expert on Bureau of Land Management lands, access points, and regulations
8. **Permits Agent**: Permit requirements, regulations, access restrictions, and application processes

#### Safety & Conditions

9. **Weather Agent**: Real-time weather forecasts, trail conditions, seasonal information, and safety considerations
10. **Safety Agent**: Safety information, emergency contacts, risk assessment, and wildlife alerts

#### Logistics & Services

11. **Accommodation Agent**: Finds hotels, campgrounds, hostels, and lodging options
12. **Transportation Agent**: Parking information, shuttle services, public transit, and bike transport
13. **Food Agent**: Food options, resupply points, water sources, and local restaurant recommendations

#### Community & Culture

14. **Community Agent**: Local clubs, events, group rides, and community resources
15. **Historical Agent**: Historical sites, cultural significance, and local history

#### Enhancement Agents

16. **Gear Agent**: Recommends gear and products with affiliate links (revenue model)
17. **Photography Agent**: Best photo spots, scenic viewpoints, sunrise/sunset locations, and media resources

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
   - Land management (blm_agent)
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

### Text-to-Adventure Example (Natural Language Only)

The simplest way to use the system is with just natural language text. The orchestrator uses LLM analysis to understand your request:

```python
import requests

# Start a new thread
response = requests.post(
    "http://127.0.0.1:8123/threads",
    json={"config": {"configurable": {"user_id": "user123", "session_id": "session456"}}}
)
thread_id = response.json()["thread_id"]

# Submit a natural language adventure request
# The AI will automatically extract preferences, activity type, location, etc.
response = requests.post(
    f"http://127.0.0.1:8123/threads/{thread_id}/runs",
    json={
        "assistant_id": "agent",
        "input": {
            "user_input": "I want to plan a 3-day mountain bike trip in Colorado for intermediate riders. I prefer camping and want to explore some challenging trails with great views."
        }
    }
)

# Get the result
run_id = response.json()["run_id"]
result = requests.get(f"http://127.0.0.1:8123/threads/{thread_id}/runs/{run_id}/state")
adventure_plan = result.json()["values"]["adventure_plan"]
```

### Example with Structured Preferences (Optional)

You can also provide structured preferences alongside or instead of natural language:

```python
import requests

# Start a new thread
response = requests.post(
    "http://127.0.0.1:8123/threads",
    json={"config": {"configurable": {"user_id": "user123", "session_id": "session456"}}}
)
thread_id = response.json()["thread_id"]

# Submit an adventure planning request with structured preferences
response = requests.post(
    f"http://127.0.0.1:8123/threads/{thread_id}/runs",
    json={
        "assistant_id": "agent",
        "input": {
            "user_input": "Plan a 3-day mountain bike adventure in Colorado",
            "user_preferences": {
                "skill_level": "intermediate",
                "activity_type": "mountain_biking",
                "duration_days": 3,
                "region": "Colorado",
                "accommodation_preference": "camping"
            }
        }
    }
)

# Get the result
run_id = response.json()["run_id"]
result = requests.get(f"http://127.0.0.1:8123/threads/{thread_id}/runs/{run_id}/state")
adventure_plan = result.json()["values"]["adventure_plan"]
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

See `docs/BEST_PRACTICES.md` for detailed best practices and compliance information.

## Additional Documentation

- **docs/AGENT_RECOMMENDATIONS.md**: Agent implementation status and available resources
- **docs/BEST_PRACTICES.md**: LangChain/LangGraph best practices compliance

## Contributing

This project follows LangChain/LangGraph best practices. When contributing:

1. Follow the existing code structure and patterns
2. Add tests for new features
3. Run linting and type checking before submitting
4. Update documentation as needed

## License

MIT

