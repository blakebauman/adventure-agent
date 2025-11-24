"""Configuration for adventure agent."""

import os
from typing import Dict

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration settings for the adventure agent."""

    # OpenAI
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

    # Anthropic
    ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-haiku-3")

    # LangSmith
    LANGCHAIN_TRACING_V2: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    LANGCHAIN_ENDPOINT: str = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    LANGCHAIN_API_KEY: str | None = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "arizona-adventure-agent")

    # Tavily (web search)
    TAVILY_API_KEY: str | None = os.getenv("TAVILY_API_KEY")

    # Affiliate
    AFFILIATE_BASE_URL: str = os.getenv("AFFILIATE_BASE_URL", "https://example.com/affiliate")

    # Geocoding API (OpenCage, Nominatim, etc.)
    OPENCAGE_API_KEY: str | None = os.getenv("OPENCAGE_API_KEY")
    # Use Nominatim (free, no key) if OPENCAGE_API_KEY not set

    # Weather API
    OPENWEATHER_API_KEY: str | None = os.getenv("OPENWEATHER_API_KEY")
    # Falls back to Weather.gov (free, no key) if OPENWEATHER_API_KEY not set

    # Google Places API (for accommodations, restaurants, etc.)
    GOOGLE_PLACES_API_KEY: str | None = os.getenv("GOOGLE_PLACES_API_KEY")

    # Recreation.gov API (for campgrounds and recreation areas)
    RECREATION_GOV_API_KEY: str | None = os.getenv("RECREATION_GOV_API_KEY")
    # Falls back to "public" key if not set (rate-limited)

    # Checkpointing
    # Set to "memory", "sqlite", "postgres", or "none" (for LangGraph API)
    # Default is "none" because LangGraph API (langgraph dev) handles checkpointing automatically
    CHECKPOINTER_TYPE: str = os.getenv("CHECKPOINTER_TYPE", "none")
    CHECKPOINTER_DB_URL: str | None = os.getenv("CHECKPOINTER_DB_URL")

    # Human-in-the-loop
    # Enable/disable human review (default: False)
    # Note: Requires a checkpointer to be configured (except when using LangGraph API)
    ENABLE_HUMAN_REVIEW: bool = os.getenv("ENABLE_HUMAN_REVIEW", "false").lower() == "true"

    # Data Archiving
    # Set to "sqlite", "json", or "none" to disable archiving
    # Default is "json" for simple file-based archiving
    ARCHIVE_TYPE: str | None = os.getenv("ARCHIVE_TYPE", "json")
    ARCHIVE_DB_PATH: str | None = os.getenv("ARCHIVE_DB_PATH")  # For SQLite backend
    ARCHIVE_DIR: str | None = os.getenv("ARCHIVE_DIR", "adventure_archive")  # For JSON backend

    # Caching and Rate Limiting
    # Enable/disable caching (default: True)
    ENABLE_CACHING: bool = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    # Enable/disable rate limiting (default: True)
    ENABLE_RATE_LIMITING: bool = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
    # Cache TTL in seconds (default: 3600 = 1 hour)
    CACHE_DEFAULT_TTL: float = float(os.getenv("CACHE_DEFAULT_TTL", "3600"))
    # Maximum cache size (default: 1000 entries)
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "1000"))

    # Graph Execution
    # Maximum number of concurrent nodes (default: 10, None for unlimited)
    # Set this to limit parallel execution for resource-constrained environments
    MAX_CONCURRENCY: int | None = (
        int(os.getenv("MAX_CONCURRENCY")) if os.getenv("MAX_CONCURRENCY") else None
    )

    # Per-Agent Model Assignments
    # Maps agent names to model identifiers (e.g., "gpt-4o-mini", "claude-haiku-3")
    # Can be overridden via environment variables: AGENT_MODEL_{AGENT_NAME}
    # Default assignments optimize for cost and performance based on task analysis:
    # - High-complexity agents (orchestrator, planning, synthesis) use premium Claude models
    # - Safety/regulatory agents use Claude for accuracy
    # - Tool-heavy and simple formatting agents use GPT-4o-mini for cost efficiency
    # See docs/MODEL_RECOMMENDATIONS.md for detailed analysis
    _AGENT_MODEL_DEFAULTS: Dict[str, str] = {
        # High-complexity: Premium Claude models for critical reasoning
        "orchestrator": "claude-sonnet-3.5",
        "planning": "claude-sonnet-3.5",
        "synthesis": "claude-sonnet-3.5",
        # Safety/Regulatory: Claude for accuracy (safety-critical, regulatory compliance)
        "safety": "claude-haiku-3",
        "permits": "claude-haiku-3",
        "blm": "claude-haiku-3",
        # Moderate complexity: Claude for nuanced understanding
        "bikepacking": "claude-haiku-3",
        "historical": "claude-haiku-3",
        "advocacy": "claude-haiku-3",
        # Tool-heavy & Simple formatting: GPT-4o-mini for cost efficiency
        # Better tool calling performance, faster responses, 3-5x lower cost
        "trail": "gpt-4o-mini",
        "route_planning": "gpt-4o-mini",
        "geo": "gpt-4o-mini",
        "weather": "gpt-4o-mini",
        "transportation": "gpt-4o-mini",
        "accommodation": "gpt-4o-mini",
        "food": "gpt-4o-mini",
        "gear": "gpt-4o-mini",
        "community": "gpt-4o-mini",
        "photography": "gpt-4o-mini",
        # Location agents: GPT-4o-mini (heavy tool usage, high volume, cost-sensitive)
        "jerome": "gpt-4o-mini",
        "sedona": "gpt-4o-mini",
        "prescott": "gpt-4o-mini",
        "flagstaff": "gpt-4o-mini",
        "grand_canyon": "gpt-4o-mini",
        "payson": "gpt-4o-mini",
        "pine": "gpt-4o-mini",
        "strawberry": "gpt-4o-mini",
        "pinetop": "gpt-4o-mini",
        "williams": "gpt-4o-mini",
        "phoenix": "gpt-4o-mini",
        "tucson": "gpt-4o-mini",
        "cottonwood": "gpt-4o-mini",
        "camp_verde": "gpt-4o-mini",
        "show_low": "gpt-4o-mini",
        "bisbee": "gpt-4o-mini",
        "tombstone": "gpt-4o-mini",
        "sierra_vista": "gpt-4o-mini",
        "patagonia": "gpt-4o-mini",
        "page": "gpt-4o-mini",
        "kingman": "gpt-4o-mini",
        "lake_havasu": "gpt-4o-mini",
        "globe_miami": "gpt-4o-mini",
        "springerville_eagar": "gpt-4o-mini",
        "ajo": "gpt-4o-mini",
        "sonoita": "gpt-4o-mini",
        "yuma": "gpt-4o-mini",
        "parker": "gpt-4o-mini",
    }

    @classmethod
    def get_agent_model(cls, agent_name: str) -> str:
        """Get the configured model for a specific agent.
        
        Checks environment variable first (AGENT_MODEL_{AGENT_NAME}),
        then falls back to default assignments, then to OPENAI_MODEL.
        
        Args:
            agent_name: Name of the agent (e.g., "orchestrator", "trail_agent")
            
        Returns:
            Model identifier string (e.g., "gpt-4o-mini", "claude-haiku-3")
        """
        # Normalize agent name (remove _agent suffix, convert to lowercase)
        normalized = agent_name.lower().replace("_agent", "").replace("-", "_")
        
        # Check environment variable override
        env_key = f"AGENT_MODEL_{normalized.upper()}"
        env_model = os.getenv(env_key)
        if env_model:
            return env_model
        
        # Check default assignments
        if normalized in cls._AGENT_MODEL_DEFAULTS:
            return cls._AGENT_MODEL_DEFAULTS[normalized]
        
        # Fallback to default OpenAI model
        return cls.OPENAI_MODEL

    @classmethod
    def validate(cls) -> list[str]:
        """Validate configuration and return list of missing required fields."""
        missing = []
        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        # Note: ANTHROPIC_API_KEY is optional unless using Anthropic models
        return missing

