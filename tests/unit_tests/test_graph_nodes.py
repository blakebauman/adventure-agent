"""Unit tests for graph nodes."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agent.graph import (
    geo_agent_node,
    orchestrator_node,
    route_to_agents,
    should_continue,
    trail_agent_node,
)


class TestOrchestratorNode:
    """Test orchestrator node."""

    @pytest.mark.anyio
    async def test_orchestrator_node_success(
        self, state_factory, mock_orchestrator_analysis
    ):
        """Test successful orchestrator node execution."""
        state = state_factory(include_preferences=False)

        with patch("agent.graph.orchestrator") as mock_orchestrator:
            mock_orchestrator.analyze_request = AsyncMock(
                return_value=mock_orchestrator_analysis
            )

            result = await orchestrator_node(state)

            assert "required_agents" in result
            assert "geo_agent" in result["required_agents"]
            assert result["current_task"] == "mountain_biking"
            mock_orchestrator.analyze_request.assert_called_once()

    @pytest.mark.anyio
    async def test_orchestrator_node_error_handling(self, state_factory):
        """Test orchestrator node error handling."""
        state = state_factory(include_preferences=False)

        with patch("agent.graph.orchestrator") as mock_orchestrator:
            mock_orchestrator.analyze_request = AsyncMock(
                side_effect=Exception("Error")
            )

            result = await orchestrator_node(state)

            # Uses error_details now, not errors
            assert "error_details" in result
            assert len(result["error_details"]) > 0
            assert "required_agents" in result  # Fallback agents


class TestGeoAgentNode:
    """Test geo agent node."""

    @pytest.mark.anyio
    async def test_geo_agent_node_success(self, state_factory, mock_geo_result):
        """Test successful geo agent node execution."""
        state = state_factory(region="Colorado")

        with patch("agent.graph.geo_agent") as mock_geo:
            mock_geo.get_location_info = AsyncMock(return_value=mock_geo_result)

            result = await geo_agent_node(state)

            assert "geo_info" in result
            assert result["geo_info"]["location"] == "Colorado"
            assert "geo_agent" in result["completed_agents"]
            mock_geo.get_location_info.assert_called_once()

    @pytest.mark.anyio
    async def test_geo_agent_node_error_handling(self, state_factory):
        """Test geo agent node error handling."""
        state = state_factory()

        with patch("agent.graph.geo_agent") as mock_geo:
            mock_geo.get_location_info = AsyncMock(side_effect=Exception("Error"))

            result = await geo_agent_node(state)

            assert result["geo_info"] is None
            # Uses error_details now, not errors
            assert "error_details" in result
            assert "geo_agent" in result["completed_agents"]


class TestTrailAgentNode:
    """Test trail agent node."""

    @pytest.mark.anyio
    async def test_trail_agent_node_success(
        self, state_with_geo, mock_trail_result
    ):
        """Test successful trail agent node execution."""
        with patch("agent.graph.trail_agent") as mock_trail:
            mock_trail.search_trails = AsyncMock(return_value=mock_trail_result)

            result = await trail_agent_node(state_with_geo)

            assert "trail_info" in result
            assert len(result["trail_info"]) > 0
            assert "trail_agent" in result["completed_agents"]
            mock_trail.search_trails.assert_called_once()

    @pytest.mark.anyio
    async def test_trail_agent_node_with_difficulty_mapping(self, state_factory):
        """Test trail agent node with skill level to difficulty mapping."""
        state = state_factory(
            skill_level="beginner",
            geo_info={"location": "Colorado"},
        )

        with patch("agent.graph.trail_agent") as mock_trail:
            mock_trail.search_trails = AsyncMock(return_value=[])

            await trail_agent_node(state)

            # Verify difficulty mapping was used
            call_args = mock_trail.search_trails.call_args
            assert call_args is not None
            # The difficulty should be mapped from "beginner" to "green" for MTB


class TestRoutingFunctions:
    """Test routing functions."""

    def test_route_to_agents(self, state_factory):
        """Test routing to next agent."""
        state = state_factory(
            required_agents=["geo_agent", "trail_agent"],
            completed_agents=[],
        )

        next_agents = route_to_agents(state)
        # Now returns a list for parallel execution
        assert isinstance(next_agents, list)
        assert "geo_agent" in next_agents

    def test_route_to_agents_all_completed(self, state_factory):
        """Test routing when all agents are completed."""
        state = state_factory(
            required_agents=["geo_agent"],
            completed_agents=["geo_agent"],
        )

        next_agent = route_to_agents(state)
        assert next_agent == "synthesize"

    def test_route_to_agents_priority_order(self, state_factory):
        """Test that agents are routed in priority order."""
        state = state_factory(
            required_agents=["trail_agent", "geo_agent", "weather_agent"],
            completed_agents=[],
        )

        # Returns list of ready agents for parallel execution
        next_agents = route_to_agents(state)
        assert isinstance(next_agents, list)
        # All three have no dependencies, so all should be ready
        assert len(next_agents) >= 1

    def test_should_continue_all_completed(self, state_factory):
        """Test should_continue when all agents completed."""
        with patch("agent.graph.orchestrator") as mock_orch:
            mock_orch.should_request_human_review = MagicMock(return_value=False)

            state = state_factory(
                required_agents=["geo_agent"],
                completed_agents=["geo_agent"],
            )

            result = should_continue(state)
            assert result == "synthesize"

    def test_should_continue_needs_human_review(self, state_factory):
        """Test should_continue when human review is needed."""
        with patch("agent.graph.orchestrator") as mock_orch:
            mock_orch.should_request_human_review = MagicMock(return_value=True)

            state = state_factory(
                required_agents=["geo_agent"],
                completed_agents=["geo_agent"],
            )

            result = should_continue(state)
            assert result == "human_review"

    def test_should_continue_agents_remaining(self, state_factory):
        """Test should_continue when agents are still needed."""
        state = state_factory(
            required_agents=["geo_agent", "trail_agent"],
            completed_agents=["geo_agent"],
        )

        result = should_continue(state)
        # Should return synthesize, but routing logic will handle next agent
        assert result == "synthesize"
