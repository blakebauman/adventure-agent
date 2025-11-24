# Per-Agent Model Assignment - Implementation Summary

## What Was Implemented

A complete system for assigning specific LLM models to each agent based on task complexity, enabling cost optimization and performance tuning.

## Files Created/Modified

### New Files
1. **`src/agent/models.py`** - Model factory for creating LLMs from different providers
   - `create_llm()` function that auto-detects provider (OpenAI/Anthropic)
   - Handles model name normalization
   - Provides clear error messages for missing dependencies/keys

2. **`docs/PER_AGENT_MODEL_ASSIGNMENT.md`** - Strategy document
   - Model assignment recommendations by complexity
   - Architecture overview

3. **`docs/MODEL_ASSIGNMENT_MIGRATION.md`** - Migration guide
   - Step-by-step instructions
   - Code examples
   - Testing checklist

### Modified Files
1. **`src/agent/config.py`**
   - Added `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL` config
   - Added `_AGENT_MODEL_DEFAULTS` dictionary with per-agent assignments
   - Added `get_agent_model()` method to retrieve agent-specific models
   - Supports environment variable overrides

2. **`pyproject.toml`**
   - Added `langchain-anthropic>=0.2.0` dependency

## Model Assignment Strategy

### High-Complexity Agents → Premium Models
- **Orchestrator**: `claude-sonnet-3.5` (complex routing, structured output)
- **Planning**: `claude-sonnet-3.5` (itinerary synthesis)
- **Synthesis**: `claude-sonnet-3.5` (final plan generation)

### Medium-Complexity Agents → Mid-Tier Models
- **Trail, Route Planning, Bikepacking**: `claude-haiku-3`
- **Safety, Permits**: `claude-haiku-3`
- **All Location Agents** (27 agents): `claude-haiku-3`

### Low-Complexity Agents → Cost-Optimized Models
- **Geo, Weather, Accommodation, Food, Transportation**: `claude-haiku-3`
- **Gear, Community, Photography, Historical**: `claude-haiku-3`
- **BLM, Advocacy**: `claude-haiku-3`

## Configuration Options

### 1. Use Defaults (No Configuration Needed)
Default assignments are already set in `Config._AGENT_MODEL_DEFAULTS`.

### 2. Override via Environment Variables
```bash
# .env
AGENT_MODEL_ORCHESTRATOR=claude-sonnet-3.5
AGENT_MODEL_TRAIL=claude-haiku-3
AGENT_MODEL_GEO=gpt-4o-mini
```

### 3. Override in Code
```python
orchestrator = OrchestratorAgent(model_name="claude-opus-3")
```

## Next Steps (Migration)

To actually use this system, you need to:

1. **Install dependency**:
   ```bash
   uv pip install langchain-anthropic
   ```

2. **Set API key**:
   ```bash
   # .env
   ANTHROPIC_API_KEY=your_key_here
   ```

3. **Update agents** to use `create_llm()` instead of `ChatOpenAI()`:
   - Start with `orchestrator.py`
   - Then `location_agent_base.py` (affects all 27 location agents)
   - Then other specialized agents

4. **Test** each agent type after migration

See `docs/MODEL_ASSIGNMENT_MIGRATION.md` for detailed migration steps.

## Benefits

1. **Cost Optimization**: Use expensive models only where needed
   - Orchestrator: ~$3/1M input tokens (Sonnet) vs $0.15/1M (Haiku)
   - 17+ agents using Haiku saves significant costs

2. **Performance**: Fast models for simple tasks, better models for complex ones

3. **Flexibility**: Easy to adjust per agent without code changes

4. **Provider Diversity**: Mix OpenAI and Anthropic models

5. **Backward Compatible**: Falls back to `OPENAI_MODEL` if agent not configured

## Example Usage

```python
from agent.models import create_llm

# Automatically uses orchestrator's configured model (claude-sonnet-3.5)
orchestrator_llm = create_llm("orchestrator")

# Automatically uses trail agent's configured model (claude-haiku-3)
trail_llm = create_llm("trail")

# Override with specific model
custom_llm = create_llm("geo", model_name="gpt-4o-mini")
```

## Architecture

```
Agent → create_llm(agent_name) 
      → Config.get_agent_model(agent_name)
      → Check env var (AGENT_MODEL_{NAME})
      → Check defaults (_AGENT_MODEL_DEFAULTS)
      → Fallback to OPENAI_MODEL
      → Detect provider (claude* → Anthropic, else → OpenAI)
      → Return ChatAnthropic or ChatOpenAI instance
```

## Status

✅ **Implementation Complete** - All infrastructure is in place
⏳ **Migration Pending** - Agents still need to be updated to use `create_llm()`

The system is ready to use once agents are migrated. See migration guide for details.

