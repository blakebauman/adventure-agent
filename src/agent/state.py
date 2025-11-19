"""State schema for the adventure agent system."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from typing_extensions import TypedDict


class UserPreferences(TypedDict, total=False):
    """User preferences for adventure planning."""

    skill_level: str  # beginner, intermediate, advanced, expert
    preferred_terrain: List[str]  # mountain, desert, forest, etc.
    activity_type: str  # mountain_biking, hiking, trail_running, bikepacking, etc.
    adventure_type: Optional[str]  # Deprecated, use activity_type instead
    duration_days: Optional[int]
    distance_preference: Optional[str]  # short, medium, long, epic
    accommodation_preference: Optional[str]  # camping, hotels, mixed
    region: Optional[str]  # US state or Canadian province
    budget_range: Optional[str]
    gear_owned: Optional[List[str]]


class Location(TypedDict, total=False):
    """Geographic location information."""

    name: str
    coordinates: Optional[Dict[str, float]]  # {"lat": float, "lon": float}
    region: str
    country: str  # US or Canada
    description: Optional[str]


class TrailInfo(TypedDict, total=False):
    """Trail information from various sources."""

    name: str
    source: str  # mtbproject, blm, etc.
    difficulty: Optional[str]
    length_miles: Optional[float]
    elevation_gain: Optional[float]
    description: Optional[str]
    url: Optional[str]
    coordinates: Optional[Dict[str, float]]


class BLMLandInfo(TypedDict, total=False):
    """BLM land information."""

    land_name: str
    access_points: List[str]
    regulations: List[str]
    permits_required: bool
    camping_allowed: bool
    description: Optional[str]
    coordinates: Optional[Dict[str, float]]


class AccommodationInfo(TypedDict, total=False):
    """Accommodation information."""

    name: str
    type: str  # hotel, campground, hostel, etc.
    location: str
    coordinates: Optional[Dict[str, float]]
    price_range: Optional[str]
    amenities: List[str]
    booking_url: Optional[str]


class GearRecommendation(TypedDict, total=False):
    """Gear and product recommendations."""

    name: str
    category: str  # bike, clothing, camping, etc.
    description: str
    affiliate_url: str
    price_range: Optional[str]
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
    total_distance_miles: Optional[float]
    estimated_duration_days: int
    difficulty: str
    weather_info: Optional[Dict[str, Any]]
    permits_info: Optional[Dict[str, Any]]
    safety_info: Optional[Dict[str, Any]]
    transportation_info: Optional[Dict[str, Any]]
    food_info: Optional[Dict[str, Any]]
    community_info: Optional[Dict[str, Any]]
    photography_info: Optional[Dict[str, Any]]
    historical_info: Optional[Dict[str, Any]]


class AdventureState(TypedDict, total=False):
    """Main state for the adventure agent system."""

    # User input
    user_input: str
    user_preferences: Optional[UserPreferences]

    # Context from orchestrator
    current_task: str
    required_agents: List[str]
    completed_agents: List[str]
    agent_context: Dict[str, str]

    # Agent outputs
    geo_info: Optional[Dict[str, Any]]
    trail_info: List[TrailInfo]
    blm_info: List[BLMLandInfo]
    accommodation_info: List[AccommodationInfo]
    gear_recommendations: List[GearRecommendation]
    planning_info: Optional[Dict[str, Any]]
    weather_info: Optional[Dict[str, Any]]
    permits_info: Optional[Dict[str, Any]]
    safety_info: Optional[Dict[str, Any]]
    transportation_info: Optional[Dict[str, Any]]
    food_info: Optional[Dict[str, Any]]
    community_info: Optional[Dict[str, Any]]
    photography_info: Optional[Dict[str, Any]]
    historical_info: Optional[Dict[str, Any]]
    route_planning_info: List[TrailInfo]
    bikepacking_info: List[TrailInfo]
    advocacy_info: Optional[Dict[str, Any]]

    # Final output
    adventure_plan: Optional[AdventurePlan]

    # Human-in-the-loop
    needs_human_review: bool
    human_feedback: Optional[str]
    approval_status: Optional[str]  # pending, approved, rejected, needs_revision

    # Metadata
    conversation_history: List[Dict[str, str]]
    errors: List[str]

