"""Integration tests for tool interactions."""

import json
import pytest
from agent.tools import (
    search_trails,
    get_coordinates,
    search_accommodations,
    recommend_gear,
    create_itinerary,
    get_weather_forecast,
    check_permit_requirements,
)


class TestToolIntegration:
    """Test tool integration scenarios."""

    def test_trail_search_to_details_flow(self):
        """Test flow from trail search to getting details."""
        # Search for trails
        search_result = search_trails.invoke({
            "location": "Colorado",
            "activity_type": "mountain_biking",
            "source": "mtbproject",
            "difficulty": "blue",
        })
        search_data = json.loads(search_result)
        
        assert "trails" in search_data
        assert len(search_data["trails"]) > 0
        
        # Get details for first trail (would use trail_id in real scenario)
        trail = search_data["trails"][0]
        assert trail["name"] is not None
        assert trail["source"] == "mtbproject"

    def test_location_to_trails_flow(self):
        """Test flow from getting location to searching trails."""
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": "Colorado"})
        coord_data = json.loads(coord_result)
        
        assert "coordinates" in coord_data
        assert "region" in coord_data
        
        # Use location to search trails
        trail_result = search_trails.invoke({
            "location": coord_data["region"],
            "activity_type": "mountain_biking",
            "source": "mtbproject",
        })
        trail_data = json.loads(trail_result)
        
        assert "trails" in trail_data
        assert len(trail_data["trails"]) > 0

    def test_trails_to_itinerary_flow(self):
        """Test flow from trails to creating itinerary."""
        # Search for trails
        trail_result = search_trails.invoke({
            "location": "Colorado",
            "activity_type": "mountain_biking",
            "source": "mtbproject",
        })
        trail_data = json.loads(trail_result)
        trails = trail_data["trails"]
        
        # Create itinerary from trails
        itinerary_result = create_itinerary.invoke({
            "trails": trails,
            "start_location": "Colorado",
            "duration_days": 3,
        })
        itinerary_data = json.loads(itinerary_result)
        
        assert "itinerary" in itinerary_data
        assert len(itinerary_data["itinerary"]) == 3
        assert all("day" in day for day in itinerary_data["itinerary"])

    def test_gear_recommendation_flow(self):
        """Test flow from activity type to gear recommendations."""
        # Get gear recommendations
        gear_result = recommend_gear.invoke({
            "adventure_type": "bikepacking",
            "duration_days": 5,
            "skill_level": "intermediate",
            "gear_owned": ["bike", "helmet"],
        })
        gear_data = json.loads(gear_result)
        
        assert "recommendations" in gear_data
        assert len(gear_data["recommendations"]) > 0
        
        # Verify essential gear is included
        essential_items = [g for g in gear_data["recommendations"] if g.get("essential")]
        assert len(essential_items) > 0

    def test_location_to_accommodations_flow(self):
        """Test flow from location to accommodations."""
        # Get location
        coord_result = get_coordinates.invoke({"location_name": "Colorado"})
        coord_data = json.loads(coord_result)
        
        # Search accommodations
        acc_result = search_accommodations.invoke({
            "location": coord_data["region"],
            "accommodation_type": "campground",
        })
        acc_data = json.loads(acc_result)
        
        assert "accommodations" in acc_data
        assert len(acc_data["accommodations"]) > 0

    def test_weather_and_permits_flow(self):
        """Test flow from weather to permit requirements."""
        # Get weather forecast
        weather_result = get_weather_forecast.invoke({
            "location": "Colorado",
            "dates": ["2024-06-01", "2024-06-02"],
        })
        weather_data = json.loads(weather_result)
        
        assert "forecast" in weather_data
        
        # Check permit requirements
        permit_result = check_permit_requirements.invoke({
            "location": "Colorado",
            "activity_type": "mountain_biking",
            "group_size": 8,
        })
        permit_data = json.loads(permit_result)
        
        assert "permits_required" in permit_data
        assert permit_data["location"] == "Colorado"

