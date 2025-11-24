"""Model factory for creating LLM instances from different providers."""

from __future__ import annotations

from typing import Any

from langchain_core.language_models import BaseChatModel

from agent.config import Config

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None  # type: ignore[assignment, misc]

from langchain_openai import ChatOpenAI


def create_llm(
    agent_name: str,
    model_name: str | None = None,
    temperature: float | None = None,
    **kwargs: Any,
) -> BaseChatModel:
    """Create an LLM instance for a specific agent.
    
    Automatically detects provider from model name and creates appropriate instance.
    Falls back to default model if model_name is None.
    
    Args:
        agent_name: Name of the agent (e.g., "orchestrator", "trail_agent")
        model_name: Model identifier (e.g., "gpt-4o-mini", "claude-haiku-3")
                   If None, uses agent's configured model from Config
        temperature: Temperature setting (defaults to Config.OPENAI_TEMPERATURE)
        **kwargs: Additional arguments to pass to LLM constructor
        
    Returns:
        BaseChatModel instance (ChatOpenAI or ChatAnthropic)
        
    Raises:
        ValueError: If model provider cannot be determined or provider not available
    """
    # Get model name from config if not provided
    if model_name is None:
        model_name = Config.get_agent_model(agent_name)
    
    # Get temperature from config if not provided
    if temperature is None:
        temperature = Config.OPENAI_TEMPERATURE
    
    # Detect provider from model name
    model_lower = model_name.lower()
    
    # Anthropic models
    if model_lower.startswith("claude"):
        if ChatAnthropic is None:
            raise ValueError(
                "Anthropic models require langchain-anthropic package. "
                "Install with: uv pip install langchain-anthropic"
            )
        if not Config.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY is required for Anthropic models. "
                "Set it in your .env file."
            )
        
        # Map model names to Anthropic format
        anthropic_model = _normalize_anthropic_model(model_name)
        
        return ChatAnthropic(
            model=anthropic_model,
            temperature=temperature,
            api_key=Config.ANTHROPIC_API_KEY,
            **kwargs,
        )
    
    # OpenAI models (default)
    if not Config.OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY is required for OpenAI models. "
            "Set it in your .env file."
        )
    
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=Config.OPENAI_API_KEY,
        **kwargs,
    )


def _normalize_anthropic_model(model_name: str) -> str:
    """Normalize Anthropic model names to API format.
    
    Maps common model name variations to official API model names.
    
    Args:
        model_name: Model name (e.g., "claude-haiku-3", "claude-sonnet-3.5")
        
    Returns:
        Normalized model name for API
    """
    model_lower = model_name.lower()
    
    # Map common variations to official model names
    # LangChain's ChatAnthropic accepts model names without date suffixes
    # It will use the latest available version automatically
    model_mapping = {
        "claude-haiku-3": "claude-3-5-haiku",
        "claude-haiku": "claude-3-5-haiku",
        "claude-sonnet-3.5": "claude-3-5-sonnet",
        "claude-sonnet": "claude-3-5-sonnet",
        "claude-opus-3": "claude-3-opus",
        "claude-opus": "claude-3-opus",
    }
    
    # Check for exact match first
    if model_lower in model_mapping:
        return model_mapping[model_lower]
    
    # Check for model type in name
    if "haiku" in model_lower:
        return "claude-3-5-haiku"
    elif "sonnet" in model_lower:
        return "claude-3-5-sonnet"
    elif "opus" in model_lower:
        return "claude-3-opus"
    
    # Return as-is if no mapping found (assume it's already in correct format)
    return model_name

