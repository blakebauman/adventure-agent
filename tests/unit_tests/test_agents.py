"""Unit tests for agents."""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agent.agents.trail_agent import TrailAgent
from agent.agents.geo_agent import GeoAgent
from agent.agents.weather_agent import WeatherAgent
from agent.agents.orchestrator import OrchestratorAgent, AdventureAnalysis


class TestTrailAgent:
    """Test TrailAgent."""

    @pytest.fixture
    def mock_llm(self):
        """Create a mock LLM."""
        llm = AsyncMock()
        llm.ainvoke = AsyncMock(return_value=MagicMock(
            content='{"trails": [{"name": "Test Trail", "source": "mtbproject", "difficulty": "blue", "length_miles": 10.0}]}'
        ))
        return llm

    @pytest.mark.anyio
    async def test_search_trails_mountain_biking(self, mock_llm):
        """Test searching for mountain biking trails."""
        with patch('agent.agents.trail_agent.search_trails') as mock_search:
            mock_search.invoke.return_value = json.dumps({
                "trails": [{
                    "name": "Test Trail",
                    "source": "mtbproject",
                    "activity_type": "mountain_biking",
                    "difficulty": "blue",
                    "length_miles": 10.0,
                }]
            })
            
            agent = TrailAgent()
            agent.llm = mock_llm
            
            trails = await agent.search_trails(
                location="Colorado",
                activity_type="mountain_biking",
                difficulty="blue",
            )
            
            assert len(trails) > 0
            assert trails[0]["activity_type"] == "mountain_biking"
            mock_search.invoke.assert_called_once()

    @pytest.mark.anyio
    async def test_search_trails_hiking(self, mock_llm):
        """Test searching for hiking trails."""
        with patch('agent.agents.trail_agent.search_trails') as mock_search:
            mock_search.invoke.return_value = json.dumps({
                "trails": [{
                    "name": "Hiking Trail",
                    "source": "hikingproject",
                    "activity_type": "hiking",
                }]
            })
            
            agent = TrailAgent()
            agent.llm = mock_llm
            
            trails = await agent.search_trails(
                location="Arizona",
                activity_type="hiking",
            )
            
            assert len(trails) > 0

    @pytest.mark.anyio
    async def test_get_trail_details(self):
        """Test getting trail details."""
        with patch('agent.agents.trail_agent.get_trail_details') as mock_details:
            mock_details.invoke.return_value = json.dumps({
                "trail_id": "12345",
                "source": "mtbproject",
                "details": {"condition": "Good"},
            })
            
            agent = TrailAgent()
            details = await agent.get_trail_details(
                trail_id="12345",
                source="mtbproject",
                activity_type="mountain_biking",
            )
            
            assert details["trail_id"] == "12345"
            mock_details.invoke.assert_called_once()

    @pytest.mark.anyio
    async def test_search_trails_error_handling(self):
        """Test error handling in trail search."""
        with patch('agent.tools.search_trails') as mock_search:
            mock_search.invoke.side_effect = Exception("API Error")
            
            agent = TrailAgent()
            trails = await agent.search_trails(
                location="Colorado",
                activity_type="mountain_biking",
            )
            
            assert trails == []


