# Testing Readiness Checklist

## ✅ Pre-Testing Checklist

### Critical Issues (Must Fix Before Testing)
- [x] **Graph Compilation** - Graph structure is correct
- [x] **All Agents Imported** - All 17 agents + orchestrator are properly imported
- [x] **State Schema** - AdventureState properly defined
- [x] **Node Functions** - All node functions have error handling
- [x] **Routing Logic** - Conditional edges properly configured

### Configuration
- [ ] **Environment Variables** - `.env` file configured with:
  - [ ] `OPENAI_API_KEY` (required)
  - [ ] `OPENAI_MODEL` (optional, defaults to gpt-4o-mini)
  - [ ] `TAVILY_API_KEY` (optional, for web search)
  - [ ] `LANGCHAIN_API_KEY` (optional, for LangSmith tracing)
  - [ ] `CHECKPOINTER_TYPE` (optional, defaults to "none" for LangGraph API)
  - [ ] `CHECKPOINTER_DB_URL` (required if using sqlite/postgres)

### Dependencies
- [ ] **Python Version** - Python 3.13+ installed
- [ ] **uv Installed** - Package manager installed
- [ ] **Virtual Environment** - Created and activated
- [ ] **Dependencies Installed** - `uv pip install -e .`
- [ ] **LangGraph CLI** - `uv pip install -U "langgraph-cli[inmem]"`

### Code Quality
- [x] **Error Handling** - All nodes have try/except blocks
- [x] **Type Hints** - Proper type annotations
- [x] **Docstrings** - Functions documented
- [ ] **Linting** - Run `./run.sh lint` (warnings about optional imports are OK)
- [ ] **Type Checking** - Run `./run.sh typecheck`

## 🧪 Testing Plan

### 1. Basic Graph Compilation Test

**Goal**: Verify the graph compiles without errors

```bash
# Start the dev server - this will compile the graph
./run.sh dev
```

**Expected**: Server starts on port 8123 (or specified port)

**If it fails**: Check for syntax errors, import errors, or missing dependencies

### 2. Simple Request Test

**Goal**: Test a basic adventure planning request

```python
import requests

# Start a new thread
response = requests.post(
    "http://127.0.0.1:8123/threads",
    json={"config": {"configurable": {"user_id": "test_user", "session_id": "test_session"}}}
)
thread_id = response.json()["thread_id"]

# Submit a simple request
response = requests.post(
    f"http://127.0.0.1:8123/threads/{thread_id}/runs",
    json={
        "assistant_id": "agent",
        "input": {
            "user_input": "I want to go mountain biking in Colorado for 3 days",
            "user_preferences": {
                "activity_type": "mountain_biking",
                "region": "Colorado",
                "duration_days": 3,
                "skill_level": "intermediate"
            }
        }
    }
)
run_id = response.json()["run_id"]

# Check status
response = requests.get(f"http://127.0.0.1:8123/threads/{thread_id}/runs/{run_id}")
print(response.json())
```

**Expected**: 
- Thread created successfully
- Run starts and processes
- Eventually completes with an adventure plan

**Common Issues**:
- Missing API keys → Check `.env` file
- Graph compilation errors → Check logs
- Timeout → May need to increase timeout for long-running requests

### 3. Text-to-Adventure Test (Natural Language)

**Goal**: Test the orchestrator's natural language understanding

```python
# Submit natural language request (no structured preferences)
response = requests.post(
    f"http://127.0.0.1:8123/threads/{thread_id}/runs",
    json={
        "assistant_id": "agent",
        "input": {
            "user_input": "I'm looking for a weekend bikepacking trip in Utah, something challenging but not too extreme"
        }
    }
)
```

**Expected**: 
- Orchestrator extracts: activity_type="bikepacking", region="Utah", duration_days=2, skill_level="advanced"
- Appropriate agents are called
- Plan is generated

### 4. Error Handling Test

**Goal**: Verify graceful error handling

```python
# Test with invalid/missing location
response = requests.post(
    f"http://127.0.0.1:8123/threads/{thread_id}/runs",
    json={
        "assistant_id": "agent",
        "input": {
            "user_input": "I want to go biking in Nowhere, Antarctica"
        }
    }
)
```

**Expected**: 
- Errors are caught and stored in state
- Graph continues execution
- Partial results returned with error messages

### 5. Human-in-the-Loop Test

**Goal**: Test interrupt functionality

**Note**: This requires manual interaction via the LangGraph Studio UI or API

1. Submit a request that triggers human review (e.g., >7 days, errors)
2. Graph should pause at `human_review` node
3. Resume with approval/rejection/revision decision

**Expected**: 
- Graph pauses at interrupt
- State is saved
- Can resume with decision

### 6. Agent Coverage Test

**Goal**: Verify all agents can be called

Test requests that trigger different agent combinations:

```python
# Test all agents
test_cases = [
    {"input": "Mountain biking in Moab, need permits and safety info", "expected_agents": ["geo", "trail", "permits", "safety"]},
    {"input": "Bikepacking route in Colorado, need gear recommendations", "expected_agents": ["geo", "bikepacking", "gear"]},
    {"input": "Hiking trip in Yosemite, need accommodations and food", "expected_agents": ["geo", "trail", "accommodation", "food"]},
]
```

## 🔧 Known Issues & Workarounds

### Optional Import Warnings
- **Issue**: Linter warns about `langgraph.checkpoint.sqlite` and `langgraph.checkpoint.postgres`
- **Status**: ✅ **OK** - These are optional dependencies, conditionally imported
- **Action**: No fix needed, warnings can be ignored

### Tool Implementations
- **Issue**: Many tools return mock/placeholder data
- **Status**: ⚠️ **Expected** - Tools need real API integrations
- **Action**: Tools will return structured placeholders until real APIs are integrated

### State Initialization
- **Issue**: Some state fields may be None initially
- **Status**: ✅ **OK** - TypedDict with `total=False` allows optional fields
- **Action**: Nodes handle None values with `.get()` and defaults

## 🚀 Ready to Test?

### Before You Start:
1. ✅ Graph compiles without errors
2. ✅ Environment variables configured
3. ✅ Dependencies installed
4. ✅ Dev server can start

### Start Testing:
```bash
# Start dev server
./run.sh dev

# In another terminal, run the API integration tests
./run.sh test tests/integration_tests/test_api_integration.py
```

### Success Criteria:
- ✅ Graph compiles and server starts
- ✅ Can create threads
- ✅ Can submit requests
- ✅ Orchestrator routes correctly
- ✅ Agents execute (even if tools return placeholders)
- ✅ Plan is synthesized
- ✅ Errors are handled gracefully

## 📝 Next Steps After Testing

1. **If tests pass**: 
   - Integrate real API endpoints for tools
   - Add more comprehensive test cases
   - Performance optimization

2. **If tests fail**:
   - Check error logs
   - Verify environment variables
   - Check graph compilation
   - Review agent implementations

3. **Enhancements**:
   - Add streaming support
   - Improve error messages
   - Add more validation
   - Performance monitoring

## 🐛 Debugging Tips

### Check Graph Compilation
```python
from src.agent.graph import graph
# If this imports without error, graph is compiled
```

### Check Agent Initialization
```python
from src.agent.agents import OrchestratorAgent
orchestrator = OrchestratorAgent()
# Should initialize without errors
```

### Check Configuration
```python
from agent.config import Config
missing = Config.validate()
if missing:
    print(f"Missing required config: {missing}")
```

### View LangGraph Studio
- Navigate to `http://localhost:8123` (or your port)
- Use LangGraph Studio UI to visualize graph execution
- Inspect state at each step

