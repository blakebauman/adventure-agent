# API Key Setup Guide

## Issue
The error shows: `Incorrect API key provided: lsv2_pt_...` - This is a **LangSmith API key**, not an OpenAI API key.

## Solution

### 1. Get Your OpenAI API Key
1. Go to https://platform.openai.com/account/api-keys
2. Create a new API key or copy an existing one
3. OpenAI keys start with `sk-` (e.g., `sk-proj-...`)

### 2. Update Your `.env` File

Add or update the `OPENAI_API_KEY` in your `.env` file:

```bash
# Required: OpenAI API Key (starts with sk-)
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Optional: LangSmith API Key (for tracing, starts with lsv2_pt_)
LANGCHAIN_API_KEY=lsv2_pt_your-langsmith-key-here

# Optional: Model configuration
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7

# Optional: LangSmith tracing
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=adventure-agent
```

### 3. Verify Your Setup

Run this to check your configuration:

```python
from agent.config import Config

# Check what's loaded
print(f"OPENAI_API_KEY set: {Config.OPENAI_API_KEY is not None}")
print(f"OPENAI_API_KEY starts with 'sk-': {Config.OPENAI_API_KEY.startswith('sk-') if Config.OPENAI_API_KEY else False}")
print(f"OPENAI_MODEL: {Config.OPENAI_MODEL}")

# Validate
missing = Config.validate()
if missing:
    print(f"Missing required config: {missing}")
else:
    print("✅ Configuration is valid!")
```

### 4. Restart the Dev Server

After updating `.env`, restart your dev server:

```bash
# Stop the current server (Ctrl+C)
# Then restart
./run.sh dev
```

## Key Differences

| Key Type | Variable Name | Format | Purpose |
|----------|--------------|--------|---------|
| **OpenAI** | `OPENAI_API_KEY` | `sk-...` | For LLM calls (ChatGPT, GPT-4, etc.) |
| **LangSmith** | `LANGCHAIN_API_KEY` | `lsv2_pt_...` | For tracing and monitoring (optional) |

## Common Mistakes

1. ❌ Using LangSmith key for `OPENAI_API_KEY`
2. ❌ Not setting `OPENAI_API_KEY` at all
3. ❌ Using an expired or invalid OpenAI key
4. ❌ Having extra spaces or quotes in `.env` file

## Quick Fix Command

```bash
# Edit your .env file
nano .env  # or use your preferred editor

# Add this line (replace with your actual key):
OPENAI_API_KEY=sk-your-key-here
```

## Testing

After setting the key, test with:

```bash
# Start the dev server first
./run.sh dev

# In another terminal, run the API integration tests
./run.sh test tests/integration_tests/test_api_integration.py
```

You should see the graph execute without API key errors.

