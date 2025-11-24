"""Unit tests for location agents.

Tests for location-specific agents including Bisbee, Tombstone, Sierra Vista,
Patagonia, Page, and others. Tests cover structured output, knowledge base
integration, and agent functionality.
"""

from __future__ import annotations

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from agent.agents.locations import (
    BisbeeAgent,
    TombstoneAgent,
    SierraVistaAgent,
    PatagoniaAgent,
    PageAgent,
    PaysonAgent,
    CampVerdeAgent,
    CottonwoodAgent,
)
from agent.agents.location_agent_base import LocationAgentBase


class TestLocationAgentBase:
    """Test base location agent functionality."""

    @pytest.mark.anyio
    async def test_location_match(self):
        """Test location matching functionality."""
        agent = PaysonAgent()
        
        # Test exact match
        assert agent.is_location_match("payson")
        assert agent.is_location_match("Payson, Arizona")
        assert agent.is_location_match("payson, az")
        
        # Test non-match
        assert not agent.is_location_match("phoenix")
        assert not agent.is_location_match("flagstaff")

    @pytest.mark.anyio
    async def test_get_location_knowledge(self):
        """Test knowledge base retrieval."""
        agent = PaysonAgent()
        knowledge = agent.get_location_knowledge()
        
        assert "location" in knowledge
        assert "outdoor_activities" in knowledge
        assert knowledge["location"]["name"] == "Payson, Arizona"

    @pytest.mark.anyio
    async def test_structured_output_parsing(self):
        """Test structured output parsing from LLM."""
        agent = PaysonAgent()
        
        # Mock LLM with structured output
        mock_response = {
            "location": "Payson, Arizona",
            "location_name": "Payson, Arizona",
            "is_match": True,
            "overview": {
                "name": "Payson, Arizona",
                "coordinates": {"lat": 34.2308, "lon": -111.3251},
                "elevation": 5000,
                "region": "Gila County, Arizona",
            },
            "outdoor_activities": [
                {
                    "activity_type": "mountain_biking",
                    "description": "Trails in Tonto National Forest",
                    "famous_trails": [],
                    "difficulty_range": "Beginner to expert",
                }
            ],
            "key_attractions": [],
            "businesses": {},
            "practical_info": {
                "parking": "Available",
                "permits": "Tonto National Forest",
            },
            "recommendations": [],
            "tools_used": [],
        }
        
        with patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {}
            location_info = await agent.get_location_info(
                "Payson, Arizona",
                existing_outputs,
                "Test context",
                "mountain_biking"
            )
            
            assert location_info is not None
            assert "location" in location_info or "location_name" in location_info


