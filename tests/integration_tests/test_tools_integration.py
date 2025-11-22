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
    search_blm_lands,
    calculate_distance,
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

    def test_blm_land_search(self):
        """Test BLM land search functionality."""
        # Search for BLM lands
        blm_result = search_blm_lands.invoke({
            "region": "Colorado",
            "activity_type": "mountain_biking",
        })
        blm_data = json.loads(blm_result)
        
        assert "lands" in blm_data
        assert len(blm_data["lands"]) > 0
        assert "region" in blm_data
        
        # Verify structure
        land = blm_data["lands"][0]
        assert "name" in land
        assert "regulations" in land
        assert "permits_required" in land

    def test_distance_calculation(self):
        """Test distance calculation between two points."""
        # Calculate distance between Denver and Boulder
        distance_result = calculate_distance.invoke({
            "point1": {"lat": 39.7392, "lon": -104.9903},  # Denver
            "point2": {"lat": 40.0149, "lon": -105.2705},  # Boulder
        })
        distance_data = json.loads(distance_result)
        
        assert "distance_miles" in distance_data
        assert "distance_km" in distance_data
        assert distance_data["distance_miles"] > 0
        assert distance_data["distance_km"] > 0
        # Denver to Boulder is approximately 25-30 miles
        assert 20 < distance_data["distance_miles"] < 35

    def test_geocoding_accuracy(self):
        """Test geocoding returns valid coordinates."""
        # Test with known location
        coord_result = get_coordinates.invoke({"location_name": "Denver, Colorado"})
        coord_data = json.loads(coord_result)
        
        assert "coordinates" in coord_data
        lat = coord_data["coordinates"]["lat"]
        lon = coord_data["coordinates"]["lon"]
        
        # Denver is approximately 39.7°N, 104.9°W
        assert 39.0 < lat < 40.0
        assert -106.0 < lon < -104.0
        assert "region" in coord_data

    def test_weather_forecast_structure(self):
        """Test weather forecast returns proper structure."""
        weather_result = get_weather_forecast.invoke({
            "location": "Denver, Colorado",
            "dates": ["2024-06-01", "2024-06-02"],
        })
        weather_data = json.loads(weather_result)
        
        assert "forecast" in weather_data
        assert "location" in weather_data
        forecast = weather_data["forecast"]
        assert "current" in forecast
        assert "daily" in forecast
        
        # Verify current weather structure
        current = forecast["current"]
        assert "temp" in current
        assert "condition" in current

    def test_trail_search_with_osm(self):
        """Test trail search using OpenStreetMap."""
        trail_result = search_trails.invoke({
            "location": "Boulder, Colorado",
            "activity_type": "hiking",
            "source": "osm",
        })
        trail_data = json.loads(trail_result)
        
        assert "trails" in trail_data
        # May return 0 trails if location has no OSM data, but structure should be valid
        assert isinstance(trail_data["trails"], list)

    def test_accommodation_search_campgrounds(self):
        """Test accommodation search specifically for campgrounds."""
        acc_result = search_accommodations.invoke({
            "location": "Colorado",
            "accommodation_type": "campground",
        })
        acc_data = json.loads(acc_result)
        
        assert "accommodations" in acc_data
        assert len(acc_data["accommodations"]) > 0
        
        # Verify campground structure
        campground = acc_data["accommodations"][0]
        assert "name" in campground
        assert "type" in campground
        assert campground["type"] == "campground" or "camp" in campground["type"].lower()

    def test_end_to_end_adventure_planning(self):
        """Test complete flow from location to full adventure plan."""
        # 1. Get location coordinates
        coord_result = get_coordinates.invoke({"location_name": "Moab, Utah"})
        coord_data = json.loads(coord_result)
        assert "coordinates" in coord_data
        
        # 2. Search for trails
        trail_result = search_trails.invoke({
            "location": "Moab, Utah",
            "activity_type": "mountain_biking",
            "source": "osm",
        })
        trail_data = json.loads(trail_result)
        assert "trails" in trail_data
        
        # 3. Search for accommodations
        acc_result = search_accommodations.invoke({
            "location": "Moab, Utah",
            "accommodation_type": "campground",
        })
        acc_data = json.loads(acc_result)
        assert "accommodations" in acc_data
        
        # 4. Get weather forecast
        weather_result = get_weather_forecast.invoke({
            "location": "Moab, Utah",
        })
        weather_data = json.loads(weather_result)
        assert "forecast" in weather_data
        
        # 5. Search for BLM lands
        blm_result = search_blm_lands.invoke({
            "region": "Utah",
            "activity_type": "mountain_biking",
        })
        blm_data = json.loads(blm_result)
        assert "lands" in blm_data

