"""Food and resupply tools."""

from __future__ import annotations

import json
from typing import Any, Dict, List

import httpx
from langchain.tools import tool

from agent.cache import cached_api_call
from agent.config import Config
from agent.tools.geo import calculate_distance, get_coordinates


@tool
def find_grocery_stores(location: str, route_info: Dict[str, Any] | None = None) -> str:
    """Find grocery stores near a location or route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with grocery stores
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        grocery_stores = []

        # Use Google Places API if available
        if Config.GOOGLE_PLACES_API_KEY:
            def _search_google_grocery() -> List[dict]:
                """Search for grocery stores via Google Places API."""
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 10000,  # 10km radius
                        "type": "supermarket",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        return response.json().get("results", [])[:10]
                    return []

            try:
                # Cache grocery store search for 12 hours (stores don't move)
                places = cached_api_call(
                    endpoint="google_places",
                    params={"lat": lat, "lon": lon, "type": "supermarket"},
                    api_func=_search_google_grocery,
                    ttl=43200.0,  # 12 hours
                )

                for place in places or []:
                    place_lat = place.get("geometry", {}).get("location", {}).get("lat")
                    place_lon = place.get("geometry", {}).get("location", {}).get("lng")

                    # Calculate distance
                    distance_miles = None
                    if place_lat and place_lon:
                        dist_result = calculate_distance.invoke({
                            "point1": {"lat": lat, "lon": lon},
                            "point2": {"lat": place_lat, "lon": place_lon},
                        })
                        dist_data = json.loads(dist_result)
                        distance_miles = dist_data.get("distance_miles")

                    grocery_stores.append({
                        "name": place.get("name", "Grocery Store"),
                        "location": place.get("vicinity", location),
                        "distance_miles": round(distance_miles, 1) if distance_miles else None,
                        "rating": place.get("rating"),
                        "coordinates": {
                            "lat": place_lat,
                            "lon": place_lon,
                        },
                    })

                if grocery_stores:
                    return json.dumps({
                        "location": location,
                        "grocery_stores": grocery_stores,
                        "source": "google_places",
                    })
            except Exception as e:
                print(f"Google Places API error for grocery stores: {e}")
        
        # Fallback: Use OpenStreetMap Overpass API for grocery stores
        def _search_osm_grocery() -> List[dict]:
            """Search for grocery stores via Overpass API."""
            with httpx.Client() as client:
                overpass_url = "https://overpass-api.de/api/interpreter"
                query = f"""
                [out:json][timeout:25];
                (
                  node["shop"="supermarket"](around:10000,{lat},{lon});
                  node["shop"="grocery"](around:10000,{lat},{lon});
                  way["shop"="supermarket"](around:10000,{lat},{lon});
                  way["shop"="grocery"](around:10000,{lat},{lon});
                );
                out center;
                """
                response = client.post(overpass_url, data=query, timeout=30.0)
                if response.status_code == 200:
                    return response.json().get("elements", [])[:10]
                return []

        try:
            # Cache OSM grocery search for 24 hours (OSM data changes slowly)
            elements = cached_api_call(
                endpoint="overpass",
                params={"lat": lat, "lon": lon, "type": "grocery"},
                api_func=_search_osm_grocery,
                ttl=86400.0,  # 24 hours
            )

            for element in elements or []:
                tags = element.get("tags", {})
                name = tags.get("name", "Grocery Store")

                # Get coordinates
                if "center" in element:
                    place_lat = element["center"].get("lat")
                    place_lon = element["center"].get("lon")
                elif "lat" in element:
                    place_lat = element.get("lat")
                    place_lon = element.get("lon")
                else:
                    continue

                # Calculate distance
                distance_miles = None
                if place_lat and place_lon:
                    dist_result = calculate_distance.invoke({
                        "point1": {"lat": lat, "lon": lon},
                        "point2": {"lat": place_lat, "lon": place_lon},
                    })
                    dist_data = json.loads(dist_result)
                    distance_miles = dist_data.get("distance_miles")

                grocery_stores.append({
                    "name": name,
                    "location": tags.get("addr:full") or location,
                    "distance_miles": round(distance_miles, 1) if distance_miles else None,
                    "coordinates": {
                        "lat": place_lat,
                        "lon": place_lon,
                    },
                })

            if grocery_stores:
                return json.dumps({
                    "location": location,
                    "grocery_stores": grocery_stores,
                    "source": "openstreetmap",
                })
        except Exception as e:
            print(f"OpenStreetMap API error for grocery stores: {e}")
    except Exception as e:
        print(f"Grocery store search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "grocery_stores": [
            {
                "name": "Local Grocery Store",
                "location": "Near trailhead",
                "distance_miles": 2.5,
            }
        ],
        "source": "placeholder",
    })


@tool
def find_restaurants(location: str, route_info: Dict[str, Any] | None = None) -> str:
    """Find restaurants and cafes near a location or route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with restaurants
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        restaurants = []

        # Use Google Places API if available
        if Config.GOOGLE_PLACES_API_KEY:
            def _search_google_restaurants() -> List[dict]:
                """Search for restaurants via Google Places API."""
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 10000,  # 10km radius
                        "type": "restaurant",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        return response.json().get("results", [])[:10]
                    return []

            try:
                # Cache restaurant search for 6 hours (restaurant data may change)
                places = cached_api_call(
                    endpoint="google_places",
                    params={"lat": lat, "lon": lon, "type": "restaurant"},
                    api_func=_search_google_restaurants,
                    ttl=21600.0,  # 6 hours
                )

                for place in places or []:
                    place_lat = place.get("geometry", {}).get("location", {}).get("lat")
                    place_lon = place.get("geometry", {}).get("location", {}).get("lng")

                    # Calculate distance
                    distance_miles = None
                    if place_lat and place_lon:
                        dist_result = calculate_distance.invoke({
                            "point1": {"lat": lat, "lon": lon},
                            "point2": {"lat": place_lat, "lon": place_lon},
                        })
                        dist_data = json.loads(dist_result)
                        distance_miles = dist_data.get("distance_miles")

                    # Get restaurant type from types array
                    types = place.get("types", [])
                    restaurant_type = "Restaurant"
                    if "cafe" in types:
                        restaurant_type = "Cafe"
                    elif "fast_food" in types:
                        restaurant_type = "Fast Food"
                    elif "bakery" in types:
                        restaurant_type = "Bakery"

                    restaurants.append({
                        "name": place.get("name", "Restaurant"),
                        "type": restaurant_type,
                        "location": place.get("vicinity", location),
                        "distance_miles": round(distance_miles, 1) if distance_miles else None,
                        "rating": place.get("rating"),
                        "price_level": place.get("price_level"),
                        "coordinates": {
                            "lat": place_lat,
                            "lon": place_lon,
                        },
                    })

                if restaurants:
                    return json.dumps({
                        "location": location,
                        "restaurants": restaurants,
                        "source": "google_places",
                    })
            except Exception as e:
                print(f"Google Places API error for restaurants: {e}")
        
        # Fallback: Use OpenStreetMap Overpass API
        def _search_osm_restaurants() -> List[dict]:
            """Search for restaurants via Overpass API."""
            with httpx.Client() as client:
                overpass_url = "https://overpass-api.de/api/interpreter"
                query = f"""
                [out:json][timeout:25];
                (
                  node["amenity"="restaurant"](around:10000,{lat},{lon});
                  node["amenity"="cafe"](around:10000,{lat},{lon});
                  way["amenity"="restaurant"](around:10000,{lat},{lon});
                  way["amenity"="cafe"](around:10000,{lat},{lon});
                );
                out center;
                """
                response = client.post(overpass_url, data=query, timeout=30.0)
                if response.status_code == 200:
                    return response.json().get("elements", [])[:10]
                return []

        try:
            # Cache OSM restaurant search for 24 hours
            elements = cached_api_call(
                endpoint="overpass",
                params={"lat": lat, "lon": lon, "type": "restaurant"},
                api_func=_search_osm_restaurants,
                ttl=86400.0,  # 24 hours
            )

            for element in elements or []:
                tags = element.get("tags", {})
                name = tags.get("name", "Restaurant")
                amenity = tags.get("amenity", "restaurant")
                restaurant_type = "Cafe" if amenity == "cafe" else "Restaurant"

                # Get coordinates
                if "center" in element:
                    place_lat = element["center"].get("lat")
                    place_lon = element["center"].get("lon")
                elif "lat" in element:
                    place_lat = element.get("lat")
                    place_lon = element.get("lon")
                else:
                    continue

                # Calculate distance
                distance_miles = None
                if place_lat and place_lon:
                    dist_result = calculate_distance.invoke({
                        "point1": {"lat": lat, "lon": lon},
                        "point2": {"lat": place_lat, "lon": place_lon},
                    })
                    dist_data = json.loads(dist_result)
                    distance_miles = dist_data.get("distance_miles")

                restaurants.append({
                    "name": name,
                    "type": restaurant_type,
                    "location": tags.get("addr:full") or location,
                    "distance_miles": round(distance_miles, 1) if distance_miles else None,
                    "coordinates": {
                        "lat": place_lat,
                        "lon": place_lon,
                    },
                })

            if restaurants:
                return json.dumps({
                    "location": location,
                    "restaurants": restaurants,
                    "source": "openstreetmap",
                })
        except Exception as e:
            print(f"OpenStreetMap API error for restaurants: {e}")
    except Exception as e:
        print(f"Restaurant search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "restaurants": [
            {
                "name": "Trailside Cafe",
                "type": "Cafe",
                "location": "Along route",
                "distance_miles": 5.0,
            }
        ],
        "source": "placeholder",
    })