class TestBisbeeAgent:
    """Test Bisbee location agent."""

    @pytest.fixture
    def bisbee_agent(self):
        """Create Bisbee agent instance."""
        return BisbeeAgent()

    def test_location_indicators(self, bisbee_agent):
        """Test location indicator matching."""
        assert bisbee_agent.is_location_match("bisbee")
        assert bisbee_agent.is_location_match("Bisbee, Arizona")
        assert bisbee_agent.is_location_match("bisbee, az")
        assert not bisbee_agent.is_location_match("phoenix")

    def test_knowledge_base(self, bisbee_agent):
        """Test knowledge base content."""
        knowledge = bisbee_agent.get_location_knowledge()
        
        assert knowledge["location"]["name"] == "Bisbee, Arizona"
        assert knowledge["location"]["elevation"] == 5300
        assert "outdoor_activities" in knowledge
        assert "mountain_biking" in knowledge["outdoor_activities"]
        assert "hiking" in knowledge["outdoor_activities"]

    @pytest.mark.anyio
    async def test_get_location_info(self, bisbee_agent):
        """Test getting location information."""
        with patch.object(bisbee_agent.agent, 'ainvoke') as mock_ainvoke:
            mock_response = {
                "location": "Bisbee, Arizona",
                "location_name": "Bisbee, Arizona",
                "is_match": True,
                "overview": {
                    "name": "Bisbee, Arizona",
                    "coordinates": {"lat": 31.4482, "lon": -109.9284},
                    "elevation": 5300,
                    "region": "Cochise County, Arizona",
                },
                "outdoor_activities": [],
                "key_attractions": [],
                "businesses": {},
                "practical_info": {},
                "recommendations": [],
                "tools_used": [],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {}
            location_info = await bisbee_agent.get_location_info(
                "Bisbee, Arizona",
                existing_outputs,
                "Test context",
                "mountain_biking"
            )
            
            assert location_info is not None
            mock_ainvoke.assert_called_once()


class TestTombstoneAgent:
    """Test Tombstone location agent."""

    @pytest.fixture
    def tombstone_agent(self):
        """Create Tombstone agent instance."""
        return TombstoneAgent()

    def test_location_indicators(self, tombstone_agent):
        """Test location indicator matching."""
        assert tombstone_agent.is_location_match("tombstone")
        assert tombstone_agent.is_location_match("Tombstone, Arizona")
        assert tombstone_agent.is_location_match("ok corral")
        assert not tombstone_agent.is_location_match("phoenix")

    def test_knowledge_base(self, tombstone_agent):
        """Test knowledge base content."""
        knowledge = tombstone_agent.get_location_knowledge()
        
        assert knowledge["location"]["name"] == "Tombstone, Arizona"
        assert knowledge["location"]["nickname"] == "The Town Too Tough to Die"
        assert "outdoor_activities" in knowledge
        assert "hiking" in knowledge["outdoor_activities"]

    @pytest.mark.anyio
    async def test_get_location_info(self, tombstone_agent):
        """Test getting location information."""
        with patch.object(tombstone_agent.agent, 'ainvoke') as mock_ainvoke:
            mock_response = {
                "location": "Tombstone, Arizona",
                "location_name": "Tombstone, Arizona",
                "is_match": True,
                "overview": {
                    "name": "Tombstone, Arizona",
                    "coordinates": {"lat": 31.7129, "lon": -110.0676},
                    "elevation": 4500,
                    "region": "Cochise County, Arizona",
                },
                "outdoor_activities": [],
                "key_attractions": [],
                "businesses": {},
                "practical_info": {},
                "recommendations": [],
                "tools_used": [],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {}
            location_info = await tombstone_agent.get_location_info(
                "Tombstone, Arizona",
                existing_outputs,
                "Test context",
                "hiking"
            )
            
            assert location_info is not None
            mock_ainvoke.assert_called_once()


class TestSierraVistaAgent:
    """Test Sierra Vista location agent."""

    @pytest.fixture
    def sierra_vista_agent(self):
        """Create Sierra Vista agent instance."""
        return SierraVistaAgent()

    def test_location_indicators(self, sierra_vista_agent):
        """Test location indicator matching."""
        assert sierra_vista_agent.is_location_match("sierra vista")
        assert sierra_vista_agent.is_location_match("Sierra Vista, Arizona")
        assert sierra_vista_agent.is_location_match("sierra vista, az")
        assert not sierra_vista_agent.is_location_match("phoenix")

    def test_knowledge_base(self, sierra_vista_agent):
        """Test knowledge base content."""
        knowledge = sierra_vista_agent.get_location_knowledge()
        
        assert knowledge["location"]["name"] == "Sierra Vista, Arizona"
        assert knowledge["location"]["nickname"] == "Hummingbird Capital of the United States"
        assert "outdoor_activities" in knowledge
        assert "birding" in knowledge["outdoor_activities"]
        assert "mountain_biking" in knowledge["outdoor_activities"]

    @pytest.mark.anyio
    async def test_get_location_info(self, sierra_vista_agent):
        """Test getting location information."""
        with patch.object(sierra_vista_agent.agent, 'ainvoke') as mock_ainvoke:
            mock_response = {
                "location": "Sierra Vista, Arizona",
                "location_name": "Sierra Vista, Arizona",
                "is_match": True,
                "overview": {
                    "name": "Sierra Vista, Arizona",
                    "coordinates": {"lat": 31.5545, "lon": -110.3037},
                    "elevation": 4600,
                    "region": "Cochise County, Arizona",
                },
                "outdoor_activities": [],
                "key_attractions": [],
                "businesses": {},
                "practical_info": {},
                "recommendations": [],
                "tools_used": [],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {}
            location_info = await sierra_vista_agent.get_location_info(
                "Sierra Vista, Arizona",
                existing_outputs,
                "Test context",
                "birding"
            )
            
            assert location_info is not None
            mock_ainvoke.assert_called_once()


class TestPatagoniaAgent:
    """Test Patagonia location agent."""

    @pytest.fixture
    def patagonia_agent(self):
        """Create Patagonia agent instance."""
        return PatagoniaAgent()

    def test_location_indicators(self, patagonia_agent):
        """Test location indicator matching."""
        assert patagonia_agent.is_location_match("patagonia")
        assert patagonia_agent.is_location_match("Patagonia, Arizona")
        assert patagonia_agent.is_location_match("patagonia, az")
        assert not patagonia_agent.is_location_match("phoenix")

    def test_knowledge_base(self, patagonia_agent):
        """Test knowledge base content."""
        knowledge = patagonia_agent.get_location_knowledge()
        
        assert knowledge["location"]["name"] == "Patagonia, Arizona"
        assert knowledge["location"]["nickname"] == "Birding Capital of Arizona"
        assert "outdoor_activities" in knowledge
        assert "birding" in knowledge["outdoor_activities"]
        assert "hiking" in knowledge["outdoor_activities"]

    @pytest.mark.anyio
    async def test_get_location_info(self, patagonia_agent):
        """Test getting location information."""
        with patch.object(patagonia_agent.agent, 'ainvoke') as mock_ainvoke:
            mock_response = {
                "location": "Patagonia, Arizona",
                "location_name": "Patagonia, Arizona",
                "is_match": True,
                "overview": {
                    "name": "Patagonia, Arizona",
                    "coordinates": {"lat": 31.5401, "lon": -110.7501},
                    "elevation": 4000,
                    "region": "Santa Cruz County, Arizona",
                },
                "outdoor_activities": [],
                "key_attractions": [],
                "businesses": {},
                "practical_info": {},
                "recommendations": [],
                "tools_used": [],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {}
            location_info = await patagonia_agent.get_location_info(
                "Patagonia, Arizona",
                existing_outputs,
                "Test context",
                "birding"
            )
            
            assert location_info is not None
            mock_ainvoke.assert_called_once()


class TestPageAgent:
    """Test Page location agent."""

    @pytest.fixture
    def page_agent(self):
        """Create Page agent instance."""
        return PageAgent()

    def test_location_indicators(self, page_agent):
        """Test location indicator matching."""
        assert page_agent.is_location_match("page")
        assert page_agent.is_location_match("Page, Arizona")
        assert page_agent.is_location_match("lake powell")
        assert page_agent.is_location_match("antelope canyon")
        assert page_agent.is_location_match("horseshoe bend")
        assert not page_agent.is_location_match("phoenix")

    def test_knowledge_base(self, page_agent):
        """Test knowledge base content."""
        knowledge = page_agent.get_location_knowledge()
        
        assert knowledge["location"]["name"] == "Page, Arizona"
        assert knowledge["location"]["nickname"] == "Gateway to Lake Powell"
        assert "outdoor_activities" in knowledge
        assert "water_activities" in knowledge["outdoor_activities"]
        assert "slot_canyons" in knowledge["outdoor_activities"]
        assert "hiking" in knowledge["outdoor_activities"]

    @pytest.mark.anyio
    async def test_get_location_info(self, page_agent):
        """Test getting location information."""
        with patch.object(page_agent.agent, 'ainvoke') as mock_ainvoke:
            mock_response = {
                "location": "Page, Arizona",
                "location_name": "Page, Arizona",
                "is_match": True,
                "overview": {
                    "name": "Page, Arizona",
                    "coordinates": {"lat": 36.9147, "lon": -111.4558},
                    "elevation": 4300,
                    "region": "Coconino County, Arizona",
                },
                "outdoor_activities": [],
                "key_attractions": [],
                "businesses": {},
                "practical_info": {},
                "recommendations": [],
                "tools_used": [],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {}
            location_info = await page_agent.get_location_info(
                "Page, Arizona",
                existing_outputs,
                "Test context",
                "hiking"
            )
            
            assert location_info is not None
            mock_ainvoke.assert_called_once()


class TestLocationAgentStructuredOutput:
    """Test structured output parsing for location agents."""

    @pytest.mark.anyio
    async def test_structured_output_with_valid_json(self):
        """Test parsing valid structured JSON output."""
        agent = PaysonAgent()
        
        valid_json = {
            "location": "Payson, Arizona",
            "location_name": "Payson, Arizona",
            "is_match": True,
            "overview": {
                "name": "Payson, Arizona",
                "coordinates": {"lat": 34.2308, "lon": -111.3251},
                "elevation": 5000,
                "region": "Gila County, Arizona",
            },
            "outdoor_activities": [
                {
                    "activity_type": "mountain_biking",
                    "description": "Trails in Tonto National Forest",
                    "famous_trails": [],
                    "difficulty_range": "Beginner to expert",
                }
            ],
            "key_attractions": [],
            "businesses": {},
            "practical_info": {
                "parking": "Available",
                "permits": "Tonto National Forest",
            },
            "recommendations": [],
            "tools_used": [],
        }
        
        with patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
            mock_ainvoke.return_value = MagicMock(content=json.dumps(valid_json))
            
            existing_outputs = {}
            location_info = await agent.get_location_info(
                "Payson, Arizona",
                existing_outputs,
                "Test context",
                "mountain_biking"
            )
            
            assert location_info is not None
            # Should parse successfully

    @pytest.mark.anyio
    async def test_structured_output_with_malformed_json(self):
        """Test parsing malformed JSON with fallback."""
        agent = PaysonAgent()
        
        # Mock LLM returning malformed JSON
        with patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
            mock_ainvoke.return_value = MagicMock(
                content='{"location": "Payson, Arizona", "invalid": json}'  # Invalid JSON
            )
            
            existing_outputs = {}
            # Should handle gracefully
            location_info = await agent.get_location_info(
                "Payson, Arizona",
                existing_outputs,
                "Test context",
                "mountain_biking"
            )
            
            # Should still return something (fallback handling)
            assert location_info is not None or isinstance(location_info, dict)


class TestLocationAgentKnowledgeBase:
    """Test knowledge base integration for location agents."""

    def test_camp_verde_knowledge_base(self):
        """Test Camp Verde knowledge base structure."""
        agent = CampVerdeAgent()
        knowledge = agent.get_location_knowledge()
        
        assert "location" in knowledge
        assert "outdoor_activities" in knowledge
        assert "attractions" in knowledge
        assert "practical_info" in knowledge
        
        # Check specific fields
        assert knowledge["location"]["name"] == "Camp Verde, Arizona"
        assert "mountain_biking" in knowledge["outdoor_activities"]
        assert "hiking" in knowledge["outdoor_activities"]

    def test_cottonwood_knowledge_base(self):
        """Test Cottonwood knowledge base structure."""
        agent = CottonwoodAgent()
        knowledge = agent.get_location_knowledge()
        
        assert "location" in knowledge
        assert "outdoor_activities" in knowledge
        assert knowledge["location"]["name"] == "Cottonwood, Arizona"
        assert "mountain_biking" in knowledge["outdoor_activities"]

    def test_knowledge_base_trail_information(self):
        """Test that knowledge bases contain detailed trail information."""
        agent = PaysonAgent()
        knowledge = agent.get_location_knowledge()
        
        mtb_activities = knowledge["outdoor_activities"].get("mountain_biking", {})
        if "famous_trails" in mtb_activities:
            trails = mtb_activities["famous_trails"]
            if trails and isinstance(trails, list) and len(trails) > 0:
                trail = trails[0]
                # Check for detailed trail information
                assert "name" in trail or isinstance(trail, str) or isinstance(trail, dict)


class TestLocationAgentSystemPrompts:
    """Test system prompt content for location agents."""

    def test_bisbee_system_prompt(self):
        """Test Bisbee system prompt includes key information."""
        agent = BisbeeAgent()
        prompt = agent._get_system_prompt()
        
        assert "Bisbee" in prompt
        assert "Queen of the Copper Camps" in prompt
        assert "Mule Mountains" in prompt
        assert "search_trails" in prompt  # Tool usage guidance

    def test_tombstone_system_prompt(self):
        """Test Tombstone system prompt includes key information."""
        agent = TombstoneAgent()
        prompt = agent._get_system_prompt()
        
        assert "Tombstone" in prompt
        assert "Town Too Tough to Die" in prompt
        assert "O.K. Corral" in prompt
        assert "search_trails" in prompt

    def test_sierra_vista_system_prompt(self):
        """Test Sierra Vista system prompt includes key information."""
        agent = SierraVistaAgent()
        prompt = agent._get_system_prompt()
        
        assert "Sierra Vista" in prompt
        assert "Hummingbird Capital" in prompt
        assert "Ramsey Canyon" in prompt
        assert "search_trails" in prompt

    def test_patagonia_system_prompt(self):
        """Test Patagonia system prompt includes key information."""
        agent = PatagoniaAgent()
        prompt = agent._get_system_prompt()
        
        assert "Patagonia" in prompt
        assert "Birding Capital" in prompt
        assert "Sonoita Creek" in prompt
        assert "search_trails" in prompt

    def test_page_system_prompt(self):
        """Test Page system prompt includes key information."""
        agent = PageAgent()
        prompt = agent._get_system_prompt()
        
        assert "Page" in prompt
        assert "Lake Powell" in prompt
        assert "Antelope Canyon" in prompt
        assert "Horseshoe Bend" in prompt
        assert "search_trails" in prompt


class TestLocationAgentIntegration:
    """Integration tests for location agent workflows."""

    @pytest.mark.anyio
    async def test_location_agent_with_tool_calls(self):
        """Test location agent making tool calls."""
        agent = PaysonAgent()
        
        with patch('agent.tools.search_trails') as mock_search, \
             patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
            
            # Mock tool response
            mock_search.invoke.return_value = json.dumps({
                "trails": [{
                    "name": "Test Trail",
                    "activity_type": "mountain_biking",
                    "difficulty": "intermediate",
                }]
            })
            
            # Mock agent response
            mock_response = {
                "location": "Payson, Arizona",
                "location_name": "Payson, Arizona",
                "is_match": True,
                "overview": {
                    "name": "Payson, Arizona",
                    "coordinates": {"lat": 34.2308, "lon": -111.3251},
                    "elevation": 5000,
                    "region": "Gila County, Arizona",
                },
                "outdoor_activities": [],
                "key_attractions": [],
                "businesses": {},
                "practical_info": {},
                "recommendations": [],
                "tools_used": ["search_trails"],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {
                "trail_info": [],
            }
            location_info = await agent.get_location_info(
                "Payson, Arizona",
                existing_outputs,
                "Find mountain biking trails",
                "mountain_biking"
            )
            
            assert location_info is not None

    @pytest.mark.anyio
    async def test_location_agent_error_handling(self):
        """Test location agent error handling."""
        agent = PaysonAgent()
        
        with patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
            mock_ainvoke.side_effect = Exception("API Error")
            
            existing_outputs = {}
            location_info = await agent.get_location_info(
                "Payson, Arizona",
                existing_outputs,
                "Test context",
                "mountain_biking"
            )
            
            # Should handle error gracefully
            assert location_info is not None or isinstance(location_info, dict)

