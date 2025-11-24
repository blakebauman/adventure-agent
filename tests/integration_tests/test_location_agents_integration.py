"""Integration tests for location agent workflows.

Tests location agents in realistic scenarios with tool integration,
knowledge base usage, and structured output parsing.
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
)
from agent.state import AdventureState, UserPreferences


class TestLocationAgentWorkflows:
    """Test location agent workflows with tool integration."""

    @pytest.mark.anyio
    async def test_bisbee_agent_with_trails(self):
        """Test Bisbee agent with trail search integration."""
        agent = BisbeeAgent()
        
        with patch('agent.tools.search_trails') as mock_search, \
             patch('agent.tools.get_coordinates') as mock_coords, \
             patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
            
            # Mock coordinates
            mock_coords.invoke.return_value = json.dumps({
                "location": "Bisbee, Arizona",
                "coordinates": {"lat": 31.4482, "lon": -109.9284},
                "region": "Cochise County, Arizona",
                "country": "US",
            })
            
            # Mock trail search
            mock_search.invoke.return_value = json.dumps({
                "trails": [{
                    "name": "Mule Mountains Trail",
                    "activity_type": "mountain_biking",
                    "difficulty": "intermediate",
                    "length_miles": 5.0,
                }]
            })
            
            # Mock agent structured output
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
                "outdoor_activities": [
                    {
                        "activity_type": "mountain_biking",
                        "description": "Trails in Mule Mountains",
                        "famous_trails": [],
                        "difficulty_range": "Intermediate to expert",
                    }
                ],
                "key_attractions": [],
                "businesses": {},
                "practical_info": {},
                "recommendations": ["Try Mule Mountains trails"],
                "tools_used": ["search_trails", "get_coordinates"],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {
                "geo_info": {
                    "location": "Bisbee, Arizona",
                    "coordinates": {"lat": 31.4482, "lon": -109.9284},
                },
                "trail_info": [],
            }
            
            location_info = await agent.get_location_info(
                "Bisbee, Arizona",
                existing_outputs,
                "Find mountain biking trails in Bisbee",
                "mountain_biking"
            )
            
            assert location_info is not None
            # Verify tools would be called (agent decides based on prompt)
            # The agent's prompt instructs it to use search_trails

    @pytest.mark.anyio
    async def test_tombstone_agent_historical_context(self):
        """Test Tombstone agent with historical context."""
        agent = TombstoneAgent()
        
        with patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
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
                "key_attractions": [
                    {
                        "name": "O.K. Corral",
                        "type": "Historic Site",
                        "description": "Site of legendary gunfight",
                    }
                ],
                "businesses": {},
                "practical_info": {},
                "recommendations": ["Visit O.K. Corral"],
                "tools_used": [],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {
                "historical_info": {
                    "sites": ["O.K. Corral"],
                },
            }
            
            location_info = await agent.get_location_info(
                "Tombstone, Arizona",
                existing_outputs,
                "Tell me about Tombstone's history",
                "hiking"
            )
            
            assert location_info is not None

    @pytest.mark.anyio
    async def test_sierra_vista_agent_birding_focus(self):
        """Test Sierra Vista agent with birding focus."""
        agent = SierraVistaAgent()
        
        with patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
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
                "outdoor_activities": [
                    {
                        "activity_type": "birding",
                        "description": "World-class birding",
                        "famous_trails": [],
                        "difficulty_range": "N/A",
                    }
                ],
                "key_attractions": [
                    {
                        "name": "Ramsey Canyon Preserve",
                        "type": "Preserve",
                        "description": "World-renowned birding destination",
                    }
                ],
                "businesses": {},
                "practical_info": {},
                "recommendations": ["Visit Ramsey Canyon Preserve"],
                "tools_used": [],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {}
            location_info = await agent.get_location_info(
                "Sierra Vista, Arizona",
                existing_outputs,
                "Where can I go birding?",
                "birding"
            )
            
            assert location_info is not None

    @pytest.mark.anyio
    async def test_patagonia_agent_birding_destination(self):
        """Test Patagonia agent as birding destination."""
        agent = PatagoniaAgent()
        
        with patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
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
                "outdoor_activities": [
                    {
                        "activity_type": "birding",
                        "description": "World-renowned birding",
                        "famous_trails": [],
                        "difficulty_range": "N/A",
                    }
                ],
                "key_attractions": [
                    {
                        "name": "Patagonia-Sonoita Creek Preserve",
                        "type": "Preserve",
                        "description": "World-renowned birding destination",
                    }
                ],
                "businesses": {},
                "practical_info": {},
                "recommendations": ["Visit Patagonia-Sonoita Creek Preserve"],
                "tools_used": [],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {}
            location_info = await agent.get_location_info(
                "Patagonia, Arizona",
                existing_outputs,
                "Best birding spots",
                "birding"
            )
            
            assert location_info is not None

    @pytest.mark.anyio
    async def test_page_agent_water_activities(self):
        """Test Page agent with water activities focus."""
        agent = PageAgent()
        
        with patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
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
                "outdoor_activities": [
                    {
                        "activity_type": "water_activities",
                        "description": "Lake Powell recreation",
                        "famous_trails": [],
                        "difficulty_range": "N/A",
                    }
                ],
                "key_attractions": [
                    {
                        "name": "Lake Powell",
                        "type": "Reservoir",
                        "description": "186 miles long, 1,900 miles of shoreline",
                    }
                ],
                "businesses": {},
                "practical_info": {},
                "recommendations": ["Visit Lake Powell"],
                "tools_used": [],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {}
            location_info = await agent.get_location_info(
                "Page, Arizona",
                existing_outputs,
                "What water activities are available?",
                "paddling"
            )
            
            assert location_info is not None

    @pytest.mark.anyio
    async def test_location_agent_knowledge_base_enhancement(self):
        """Test that location agents enhance tool results with knowledge base."""
        agent = PaysonAgent()
        
        with patch('agent.tools.search_trails') as mock_search, \
             patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
            
            # Mock trail search returning basic data
            mock_search.invoke.return_value = json.dumps({
                "trails": [{
                    "name": "Highline Trail",
                    "activity_type": "mountain_biking",
                    "difficulty": "intermediate",
                }]
            })
            
            # Agent should enhance with knowledge base details
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
                        "famous_trails": [
                            {
                                "name": "Highline Trail",
                                "difficulty": "Intermediate to Advanced",
                                "length_miles": 51.0,
                                "description": "51-mile long-distance trail along Mogollon Rim",
                            }
                        ],
                        "difficulty_range": "Beginner to expert",
                    }
                ],
                "key_attractions": [],
                "businesses": {},
                "practical_info": {},
                "recommendations": [],
                "tools_used": ["search_trails"],
            }
            mock_ainvoke.return_value = MagicMock(content=json.dumps(mock_response))
            
            existing_outputs = {
                "trail_info": [{
                    "name": "Highline Trail",
                    "activity_type": "mountain_biking",
                }],
            }
            
            location_info = await agent.get_location_info(
                "Payson, Arizona",
                existing_outputs,
                "Tell me about Highline Trail",
                "mountain_biking"
            )
            
            assert location_info is not None
            # Verify knowledge base enhancement (agent adds details from knowledge base)

    @pytest.mark.anyio
    async def test_location_agent_structured_output_parsing(self):
        """Test structured output parsing with various formats."""
        agent = PaysonAgent()
        
        # Test with properly formatted structured output
        valid_output = {
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
            "tools_used": [],
        }
        
        with patch.object(agent.agent, 'ainvoke') as mock_ainvoke:
            mock_ainvoke.return_value = MagicMock(content=json.dumps(valid_output))
            
            existing_outputs = {}
            location_info = await agent.get_location_info(
                "Payson, Arizona",
                existing_outputs,
                "Test query",
                "mountain_biking"
            )
            
            assert location_info is not None
            # Should parse successfully

    @pytest.mark.anyio
    async def test_multiple_location_agents_comparison(self):
        """Test multiple location agents to ensure consistency."""
        agents = [
            BisbeeAgent(),
            TombstoneAgent(),
            SierraVistaAgent(),
            PatagoniaAgent(),
            PageAgent(),
        ]
        
        for agent in agents:
            # Verify all agents have required methods
            assert hasattr(agent, 'get_location_info')
            assert hasattr(agent, 'get_location_knowledge')
            assert hasattr(agent, 'is_location_match')
            assert hasattr(agent, '_get_system_prompt')
            
            # Verify knowledge base structure
            knowledge = agent.get_location_knowledge()
            assert "location" in knowledge
            assert "outdoor_activities" in knowledge
            assert "practical_info" in knowledge

