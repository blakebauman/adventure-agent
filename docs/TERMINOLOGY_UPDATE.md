# Terminology Update: "Hardcoded" → "Default/Curated"

## Change Summary

We've updated terminology from "hardcoded" to "default" or "curated" knowledge to better reflect the value and purpose of this knowledge.

## Why the Change?

The term "hardcoded" has negative connotations suggesting:
- Inflexibility
- Poor design
- Something to be avoided

But our knowledge bases are actually:
- **Carefully curated** - Expert knowledge about locations
- **Essential context** - Provides foundational information
- **Default fallback** - Reliable source when external files aren't available
- **High quality** - Detailed, accurate, and comprehensive

## New Terminology

### Method Names
- `_get_hardcoded_knowledge()` → `_get_default_knowledge()`

### Documentation Terms
- "hardcoded knowledge" → "default knowledge" or "curated knowledge"
- "hardcoded in code" → "embedded in code" or "defined in code"

## What Changed

### Code
- ✅ `location_agent_base.py`: Method renamed to `_get_default_knowledge()`
- ✅ `payson_agent.py`: Updated method name
- ✅ `sedona_agent.py`: Updated method name

### Documentation
- ✅ `DYNAMIC_KNOWLEDGE_IMPLEMENTATION.md`: Updated terminology
- ✅ `KNOWLEDGE_SOURCE_MIGRATION.md`: Updated terminology
- ✅ `LOCATION_KNOWLEDGE_ARCHITECTURE.md`: Updated terminology

## Benefits

1. **More Accurate**: "Default" accurately describes the fallback behavior
2. **Positive Connotation**: "Curated" emphasizes quality and care
3. **Professional**: Standard software terminology
4. **Clear Intent**: Better communicates the purpose

## Migration for Other Agents

When updating other location agents, use:
- `_get_default_knowledge()` instead of `_get_hardcoded_knowledge()`
- "default knowledge" or "curated knowledge" in comments
- "embedded in code" or "defined in code" instead of "hardcoded"

