"""Accommodation search tools."""

from __future__ import annotations

import json

import httpx
from langchain.tools import tool

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
            try:
                with httpx.Client() as client:
                    url = "https://ridb.recreation.gov/api/v1/facilities"
                    # Use API key from config, fallback to "public" for rate-limited access
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
                        
                        for facility in facilities[:10]:  # Limit to 10 results
                            accommodations.append({
                                "name": facility.get("FacilityName", "Campground"),
                                "type": "campground",
                                "location": facility.get("FacilityAddressState", location),
                                "price_range": "$20-60/night",  # Recreation.gov doesn't always provide pricing
                                "amenities": [
                                    "Restrooms",
                                    "Water",
                                    "Fire pits",
                                    "Picnic tables",
                                ],
                                "coordinates": {
                                    "lat": facility.get("FacilityLatitude"),
                                    "lon": facility.get("FacilityLongitude"),
                                },
                                "description": facility.get("FacilityDescription", "")[:200],
                                "url": f"https://www.recreation.gov/camping/campgrounds/{facility.get('FacilityID')}" if facility.get("FacilityID") else None,
                                "reservable": facility.get("Reservable", False),
                            })
                    elif response.status_code == 401:
                        print(f"Recreation.gov API authentication failed. Check your RECREATION_GOV_API_KEY in .env file.")
                    else:
                        print(f"Recreation.gov API error: {response.status_code} - {response.text[:200]}")
            except Exception as e:
                print(f"Recreation.gov API error: {e}")
        
        # For hotels/hostels, use Google Places API if available
        if Config.GOOGLE_PLACES_API_KEY and (not accommodation_type or accommodation_type.lower() in ["hotel", "hostel", "lodging"]):
            try:
                with httpx.Client() as client:
                    # First, find nearby places
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
                        places = data.get("results", [])
                        
                        for place in places[:10]:  # Limit to 10 results
                            place_id = place.get("place_id")
                            name = place.get("name", "Accommodation")
                            rating = place.get("rating")
                            price_level = place.get("price_level")  # 0-4 scale
                            
                            # Get more details
                            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
                            details_params = {
                                "place_id": place_id,
                                "fields": "name,formatted_address,formatted_phone_number,website,rating,price_level",
                                "key": Config.GOOGLE_PLACES_API_KEY,
                            }
                            
                            try:
                                details_response = client.get(details_url, params=details_params, timeout=10.0)
                                if details_response.status_code == 200:
                                    details_data = details_response.json().get("result", {})
                                    
                                    # Convert price level to range
                                    price_ranges = {
                                        0: "$",
                                        1: "$$",
                                        2: "$$$",
                                        3: "$$$$",
                                        4: "$$$$$",
                                    }
                                    price_range = price_ranges.get(price_level, "$$")
                                    
                                    accommodations.append({
                                        "name": details_data.get("name", name),
                                        "type": "hotel",
                                        "location": details_data.get("formatted_address", location),
                                        "price_range": price_range,
                                        "rating": rating,
                                        "phone": details_data.get("formatted_phone_number"),
                                        "website": details_data.get("website"),
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

