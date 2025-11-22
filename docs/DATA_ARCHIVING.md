# Data Archiving

The adventure agent system includes a comprehensive data archiving system that automatically saves completed adventure plans for future retrieval and analysis.

## Overview

When an adventure plan is completed (after synthesis or human review approval), it is automatically archived to a persistent storage backend. This allows you to:

- Retrieve past adventure plans
- Search plans by location, activity type, or keywords
- Analyze planning patterns and preferences
- Export plans to JSON files
- Build analytics and reporting on past adventures

## Configuration

Archiving is configured via environment variables in your `.env` file:

```bash
# Archive type: "sqlite", "json", or "none" to disable
ARCHIVE_TYPE=json

# For SQLite backend (optional, defaults to "adventure_archive.db")
ARCHIVE_DB_PATH=adventure_archive.db

# For JSON backend (optional, defaults to "adventure_archive" directory)
ARCHIVE_DIR=adventure_archive
```

### Archive Backends

#### JSON File Backend (Default)
- **Type**: `json`
- **Storage**: Individual JSON files in a directory
- **Pros**: Simple, no database required, easy to browse
- **Cons**: Slower for large datasets, no advanced querying
- **Best for**: Development, small to medium deployments

#### SQLite Backend
- **Type**: `sqlite`
- **Storage**: Single SQLite database file
- **Pros**: Fast queries, full-text search, better for larger datasets
- **Cons**: Requires SQLite
- **Best for**: Production deployments, larger datasets

#### Disable Archiving
- **Type**: `none`
- **Storage**: None
- **Use when**: You don't need to archive plans

## Automatic Archiving

Plans are automatically archived when:
1. A plan is successfully synthesized (if human review is not required)
2. A plan is approved after human review
3. The workflow completes successfully

The archive node runs automatically at the end of the workflow and saves:
- Complete adventure state (all agent outputs)
- Final adventure plan
- User preferences
- Metadata (user_id, session_id if provided)
- Timestamp

## Retrieving Archived Plans

### Get a Specific Plan

```python
from agent.archive_utils import get_archived_plan

# Get a plan by archive ID
plan = get_archived_plan("123e4567-e89b-12d3-a456-426614174000")

if plan:
    print(f"Title: {plan['state']['adventure_plan']['title']}")
    print(f"Created: {plan['created_at']}")
    # Access full state
    state = plan['state']
    trails = state['trail_info']
    weather = state['weather_info']
```

### List All Plans

```python
from agent.archive_utils import list_archived_plans

# List all plans (most recent first)
plans = list_archived_plans(limit=50)

for plan in plans:
    print(f"{plan['title']} - {plan['location']} ({plan['created_at']})")

# Filter by user
user_plans = list_archived_plans(user_id="user123", limit=20)
```

### Search Plans

```python
from agent.archive_utils import search_archived_plans

# Search by keywords
results = search_archived_plans("Colorado mountain biking")

for result in results:
    print(f"{result['title']} - {result['description'][:100]}...")
```

### Export to JSON

```python
from agent.archive_utils import export_plan_to_json

# Export a plan to a JSON file
success = export_plan_to_json(
    archive_id="123e4567-e89b-12d3-a456-426614174000",
    output_path="my_adventure_plan.json"
)
```

## Archive Data Structure

Each archived plan contains:

```python
{
    "archive_id": "unique-uuid",
    "created_at": "2024-01-15T10:30:00",
    "user_id": "optional-user-id",
    "session_id": "optional-session-id",
    "title": "Adventure Plan Title",
    "description": "Plan description",
    "location": "Location name",
    "activity_type": "mountain_biking",
    "duration_days": 5,
    "state": {
        # Complete AdventureState with all agent outputs
        "user_input": "...",
        "user_preferences": {...},
        "adventure_plan": {...},
        "trail_info": [...],
        "weather_info": {...},
        # ... all other state fields
    },
    "metadata": {
        # Additional metadata
    }
}
```

## Integration with Workflow

The archiving system is integrated into the graph workflow:

```
... → synthesize → archive → END
... → synthesize → human_review → archive → END
```

The archive node:
- Only runs if a plan exists
- Does not fail the workflow if archiving fails (logs error instead)
- Extracts user_id and session_id from state if available
- Returns archive_id in state (can be accessed after workflow completes)

## Accessing Archive ID After Workflow

After running the workflow, you can access the archive ID:

```python
from agent.graph import graph

result = graph.invoke({
    "user_input": "Plan a mountain biking trip in Colorado",
    "user_preferences": {
        "activity_type": "mountain_biking",
        "region": "Colorado"
    }
})

# Get the archive ID if archiving succeeded
archive_id = result.get("archive_id")
if archive_id:
    print(f"Plan archived with ID: {archive_id}")
```

## Best Practices

1. **Use SQLite for Production**: SQLite backend provides better performance and full-text search for production deployments.

2. **Set User IDs**: If you have user authentication, set `user_id` in the initial state to enable user-specific filtering:
   ```python
   state = {
       "user_input": "...",
       "user_preferences": {...},
       "user_id": "user123",  # Optional but recommended
   }
   ```

3. **Regular Backups**: For JSON backend, backup the archive directory. For SQLite, backup the database file.

4. **Archive Cleanup**: Consider implementing cleanup policies for old plans if storage becomes an issue.

5. **Privacy**: Archived plans contain all user input and preferences. Ensure appropriate data protection measures are in place.

## Troubleshooting

### Archiving Not Working
- Check `ARCHIVE_TYPE` is set correctly (not "none")
- Verify write permissions for archive directory/database
- Check logs for archiving errors (archiving failures don't stop the workflow)

### Can't Find Plans
- Verify the archive backend is initialized correctly
- Check that plans were actually completed (check for `adventure_plan` in state)
- For SQLite, verify database file exists and is readable

### Performance Issues
- For large datasets, consider using SQLite backend instead of JSON
- Use pagination when listing plans (`limit` and `offset` parameters)
- Index queries by user_id if you have many users