@tool
def find_water_sources(location: str, route_info: Dict[str, Any] | None = None) -> str:
    """Find water sources along a route.

    Args:
        location: Location name or region
        route_info: Information about the route

    Returns:
        JSON string with water sources
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        water_sources = []

        # Use OpenStreetMap Overpass API for water sources
        def _search_osm_water() -> List[dict]:
            """Search for water sources via Overpass API."""
            with httpx.Client() as client:
                overpass_url = "https://overpass-api.de/api/interpreter"
                query = f"""
                [out:json][timeout:25];
                (
                  node["natural"="spring"](around:5000,{lat},{lon});
                  node["amenity"="drinking_water"](around:5000,{lat},{lon});
                  way["natural"="spring"](around:5000,{lat},{lon});
                  way["amenity"="drinking_water"](around:5000,{lat},{lon});
                );
                out center;
                """
                response = client.post(overpass_url, data=query, timeout=30.0)
                if response.status_code == 200:
                    return response.json().get("elements", [])[:10]
                return []

        try:
            # Cache water source search for 24 hours (water sources don't move)
            elements = cached_api_call(
                endpoint="overpass",
                params={"lat": lat, "lon": lon, "type": "water"},
                api_func=_search_osm_water,
                ttl=86400.0,  # 24 hours
            )

            for element in elements or []:
                tags = element.get("tags", {})
                natural = tags.get("natural", "")
                amenity = tags.get("amenity", "")

                if natural == "spring":
                    source_type = "Spring"
                    quality = "Filter recommended"
                elif amenity == "drinking_water":
                    source_type = "Drinking Water"
                    quality = "Potable"
                else:
                    source_type = "Water Source"
                    quality = "Filter recommended"

                # Get coordinates
                if "center" in element:
                    place_lat = element["center"].get("lat")
                    place_lon = element["center"].get("lon")
                elif "lat" in element:
                    place_lat = element.get("lat")
                    place_lon = element.get("lon")
                else:
                    continue

                name = tags.get("name", source_type)

                water_sources.append({
                    "type": source_type,
                    "name": name,
                    "location": f"Near {location}",
                    "quality": quality,
                    "coordinates": {
                        "lat": place_lat,
                        "lon": place_lon,
                    },
                })

            if water_sources:
                return json.dumps({
                    "location": location,
                    "water_sources": water_sources,
                    "source": "openstreetmap",
                        })
        except Exception as e:
            print(f"OpenStreetMap API error for water sources: {e}")
    except Exception as e:
        print(f"Water source search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "water_sources": [
            {
                "type": "Stream",
                "location": "Mile 5",
                "quality": "Filter recommended",
            }
        ],
        "source": "placeholder",
    })


@tool
def find_resupply_points(location: str, duration_days: int = 1) -> str:
    """Find resupply points for multi-day trips.

    Args:
        location: Location name or region
        duration_days: Duration of trip in days

    Returns:
        JSON string with resupply points
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        resupply_points = []

        # Use Google Places API to find towns with services
        if Config.GOOGLE_PLACES_API_KEY:
            def _search_resupply_points() -> List[dict]:
                """Search for resupply points via Google Places API."""
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 50000,  # 50km radius for multi-day trips
                        "type": "supermarket",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        return response.json().get("results", [])[:5]
                    return []

            try:
                # Cache resupply point search for 12 hours
                places = cached_api_call(
                    endpoint="google_places",
                    params={"lat": lat, "lon": lon, "type": "resupply", "radius": 50000},
                    api_func=_search_resupply_points,
                    ttl=43200.0,  # 12 hours
                )

                for place in places or []:
                    name = place.get("name", "Resupply Point")
                    vicinity = place.get("vicinity", location)

                    # Determine services available
                    services = ["Grocery"]
                    if "restaurant" in vicinity.lower() or "cafe" in vicinity.lower():
                        services.append("Restaurant")
                    if "post" in vicinity.lower() or "mail" in vicinity.lower():
                        services.append("Post office")

                    resupply_points.append({
                        "name": name,
                        "location": vicinity,
                        "services": services,
                        "coordinates": {
                            "lat": place.get("geometry", {}).get("location", {}).get("lat"),
                            "lon": place.get("geometry", {}).get("location", {}).get("lng"),
                        },
                    })

                if resupply_points:
                    return json.dumps({
                        "location": location,
                        "resupply_points": resupply_points,
                        "duration_days": duration_days,
                        "source": "google_places",
                    })
            except Exception as e:
                print(f"Google Places API error for resupply points: {e}")
    except Exception as e:
        print(f"Resupply point search error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "resupply_points": [
            {
                "name": "Trail Town",
                "location": "Mile 50",
                "services": ["Grocery", "Restaurant", "Post office"],
            }
        ],
        "duration_days": duration_days,
        "source": "placeholder",
    })


