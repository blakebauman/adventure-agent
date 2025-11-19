"""Unit tests for tools."""

import json
import pytest
from agent.tools import (
    search_blm_lands,
    get_blm_regulations,
    search_trails,
    get_trail_details,
    get_coordinates,
    calculate_distance,
    search_accommodations,
    recommend_gear,
    create_itinerary,
    get_weather_forecast,
    check_permit_requirements,
    get_safety_information,
    get_parking_information,
    find_grocery_stores,
    find_local_clubs,
    find_photo_spots,
    find_historical_sites,
    WebSearchTool,
)


class TestBLMTools:
    """Test BLM-related tools."""

    def test_search_blm_lands(self):
        """Test searching for BLM lands."""
        result = search_blm_lands.invoke({"region": "Nevada", "activity_type": "mountain_biking"})
        data = json.loads(result)
        assert "lands" in data
        assert len(data["lands"]) > 0
        assert data["lands"][0]["name"] == "BLM Land in Nevada"
        assert data["lands"][0]["permits_required"] is True

    def test_get_blm_regulations(self):
        """Test getting BLM regulations."""
        result = get_blm_regulations.invoke({"land_name": "Test BLM Area"})
        data = json.loads(result)
        assert "regulations" in data
        assert data["permits_required"] is True
        assert len(data["regulations"]) > 0


class TestTrailTools:
    """Test trail-related tools."""

    def test_search_trails_mountain_biking(self):
        """Test searching for mountain biking trails."""
        result = search_trails.invoke({
            "location": "Colorado",
            "activity_type": "mountain_biking",
            "source": "mtbproject",
            "difficulty": "blue",
        })
        data = json.loads(result)
        assert "trails" in data
        assert len(data["trails"]) > 0
        assert data["trails"][0]["activity_type"] == "mountain_biking"
        assert data["trails"][0]["source"] == "mtbproject"

    def test_search_trails_hiking(self):
        """Test searching for hiking trails."""
        result = search_trails.invoke({
            "location": "Arizona",
            "activity_type": "hiking",
            "source": "hikingproject",
            "difficulty": "intermediate",
        })
        data = json.loads(result)
        assert "trails" in data
        assert data["trails"][0]["activity_type"] == "hiking"

    def test_get_trail_details(self):
        """Test getting trail details."""
        result = get_trail_details.invoke({
            "trail_id": "12345",
            "source": "mtbproject",
            "activity_type": "mountain_biking",
        })
        data = json.loads(result)
        assert data["trail_id"] == "12345"
        assert data["source"] == "mtbproject"
        assert "details" in data


class TestGeoTools:
    """Test geo-related tools."""

    def test_get_coordinates(self):
        """Test getting coordinates for a location."""
        result = get_coordinates.invoke({"location_name": "Las Vegas"})
        data = json.loads(result)
        assert "coordinates" in data
        assert "lat" in data["coordinates"]
        assert "lon" in data["coordinates"]
        assert data["region"] == "Nevada"

    def test_calculate_distance(self):
        """Test calculating distance between points."""
        point1 = {"lat": 36.1699, "lon": -115.1398}
        point2 = {"lat": 40.0, "lon": -105.0}
        result = calculate_distance.invoke({"point1": point1, "point2": point2})
        data = json.loads(result)
        assert "distance_miles" in data
        assert "distance_km" in data


class TestAccommodationTools:
    """Test accommodation-related tools."""

    def test_search_accommodations(self):
        """Test searching for accommodations."""
        result = search_accommodations.invoke({
            "location": "Colorado",
            "accommodation_type": "campground",
        })
        data = json.loads(result)
        assert "accommodations" in data
        assert len(data["accommodations"]) > 0
        assert data["accommodations"][0]["type"] == "campground"


class TestGearTools:
    """Test gear-related tools."""

    def test_recommend_gear(self):
        """Test gear recommendations."""
        result = recommend_gear.invoke({
            "adventure_type": "mountain_biking",
            "duration_days": 3,
            "skill_level": "intermediate",
            "gear_owned": ["bike"],
        })
        data = json.loads(result)
        assert "recommendations" in data
        assert len(data["recommendations"]) > 0
        assert any(rec["essential"] for rec in data["recommendations"])


