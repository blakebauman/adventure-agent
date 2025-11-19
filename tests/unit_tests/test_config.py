"""Unit tests for configuration."""

import os
import pytest
from unittest.mock import patch
from agent.config import Config


class TestConfig:
    """Test Config class."""

    def test_default_model(self):
        """Test default model setting."""
        with patch.dict(os.environ, {}, clear=True):
            # Reload config to get defaults
            from importlib import reload
            import agent.config
            reload(agent.config)
            from agent.config import Config as ReloadedConfig
            assert ReloadedConfig.OPENAI_MODEL == "gpt-4o-mini"

    def test_default_temperature(self):
        """Test default temperature setting."""
        with patch.dict(os.environ, {}, clear=True):
            from importlib import reload
            import agent.config
            reload(agent.config)
            from agent.config import Config as ReloadedConfig
            assert ReloadedConfig.OPENAI_TEMPERATURE == 0.7

    def test_validate_missing_api_key(self):
        """Test validation with missing API key."""
        with patch.dict(os.environ, {}, clear=True):
            from importlib import reload
            import agent.config
            reload(agent.config)
            from agent.config import Config as ReloadedConfig
            missing = ReloadedConfig.validate()
            assert "OPENAI_API_KEY" in missing

    def test_validate_with_api_key(self):
        """Test validation with API key present."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            from importlib import reload
            import agent.config
            reload(agent.config)
            from agent.config import Config as ReloadedConfig
            missing = ReloadedConfig.validate()
            assert "OPENAI_API_KEY" not in missing

    def test_checkpointer_type_default(self):
        """Test default checkpointer type."""
        with patch.dict(os.environ, {}, clear=True):
            from importlib import reload
            import agent.config
            reload(agent.config)
            from agent.config import Config as ReloadedConfig
            assert ReloadedConfig.CHECKPOINTER_TYPE == "none"

    def test_checkpointer_type_memory(self):
        """Test memory checkpointer type."""
        with patch.dict(os.environ, {"CHECKPOINTER_TYPE": "memory"}):
            from importlib import reload
            import agent.config
            reload(agent.config)
            from agent.config import Config as ReloadedConfig
            assert ReloadedConfig.CHECKPOINTER_TYPE == "memory"

    def test_langchain_tracing_default(self):
        """Test default LangChain tracing setting."""
        with patch.dict(os.environ, {}, clear=True):
            from importlib import reload
            import agent.config
            reload(agent.config)
            from agent.config import Config as ReloadedConfig
            assert ReloadedConfig.LANGCHAIN_TRACING_V2 is False

    def test_langchain_tracing_enabled(self):
        """Test enabled LangChain tracing."""
        with patch.dict(os.environ, {"LANGCHAIN_TRACING_V2": "true"}):
            from importlib import reload
            import agent.config
            reload(agent.config)
            from agent.config import Config as ReloadedConfig
            assert ReloadedConfig.LANGCHAIN_TRACING_V2 is True