@tool
def get_local_food_recommendations(location: str) -> str:
    """Get local food recommendations for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with local food recommendations
    """
    try:
        # Use Google Places API to find highly-rated restaurants
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")
        
        local_specialties = []

        if Config.GOOGLE_PLACES_API_KEY:
            def _search_top_restaurants() -> List[dict]:
                """Search for top-rated restaurants via Google Places API."""
                with httpx.Client() as client:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lon}",
                        "radius": 10000,
                        "type": "restaurant",
                        "key": Config.GOOGLE_PLACES_API_KEY,
                    }
                    response = client.get(url, params=params, timeout=10.0)
                    if response.status_code == 200:
                        places = response.json().get("results", [])
                        # Sort by rating and return top 3
                        return sorted(
                            [p for p in places if p.get("rating")],
                            key=lambda x: x.get("rating", 0),
                            reverse=True
                        )[:3]
                    return []

            try:
                # Cache top restaurant search for 6 hours
                sorted_places = cached_api_call(
                    endpoint="google_places",
                    params={"lat": lat, "lon": lon, "type": "top_restaurants"},
                    api_func=_search_top_restaurants,
                    ttl=21600.0,  # 6 hours
                )

                for place in sorted_places or []:
                    name = place.get("name", "Restaurant")
                    rating = place.get("rating")
                    types = place.get("types", [])

                    # Determine cuisine type
                    cuisine = "Local cuisine"
                    if "mexican" in str(types).lower():
                        cuisine = "Mexican"
                    elif "american" in str(types).lower():
                        cuisine = "American"
                    elif "italian" in str(types).lower():
                        cuisine = "Italian"

                    local_specialties.append({
                        "name": name,
                        "description": f"Highly-rated {cuisine.lower()} restaurant (Rating: {rating})",
                        "where_to_find": place.get("vicinity", location),
                    })

                if local_specialties:
                    return json.dumps({
                        "location": location,
                        "local_specialties": local_specialties,
                        "source": "google_places",
                    })
            except Exception as e:
                print(f"Google Places API error for food recommendations: {e}")
    except Exception as e:
        print(f"Food recommendations error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "local_specialties": [
            {
                "name": "Local specialty",
                "description": "Regional favorite",
                "where_to_find": "Local restaurants",
            }
        ],
        "source": "placeholder",
    })

