"""State schema for the adventure agent system."""

from __future__ import annotations

import operator
from typing import Annotated, Any, Dict, List

from typing_extensions import TypedDict


class UserPreferences(TypedDict, total=False):
    """User preferences for adventure planning."""

    skill_level: str  # beginner, intermediate, advanced, expert
    preferred_terrain: List[str]  # mountain, desert, forest, etc.
    activity_type: str  # mountain_biking, hiking, trail_running, bikepacking, etc.
    adventure_type: str | None  # Deprecated, use activity_type instead
    duration_days: int | None
    distance_preference: str | None  # short, medium, long, epic
    accommodation_preference: str | None  # camping, hotels, mixed
    region: str | None  # US state or Canadian province
    budget_range: str | None
    gear_owned: List[str] | None


class Location(TypedDict, total=False):
    """Geographic location information."""

    name: str
    coordinates: Dict[str, float] | None  # {"lat": float, "lon": float}
    region: str
    country: str  # US or Canada
    description: str | None


class TrailInfo(TypedDict, total=False):
    """Trail information from various sources."""

    name: str
    source: str  # mtbproject, blm, etc.
    difficulty: str | None
    length_miles: float | None
    elevation_gain: float | None
    description: str | None
    url: str | None
    coordinates: Dict[str, float] | None


class BLMLandInfo(TypedDict, total=False):
    """BLM land information."""

    land_name: str
    access_points: List[str]
    regulations: List[str]
    permits_required: bool
    camping_allowed: bool
    description: str | None
    coordinates: Dict[str, float] | None


class AccommodationInfo(TypedDict, total=False):
    """Accommodation information."""

    name: str
    type: str  # hotel, campground, hostel, etc.
    location: str
    coordinates: Dict[str, float] | None
    price_range: str | None
    amenities: List[str]
    booking_url: str | None


class GearRecommendation(TypedDict, total=False):
    """Gear and product recommendations."""

    name: str
    category: str  # bike, clothing, camping, etc.
    description: str
    affiliate_url: str
    price_range: str | None
    essential: bool


class AdventurePlan(TypedDict, total=False):
    """Complete adventure plan."""

    title: str
    description: str
    location: Location
    trails: List[TrailInfo]
    blm_lands: List[BLMLandInfo]
    accommodations: List[AccommodationInfo]
    gear_recommendations: List[GearRecommendation]
    itinerary: List[Dict[str, Any]]
    total_distance_miles: float | None
    estimated_duration_days: int
    difficulty: str
    weather_info: Dict[str, Any] | None
    permits_info: Dict[str, Any] | None
    safety_info: Dict[str, Any] | None
    transportation_info: Dict[str, Any] | None
    food_info: Dict[str, Any] | None
    community_info: Dict[str, Any] | None
    photography_info: Dict[str, Any] | None
    historical_info: Dict[str, Any] | None


class AdventureState(TypedDict, total=False):
    """Main state for the adventure agent system."""

    # User input
    user_input: str
    user_preferences: UserPreferences | None

    # Context from orchestrator
    current_task: str
    required_agents: List[str]
    # Use operator.add as reducer to merge lists from parallel nodes
    # Each agent returns ["agent_name"] and they get concatenated
    completed_agents: Annotated[List[str], operator.add]
    agent_context: Dict[str, str]

    # Agent outputs
    geo_info: Dict[str, Any] | None
    trail_info: List[TrailInfo]
    blm_info: List[BLMLandInfo]
    accommodation_info: List[AccommodationInfo]
    gear_recommendations: List[GearRecommendation]
    planning_info: Dict[str, Any] | None
    weather_info: Dict[str, Any] | None
    permits_info: Dict[str, Any] | None
    safety_info: Dict[str, Any] | None
    transportation_info: Dict[str, Any] | None
    food_info: Dict[str, Any] | None
    community_info: Dict[str, Any] | None
    photography_info: Dict[str, Any] | None
    historical_info: Dict[str, Any] | None
    route_planning_info: List[TrailInfo]
    bikepacking_info: List[TrailInfo]
    advocacy_info: Dict[str, Any] | None
    location_info: Dict[str, Any] | None  # Generic location agent output

    # Final output
    adventure_plan: AdventurePlan | None

    # Human-in-the-loop
    needs_human_review: bool
    human_feedback: str | None
    approval_status: str | None  # pending, approved, rejected, needs_revision

    # Metadata
    conversation_history: List[Dict[str, str]]
    error_details: Annotated[List[Dict[str, Any]], operator.add]  # Structured error information with categorization

