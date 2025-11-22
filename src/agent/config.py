"""Configuration for adventure agent."""

import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration settings for the adventure agent."""

    # OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

    # LangSmith
    LANGCHAIN_TRACING_V2: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    LANGCHAIN_ENDPOINT: str = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    LANGCHAIN_API_KEY: Optional[str] = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "adventure-agent")

    # Tavily (web search)
    TAVILY_API_KEY: Optional[str] = os.getenv("TAVILY_API_KEY")

    # Affiliate
    AFFILIATE_BASE_URL: str = os.getenv("AFFILIATE_BASE_URL", "https://example.com/affiliate")

    # Checkpointing
    # Set to "memory", "sqlite", "postgres", or "none" (for LangGraph API)
    # Default is "none" because LangGraph API (langgraph dev) handles checkpointing automatically
    CHECKPOINTER_TYPE: str = os.getenv("CHECKPOINTER_TYPE", "none")
    CHECKPOINTER_DB_URL: Optional[str] = os.getenv("CHECKPOINTER_DB_URL")

    # Data Archiving
    # Set to "sqlite", "json", or "none" to disable archiving
    # Default is "json" for simple file-based archiving
    ARCHIVE_TYPE: Optional[str] = os.getenv("ARCHIVE_TYPE", "json")
    ARCHIVE_DB_PATH: Optional[str] = os.getenv("ARCHIVE_DB_PATH")  # For SQLite backend
    ARCHIVE_DIR: Optional[str] = os.getenv("ARCHIVE_DIR", "adventure_archive")  # For JSON backend

    @classmethod
    def validate(cls) -> list[str]:
        """Validate configuration and return list of missing required fields."""
        missing = []
        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        return missing

