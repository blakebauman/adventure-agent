# Per-Agent Model Assignment Implementation

## Overview
Assign specific LLM models to each agent based on task complexity, cost optimization, and performance requirements.

## Model Assignment Strategy

### High-Complexity Agents (Premium Models)
**Require sophisticated reasoning, structured output, or critical decision-making**

- **Orchestrator**: `claude-sonnet-3.5` or `gpt-4o`
  - Complex routing decisions
  - Structured output extraction
  - Multi-agent coordination
  
- **Planning Agent**: `claude-sonnet-3.5` or `gpt-4o`
  - Itinerary synthesis
  - Multi-day planning logic
  - Complex preference matching

- **Synthesis Node**: `claude-sonnet-3.5` or `gpt-4o`
  - Final plan generation
  - Information consolidation

### Medium-Complexity Agents (Mid-Tier Models)
**Require good reasoning but less critical than orchestrator**

- **Trail Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Trail data analysis
  - Difficulty matching
  - Multiple data sources

- **Route Planning Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Route analysis
  - Navigation planning

- **Bikepacking Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Route curation
  - Multi-day planning

- **Location Agents** (all 27): `claude-haiku-3` or `gpt-4o-mini`
  - Knowledge synthesis
  - Local context integration

- **Safety Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Risk assessment
  - Important but structured

- **Permits Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Regulation interpretation
  - Structured data

### Low-Complexity Agents (Cost-Optimized Models)
**Simple data formatting, lookups, or basic recommendations**

- **Geo Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Coordinate lookups
  - Simple formatting

- **Weather Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Data formatting
  - Simple analysis

- **Accommodation Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Search results formatting

- **Food Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Search results formatting

- **Transportation Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Search results formatting

- **Gear Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Basic recommendations

- **Community Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Basic recommendations

- **Photography Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Basic recommendations

- **Historical Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Basic recommendations

- **BLM Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Data formatting

- **Advocacy Agent**: `claude-haiku-3` or `gpt-4o-mini`
  - Data formatting

## Implementation Architecture

### 1. Model Factory (`src/agent/models.py`)
Central factory for creating LLM instances with provider abstraction.

### 2. Model Registry (`src/agent/config.py`)
Configuration for per-agent model assignments with fallbacks.

### 3. Agent Updates
Update all agents to use model factory instead of direct `ChatOpenAI` instantiation.

## File Structure

```
src/agent/
├── models.py          # Model factory and provider abstraction
├── config.py          # Updated with per-agent model config
└── agents/
    ├── orchestrator.py    # Uses model factory
    ├── location_agent_base.py  # Uses model factory
    └── [all other agents]      # Use model factory
```

## Configuration Format

### Environment Variables
```bash
# Default models (fallback)
OPENAI_MODEL=gpt-4o-mini
ANTHROPIC_MODEL=claude-haiku-3

# Per-agent model assignments (optional, overrides defaults)
AGENT_MODEL_ORCHESTRATOR=claude-sonnet-3.5
AGENT_MODEL_PLANNING=claude-sonnet-3.5
AGENT_MODEL_SYNTHESIS=claude-sonnet-3.5
AGENT_MODEL_TRAIL=claude-haiku-3
AGENT_MODEL_ROUTE_PLANNING=claude-haiku-3
# ... etc
```

### Config Class Structure
```python
# In config.py
AGENT_MODELS: Dict[str, str] = {
    "orchestrator": os.getenv("AGENT_MODEL_ORCHESTRATOR", "claude-sonnet-3.5"),
    "planning": os.getenv("AGENT_MODEL_PLANNING", "claude-sonnet-3.5"),
    "synthesis": os.getenv("AGENT_MODEL_SYNTHESIS", "claude-sonnet-3.5"),
    "trail": os.getenv("AGENT_MODEL_TRAIL", "claude-haiku-3"),
    # ... defaults for all agents
}
```

## Benefits

1. **Cost Optimization**: Use expensive models only where needed
2. **Performance**: Fast models for simple tasks, better models for complex ones
3. **Flexibility**: Easy to adjust per agent without code changes
4. **Backward Compatible**: Falls back to defaults if not configured
5. **Provider Diversity**: Mix OpenAI and Anthropic models

## Migration Path

1. Add `langchain-anthropic` dependency
2. Create model factory
3. Update config
4. Update agents one by one (orchestrator first, then others)
5. Test each agent
6. Deploy with monitoring

