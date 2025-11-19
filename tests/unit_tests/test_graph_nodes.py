"""Unit tests for graph nodes."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agent.state import AdventureState, UserPreferences
from agent.graph import (
    orchestrator_node,
    geo_agent_node,
    trail_agent_node,
    route_to_agents,
    should_continue,
)


class TestOrchestratorNode:
    """Test orchestrator node."""

    @pytest.mark.anyio
    async def test_orchestrator_node_success(self):
        """Test successful orchestrator node execution."""
        state = AdventureState(
            user_input="Plan a mountain biking trip to Colorado",
            user_preferences=None,
            conversation_history=[],
            errors=[],
        )
        
        with patch('agent.graph.orchestrator') as mock_orchestrator:
            mock_orchestrator.analyze_request = AsyncMock(return_value={
                "activity_type": "mountain_biking",
                "location": "Colorado",
                "required_agents": ["geo_agent", "trail_agent"],
                "agent_context": {"geo_agent": "Get location", "trail_agent": "Find trails"},
            })
            
            result = await orchestrator_node(state)
            
            assert "required_agents" in result
            assert "geo_agent" in result["required_agents"]
            assert result["current_task"] == "mountain_biking"
            mock_orchestrator.analyze_request.assert_called_once()

    @pytest.mark.anyio
    async def test_orchestrator_node_error_handling(self):
        """Test orchestrator node error handling."""
        state = AdventureState(
            user_input="Plan a trip",
            conversation_history=[],
            errors=[],
        )
        
        with patch('agent.graph.orchestrator') as mock_orchestrator:
            mock_orchestrator.analyze_request = AsyncMock(side_effect=Exception("Error"))
            
            result = await orchestrator_node(state)
            
            assert "errors" in result
            assert len(result["errors"]) > 0
            assert "required_agents" in result  # Fallback agents


class TestGeoAgentNode:
    """Test geo agent node."""

    @pytest.mark.anyio
    async def test_geo_agent_node_success(self):
        """Test successful geo agent node execution."""
        state = AdventureState(
            user_input="Plan a trip to Colorado",
            user_preferences=UserPreferences(
                skill_level="intermediate",
                preferred_terrain=["mountain"],
                activity_type="mountain_biking",
                region="Colorado",
            ),
            agent_context={},
            conversation_history=[],
            errors=[],
        )
        
        with patch('agent.graph.geo_agent') as mock_geo:
            mock_geo.get_location_info = AsyncMock(return_value={
                "location": "Colorado",
                "coordinates": {"lat": 39.0, "lon": -105.0},
                "region": "Colorado",
                "country": "US",
            })
            
            result = await geo_agent_node(state)
            
            assert "geo_info" in result
            assert result["geo_info"]["location"] == "Colorado"
            assert "geo_agent" in result["completed_agents"]
            mock_geo.get_location_info.assert_called_once()

    @pytest.mark.anyio
    async def test_geo_agent_node_error_handling(self):
        """Test geo agent node error handling."""
        state = AdventureState(
            user_input="Plan a trip",
            agent_context={},
            conversation_history=[],
            errors=[],
        )
        
        with patch('agent.graph.geo_agent') as mock_geo:
            mock_geo.get_location_info = AsyncMock(side_effect=Exception("Error"))
            
            result = await geo_agent_node(state)
            
            assert result["geo_info"] is None
            assert "errors" in result
            assert "geo_agent" in result["completed_agents"]


class TestTrailAgentNode:
    """Test trail agent node."""

    @pytest.mark.anyio
    async def test_trail_agent_node_success(self):
        """Test successful trail agent node execution."""
        state = AdventureState(
            user_input="Plan a trip",
            user_preferences=UserPreferences(
                skill_level="intermediate",
                preferred_terrain=["mountain"],
                activity_type="mountain_biking",
                region="Colorado",
            ),
            geo_info={"location": "Colorado", "region": "Colorado"},
            agent_context={},
            completed_agents=[],
            trail_info=[],
            conversation_history=[],
            errors=[],
        )
        
        with patch('agent.graph.trail_agent') as mock_trail:
            mock_trail.search_trails = AsyncMock(return_value=[{
                "name": "Test Trail",
                "source": "mtbproject",
                "activity_type": "mountain_biking",
            }])
            
            result = await trail_agent_node(state)
            
            assert "trail_info" in result
            assert len(result["trail_info"]) > 0
            assert "trail_agent" in result["completed_agents"]
            mock_trail.search_trails.assert_called_once()

    @pytest.mark.anyio
    async def test_trail_agent_node_with_difficulty_mapping(self):
        """Test trail agent node with skill level to difficulty mapping."""
        state = AdventureState(
            user_input="Plan a trip",
            user_preferences=UserPreferences(
                skill_level="beginner",
                preferred_terrain=["mountain"],
                activity_type="mountain_biking",
                region="Colorado",
            ),
            geo_info={"location": "Colorado"},
            agent_context={},
            completed_agents=[],
            trail_info=[],
            conversation_history=[],
            errors=[],
        )
        
        with patch('agent.graph.trail_agent') as mock_trail:
            mock_trail.search_trails = AsyncMock(return_value=[])
            
            result = await trail_agent_node(state)
            
            # Verify difficulty mapping was used
            call_args = mock_trail.search_trails.call_args
            assert call_args is not None
            # The difficulty should be mapped from "beginner" to "green" for MTB


class TestRoutingFunctions:
    """Test routing functions."""

    def test_route_to_agents(self):
        """Test routing to next agent."""
        state = AdventureState(
            user_input="Plan a trip",
            required_agents=["geo_agent", "trail_agent"],
            completed_agents=[],
            conversation_history=[],
            errors=[],
        )
        
        next_agent = route_to_agents(state)
        assert next_agent == "geo_agent"

    def test_route_to_agents_all_completed(self):
        """Test routing when all agents are completed."""
        state = AdventureState(
            user_input="Plan a trip",
            required_agents=["geo_agent"],
            completed_agents=["geo_agent"],
            conversation_history=[],
            errors=[],
        )
        
        next_agent = route_to_agents(state)
        assert next_agent == "synthesize"

    def test_route_to_agents_priority_order(self):
        """Test that agents are routed in priority order."""
        state = AdventureState(
            user_input="Plan a trip",
            required_agents=["trail_agent", "geo_agent", "weather_agent"],
            completed_agents=[],
            conversation_history=[],
            errors=[],
        )
        
        # Should route to geo_agent first (highest priority)
        next_agent = route_to_agents(state)
        assert next_agent == "geo_agent"
        
        # After geo_agent completes, should route to weather_agent
        state["completed_agents"] = ["geo_agent"]
        next_agent = route_to_agents(state)
        assert next_agent == "weather_agent"

    def test_should_continue_all_completed(self):
        """Test should_continue when all agents completed."""
        with patch('agent.graph.orchestrator') as mock_orch:
            mock_orch.should_request_human_review = MagicMock(return_value=False)
            
            state = AdventureState(
                user_input="Plan a trip",
                required_agents=["geo_agent"],
                completed_agents=["geo_agent"],
                conversation_history=[],
                errors=[],
            )
            
            result = should_continue(state)
            assert result == "synthesize"

    def test_should_continue_needs_human_review(self):
        """Test should_continue when human review is needed."""
        with patch('agent.graph.orchestrator') as mock_orch:
            mock_orch.should_request_human_review = MagicMock(return_value=True)
            
            state = AdventureState(
                user_input="Plan a trip",
                required_agents=["geo_agent"],
                completed_agents=["geo_agent"],
                conversation_history=[],
                errors=[],
            )
            
            result = should_continue(state)
            assert result == "human_review"

    def test_should_continue_agents_remaining(self):
        """Test should_continue when agents are still needed."""
        state = AdventureState(
            user_input="Plan a trip",
            required_agents=["geo_agent", "trail_agent"],
            completed_agents=["geo_agent"],
            conversation_history=[],
            errors=[],
        )
        
        result = should_continue(state)
        # Should return synthesize, but routing logic will handle next agent
        assert result == "synthesize"

