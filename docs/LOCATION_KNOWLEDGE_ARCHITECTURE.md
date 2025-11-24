# Location Knowledge Architecture - Dynamic vs Static

## Current State

Currently, location knowledge is **embedded in code** in each agent file as Python dictionaries. This has limitations:

### Problems with Knowledge Embedded in Code

1. **Maintenance Burden**: Updates require code changes
2. **Static Data**: Can't easily update without redeployment
3. **Duplication**: Same information might be in tools and knowledge base
4. **Scalability**: Hard to manage knowledge for many locations
5. **Version Control**: Knowledge changes mixed with code changes

## Recommended Architecture: Hybrid Approach

### Knowledge Categories

#### 1. **Static Knowledge** (Keep in Code/Config)
- Historical facts (founding dates, historical events)
- Geographic features (elevation, coordinates, terrain type)
- General characteristics (nickname, region, proximity)
- Rarely-changing facts

**Why**: These don't change often and provide stable context

#### 2. **Semi-Static Knowledge** (Load from External Sources)
- Trail names and general descriptions
- Attraction names and types
- Business categories
- General practical info

**Why**: Can be updated without code changes, stored in JSON/DB

#### 3. **Dynamic Knowledge** (Fetch via Tools)
- Current trail conditions
- Restaurant hours and availability
- Accommodation availability and prices
- Real-time weather
- Current permits and regulations
- Parking availability

**Why**: Changes frequently, should come from live data sources

## Proposed Implementation

### Option 1: External Knowledge Files (Recommended for Start)

```python
# knowledge/payson.json
{
  "location": {
    "name": "Payson, Arizona",
    "coordinates": {"lat": 34.2309, "lon": -111.3251},
    "elevation": 5000,
    "region": "Gila County, Arizona"
  },
  "history": {
    "founded": 1882,
    "known_for": ["Mogollon Rim gateway", "Tonto National Forest"]
  },
  "static_attractions": [
    {"name": "Mogollon Rim", "type": "natural", "description": "2,000-foot escarpment"}
  ]
}
```

**Benefits**:
- Easy to update without code changes
- Can be version controlled separately
- Can be loaded from multiple sources (local files, S3, database)

### Option 2: Vector Store / RAG (Advanced)

Store knowledge in a vector database and retrieve relevant chunks:

```python
# Retrieve relevant knowledge chunks based on query
knowledge_chunks = vector_store.similarity_search(
    query=f"{location} {activity_type} {context}",
    k=5
)
```

**Benefits**:
- Only relevant knowledge retrieved (reduces token usage)
- Can handle large knowledge bases
- Supports semantic search
- Easy to update knowledge

### Option 3: Database (Production)

Store in database with caching:

```python
# Load from database with caching
knowledge = cache.get_or_fetch(
    key=f"location_knowledge:{location}",
    fetch_fn=lambda: db.get_location_knowledge(location)
)
```

**Benefits**:
- Centralized knowledge management
- Easy updates via admin interface
- Versioning and audit trails
- Multi-source support

## Implementation Plan

### Phase 1: Refactor Base Class (Immediate)

Make `get_location_knowledge()` support multiple sources:

```python
class LocationAgentBase(ABC):
    def get_location_knowledge(self) -> Dict[str, Any]:
        """Get location-specific knowledge from multiple sources.
        
        Priority:
        1. External knowledge file (if exists)
        2. Default/curated knowledge (fallback)
        3. Dynamic tool data (always fetched)
        """
        # Try to load from external source first
        external_knowledge = self._load_external_knowledge()
        if external_knowledge:
            return external_knowledge
        
        # Fallback to default knowledge
        return self._get_default_knowledge()
    
    def _load_external_knowledge(self) -> Optional[Dict[str, Any]]:
        """Load knowledge from external source (JSON, DB, etc.)."""
        # Try JSON file first
        json_path = f"knowledge/{self.AGENT_NAME}.json"
        if os.path.exists(json_path):
            with open(json_path) as f:
                return json.load(f)
        return None
    
    @abstractmethod
    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Fallback default/curated knowledge."""
        pass
```

### Phase 2: Separate Static vs Dynamic (Next)

Refactor knowledge base structure:

```python
KNOWLEDGE = {
    # Static - rarely changes
    "static": {
        "location": {...},
        "history": {...},
        "geography": {...}
    },
    # Semi-static - can be loaded from external source
    "semi_static": {
        "attractions": [...],
        "trail_names": [...],
        "business_categories": [...]
    },
    # Dynamic - always fetched via tools
    "dynamic": {
        "trail_conditions": "fetched_via_tools",
        "restaurant_hours": "fetched_via_tools",
        "current_weather": "fetched_via_tools"
    }
}
```

### Phase 3: Tool-First Approach (Advanced)

Prioritize tools over knowledge base:

```python
async def get_location_info(...):
    # 1. Fetch dynamic data via tools FIRST
    tool_data = await self._fetch_dynamic_data(location, activity_type)
    
    # 2. Load static/semi-static knowledge
    static_knowledge = self.get_location_knowledge()
    
    # 3. Enhance tool data with static knowledge
    enhanced = self._enhance_with_knowledge(tool_data, static_knowledge)
    
    return enhanced
```

## Recommended Approach

### For Current Implementation

1. **Keep minimal static knowledge** in code (location name, coordinates, elevation)
2. **Move detailed knowledge to JSON files** in `knowledge/` directory
3. **Fetch dynamic data via tools** (trails, restaurants, conditions)
4. **Combine both** in agent response

### Knowledge File Structure

```
knowledge/
  payson.json
  sedona.json
  phoenix.json
  ...
```

Each file contains:
- Static facts (history, geography)
- Semi-static (attraction names, trail names)
- References to tools for dynamic data

### Example: Payson Agent Refactored

```python
class PaysonAgent(LocationAgentBase):
    def _get_default_knowledge(self) -> Dict[str, Any]:
        """Minimal default knowledge - just essentials."""
        return {
            "location": {
                "name": "Payson, Arizona",
                "coordinates": {"lat": 34.2309, "lon": -111.3251},
                "elevation": 5000,
                "region": "Gila County, Arizona"
            }
        }
    
    # Detailed knowledge loaded from knowledge/payson.json
    # Dynamic data fetched via tools
```

## Benefits

1. **Maintainability**: Update knowledge without code changes
2. **Flexibility**: Multiple knowledge sources
3. **Accuracy**: Dynamic data always current
4. **Scalability**: Easy to add new locations
5. **Separation of Concerns**: Code vs data

## Migration Path

1. Create `knowledge/` directory structure
2. Extract detailed knowledge to JSON files
3. Update base class to load from files
4. Keep minimal default/curated knowledge as fallback
5. Update agents to use new structure
6. Test and validate

## Future Enhancements

- **Vector Store**: Semantic search for relevant knowledge chunks
- **Database**: Centralized knowledge management
- **API Integration**: Fetch knowledge from external APIs
- **Community Contributions**: Allow knowledge updates via API
- **Versioning**: Track knowledge changes over time
- **A/B Testing**: Test different knowledge configurations

