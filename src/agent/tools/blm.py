"""BLM (Bureau of Land Management) land tools."""

from __future__ import annotations

import json

import httpx
from langchain.tools import tool

from agent.config import Config

# Import tools - use relative imports to avoid circular dependencies
from agent.tools.geo import get_coordinates
from agent.tools.web_search import WebSearchTool


@tool
def search_blm_lands(region: str, activity_type: str = "mountain_biking") -> str:
    """Search for BLM (Bureau of Land Management) lands in a region.

    Args:
        region: US state or region name
        activity_type: Type of activity (mountain_biking, camping, etc.)

    Returns:
        JSON string with BLM land information
    """
    try:
        # Get coordinates for the region
        coord_result = get_coordinates.invoke({"location_name": region})
        coord_data = json.loads(coord_result)
        lat = coord_data.get("coordinates", {}).get("lat")
        lon = coord_data.get("coordinates", {}).get("lon")
        
        if not lat or not lon:
            raise ValueError("Could not get coordinates for region")
        
        # Use Recreation.gov API to find nearby BLM sites
        # Recreation.gov has some BLM data
        with httpx.Client() as client:
            # Search for recreation areas near the location
            url = "https://ridb.recreation.gov/api/v1/recareas"
            # Use API key from config, fallback to "public" for rate-limited access
            api_key = Config.RECREATION_GOV_API_KEY or "public"
            headers = {"apikey": api_key}
            params = {
                "limit": 10,
                "offset": 0,
                "latitude": lat,
                "longitude": lon,
                "radius": 50,  # 50 mile radius
            }
            
            try:
                response = client.get(url, headers=headers, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    rec_areas = data.get("RECDATA", [])
                    
                    # Filter for BLM managed areas
                    blm_lands = []
                    for area in rec_areas:
                        org_name = area.get("OrgName", "").upper()
                        if "BLM" in org_name or "BUREAU OF LAND MANAGEMENT" in org_name:
                            blm_lands.append({
                                "name": area.get("RecAreaName", "BLM Land"),
                                "description": area.get("RecAreaDescription", ""),
                                "access_points": [area.get("RecAreaDirections", "")],
                                "regulations": [
                                    "Follow Leave No Trace principles",
                                    "Check local BLM office for specific regulations",
                                ],
                                "permits_required": area.get("Reservable", False),
                                "camping_allowed": True,
                                "coordinates": {
                                    "lat": area.get("RecAreaLatitude"),
                                    "lon": area.get("RecAreaLongitude"),
                                },
                                "url": f"https://www.recreation.gov/camping/campgrounds/{area.get('RecAreaID')}" if area.get("RecAreaID") else None,
                            })
                    
                    if blm_lands:
                        return json.dumps({
                            "lands": blm_lands,
                            "region": region,
                            "source": "recreation.gov",
                        })
                elif response.status_code == 401:
                    print(f"Recreation.gov API authentication failed. Check your RECREATION_GOV_API_KEY in .env file.")
                else:
                    print(f"Recreation.gov API error: {response.status_code} - {response.text[:200]}")
            except Exception as e:
                print(f"Recreation.gov API error: {e}")
        
        # Fallback: Use web search via Tavily if available
        if Config.TAVILY_API_KEY:
            try:
                search_tool = WebSearchTool(api_key=Config.TAVILY_API_KEY)
                query = f"BLM Bureau of Land Management {region} {activity_type} recreation areas"
                results = search_tool.search_web(query)
                
                if results:
                    # Extract information from search results
                    blm_info = []
                    for result in results[:3]:  # Top 3 results
                        title = result.get("title", "")
                        content = result.get("content", "")
                        url = result.get("url", "")
                        
                        if "BLM" in title.upper() or "BUREAU OF LAND MANAGEMENT" in title.upper():
                            blm_info.append({
                                "name": title,
                                "description": content[:200] + "..." if len(content) > 200 else content,
                                "access_points": ["Contact local BLM office"],
                                "regulations": [
                                    "Permits may be required for overnight use",
                                    "Stay on designated trails",
                                    "Pack in, pack out",
                                ],
                                "permits_required": "overnight" in content.lower(),
                                "camping_allowed": "camping" in content.lower() or "camp" in content.lower(),
                                "url": url,
                            })
                    
                    if blm_info:
                        return json.dumps({
                            "lands": blm_info,
                            "region": region,
                            "source": "web_search",
                        })
            except Exception as e:
                print(f"Web search error for BLM data: {e}")
    except Exception as e:
        print(f"BLM land search error for {region}: {e}")
    
    # Fallback to structured placeholder data
    return json.dumps({
        "lands": [
            {
                "name": f"BLM Land in {region}",
                "access_points": ["Main trailhead", "Secondary access"],
                "regulations": ["Permits required for overnight", "Stay on designated trails"],
                "permits_required": True,
                "camping_allowed": True,
                "description": f"BLM managed land suitable for {activity_type}. Contact local BLM office for specific information.",
            }
        ],
        "region": region,
        "source": "placeholder",
    })


@tool
def get_blm_regulations(land_name: str) -> str:
    """Get specific regulations for a BLM land area.

    Args:
        land_name: Name of the BLM land area

    Returns:
        JSON string with regulations
    """
    return json.dumps({
        "regulations": [
            "Permits required for groups over 10",
            "No motorized vehicles",
            "Pack in, pack out",
            "Campfires only in designated areas",
        ],
        "permits_required": True,
        "contact_info": "Contact local BLM office",
    })