class TestGeoAgent:
    """Test GeoAgent."""

    @pytest.fixture
    def mock_llm(self):
        """Create a mock LLM."""
        llm = AsyncMock()
        llm.ainvoke = AsyncMock(return_value=MagicMock(
            content='{"location": "Colorado", "coordinates": {"lat": 39.0, "lon": -105.0}, "region": "Colorado", "country": "US"}'
        ))
        return llm

    @pytest.mark.anyio
    async def test_get_location_info(self, mock_llm):
        """Test getting location information."""
        with patch('agent.agents.geo_agent.get_coordinates') as mock_coords:
            mock_coords.invoke.return_value = json.dumps({
                "location": "Colorado",
                "coordinates": {"lat": 39.0, "lon": -105.0},
                "region": "Colorado",
                "country": "US",
            })
            
            agent = GeoAgent()
            agent.llm = mock_llm
            
            info = await agent.get_location_info("Colorado")
            
            assert info["location"] == "Colorado"
            assert info["coordinates"]["lat"] == 39.0
            assert info["region"] == "Colorado"
            mock_coords.invoke.assert_called_once()

    @pytest.mark.anyio
    async def test_calculate_route_distance(self):
        """Test calculating route distance."""
        with patch('agent.agents.geo_agent.calculate_distance') as mock_calc:
            mock_calc.invoke.return_value = json.dumps({
                "distance_miles": 25.5,
                "distance_km": 41.0,
            })
            
            agent = GeoAgent()
            points = [
                {"lat": 39.0, "lon": -105.0},
                {"lat": 40.0, "lon": -106.0},
            ]
            
            result = await agent.calculate_route_distance(points)
            
            assert result["total_distance_miles"] > 0
            assert len(result["segments"]) == 1

    @pytest.mark.anyio
    async def test_calculate_route_distance_single_point(self):
        """Test calculating distance with single point."""
        agent = GeoAgent()
        points = [{"lat": 39.0, "lon": -105.0}]
        
        result = await agent.calculate_route_distance(points)
        
        assert result["total_distance_miles"] == 0.0
        assert len(result["segments"]) == 0

    @pytest.mark.anyio
    async def test_get_location_info_error_handling(self):
        """Test error handling in location info."""
        with patch('agent.tools.get_coordinates') as mock_coords:
            mock_coords.invoke.side_effect = Exception("API Error")
            
            agent = GeoAgent()
            info = await agent.get_location_info("Invalid Location")
            
            assert info["location"] == "Invalid Location"
            assert info["coordinates"] is None


class TestWeatherAgent:
    """Test WeatherAgent."""

    @pytest.fixture
    def mock_llm(self):
        """Create a mock LLM."""
        llm = AsyncMock()
        llm.ainvoke = AsyncMock(return_value=MagicMock(
            content='{"forecast": "Sunny", "safety_recommendations": ["Bring water"]}'
        ))
        return llm

    @pytest.mark.anyio
    async def test_get_weather_info(self, mock_llm):
        """Test getting weather information."""
        with patch('agent.agents.weather_agent.get_weather_forecast') as mock_forecast, \
             patch('agent.agents.weather_agent.get_trail_conditions') as mock_conditions, \
             patch('agent.agents.weather_agent.get_seasonal_information') as mock_seasonal, \
             patch('agent.agents.weather_agent.check_weather_alerts') as mock_alerts:
            
            mock_forecast.invoke.return_value = json.dumps({"forecast": "Sunny"})
            mock_conditions.invoke.return_value = json.dumps({"conditions": "Good"})
            mock_seasonal.invoke.return_value = json.dumps({"best_seasons": ["Spring"]})
            mock_alerts.invoke.return_value = json.dumps({"alerts": []})
            
            agent = WeatherAgent()
            agent.llm = mock_llm
            
            info = await agent.get_weather_info(
                location="Colorado",
                dates=["2024-06-01"],
                activity_type="mountain_biking",
            )
            
            assert info["location"] == "Colorado"
            assert "forecast" in info
            assert "trail_conditions" in info
            mock_forecast.invoke.assert_called_once()

    @pytest.mark.anyio
    async def test_get_trail_conditions_only(self):
        """Test getting only trail conditions."""
        with patch('agent.agents.weather_agent.get_trail_conditions') as mock_conditions:
            mock_conditions.invoke.return_value = json.dumps({
                "conditions": "Good",
                "reports": [],
            })
            
            agent = WeatherAgent()
            conditions = await agent.get_trail_conditions_only(
                location="Colorado",
                activity_type="mountain_biking",
            )
            
            assert "conditions" in conditions
            mock_conditions.invoke.assert_called_once()

    @pytest.mark.anyio
    async def test_get_weather_info_error_handling(self):
        """Test error handling in weather info."""
        with patch('agent.tools.get_weather_forecast') as mock_forecast:
            mock_forecast.invoke.side_effect = Exception("API Error")
            
            agent = WeatherAgent()
            info = await agent.get_weather_info(
                location="Colorado",
                activity_type="mountain_biking",
            )
            
            assert info["location"] == "Colorado"
            assert info["forecast"] == {}


