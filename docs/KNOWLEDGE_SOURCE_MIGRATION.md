# Knowledge Source Migration Guide

## Overview

Location agents now support **multiple knowledge sources** instead of only knowledge embedded in code. This allows knowledge to be:

1. **External JSON files** (recommended) - Easy updates without code changes
2. **Default/curated knowledge in code** (fallback) - Backward compatible
3. **Dynamic via tools** (always) - Real-time data

## Architecture Change

### Before (Embedded in Code Only)

```python
class PaysonAgent(LocationAgentBase):
    def get_location_knowledge(self) -> Dict[str, Any]:
        return PAYSON_KNOWLEDGE  # Embedded knowledge dictionary
```

### After (Multi-Source)

```python
class PaysonAgent(LocationAgentBase):
    def _get_default_knowledge(self) -> Dict[str, Any]:
        return PAYSON_KNOWLEDGE  # Fallback only
    
    # get_location_knowledge() now automatically:
    # 1. Tries to load from knowledge/payson_agent.json
    # 2. Falls back to _get_default_knowledge() if file not found
```

## Migration Steps

### Step 1: Create Knowledge Directory

```bash
mkdir -p knowledge
```

### Step 2: Extract Knowledge to JSON

For each agent, create a JSON file:

```bash
# Example: knowledge/payson_agent.json
{
  "location": {
    "name": "Payson, Arizona",
    "coordinates": {"lat": 34.2309, "lon": -111.3251},
    "elevation": 5000,
    "region": "Gila County, Arizona",
    "country": "US",
    "nickname": "Heart of Arizona"
  },
  "history": {
    "founded": 1882,
    "incorporated": 1973,
    "current_population": "~16,000 residents"
  },
  "outdoor_activities": {
    "mountain_biking": {
      "description": "Extensive trail network in Tonto National Forest",
      "famous_trails": [
        {
          "name": "Highline Trail",
          "difficulty": "Intermediate to Advanced",
          "description": "Scenic trail along Mogollon Rim"
        }
      ]
    }
  }
}
```

### Step 3: Update Agent Class

Change method name from `get_location_knowledge()` to `_get_default_knowledge()`:

```python
# Before
def get_location_knowledge(self) -> Dict[str, Any]:
    return PAYSON_KNOWLEDGE

# After
def _get_default_knowledge(self) -> Dict[str, Any]:
    return PAYSON_KNOWLEDGE
```

### Step 4: Test

1. Test with JSON file present (should load from file)
2. Test with JSON file removed (should use default knowledge fallback)
3. Verify agent behavior is unchanged

## Knowledge File Naming

Files should be named: `{agent_name}.json`

Examples:
- `payson_agent.json`
- `sedona_agent.json`
- `phoenix_agent.json`

## Knowledge Structure

### Recommended Structure

```json
{
  "location": {
    "name": "Location Name",
    "coordinates": {"lat": 0.0, "lon": 0.0},
    "elevation": 0,
    "region": "County, State",
    "country": "US"
  },
  "history": {
    "founded": 1882,
    "known_for": ["item1", "item2"]
  },
  "geography": {
    "terrain": "...",
    "features": [...]
  },
  "outdoor_activities": {
    "mountain_biking": {
      "description": "...",
      "famous_trails": [...]
    }
  },
  "attractions": {
    "natural": [...],
    "cultural": [...]
  },
  "businesses": {
    "restaurants": [...],
    "accommodations": [...]
  },
  "practical_info": {
    "parking": "...",
    "permits": "...",
    "best_times": "..."
  }
}
```

## What Should Be in Knowledge vs Tools?

### Knowledge Base (Static/Semi-Static)
- ✅ Historical facts
- ✅ Geographic features
- ✅ General trail names and descriptions
- ✅ Attraction names and types
- ✅ General practical info (elevation, region, etc.)

### Tools (Dynamic)
- ✅ Current trail conditions
- ✅ Restaurant hours and availability
- ✅ Accommodation prices and availability
- ✅ Real-time weather
- ✅ Current permits and regulations
- ✅ Parking availability

### Hybrid Approach
- Knowledge base provides: "Highline Trail is a scenic trail along Mogollon Rim"
- Tools provide: "Current conditions: dry, 72°F, moderate traffic"

## Benefits

1. **Easy Updates**: Change JSON files without code deployment
2. **Version Control**: Track knowledge changes separately from code
3. **Multiple Sources**: Can load from files, database, API, etc.
4. **Backward Compatible**: Still works with default/curated knowledge
5. **Flexible**: Can mix sources (some from file, some from DB)

## Future Enhancements

### Database Support

```python
def _load_external_knowledge(self) -> Optional[Dict[str, Any]]:
    # Try database
    db_knowledge = db.get_location_knowledge(self.AGENT_NAME)
    if db_knowledge:
        return db_knowledge
    
    # Fallback to JSON file
    return self._load_from_json()
```

### Vector Store / RAG

```python
def _load_external_knowledge(self) -> Optional[Dict[str, Any]]:
    # Retrieve relevant knowledge chunks
    chunks = vector_store.similarity_search(
        query=f"{self.LOCATION_NAME} {activity_type}",
        k=5
    )
    return self._combine_chunks(chunks)
```

### Environment-Specific

```python
def _load_external_knowledge(self) -> Optional[Dict[str, Any]]:
    env = os.getenv("KNOWLEDGE_SOURCE", "file")
    
    if env == "database":
        return self._load_from_database()
    elif env == "api":
        return self._load_from_api()
    else:
        return self._load_from_json()
```

## Testing

### Test External Knowledge Loading

```python
# Test with JSON file
agent = PaysonAgent()
knowledge = agent.get_location_knowledge()
assert knowledge["location"]["name"] == "Payson, Arizona"

# Test fallback (remove JSON file)
os.remove("knowledge/payson_agent.json")
knowledge = agent.get_location_knowledge()
assert knowledge["location"]["name"] == "Payson, Arizona"  # Still works
```

## Rollout Plan

1. ✅ Update base class to support external sources
2. ⏳ Create knowledge/ directory structure
3. ⏳ Migrate one agent (Payson) as proof of concept
4. ⏳ Test and validate
5. ⏳ Migrate remaining agents
6. ⏳ Update documentation