class TestPlanningTools:
    """Test planning-related tools."""

    def test_create_itinerary(self):
        """Test creating an itinerary."""
        trails = [
            {"name": "Trail 1", "length_miles": 10.0},
            {"name": "Trail 2", "length_miles": 15.0},
        ]
        result = create_itinerary.invoke({
            "trails": trails,
            "start_location": "Colorado",
            "duration_days": 2,
        })
        data = json.loads(result)
        assert "itinerary" in data
        assert len(data["itinerary"]) == 2
        assert data["itinerary"][0]["day"] == 1


class TestWeatherTools:
    """Test weather-related tools."""

    def test_get_weather_forecast(self):
        """Test getting weather forecast."""
        result = get_weather_forecast.invoke({
            "location": "Colorado",
            "dates": ["2024-06-01", "2024-06-02"],
        })
        data = json.loads(result)
        assert "forecast" in data
        assert "current" in data["forecast"]
        assert "daily" in data["forecast"]


class TestPermitTools:
    """Test permit-related tools."""

    def test_check_permit_requirements(self):
        """Test checking permit requirements."""
        result = check_permit_requirements.invoke({
            "location": "Colorado",
            "activity_type": "mountain_biking",
            "group_size": 5,
        })
        data = json.loads(result)
        assert "permits_required" in data
        assert data["location"] == "Colorado"

    def test_check_permit_requirements_large_group(self):
        """Test permit requirements for large group."""
        result = check_permit_requirements.invoke({
            "location": "Colorado",
            "activity_type": "mountain_biking",
            "group_size": 15,
        })
        data = json.loads(result)
        # Large groups typically require permits
        assert data["permits_required"] is True


class TestSafetyTools:
    """Test safety-related tools."""

    def test_get_safety_information(self):
        """Test getting safety information."""
        result = get_safety_information.invoke({
            "location": "Colorado",
            "activity_type": "mountain_biking",
        })
        data = json.loads(result)
        assert "safety_tips" in data
        assert "common_hazards" in data
        assert len(data["safety_tips"]) > 0


class TestTransportationTools:
    """Test transportation-related tools."""

    def test_get_parking_information(self):
        """Test getting parking information."""
        result = get_parking_information.invoke({
            "location": "Colorado",
            "trailhead": "Main Trailhead",
        })
        data = json.loads(result)
        assert "parking" in data
        assert "available" in data["parking"]


class TestFoodTools:
    """Test food-related tools."""

    def test_find_grocery_stores(self):
        """Test finding grocery stores."""
        result = find_grocery_stores.invoke({
            "location": "Colorado",
            "route_info": None,
        })
        data = json.loads(result)
        assert "grocery_stores" in data
        assert len(data["grocery_stores"]) > 0


class TestCommunityTools:
    """Test community-related tools."""

    def test_find_local_clubs(self):
        """Test finding local clubs."""
        result = find_local_clubs.invoke({
            "location": "Colorado",
            "activity_type": "mountain_biking",
        })
        data = json.loads(result)
        assert "clubs" in data
        assert len(data["clubs"]) > 0


class TestPhotographyTools:
    """Test photography-related tools."""

    def test_find_photo_spots(self):
        """Test finding photo spots."""
        result = find_photo_spots.invoke({
            "location": "Colorado",
            "route_info": None,
        })
        data = json.loads(result)
        assert "photo_spots" in data
        assert len(data["photo_spots"]) > 0


class TestHistoricalTools:
    """Test historical-related tools."""

    def test_find_historical_sites(self):
        """Test finding historical sites."""
        result = find_historical_sites.invoke({
            "location": "Colorado",
            "route_info": None,
        })
        data = json.loads(result)
        assert "historical_sites" in data
        assert len(data["historical_sites"]) > 0


class TestWebSearchTool:
    """Test WebSearchTool class."""

    def test_web_search_tool_no_api_key(self):
        """Test WebSearchTool without API key."""
        tool = WebSearchTool()
        results = tool.search_web("test query")
        assert results == []

    def test_web_search_tool_with_api_key(self):
        """Test WebSearchTool with API key (mocked)."""
        # This would require mocking TavilySearchResults
        # For now, just test initialization
        tool = WebSearchTool(api_key="test_key")
        assert tool.search is not None

