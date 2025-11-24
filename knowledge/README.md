# Knowledge Directory

This directory contains external knowledge files for location agents.

## File Naming

Knowledge files should be named: `{agent_name}.json`

Examples:
- `payson_agent.json`
- `sedona_agent.json`
- `phoenix_agent.json`

## How It Works

1. Location agents automatically try to load knowledge from `knowledge/{agent_name}.json`
2. If file exists, it's used instead of hardcoded knowledge
3. If file doesn't exist, agent falls back to hardcoded knowledge (backward compatible)

## Benefits

- **Easy Updates**: Change knowledge without code changes
- **Version Control**: Track knowledge separately from code
- **Flexibility**: Can load from files, database, API, etc. in future

## Example Structure

See `payson_agent.json` for an example knowledge file structure.

## Migration

See `docs/KNOWLEDGE_SOURCE_MIGRATION.md` for migration guide.

