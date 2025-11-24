"""Adventure agent modules."""

from agent.agents.accommodation_agent import AccommodationAgent
from agent.agents.advocacy_agent import AdvocacyAgent
from agent.agents.bikepacking_agent import BikepackingAgent
from agent.agents.blm_agent import BLMAgent
from agent.agents.community_agent import CommunityAgent
from agent.agents.food_agent import FoodAgent
from agent.agents.gear_agent import GearAgent
from agent.agents.geo_agent import GeoAgent
from agent.agents.historical_agent import HistoricalAgent
from agent.agents.location_agent_base import (
    LocationAgentBase,
    find_location_agent_for_location,
    get_all_location_agents,
    get_location_agent,
    get_location_agent_names,
    register_location_agent,
)
from agent.agents.locations import (
    AjoAgent,
    BisbeeAgent,
    CampVerdeAgent,
    CottonwoodAgent,
    FlagstaffAgent,
    GlobeMiamiAgent,
    GrandCanyonAgent,
    JeromeAgent,
    KingmanAgent,
    LakeHavasuAgent,
    PageAgent,
    ParkerAgent,
    PatagoniaAgent,
    PaysonAgent,
    PhoenixAgent,
    PineAgent,
    PinetopAgent,
    PrescottAgent,
    SedonaAgent,
    ShowLowAgent,
    SierraVistaAgent,
    SonoitaAgent,
    SpringervilleEagarAgent,
    StrawberryAgent,
    TombstoneAgent,
    TucsonAgent,
    WilliamsAgent,
    YumaAgent,
)
from agent.agents.orchestrator import OrchestratorAgent
from agent.agents.permits_agent import PermitsAgent
from agent.agents.photography_agent import PhotographyAgent
from agent.agents.planning_agent import PlanningAgent
from agent.agents.route_planning_agent import RoutePlanningAgent
from agent.agents.safety_agent import SafetyAgent
from agent.agents.trail_agent import TrailAgent
from agent.agents.transportation_agent import TransportationAgent
from agent.agents.weather_agent import WeatherAgent

__all__ = [
    "BLMAgent",
    "TrailAgent",
    "GeoAgent",
    "AccommodationAgent",
    "PlanningAgent",
    "GearAgent",
    "OrchestratorAgent",
    "RoutePlanningAgent",
    "BikepackingAgent",
    "AdvocacyAgent",
    "WeatherAgent",
    "PermitsAgent",
    "SafetyAgent",
    "TransportationAgent",
    "FoodAgent",
    "CommunityAgent",
    "PhotographyAgent",
    "HistoricalAgent",
    "JeromeAgent",
    "SedonaAgent",
    "PrescottAgent",
    "FlagstaffAgent",
    "GrandCanyonAgent",
    "PaysonAgent",
    "PineAgent",
    "StrawberryAgent",
    "PinetopAgent",
    "WilliamsAgent",
    "PhoenixAgent",
    "TucsonAgent",
    "CottonwoodAgent",
    "CampVerdeAgent",
    "ShowLowAgent",
    "BisbeeAgent",
    "TombstoneAgent",
    "SierraVistaAgent",
    "PatagoniaAgent",
    "PageAgent",
    "KingmanAgent",
    "LakeHavasuAgent",
    "GlobeMiamiAgent",
    "SpringervilleEagarAgent",
    "AjoAgent",
    "SonoitaAgent",
    "YumaAgent",
    "ParkerAgent",
    "LocationAgentBase",
    "register_location_agent",
    "get_location_agent",
    "get_all_location_agents",
    "find_location_agent_for_location",
    "get_location_agent_names",
]