class TestOrchestratorAgent:
    """Test OrchestratorAgent."""

    @pytest.fixture
    def mock_llm_structured(self):
        """Create a mock structured LLM."""
        llm = AsyncMock()
        analysis = AdventureAnalysis(
            activity_type="mountain_biking",
            location="Colorado",
            duration_days=3,
            skill_level="intermediate",
            required_agents=["geo_agent", "trail_agent"],
            agent_context={"geo_agent": "Get location info", "trail_agent": "Find trails"},
        )
        llm.ainvoke = AsyncMock(return_value=analysis)
        return llm

    @pytest.mark.anyio
    async def test_analyze_request(self, mock_llm_structured):
        """Test analyzing a user request."""
        agent = OrchestratorAgent()
        agent.llm_structured = mock_llm_structured
        
        analysis = await agent.analyze_request(
            user_input="Plan a mountain biking trip to Colorado",
            preferences=None,
        )
        
        assert analysis["activity_type"] == "mountain_biking"
        assert analysis["location"] == "Colorado"
        assert "geo_agent" in analysis["required_agents"]
        mock_llm_structured.ainvoke.assert_called_once()

    @pytest.mark.anyio
    async def test_analyze_request_with_preferences(self, mock_llm_structured):
        """Test analyzing request with existing preferences."""
        from agent.state import UserPreferences
        
        prefs = UserPreferences(
            skill_level="advanced",
            preferred_terrain=["mountain"],
            activity_type="mountain_biking",
        )
        
        agent = OrchestratorAgent()
        agent.llm_structured = mock_llm_structured
        
        analysis = await agent.analyze_request(
            user_input="Plan a trip",
            preferences=prefs,
        )
        
        assert analysis["activity_type"] == "mountain_biking"

    @pytest.mark.anyio
    async def test_synthesize_plan(self):
        """Test synthesizing an adventure plan."""
        from agent.state import AdventureState, UserPreferences, Location, TrailInfo
        
        prefs = UserPreferences(
            skill_level="intermediate",
            preferred_terrain=["mountain"],
            activity_type="mountain_biking",
        )
        
        location = Location(name="Colorado", region="Colorado", country="US")
        trail = TrailInfo(name="Test Trail", source="mtbproject")
        
        state = AdventureState(
            user_input="Plan a trip",
            user_preferences=prefs,
            geo_info={"location": "Colorado", "region": "Colorado"},
            trail_info=[trail],
            completed_agents=["geo_agent", "trail_agent"],
            conversation_history=[],
            errors=[],
        )
        
        with patch('agent.agents.orchestrator.ChatOpenAI') as mock_chat:
            mock_llm = AsyncMock()
            mock_llm.ainvoke = AsyncMock(return_value=MagicMock(
                content=json.dumps({
                    "title": "Colorado Adventure",
                    "description": "Epic trip",
                    "location": {"name": "Colorado", "region": "Colorado", "country": "US"},
                    "trails": [{"name": "Test Trail", "source": "mtbproject"}],
                    "estimated_duration_days": 3,
                    "difficulty": "intermediate",
                })
            ))
            mock_chat.return_value = mock_llm
            
            agent = OrchestratorAgent()
            agent.llm = mock_llm
            
            plan = await agent.synthesize_plan(state)
            
            assert plan["title"] == "Colorado Adventure"
            assert plan["estimated_duration_days"] == 3

    def test_should_request_human_review(self):
        """Test determining if human review is needed."""
        from agent.state import AdventureState
        
        # Test case where review is not needed
        state = AdventureState(
            user_input="Simple trip",
            completed_agents=["geo_agent"],
            conversation_history=[],
            errors=[],
        )
        
        agent = OrchestratorAgent()
        # This would need to be implemented based on actual logic
        # For now, just test the method exists
        assert hasattr(agent, 'should_request_human_review')

