"""Integration tests for agent interactions."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agent.agents.trail_agent import TrailAgent
from agent.agents.geo_agent import GeoAgent
from agent.agents.weather_agent import WeatherAgent
from agent.agents.orchestrator import OrchestratorAgent


class TestAgentIntegration:
    """Test agent integration scenarios."""

    @pytest.mark.anyio
    async def test_geo_and_trail_agent_flow(self):
        """Test flow from geo agent to trail agent."""
        # Mock geo agent
        geo_agent = GeoAgent()
        with patch('agent.agents.geo_agent.get_coordinates') as mock_coords:
            mock_coords.invoke.return_value = '{"location": "Colorado", "coordinates": {"lat": 39.0, "lon": -105.0}, "region": "Colorado", "country": "US"}'
            
            with patch.object(geo_agent, 'llm') as mock_llm:
                mock_llm.ainvoke = AsyncMock(return_value=MagicMock(
                    content='{"location": "Colorado", "coordinates": {"lat": 39.0, "lon": -105.0}, "region": "Colorado"}'
                ))
                
                geo_info = await geo_agent.get_location_info("Colorado")
                assert geo_info["location"] == "Colorado"
        
        # Mock trail agent using geo info
        trail_agent = TrailAgent()
        with patch('agent.agents.trail_agent.search_trails') as mock_search:
            mock_search.invoke.return_value = '{"trails": [{"name": "Test Trail", "source": "mtbproject", "activity_type": "mountain_biking"}]}'
            
            with patch.object(trail_agent, 'llm') as mock_llm:
                mock_llm.ainvoke = AsyncMock(return_value=MagicMock(
                    content='{"trails": [{"name": "Test Trail", "source": "mtbproject"}]}'
                ))
                
                trails = await trail_agent.search_trails(
                    location=geo_info["location"],
                    activity_type="mountain_biking",
                )
                assert len(trails) > 0
                assert trails[0]["name"] == "Test Trail"

    @pytest.mark.anyio
    async def test_orchestrator_to_agents_flow(self):
        """Test flow from orchestrator to multiple agents."""
        orchestrator = OrchestratorAgent()
        
        with patch.object(orchestrator, 'llm_structured') as mock_structured:
            from agent.agents.orchestrator import AdventureAnalysis
            analysis = AdventureAnalysis(
                activity_type="mountain_biking",
                location="Colorado",
                required_agents=["geo_agent", "trail_agent", "weather_agent"],
                agent_context={
                    "geo_agent": "Get location info",
                    "trail_agent": "Find trails",
                    "weather_agent": "Check weather",
                },
            )
            mock_structured.ainvoke = AsyncMock(return_value=analysis)
            
            result = await orchestrator.analyze_request(
                user_input="Plan a mountain biking trip to Colorado",
                preferences=None,
            )
            
            assert result["activity_type"] == "mountain_biking"
            assert len(result["required_agents"]) == 3
            assert "geo_agent" in result["required_agents"]
            assert "trail_agent" in result["required_agents"]
            assert "weather_agent" in result["required_agents"]

    @pytest.mark.anyio
    async def test_weather_agent_with_dates(self):
        """Test weather agent with specific dates."""
        weather_agent = WeatherAgent()
        
        with patch('agent.agents.weather_agent.get_weather_forecast') as mock_forecast, \
             patch('agent.agents.weather_agent.get_trail_conditions') as mock_conditions, \
             patch('agent.agents.weather_agent.get_seasonal_information') as mock_seasonal, \
             patch('agent.agents.weather_agent.check_weather_alerts') as mock_alerts:
            
            mock_forecast.invoke.return_value = '{"forecast": {"daily": [{"date": "2024-06-01", "high": 70}]}}'
            mock_conditions.invoke.return_value = '{"conditions": "Good"}'
            mock_seasonal.invoke.return_value = '{"best_seasons": ["Spring"]}'
            mock_alerts.invoke.return_value = '{"alerts": []}'
            
            with patch.object(weather_agent, 'llm') as mock_llm:
                mock_llm.ainvoke = AsyncMock(return_value=MagicMock(
                    content='{"forecast": "Sunny", "safety_recommendations": ["Bring water"]}'
                ))
                
                weather_info = await weather_agent.get_weather_info(
                    location="Colorado",
                    dates=["2024-06-01", "2024-06-02"],
                    activity_type="mountain_biking",
                )
                
                assert weather_info["location"] == "Colorado"
                assert "forecast" in weather_info
                # Verify dates were passed to forecast
                mock_forecast.invoke.assert_called_once()
                call_args = mock_forecast.invoke.call_args[0][0]
                assert "dates" in call_args

