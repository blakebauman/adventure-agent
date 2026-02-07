"""Pytest configuration and shared fixtures for adventure agent tests."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from agent.state import AdventureState, UserPreferences


@pytest.fixture(scope="session")
def anyio_backend():
    """Configure anyio to use asyncio backend."""
    return "asyncio"


# =============================================================================
# State Factory Fixtures
# =============================================================================


@pytest.fixture
def user_prefs_factory():
    """Factory for creating UserPreferences with sensible defaults.

    Usage:
        prefs = user_prefs_factory()  # Get defaults
        prefs = user_prefs_factory(skill_level="expert", region="Arizona")
    """

    def _create(
        skill_level: str = "intermediate",
        activity_type: str = "mountain_biking",
        region: str = "Colorado",
        duration_days: int | None = None,
        accommodation_preference: str | None = None,
        **kwargs: Any,
    ) -> UserPreferences:
        prefs: UserPreferences = {
            "skill_level": skill_level,
            "activity_type": activity_type,
            "region": region,
            "preferred_terrain": kwargs.pop("preferred_terrain", ["mountain"]),
        }
        if duration_days is not None:
            prefs["duration_days"] = duration_days
        if accommodation_preference is not None:
            prefs["accommodation_preference"] = accommodation_preference
        # Add any extra kwargs
        prefs.update(kwargs)
        return prefs

    return _create


@pytest.fixture
def state_factory(user_prefs_factory):
    """Factory for creating AdventureState with sensible defaults.

    Reduces test boilerplate by providing a state with common defaults.
    Override any field by passing it as a keyword argument.

    Usage:
        state = state_factory()  # Get minimal valid state
        state = state_factory(region="Arizona", skill_level="expert")
        state = state_factory(geo_info={"location": "Sedona"})
        state = state_factory(user_preferences=None)  # No preferences
    """

    def _create(
        user_input: str = "Plan a mountain biking trip",
        region: str = "Colorado",
        skill_level: str = "intermediate",
        activity_type: str = "mountain_biking",
        include_preferences: bool = True,
        **overrides: Any,
    ) -> AdventureState:
        # Build user preferences unless explicitly disabled
        user_preferences = None
        if include_preferences and "user_preferences" not in overrides:
            user_preferences = user_prefs_factory(
                skill_level=skill_level,
                activity_type=activity_type,
                region=region,
            )
        elif "user_preferences" in overrides:
            user_preferences = overrides.pop("user_preferences")

        # Build base state with required fields
        state: AdventureState = {
            "user_input": user_input,
            "user_preferences": user_preferences,
            "agent_context": overrides.pop("agent_context", {}),
            "required_agents": overrides.pop("required_agents", []),
            "completed_agents": overrides.pop("completed_agents", []),
            "conversation_history": overrides.pop("conversation_history", []),
            "error_details": overrides.pop("error_details", []),
        }

        # Apply any remaining overrides
        state.update(overrides)

        return state

    return _create


# =============================================================================
# Sample Data Fixtures
# =============================================================================


@pytest.fixture
def sample_geo_info():
    """Sample geo_info data for testing."""
    return {
        "location": "Colorado",
        "coordinates": {"lat": 39.5501, "lon": -105.7821},
        "region": "Colorado",
        "country": "US",
        "description": "Rocky Mountain region",
    }


@pytest.fixture
def sample_trail_info():
    """Sample trail_info list for testing."""
    return [
        {
            "name": "Test Trail",
            "source": "mtbproject",
            "activity_type": "mountain_biking",
            "difficulty": "blue",
            "length_miles": 10.5,
            "elevation_gain": 1200,
            "description": "A fun intermediate trail",
        },
        {
            "name": "Advanced Loop",
            "source": "mtbproject",
            "activity_type": "mountain_biking",
            "difficulty": "black",
            "length_miles": 15.0,
            "elevation_gain": 2000,
        },
    ]


@pytest.fixture
def sample_weather_info():
    """Sample weather_info data for testing."""
    return {
        "location": "Colorado",
        "current": {
            "temperature": 72,
            "conditions": "Sunny",
            "wind_speed": 5,
        },
        "forecast": [
            {"day": "Monday", "high": 75, "low": 55, "conditions": "Sunny"},
            {"day": "Tuesday", "high": 70, "low": 50, "conditions": "Partly Cloudy"},
        ],
        "trail_conditions": "Dry and excellent",
    }


@pytest.fixture
def sample_accommodation_info():
    """Sample accommodation_info list for testing."""
    return [
        {
            "name": "Mountain Campground",
            "type": "campground",
            "location": "Colorado",
            "price_range": "$20-40",
            "amenities": ["restrooms", "fire pits", "water"],
        },
        {
            "name": "Trail Head Lodge",
            "type": "hotel",
            "location": "Colorado",
            "price_range": "$100-150",
            "amenities": ["wifi", "breakfast", "bike storage"],
        },
    ]


# =============================================================================
# Mock Fixtures
# =============================================================================


@pytest.fixture
def mock_llm():
    """Create a mock LLM for testing agents."""
    llm = AsyncMock()
    llm.ainvoke = AsyncMock(
        return_value=MagicMock(content='{"result": "mock response"}')
    )
    return llm


@pytest.fixture
def mock_orchestrator_analysis():
    """Mock return value for orchestrator.analyze_request."""
    return {
        "activity_type": "mountain_biking",
        "location": "Colorado",
        "duration_days": 3,
        "skill_level": "intermediate",
        "required_agents": ["geo_agent", "trail_agent", "weather_agent"],
        "agent_context": {
            "geo_agent": "Get location info for Colorado",
            "trail_agent": "Find mountain biking trails",
            "weather_agent": "Get weather forecast",
        },
    }


@pytest.fixture
def mock_geo_result(sample_geo_info):
    """Mock return value for geo_agent.get_location_info."""
    return sample_geo_info


@pytest.fixture
def mock_trail_result(sample_trail_info):
    """Mock return value for trail_agent.search_trails."""
    return sample_trail_info


@pytest.fixture
def mock_weather_result(sample_weather_info):
    """Mock return value for weather_agent.get_weather_info."""
    return sample_weather_info


# =============================================================================
# State with Pre-populated Data
# =============================================================================


@pytest.fixture
def state_with_geo(state_factory, sample_geo_info):
    """Create a state with geo_info already populated."""
    return state_factory(geo_info=sample_geo_info)


@pytest.fixture
def state_with_trails(state_factory, sample_geo_info, sample_trail_info):
    """Create a state with geo_info and trail_info populated."""
    return state_factory(
        geo_info=sample_geo_info,
        trail_info=sample_trail_info,
        completed_agents=["geo_agent", "trail_agent"],
    )


@pytest.fixture
def state_ready_for_synthesis(
    state_factory,
    sample_geo_info,
    sample_trail_info,
    sample_weather_info,
):
    """Create a state with all core agent data, ready for synthesis."""
    return state_factory(
        geo_info=sample_geo_info,
        trail_info=sample_trail_info,
        weather_info=sample_weather_info,
        required_agents=["geo_agent", "trail_agent", "weather_agent"],
        completed_agents=["geo_agent", "trail_agent", "weather_agent"],
    )
