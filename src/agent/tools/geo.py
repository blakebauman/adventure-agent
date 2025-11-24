"""Geographic tools for coordinates and distance calculations."""

from __future__ import annotations

import json
import math
from typing import Dict

import httpx
from langchain.tools import tool

from agent.cache import cached_api_call
from agent.config import Config


@tool
def get_coordinates(location_name: str) -> str:
    """Get coordinates for a location using geocoding.

    Args:
        location_name: Name of the location

    Returns:
        JSON string with coordinates
    """
    try:
        # Try OpenCage first if API key is available
        if Config.OPENCAGE_API_KEY:
            def _call_opencage() -> str:
                with httpx.Client() as client:
                    url = "https://api.opencagedata.com/geocode/v1/json"
                    # Add country code bias to prioritize US results (Arizona focus)
                    # If location contains "Arizona" or "AZ", bias more strongly
                    countrycode = "us"
                    if "arizona" in location_name.lower() or " az" in location_name.lower() or location_name.lower().endswith(" az"):
                        countrycode = "us"
                    
                    params = {
                        "q": location_name,
                        "key": Config.OPENCAGE_API_KEY,
                        "limit": 5,  # Get more results to filter
                        "countrycode": countrycode,  # Bias toward US
                        "bounds": "-115.0,31.0,-108.0,37.0",  # Arizona bounding box (rough)
                    }
                    response = client.get(url, params=params, timeout=10.0)
                    response.raise_for_status()
                    data = response.json()
                    
                    if data.get("results"):
                        # Filter results to prefer US, then Arizona
                        results = data["results"]
                        us_results = [r for r in results if r.get("components", {}).get("country_code", "").upper() == "US"]
                        az_results = [r for r in us_results if r.get("components", {}).get("state", "").upper() in ["AZ", "ARIZONA"]]
                        
                        # Prefer Arizona results, then US results, then any result
                        if az_results:
                            result = az_results[0]
                        elif us_results:
                            result = us_results[0]
                        else:
                            result = results[0]
                        
                        geometry = result["geometry"]
                        components = result.get("components", {})
                        country_code = components.get("country_code", "US").upper()
                        
                        # Warn if we got a non-US result
                        if country_code != "US":
                            print(f"Warning: Geocoding returned non-US result for '{location_name}': {result.get('formatted', 'Unknown')}")
                        
                        return json.dumps({
                            "location": location_name,
                            "coordinates": {"lat": geometry["lat"], "lon": geometry["lng"]},
                            "region": components.get("state") or components.get("region") or "Unknown",
                            "country": country_code,
                            "formatted_address": result.get("formatted", location_name),
                        })
                    raise ValueError("No results from OpenCage")
            
            # Use cached API call with rate limiting
            result = cached_api_call(
                endpoint="opencage",
                params={"location": location_name},
                api_func=_call_opencage,
                ttl=86400.0,  # Cache for 24 hours (coordinates don't change)
            )
            if result:
                return result
        
        # Fallback to Nominatim (OpenStreetMap, free, no key required)
        def _call_nominatim() -> str:
            with httpx.Client() as client:
                url = "https://nominatim.openstreetmap.org/search"
                # Add country code and viewbox to bias toward US/Arizona
                # If location contains "Arizona" or "AZ", add it to query
                query = location_name
                if "arizona" not in location_name.lower() and " az" not in location_name.lower() and not location_name.lower().endswith(" az"):
                    # Add "Arizona, USA" to help disambiguate
                    query = f"{location_name}, Arizona, USA"
                
                params = {
                    "q": query,
                    "format": "json",
                    "limit": 5,  # Get more results to filter
                    "addressdetails": 1,
                    "countrycodes": "us",  # Limit to US
                    "viewbox": "-115.0,31.0,-108.0,37.0",  # Arizona bounding box
                    "bounded": "0",  # Don't require strict bounding, just bias
                }
                headers = {"User-Agent": "AdventureAgent/1.0"}  # Required by Nominatim
                response = client.get(url, params=params, headers=headers, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                if data:
                    # Filter results to prefer US, then Arizona
                    us_results = [r for r in data if r.get("address", {}).get("country_code", "").lower() == "us"]
                    az_results = [r for r in us_results if r.get("address", {}).get("state", "").upper() in ["AZ", "ARIZONA"]]
                    
                    # Prefer Arizona results, then US results, then any result
                    if az_results:
                        result = az_results[0]
                    elif us_results:
                        result = us_results[0]
                    else:
                        result = data[0]
                    
                    country_code = result.get("address", {}).get("country_code", "us").upper()
                    
                    # Warn if we got a non-US result
                    if country_code != "US":
                        print(f"Warning: Geocoding returned non-US result for '{location_name}': {result.get('display_name', 'Unknown')}")
                    
                    return json.dumps({
                        "location": location_name,
                        "coordinates": {"lat": float(result["lat"]), "lon": float(result["lon"])},
                        "region": result.get("address", {}).get("state") or result.get("address", {}).get("region") or "Unknown",
                        "country": country_code,
                        "formatted_address": result.get("display_name", location_name),
                    })
                raise ValueError("No results from Nominatim")
        
        # Use cached API call with rate limiting
        result = cached_api_call(
            endpoint="nominatim",
            params={"location": location_name},
            api_func=_call_nominatim,
            ttl=86400.0,  # Cache for 24 hours
        )
        if result:
            return result
    except Exception as e:
        # Fallback to placeholder data on error
        print(f"Geocoding error for {location_name}: {e}")
    
    # Fallback placeholder data
    return json.dumps({
        "location": location_name,
        "coordinates": {"lat": 36.1699, "lon": -115.1398},  # Example: Las Vegas
        "region": "Unknown",
        "country": "US",
        "formatted_address": location_name,
    })


@tool
def calculate_distance(
    point1: Dict[str, float], point2: Dict[str, float]
) -> str:
    """Calculate distance between two points using Haversine formula.

    Args:
        point1: First point with lat and lon
        point2: Second point with lat and lon

    Returns:
        JSON string with distance information
    """
    try:
        lat1, lon1 = point1.get("lat", 0), point1.get("lon", 0)
        lat2, lon2 = point2.get("lat", 0), point2.get("lon", 0)
        
        # Haversine formula for great-circle distance
        R = 3958.8  # Earth radius in miles
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        distance_miles = R * c
        distance_km = distance_miles * 1.60934
        
        return json.dumps({
            "distance_miles": round(distance_miles, 2),
            "distance_km": round(distance_km, 2),
            "point1": point1,
            "point2": point2,
        })
    except Exception as e:
        print(f"Distance calculation error: {e}")
        return json.dumps({
            "distance_miles": 0.0,
            "distance_km": 0.0,
            "error": str(e),
        })

