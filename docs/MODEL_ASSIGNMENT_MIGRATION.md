# Per-Agent Model Assignment Migration Guide

## Overview
This guide shows how to migrate agents from direct `ChatOpenAI` instantiation to using the model factory, which supports per-agent model assignments.

## Step 1: Install Dependencies

```bash
uv pip install langchain-anthropic
```

## Step 2: Update Agent Imports

Replace:
```python
from langchain_openai import ChatOpenAI
```

With:
```python
from agent.models import create_llm
```

## Step 3: Update Agent Initialization

### Before (Orchestrator Example)
```python
class OrchestratorAgent:
    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else Config.OPENAI_TEMPERATURE,
            api_key=Config.OPENAI_API_KEY,
        )
        self.llm_structured = self.llm.with_structured_output(AdventureAnalysis, method="function_calling")
```

### After (Using Model Factory)
```python
class OrchestratorAgent:
    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        # Use model factory - automatically gets agent's configured model
        self.llm = create_llm(
            agent_name="orchestrator",
            model_name=model_name,  # Optional override
            temperature=temperature,  # Optional override
        )
        self.llm_structured = self.llm.with_structured_output(AdventureAnalysis, method="function_calling")
```

## Step 4: Update Location Agent Base

### Before
```python
class LocationAgentBase(ABC):
    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        self.llm = ChatOpenAI(
            model_name=model_name or Config.OPENAI_MODEL,
            temperature=temperature if temperature is not None else 0.3,
            api_key=Config.OPENAI_API_KEY,
        )
```

### After
```python
class LocationAgentBase(ABC):
    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        # Get agent name from subclass (e.g., "jerome", "sedona")
        agent_name = self.AGENT_NAME.replace("_agent", "")
        self.llm = create_llm(
            agent_name=agent_name,
            model_name=model_name,
            temperature=temperature if temperature is not None else 0.3,
        )
```

## Step 5: Update All Other Agents

Follow the same pattern for all agents:
- `TrailAgent`
- `GeoAgent`
- `WeatherAgent`
- `PlanningAgent`
- `SafetyAgent`
- etc.

## Step 6: Configure Models

### Option A: Use Defaults
Default model assignments are already configured in `Config._AGENT_MODEL_DEFAULTS`.

### Option B: Override via Environment Variables
```bash
# .env file
AGENT_MODEL_ORCHESTRATOR=claude-sonnet-3.5
AGENT_MODEL_PLANNING=claude-sonnet-3.5
AGENT_MODEL_TRAIL=claude-haiku-3
AGENT_MODEL_GEO=gpt-4o-mini
# ... etc
```

### Option C: Override in Code
```python
orchestrator = OrchestratorAgent(model_name="claude-opus-3")
```

## Step 7: Set API Keys

Add to `.env`:
```bash
# Required for Anthropic models
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Still required for OpenAI models
OPENAI_API_KEY=your_openai_api_key_here
```

## Migration Checklist

- [ ] Install `langchain-anthropic`
- [ ] Update `orchestrator.py` to use `create_llm`
- [ ] Update `location_agent_base.py` to use `create_llm`
- [ ] Update all specialized agents (trail, geo, weather, etc.)
- [ ] Set `ANTHROPIC_API_KEY` in `.env`
- [ ] Test orchestrator with new model
- [ ] Test a few specialized agents
- [ ] Test location agents
- [ ] Monitor costs and performance
- [ ] Adjust model assignments as needed

## Testing

After migration, test each agent type:

```python
# Test orchestrator
from agent.agents import OrchestratorAgent
orchestrator = OrchestratorAgent()
# Should use claude-sonnet-3.5 by default

# Test trail agent
from agent.agents import TrailAgent
trail = TrailAgent()
# Should use claude-haiku-3 by default

# Test location agent
from agent.agents.locations import JeromeAgent
jerome = JeromeAgent()
# Should use claude-haiku-3 by default
```

## Rollback Plan

If issues occur, you can quickly rollback by:
1. Reverting agent files to use `ChatOpenAI` directly
2. Or setting all `AGENT_MODEL_*` env vars to `gpt-4o-mini`

## Benefits After Migration

1. **Cost Optimization**: Expensive models only where needed
2. **Performance**: Fast models for simple tasks
3. **Flexibility**: Easy model changes via config
4. **Provider Diversity**: Mix OpenAI and Anthropic
5. **Backward Compatible**: Falls back to defaults

