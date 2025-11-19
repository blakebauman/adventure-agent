"""Unit tests for state schema."""

import pytest
from agent.state import (
    AdventureState,
    UserPreferences,
    Location,
    TrailInfo,
    BLMLandInfo,
    AccommodationInfo,
    GearRecommendation,
    AdventurePlan,
)


class TestUserPreferences:
    """Test UserPreferences TypedDict."""

    def test_minimal_user_preferences(self):
        """Test creating minimal user preferences."""
        prefs = UserPreferences(
            skill_level="intermediate",
            preferred_terrain=["mountain"],
            activity_type="mountain_biking",
        )
        assert prefs["skill_level"] == "intermediate"
        assert prefs["preferred_terrain"] == ["mountain"]
        assert prefs["activity_type"] == "mountain_biking"

    def test_full_user_preferences(self):
        """Test creating full user preferences."""
        prefs = UserPreferences(
            skill_level="advanced",
            preferred_terrain=["mountain", "desert"],
            activity_type="bikepacking",
            duration_days=5,
            distance_preference="epic",
            accommodation_preference="camping",
            region="Colorado",
            budget_range="$500-1000",
            gear_owned=["bike", "helmet"],
        )
        assert prefs["skill_level"] == "advanced"
        assert prefs["duration_days"] == 5
        assert prefs["region"] == "Colorado"


class TestLocation:
    """Test Location TypedDict."""

    def test_minimal_location(self):
        """Test creating minimal location."""
        loc = Location(name="Sedona", region="Arizona", country="US")
        assert loc["name"] == "Sedona"
        assert loc["region"] == "Arizona"
        assert loc["country"] == "US"

    def test_location_with_coordinates(self):
        """Test creating location with coordinates."""
        loc = Location(
            name="Las Vegas",
            coordinates={"lat": 36.1699, "lon": -115.1398},
            region="Nevada",
            country="US",
            description="Desert city",
        )
        assert loc["coordinates"]["lat"] == 36.1699
        assert loc["coordinates"]["lon"] == -115.1398
        assert loc["description"] == "Desert city"


class TestTrailInfo:
    """Test TrailInfo TypedDict."""

    def test_minimal_trail_info(self):
        """Test creating minimal trail info."""
        trail = TrailInfo(name="Test Trail", source="mtbproject")
        assert trail["name"] == "Test Trail"
        assert trail["source"] == "mtbproject"

    def test_full_trail_info(self):
        """Test creating full trail info."""
        trail = TrailInfo(
            name="Epic Trail",
            source="hikingproject",
            difficulty="intermediate",
            length_miles=10.5,
            elevation_gain=2000.0,
            description="Scenic mountain trail",
            url="https://example.com/trail",
            coordinates={"lat": 40.0, "lon": -105.0},
        )
        assert trail["length_miles"] == 10.5
        assert trail["elevation_gain"] == 2000.0


class TestBLMLandInfo:
    """Test BLMLandInfo TypedDict."""

    def test_blm_land_info(self):
        """Test creating BLM land info."""
        blm = BLMLandInfo(
            land_name="BLM Area",
            access_points=["Trailhead A", "Trailhead B"],
            regulations=["Permits required", "No motorized vehicles"],
            permits_required=True,
            camping_allowed=True,
        )
        assert blm["land_name"] == "BLM Area"
        assert len(blm["access_points"]) == 2
        assert blm["permits_required"] is True


class TestAccommodationInfo:
    """Test AccommodationInfo TypedDict."""

    def test_accommodation_info(self):
        """Test creating accommodation info."""
        acc = AccommodationInfo(
            name="Mountain Campground",
            type="campground",
            location="Near trailhead",
            amenities=["Restrooms", "Water", "Fire pits"],
        )
        assert acc["name"] == "Mountain Campground"
        assert acc["type"] == "campground"
        assert "Water" in acc["amenities"]


class TestGearRecommendation:
    """Test GearRecommendation TypedDict."""

    def test_gear_recommendation(self):
        """Test creating gear recommendation."""
        gear = GearRecommendation(
            name="Mountain Bike Helmet",
            category="safety",
            description="Essential safety gear",
            affiliate_url="https://example.com/helmet",
            essential=True,
        )
        assert gear["name"] == "Mountain Bike Helmet"
        assert gear["essential"] is True


class TestAdventurePlan:
    """Test AdventurePlan TypedDict."""

    def test_minimal_adventure_plan(self):
        """Test creating minimal adventure plan."""
        location = Location(name="Colorado", region="Colorado", country="US")
        plan = AdventurePlan(
            title="Mountain Adventure",
            description="Epic mountain biking trip",
            location=location,
            trails=[],
            blm_lands=[],
            accommodations=[],
            gear_recommendations=[],
            itinerary=[],
            estimated_duration_days=3,
            difficulty="intermediate",
        )
        assert plan["title"] == "Mountain Adventure"
        assert plan["estimated_duration_days"] == 3

    def test_full_adventure_plan(self):
        """Test creating full adventure plan."""
        location = Location(name="Sedona", region="Arizona", country="US")
        trail = TrailInfo(name="Trail 1", source="mtbproject")
        plan = AdventurePlan(
            title="Sedona Adventure",
            description="Multi-day bikepacking trip",
            location=location,
            trails=[trail],
            blm_lands=[],
            accommodations=[],
            gear_recommendations=[],
            itinerary=[{"day": 1, "activities": ["Ride trail"]}],
            total_distance_miles=50.0,
            estimated_duration_days=2,
            difficulty="advanced",
            weather_info={"forecast": "Sunny"},
            permits_info={"required": False},
        )
        assert plan["total_distance_miles"] == 50.0
        assert len(plan["trails"]) == 1


class TestAdventureState:
    """Test AdventureState TypedDict."""

    def test_minimal_state(self):
        """Test creating minimal state."""
        state = AdventureState(user_input="Plan a trip to Colorado")
        assert state["user_input"] == "Plan a trip to Colorado"
        assert state.get("user_preferences") is None

    def test_state_with_preferences(self):
        """Test creating state with preferences."""
        prefs = UserPreferences(
            skill_level="intermediate",
            preferred_terrain=["mountain"],
            activity_type="mountain_biking",
        )
        state = AdventureState(
            user_input="Plan a trip",
            user_preferences=prefs,
            current_task="mountain_biking",
            required_agents=["geo_agent", "trail_agent"],
            completed_agents=[],
            agent_context={},
            trail_info=[],
            blm_info=[],
            accommodation_info=[],
            gear_recommendations=[],
            needs_human_review=False,
            conversation_history=[],
            errors=[],
        )
        assert state["user_preferences"]["skill_level"] == "intermediate"
        assert "geo_agent" in state["required_agents"]

    def test_state_with_human_review(self):
        """Test state with human review flags."""
        state = AdventureState(
            user_input="Plan a trip",
            needs_human_review=True,
            approval_status="pending",
            human_feedback=None,
            conversation_history=[],
            errors=[],
        )
        assert state["needs_human_review"] is True
        assert state["approval_status"] == "pending"

