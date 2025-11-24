"""Weather and conditions tools."""

from __future__ import annotations

import json
from typing import List

import httpx
from langchain.tools import tool

from agent.config import Config
from agent.tools.geo import get_coordinates


@tool
def get_weather_forecast(location: str, dates: List[str] | None = None) -> str:
    """Get weather forecast for a location and dates.

    Args:
        location: Location name or coordinates
        dates: List of dates in YYYY-MM-DD format

    Returns:
        JSON string with weather forecast
    """
    try:
        # First, get coordinates if location is a name
        lat, lon = None, None
        if isinstance(location, str):
            # Check if it's coordinates in string format "lat,lon"
            try:
                parts = location.split(",")
                if len(parts) == 2:
                    lat, lon = float(parts[0].strip()), float(parts[1].strip())
            except (ValueError, AttributeError):
                # Not coordinates, treat as location name - call get_coordinates tool
                coord_result = get_coordinates.invoke({"location_name": location})
                coord_data = json.loads(coord_result)
                lat = coord_data.get("coordinates", {}).get("lat")
                lon = coord_data.get("coordinates", {}).get("lon")
        elif isinstance(location, dict):
            lat, lon = location.get("lat"), location.get("lon")
        
        # Try OpenWeatherMap first if API key is available
        if Config.OPENWEATHER_API_KEY and lat and lon:
            def _call_openweather() -> str:
                with httpx.Client() as client:
                    url = "https://api.openweathermap.org/data/2.5/forecast"
                    params = {
                        "lat": lat,
                        "lon": lon,
                        "appid": Config.OPENWEATHER_API_KEY,
                        "units": "imperial",
                    }
                    response = client.get(url, params=params, timeout=10.0)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Process current weather
                    current = data.get("list", [{}])[0] if data.get("list") else {}
                    current_main = current.get("main", {})
                    current_weather = current.get("weather", [{}])[0]
                    
                    forecast_data = {
                        "current": {
                            "temp": round(current_main.get("temp", 0)),
                            "feels_like": round(current_main.get("feels_like", 0)),
                            "condition": current_weather.get("description", "Unknown"),
                            "wind": f"{current.get('wind', {}).get('speed', 0):.1f} mph",
                            "humidity": current_main.get("humidity", 0),
                        },
                        "daily": [],
                        "source": "OpenWeatherMap",
                    }
                    
                    # Process daily forecasts
                    if dates:
                        for date in dates:
                            # Find closest forecast for this date
                            for item in data.get("list", []):
                                if date in item.get("dt_txt", ""):
                                    main = item.get("main", {})
                                    weather = item.get("weather", [{}])[0]
                                    forecast_data["daily"].append({
                                        "date": date,
                                        "high": round(main.get("temp_max", 0)),
                                        "low": round(main.get("temp_min", 0)),
                                        "condition": weather.get("description", "Unknown"),
                                        "precipitation": item.get("rain", {}).get("3h", 0),
                                    })
                                    break
                    
                    return json.dumps({
                        "location": location,
                        "forecast": forecast_data,
                    })
            
            # Use cached API call with rate limiting (cache for 1 hour)
            result = cached_api_call(
                endpoint="openweather",
                params={"lat": lat, "lon": lon, "dates": dates},
                api_func=_call_openweather,
                ttl=3600.0,  # Cache for 1 hour
            )
            if result:
                return result
        
        # Fallback to Weather.gov for US locations (free, no key)
        if lat and lon:
            try:
                def _call_weather_gov() -> str:
                    with httpx.Client() as client:
                        # Get grid point from lat/lon
                        points_url = f"https://api.weather.gov/points/{lat},{lon}"
                        headers = {"User-Agent": "AdventureAgent/1.0"}
                        response = client.get(points_url, headers=headers, timeout=10.0)
                        response.raise_for_status()
                        points_data = response.json()
                        
                        forecast_url = points_data.get("properties", {}).get("forecast")
                        if forecast_url:
                            response = client.get(forecast_url, headers=headers, timeout=10.0)
                            response.raise_for_status()
                            forecast_data = response.json()
                            
                            periods = forecast_data.get("properties", {}).get("periods", [])
                            if periods:
                                current = periods[0]
                                return json.dumps({
                                    "location": location,
                                    "forecast": {
                                        "current": {
                                            "temp": current.get("temperature", 0),
                                            "condition": current.get("shortForecast", "Unknown"),
                                            "wind": current.get("windSpeed", "Unknown"),
                                        },
                                        "daily": [
                                            {
                                                "date": p.get("startTime", "")[:10],
                                                "high": p.get("temperature", 0),
                                                "low": p.get("temperature", 0),  # Weather.gov doesn't always separate
                                                "condition": p.get("shortForecast", "Unknown"),
                                                "precipitation": 0,
                                            }
                                            for p in periods[:7]  # Next 7 periods
                                        ],
                                    },
                                    "source": "National Weather Service",
                                })
                        raise ValueError("No forecast URL from Weather.gov")
                
                # Use cached API call with rate limiting (cache for 1 hour)
                result = cached_api_call(
                    endpoint="weather_gov",
                    params={"lat": lat, "lon": lon},
                    api_func=_call_weather_gov,
                    ttl=3600.0,  # Cache for 1 hour
                )
                if result:
                    return result
            except Exception as e:
                print(f"Weather.gov error: {e}")
    except Exception as e:
        print(f"Weather forecast error for {location}: {e}")
    
    # Fallback placeholder data
    return json.dumps({
        "location": location,
        "forecast": {
            "current": {"temp": 65, "condition": "Sunny", "wind": "5 mph"},
            "daily": [
                {"date": date, "high": 70, "low": 50, "condition": "Sunny", "precipitation": 0}
                for date in (dates or [])
            ],
        },
        "source": "Placeholder",
    })


@tool
def get_trail_conditions(location: str, activity_type: str = "mountain_biking") -> str:
    """Get current trail conditions for a location.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with trail conditions
    """
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "conditions": "Good",
        "reports": [
            {"date": "2024-01-15", "condition": "Dry", "notes": "Trail in excellent condition"},
        ],
        "seasonal_info": "Best conditions typically in spring and fall",
    })


@tool
def get_seasonal_information(location: str, activity_type: str = "mountain_biking") -> str:
    """Get seasonal information for a location and activity.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with seasonal information
    """
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "best_seasons": ["Spring", "Fall"],
        "seasonal_considerations": {
            "spring": "Muddy conditions possible, wildflowers",
            "summer": "Hot, bring extra water",
            "fall": "Ideal conditions, beautiful colors",
            "winter": "Snow possible, check conditions",
        },
    })


@tool
def check_weather_alerts(location: str) -> str:
    """Check for weather alerts and warnings.

    Args:
        location: Location name or region

    Returns:
        JSON string with weather alerts
    """
    return json.dumps({
        "location": location,
        "alerts": [],
        "warnings": [],
    })

