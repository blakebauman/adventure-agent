"""Permits and regulations tools."""

from __future__ import annotations

import json
from typing import List

import httpx
from langchain.tools import tool

from agent.cache import cached_api_call
from agent.config import Config
from agent.tools.geo import get_coordinates
from agent.tools.web_search import WebSearchTool


@tool
def check_permit_requirements(
    location: str, activity_type: str = "mountain_biking", group_size: int = 1
) -> str:
    """Check if permits are required for a location and activity.

    Args:
        location: Location name or region
        activity_type: Type of activity
        group_size: Number of people in group

    Returns:
        JSON string with permit requirements
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")

        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")

        def _check_permits_recreation_gov() -> dict | None:
            """Check permit requirements via Recreation.gov API."""
            with httpx.Client() as client:
                url = "https://ridb.recreation.gov/api/v1/facilities"
                api_key = Config.RECREATION_GOV_API_KEY or "public"
                headers = {"apikey": api_key}
                params = {
                    "limit": 10,
                    "offset": 0,
                    "latitude": lat,
                    "longitude": lon,
                    "radius": 25,
                }

                response = client.get(url, headers=headers, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    facilities = data.get("RECDATA", [])

                    # Check if any facilities require permits
                    permit_info = []
                    for facility in facilities[:5]:
                        facility_name = facility.get("FacilityName", "")
                        reservable = facility.get("Reservable", False)
                        permit_required = reservable or group_size > 10

                        if permit_required:
                            permit_info.append({
                                "facility": facility_name,
                                "permit_required": True,
                                "permit_type": "Reservation required" if reservable else "Group permit",
                                "group_size_threshold": 10,
                            })

                    return {
                        "permit_info": permit_info,
                        "facilities_found": len(facilities),
                    }
                return None

        try:
            # Cache permit checks for 12 hours (permit requirements change infrequently)
            result = cached_api_call(
                endpoint="recreation_gov_permits",
                params={"lat": lat, "lon": lon, "group_size": group_size},
                api_func=_check_permits_recreation_gov,
                ttl=43200.0,  # 12 hours
            )

            if result:
                permit_info = result.get("permit_info", [])
                if permit_info:
                    return json.dumps({
                        "location": location,
                        "activity_type": activity_type,
                        "permits_required": True,
                        "permit_details": permit_info,
                        "group_size": group_size,
                        "source": "recreation.gov",
                    })
                else:
                    return json.dumps({
                        "location": location,
                        "activity_type": activity_type,
                        "permits_required": group_size > 10,
                        "permit_type": "Day use" if group_size <= 10 else "Group permit",
                        "group_size": group_size,
                        "source": "recreation.gov",
                    })
        except Exception as e:
            print(f"Recreation.gov API error: {e}")

        # Fallback: Use web search via Tavily if available
        if Config.TAVILY_API_KEY:
            def _search_permit_requirements() -> dict | None:
                """Search for permit requirements via Tavily."""
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} {activity_type} permit requirements"
                results = search_tool.search_web(query)

                if not results:
                    return None

                permit_required = False
                permit_type = "Day use"
                for result in results[:3]:
                    content = result.get("content", "").lower()
                    if "permit required" in content or "permit needed" in content:
                        permit_required = True
                        if "group" in content or group_size > 10:
                            permit_type = "Group permit"
                        break

                return {"permit_required": permit_required, "permit_type": permit_type}

            try:
                # Cache web search for 6 hours
                result = cached_api_call(
                    endpoint="tavily_permits",
                    params={"location": location, "activity": activity_type},
                    api_func=_search_permit_requirements,
                    ttl=21600.0,  # 6 hours
                )

                if result:
                    return json.dumps({
                        "location": location,
                        "activity_type": activity_type,
                        "permits_required": result["permit_required"] or group_size > 10,
                        "permit_type": result["permit_type"],
                        "group_size": group_size,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for permit requirements: {e}")
    except Exception as e:
        print(f"Permit check error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "activity_type": activity_type,
        "permits_required": group_size > 10,
        "permit_type": "Day use" if group_size <= 10 else "Group permit",
        "application_process": "Apply online at recreation.gov",
        "group_size": group_size,
        "source": "placeholder",
    })


@tool
def get_permit_information(location: str, activity_type: str = "mountain_biking") -> str:
    """Get detailed permit information.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with permit information
    """
    try:
        # Get coordinates for location
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")

        if not lat or not lon:
            raise ValueError("Could not get coordinates for location")

        def _get_permit_info_recreation_gov() -> list:
            """Get permit info from Recreation.gov API."""
            with httpx.Client() as client:
                url = "https://ridb.recreation.gov/api/v1/facilities"
                api_key = Config.RECREATION_GOV_API_KEY or "public"
                headers = {"apikey": api_key}
                params = {
                    "limit": 5,
                    "offset": 0,
                    "latitude": lat,
                    "longitude": lon,
                    "radius": 25,
                }

                response = client.get(url, headers=headers, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    facilities = data.get("RECDATA", [])

                    permit_info_list = []
                    for facility in facilities[:3]:
                        facility_id = facility.get("FacilityID")
                        facility_name = facility.get("FacilityName", "")
                        reservable = facility.get("Reservable", False)

                        if reservable and facility_id:
                            permit_info_list.append({
                                "facility": facility_name,
                                "where_to_apply": "recreation.gov",
                                "application_url": f"https://www.recreation.gov/camping/campgrounds/{facility_id}",
                                "deadline": "30 days in advance recommended",
                                "cost": "Varies by facility",
                                "contact": "Check recreation.gov for details",
                            })
                    return permit_info_list
                return []

        try:
            # Cache permit info for 24 hours (facility info changes rarely)
            permit_info_list = cached_api_call(
                endpoint="recreation_gov_permit_info",
                params={"lat": lat, "lon": lon},
                api_func=_get_permit_info_recreation_gov,
                ttl=86400.0,  # 24 hours
            )

            if permit_info_list:
                return json.dumps({
                    "location": location,
                    "activity_type": activity_type,
                    "permit_info": permit_info_list,
                    "source": "recreation.gov",
                })
        except Exception as e:
            print(f"Recreation.gov API error: {e}")

        # Fallback: Use web search via Tavily if available
        if Config.TAVILY_API_KEY:
            def _search_permit_info() -> dict:
                """Search for permit info via Tavily."""
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} {activity_type} permit application information"
                results = search_tool.search_web(query)

                permit_info = {
                    "where_to_apply": "recreation.gov",
                    "deadline": "30 days in advance",
                    "cost": "$5-20 per person",
                    "contact": "Local ranger station",
                }

                if results:
                    for result in results[:2]:
                        content = result.get("content", "")
                        if "recreation.gov" in content.lower():
                            permit_info["where_to_apply"] = "recreation.gov"

                return permit_info

            try:
                # Cache web search for 6 hours
                permit_info = cached_api_call(
                    endpoint="tavily_permit_info",
                    params={"location": location, "activity": activity_type},
                    api_func=_search_permit_info,
                    ttl=21600.0,  # 6 hours
                )

                if permit_info:
                    return json.dumps({
                        "location": location,
                        "activity_type": activity_type,
                        "permit_info": permit_info,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for permit information: {e}")
    except Exception as e:
        print(f"Permit information error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "permit_info": {
            "where_to_apply": "recreation.gov",
            "deadline": "30 days in advance",
            "cost": "$5-20 per person",
            "contact": "Local ranger station",
        },
        "source": "placeholder",
    })


@tool
def get_regulations(location: str, activity_type: str = "mountain_biking") -> str:
    """Get regulations for a location and activity.

    Args:
        location: Location name or region
        activity_type: Type of activity

    Returns:
        JSON string with regulations
    """
    import re

    try:
        # Use web search via Tavily for regulations
        if Config.TAVILY_API_KEY:
            def _search_regulations() -> dict | None:
                """Search for regulations via Tavily."""
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} {activity_type} regulations rules"
                results = search_tool.search_web(query)

                if not results:
                    return None

                regulations = []
                group_size_limit = 10
                camping_restrictions = "Designated sites only"

                # Extract regulations from search results
                for result in results[:3]:
                    content = result.get("content", "")

                    # Common regulation patterns
                    if "stay on trail" in content.lower() or "designated trail" in content.lower():
                        if "Stay on designated trails" not in regulations:
                            regulations.append("Stay on designated trails")
                    if "pack in pack out" in content.lower() or "leave no trace" in content.lower():
                        if "Pack in, pack out" not in regulations:
                            regulations.append("Pack in, pack out")
                    if "no motorized" in content.lower() or "no motor" in content.lower():
                        if "No motorized vehicles" not in regulations:
                            regulations.append("No motorized vehicles")
                    if "wildlife" in content.lower() and ("respect" in content.lower() or "distance" in content.lower()):
                        if "Respect wildlife" not in regulations:
                            regulations.append("Respect wildlife")
                    if "group size" in content.lower() or "group limit" in content.lower():
                        size_match = re.search(r"group.*?(\d+)", content.lower())
                        if size_match:
                            group_size_limit = int(size_match.group(1))
                    if "camping" in content.lower() and "designated" in content.lower():
                        camping_restrictions = "Designated sites only"

                # Ensure we have at least basic regulations
                if not regulations:
                    regulations = [
                        "Stay on designated trails",
                        "Pack in, pack out",
                        "No motorized vehicles",
                        "Respect wildlife",
                    ]

                return {
                    "regulations": regulations[:10],
                    "group_size_limit": group_size_limit,
                    "camping_restrictions": camping_restrictions,
                }

            try:
                # Cache regulations for 24 hours (regulations change infrequently)
                result = cached_api_call(
                    endpoint="tavily_regulations",
                    params={"location": location, "activity": activity_type},
                    api_func=_search_regulations,
                    ttl=86400.0,  # 24 hours
                )

                if result:
                    return json.dumps({
                        "location": location,
                        "activity_type": activity_type,
                        "regulations": result["regulations"],
                        "group_size_limits": result["group_size_limit"],
                        "camping_restrictions": result["camping_restrictions"],
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for regulations: {e}")
    except Exception as e:
        print(f"Regulations error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "regulations": [
            "Stay on designated trails",
            "Pack in, pack out",
            "No motorized vehicles",
            "Respect wildlife",
        ],
        "group_size_limits": 10,
        "camping_restrictions": "Designated sites only",
        "source": "placeholder",
    })


@tool
def check_fire_restrictions(location: str, dates: List[str] | None = None) -> str:
    """Check fire restrictions for a location and dates.

    Args:
        location: Location name or region
        dates: List of dates in YYYY-MM-DD format

    Returns:
        JSON string with fire restrictions
    """
    try:
        # Get coordinates for NIFC query
        coord_result = get_coordinates.invoke({"location_name": location})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")

        # Try NIFC Open Data API for active fire incidents
        if lat and lon:
            def _check_nifc_fires() -> dict | None:
                """Check NIFC for active fires near location."""
                with httpx.Client() as client:
                    # NIFC ArcGIS API for active fire perimeters
                    # Query fires within ~50km radius
                    url = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Interagency_Perimeters/FeatureServer/0/query"
                    params = {
                        "geometry": f"{lon},{lat}",
                        "geometryType": "esriGeometryPoint",
                        "spatialRel": "esriSpatialRelIntersects",
                        "distance": 50,
                        "units": "esriSRUnit_StatuteMile",
                        "outFields": "poly_IncidentName,poly_PercentContained,poly_GISAcres",
                        "returnGeometry": "false",
                        "f": "json",
                    }

                    try:
                        response = client.get(url, params=params, timeout=15.0)
                        if response.status_code == 200:
                            data = response.json()
                            features = data.get("features", [])
                            if features:
                                fires = []
                                for feature in features[:5]:
                                    attrs = feature.get("attributes", {})
                                    fires.append({
                                        "name": attrs.get("poly_IncidentName", "Unknown"),
                                        "percent_contained": attrs.get("poly_PercentContained", 0),
                                        "acres": attrs.get("poly_GISAcres", 0),
                                    })
                                return {"active_fires": fires, "fire_danger": "High"}
                    except Exception as e:
                        print(f"NIFC API error: {e}")
                return None

            try:
                # Cache NIFC data for 2 hours (fire data changes frequently)
                nifc_result = cached_api_call(
                    endpoint="nifc_fires",
                    params={"lat": lat, "lon": lon},
                    api_func=_check_nifc_fires,
                    ttl=7200.0,  # 2 hours
                )

                if nifc_result and nifc_result.get("active_fires"):
                    return json.dumps({
                        "location": location,
                        "fire_restrictions": "Active fires in area - check local conditions",
                        "current_level": "High",
                        "active_fires": nifc_result["active_fires"],
                        "restrictions": [
                            "No campfires allowed",
                            "Check with local ranger station before travel",
                        ],
                        "dates": dates,
                        "source": "nifc.gov",
                    })
            except Exception as e:
                print(f"NIFC API error: {e}")

        # Use web search via Tavily for fire restrictions
        if Config.TAVILY_API_KEY:
            def _search_fire_restrictions() -> dict:
                """Search for fire restrictions via Tavily."""
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                date_str = f" {dates[0]}" if dates else ""
                query = f"{location} fire restrictions{date_str}"
                results = search_tool.search_web(query)

                fire_restrictions = "Campfires allowed in designated areas only"
                current_level = "Moderate"
                restrictions = []

                if results:
                    for result in results[:3]:
                        content = result.get("content", "").lower()
                        title = result.get("title", "").lower()

                        if "stage 1" in content or "stage 1" in title:
                            current_level = "Stage 1"
                            if "No campfires outside designated areas" not in restrictions:
                                restrictions.append("No campfires outside designated areas")
                        elif "stage 2" in content or "stage 2" in title:
                            current_level = "Stage 2"
                            if "No campfires outside designated areas" not in restrictions:
                                restrictions.append("No campfires outside designated areas")
                            if "No smoking outside vehicles" not in restrictions:
                                restrictions.append("No smoking outside vehicles")
                        elif "stage 3" in content or "stage 3" in title:
                            current_level = "Stage 3"
                            restrictions = ["No campfires allowed", "No smoking"]
                        elif "fire ban" in content or "fire ban" in title:
                            current_level = "High"
                            if "No campfires allowed" not in restrictions:
                                restrictions.append("No campfires allowed")
                        elif "no campfire" in content:
                            if "No campfires outside designated areas" not in restrictions:
                                restrictions.append("No campfires outside designated areas")

                if not restrictions:
                    restrictions = ["No campfires outside designated areas"]

                return {
                    "fire_restrictions": fire_restrictions,
                    "current_level": current_level,
                    "restrictions": restrictions,
                }

            try:
                # Cache fire restriction search for 4 hours
                result = cached_api_call(
                    endpoint="tavily_fire_restrictions",
                    params={"location": location, "dates": dates[0] if dates else None},
                    api_func=_search_fire_restrictions,
                    ttl=14400.0,  # 4 hours
                )

                if result:
                    return json.dumps({
                        "location": location,
                        "fire_restrictions": result["fire_restrictions"],
                        "current_level": result["current_level"],
                        "restrictions": result["restrictions"],
                        "dates": dates,
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for fire restrictions: {e}")
    except Exception as e:
        print(f"Fire restrictions error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "fire_restrictions": "Campfires allowed in designated areas only",
        "current_level": "Moderate",
        "restrictions": ["No campfires outside designated areas"],
        "dates": dates,
        "source": "placeholder",
    })


@tool
def get_seasonal_closures(location: str) -> str:
    """Get seasonal closures for a location.

    Args:
        location: Location name or region

    Returns:
        JSON string with seasonal closures
    """
    try:
        # Use web search via Tavily for seasonal closures
        if Config.TAVILY_API_KEY:
            def _search_seasonal_closures() -> dict:
                """Search for seasonal closures via Tavily."""
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"{location} seasonal closures trail closures"
                results = search_tool.search_web(query)

                closures = []
                seasonal_access = "Open year-round"

                if results:
                    for result in results[:3]:
                        content = result.get("content", "").lower()

                        if "closed" in content or "closure" in content:
                            if "winter" in content and "Winter closures may apply" not in closures:
                                closures.append("Winter closures may apply")
                                seasonal_access = "Seasonal access - check current conditions"
                            if "summer" in content and "closed" in content and "Summer closures may apply" not in closures:
                                closures.append("Summer closures may apply")
                                seasonal_access = "Seasonal access - check current conditions"
                            if "seasonal" in content:
                                seasonal_access = "Seasonal access - check current conditions"

                return {"closures": closures, "seasonal_access": seasonal_access}

            try:
                # Cache seasonal closures for 24 hours
                result = cached_api_call(
                    endpoint="tavily_closures",
                    params={"location": location},
                    api_func=_search_seasonal_closures,
                    ttl=86400.0,  # 24 hours
                )

                if result:
                    return json.dumps({
                        "location": location,
                        "closures": result["closures"],
                        "seasonal_access": result["seasonal_access"],
                        "source": "web_search",
                    })
            except Exception as e:
                print(f"Web search error for seasonal closures: {e}")
    except Exception as e:
        print(f"Seasonal closures error for {location}: {e}")
    
    # Fallback to placeholder data
    return json.dumps({
        "location": location,
        "closures": [],
        "seasonal_access": "Open year-round",
        "source": "placeholder",
    })

