"""Accommodation search tools."""

from __future__ import annotations

import json

import httpx
from langchain.tools import tool

from agent.cache import cached_api_call
from agent.config import Config
from agent.tools.geo import get_coordinates


@tool
def search_accommodations(
    location: str,
    accommodation_type: str | None = None,
    check_in: str | None = None,
    check_out: str | None = None,
) -> str:
    """Search for accommodations near a location.

    Args:
        location: Location name
        accommodation_type: Type (hotel, campground, hostel, etc.)
        check_in: Check-in date (YYYY-MM-DD)
        check_out: Check-out date (YYYY-MM-DD)

    Returns:
        JSON string with accommodation options
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        accommodations = []
        
        # For campgrounds, use Recreation.gov API
        # Uses RECREATION_GOV_API_KEY from config if available, otherwise falls back to "public" key
        if not accommodation_type or accommodation_type.lower() in ["campground", "camping", "campsite"]:
            def _call_recreation_gov() -> list:
                """Fetch campgrounds from Recreation.gov API."""
                with httpx.Client() as client:
                    url = "https://ridb.recreation.gov/api/v1/facilities"
                    api_key = Config.RECREATION_GOV_API_KEY or "public"
                    headers = {"apikey": api_key}
                    params = {
                        "limit": 10,
                        "offset": 0,
                        "latitude": lat,
                        "longitude": lon,
                        "radius": 25,  # 25 mile radius
                        "query": "campground",
                    }

                    response = client.get(url, headers=headers, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        facilities = data.get("RECDATA", [])
                        results = []
                        for facility in facilities[:10]:
                            results.append({
                                "name": facility.get("FacilityName", "Campground"),
                                "type": "campground",
                                "location": facility.get("FacilityAddressState", location),
                                "price_range": "$20-60/night",
                                "amenities": ["Restrooms", "Water", "Fire pits", "Picnic tables"],
                                "coordinates": {
                                    "lat": facility.get("FacilityLatitude"),
                                    "lon": facility.get("FacilityLongitude"),
                                },
                                "description": facility.get("FacilityDescription", "")[:200],
                                "url": f"https://www.recreation.gov/camping/campgrounds/{facility.get('FacilityID')}" if facility.get("FacilityID") else None,
                                "reservable": facility.get("Reservable", False),
                            })
                        return results
                    elif response.status_code == 401:
                        print("Recreation.gov API authentication failed. Check your RECREATION_GOV_API_KEY in .env file.")
                    else:
                        print(f"Recreation.gov API error: {response.status_code} - {response.text[:200]}")
                    return []

            try:
                # Use cached API call with rate limiting (cache for 6 hours - campground data changes slowly)
                campground_results = cached_api_call(
                    endpoint="recreation_gov",
                    params={"lat": lat, "lon": lon, "type": "campground"},
                    api_func=_call_recreation_gov,
                    ttl=21600.0,  # 6 hours
                )
                if campground_results:
                    accommodations.extend(campground_results)
            except Exception as e:
                print(f"Recreation.gov API error: {e}")
        
        # For hotels/hostels, use Google Places API if available
        if Config.GOOGLE_PLACES_API_KEY and (not accommodation_type or accommodation_type.lower() in ["hotel", "hostel", "lodging"]):
            def _call_google_places_nearby() -> list:
                """Fetch nearby lodging from Google Places API."""
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 10000,  # 10km radius
                        "type": "lodging",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }

                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        return data.get("results", [])[:10]  # Limit to 10
                    return []

            def _get_place_details(place_id: str) -> dict:
                """Fetch place details from Google Places API."""
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/details/json"
                    params = {
                        "place_id": place_id,
                        "fields": "name,formatted_address,formatted_phone_number,website,rating,price_level",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        return response.json().get("result", {})
                    return {}

            try:
                # Cache nearby search for 6 hours
                places = cached_api_call(
                    endpoint="google_places",
                    params={"lat": lat, "lon": lon, "type": "lodging"},
                    api_func=_call_google_places_nearby,
                    ttl=21600.0,  # 6 hours
                )

                price_ranges = {0: "$", 1: "$$", 2: "$$$", 3: "$$$$", 4: "$$$$$"}

                for place in places or []:
                    place_id = place.get("place_id")
                    name = place.get("name", "Accommodation")
                    rating = place.get("rating")
                    price_level = place.get("price_level")

                    try:
                        # Cache each place details for 24 hours (business info changes slowly)
                        details_data = cached_api_call(
                            endpoint="google_places_details",
                            params={"place_id": place_id},
                            api_func=lambda pid=place_id: _get_place_details(pid),
                            ttl=86400.0,  # 24 hours
                        )

                        price_range = price_ranges.get(price_level, "$$")
                        accommodations.append({
                            "name": details_data.get("name", name) if details_data else name,
                            "type": "hotel",
                            "location": details_data.get("formatted_address", location) if details_data else location,
                            "price_range": price_range,
                            "rating": rating,
                            "phone": details_data.get("formatted_phone_number") if details_data else None,
                            "website": details_data.get("website") if details_data else None,
                            "coordinates": {
                                "lat": place.get("geometry", {}).get("location", {}).get("lat"),
                                "lon": place.get("geometry", {}).get("location", {}).get("lng"),
                            },
                            "url": f"https://www.google.com/maps/place/?q=place_id:{place_id}",
                        })
                    except Exception as e:
                        print(f"Google Places details error: {e}")
            except Exception as e:
                print(f"Google Places API error: {e}")
        
        if accommodations:
            return json.dumps({
                "accommodations": accommodations,
                "location": location,
                "source": "recreation.gov" if not accommodation_type or accommodation_type.lower() in ["campground", "camping"] else "google_places",
            })
    except Exception as e:
        print(f"Accommodation search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "accommodations": [
            {
                "name": f"{accommodation_type or 'Campground'} near {location}",
                "type": accommodation_type or "campground",
                "location": location,
                "price_range": "$20-40/night",
                "amenities": ["Restrooms", "Water", "Fire pits"],
            }
        ],
        "source": "placeholder",
    })

