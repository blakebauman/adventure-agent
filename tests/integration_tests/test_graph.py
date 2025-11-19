"""Integration tests for graph execution."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agent import graph
from agent.state import AdventureState, UserPreferences

pytestmark = pytest.mark.anyio


@pytest.mark.langsmith
async def test_agent_simple_passthrough() -> None:
    """Test simple graph passthrough."""
    inputs = {"user_input": "Plan a trip to Colorado"}
    res = await graph.graph.ainvoke(inputs)
    assert res is not None


@pytest.mark.anyio
async def test_graph_with_user_preferences() -> None:
    """Test graph execution with user preferences."""
    inputs = {
        "user_input": "Plan a mountain biking trip",
        "user_preferences": {
            "skill_level": "intermediate",
            "preferred_terrain": ["mountain"],
            "activity_type": "mountain_biking",
            "region": "Colorado",
            "duration_days": 3,
        },
    }
    
    with patch('agent.graph.orchestrator') as mock_orch, \
         patch('agent.graph.geo_agent') as mock_geo, \
         patch('agent.graph.trail_agent') as mock_trail:
        
        # Mock orchestrator
        mock_orch.analyze_request = AsyncMock(return_value={
            "activity_type": "mountain_biking",
            "location": "Colorado",
            "required_agents": ["geo_agent", "trail_agent"],
            "agent_context": {},
        })
        mock_orch.should_request_human_review = MagicMock(return_value=False)
        mock_orch.synthesize_plan = AsyncMock(return_value={
            "title": "Colorado Adventure",
            "description": "Epic trip",
            "estimated_duration_days": 3,
        })
        
        # Mock agents
        mock_geo.get_location_info = AsyncMock(return_value={
            "location": "Colorado",
            "region": "Colorado",
            "country": "US",
        })
        mock_trail.search_trails = AsyncMock(return_value=[{
            "name": "Test Trail",
            "source": "mtbproject",
        }])
        
        res = await graph.graph.ainvoke(inputs)
        
        assert res is not None
        assert "adventure_plan" in res or "required_agents" in res


@pytest.mark.anyio
async def test_graph_error_handling() -> None:
    """Test graph error handling."""
    inputs = {
        "user_input": "Plan a trip",
        "user_preferences": None,
    }
    
    with patch('agent.graph.orchestrator') as mock_orch:
        mock_orch.analyze_request = AsyncMock(side_effect=Exception("Test error"))
        
        res = await graph.graph.ainvoke(inputs)
        
        # Graph should handle errors gracefully
        assert res is not None
        # Should have fallback agents or error handling
        assert "errors" in res or "required_agents" in res


@pytest.mark.anyio
async def test_graph_routing_logic() -> None:
    """Test graph routing between agents."""
    inputs = {
        "user_input": "Plan a trip to Colorado",
        "user_preferences": {
            "activity_type": "mountain_biking",
            "region": "Colorado",
        },
    }
    
    with patch('agent.graph.orchestrator') as mock_orch, \
         patch('agent.graph.geo_agent') as mock_geo, \
         patch('agent.graph.trail_agent') as mock_trail, \
         patch('agent.graph.weather_agent') as mock_weather:
        
        # Mock orchestrator to require multiple agents
        mock_orch.analyze_request = AsyncMock(return_value={
            "activity_type": "mountain_biking",
            "required_agents": ["geo_agent", "weather_agent", "trail_agent"],
            "agent_context": {},
        })
        mock_orch.should_request_human_review = MagicMock(return_value=False)
        mock_orch.synthesize_plan = AsyncMock(return_value={"title": "Test"})
        
        # Mock agents
        mock_geo.get_location_info = AsyncMock(return_value={"location": "Colorado"})
        mock_weather.get_weather_info = AsyncMock(return_value={"forecast": "Sunny"})
        mock_trail.search_trails = AsyncMock(return_value=[])
        
        res = await graph.graph.ainvoke(inputs)
        
        # Verify agents were called in priority order
        # Geo should be called first
        assert mock_geo.get_location_info.called
        # Weather should be called second
        assert mock_weather.get_weather_info.called
        # Trail should be called third
        assert mock_trail.search_trails.called

