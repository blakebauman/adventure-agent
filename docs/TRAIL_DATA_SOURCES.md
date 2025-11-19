# Trail Data Sources - API Access Methods

This document provides detailed information on how to access various open trail data sources for integration into the adventure agent.

## Table of Contents

1. [USGS Trails Dataset](#usgs-trails-dataset)
2. [OpenStreetMap (OSM)](#openstreetmap-osm)
3. [OpenTrail.org](#opentrailorg)
4. [Open MTB Trails](#open-mtb-trails)
5. [National Park Service Data](#national-park-service-data)
6. [State-Level GIS Datasets](#state-level-gis-datasets)
7. [Integration Recommendations](#integration-recommendations)

---

## USGS Trails Dataset

**Source**: U.S. Geological Survey  
**License**: Public Domain  
**Coverage**: United States  
**Update Frequency**: Annually (federal sources), every 3 years (other sources)

### Access Methods

#### 1. ArcGIS REST API (Recommended for Real-Time Access)

**Base URL**: `https://partnerships.nationalmap.gov/arcgis/rest/services/USGSTrails/MapServer`

**Query Endpoint**:
```
GET https://partnerships.nationalmap.gov/arcgis/rest/services/USGSTrails/MapServer/0/query
```

**Query Parameters**:
- `where`: SQL WHERE clause (e.g., `"STATE='Colorado'"`)
- `geometry`: Bounding box as JSON (e.g., `{"xmin":-109, "ymin":37, "xmax":-102, "ymax":41}`)
- `geometryType`: `esriGeometryEnvelope`
- `spatialRel`: `esriSpatialRelIntersects`
- `outFields`: Comma-separated field names (e.g., `*` for all fields)
- `f`: Output format (`json`, `geojson`, `pjson`)

**Example Python Implementation**:
```python
import httpx

async def query_usgs_trails(bbox: dict, state: str = None) -> dict:
    """Query USGS trails within a bounding box."""
    url = "https://partnerships.nationalmap.gov/arcgis/rest/services/USGSTrails/MapServer/0/query"
    
    params = {
        "geometry": bbox,
        "geometryType": "esriGeometryEnvelope",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "*",
        "f": "geojson"
    }
    
    if state:
        params["where"] = f"STATE='{state}'"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response.json()
```

**Available Fields**:
- `TRAIL_NAME`: Trail name
- `TRAIL_TYPE`: Type of trail (hiking, biking, etc.)
- `STATE`: State abbreviation
- `LENGTH_MI`: Length in miles
- `MANAGED_BY`: Managing agency
- `ACCESS_TYPE`: Access type (public, private, etc.)

#### 2. Web Feature Service (WFS)

**Endpoint**: `https://services.nationalmap.gov/arcgis/services/USGSTrails/MapServer/WFSServer`

**Capabilities URL**: Add `?service=WFS&version=2.0.0&request=GetCapabilities`

**Usage**: Standard WFS protocol for GIS software integration

#### 3. Downloadable GIS Files

**National Map Download Application**: 
- URL: https://www.usgs.gov/national-geospatial-technical-operations-center/how-access-or-view-usgs-trails-dataset
- Formats: Shapefile, Geodatabase (GDB)
- Coverage: National or state-level extracts

**Python Library**: Use `geopandas` to read Shapefiles or `fiona` for direct access

```python
import geopandas as gpd

# Read downloaded shapefile
trails = gpd.read_file("path/to/usgs_trails.shp")
```

---

## OpenStreetMap (OSM)

**Source**: OpenStreetMap Foundation  
**License**: Open Database License (ODbL)  
**Coverage**: Global  
**Update Frequency**: Real-time (community-driven)

### Access Methods

#### 1. Overpass API (Recommended for Trail Queries)

**Base URL**: `https://overpass-api.de/api/interpreter` (or other public instances)

**Query Language**: Overpass QL

**Example Query for Hiking Trails**:
```python
import httpx

async def query_osm_trails(lat: float, lon: float, radius: int = 10000) -> dict:
    """Query OSM for trails near a location."""
    url = "https://overpass-api.de/api/interpreter"
    
    # Overpass QL query
    query = f"""
    [out:json][timeout:25];
    (
      way["highway"="path"]["mtb:scale"](around:{radius},{lat},{lon});
      way["highway"="path"]["hiking"="yes"](around:{radius},{lat},{lon});
      way["highway"="footway"](around:{radius},{lat},{lon});
      relation["type"="route"]["route"="hiking"](around:{radius},{lat},{lon});
    );
    out geom;
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=query)
        return response.json()
```

**Trail-Specific Tags**:
- `highway=path`: General trail
- `highway=footway`: Footpath
- `mtb:scale=*`: Mountain bike difficulty (0-6)
- `hiking=yes`: Hiking trail
- `trail_visibility=*`: Trail visibility
- `surface=*`: Surface type (dirt, gravel, paved, etc.)
- `smoothness=*`: Smoothness rating

**Activity-Specific Queries**:
```python
# Mountain biking trails
mtb_query = """
[out:json][timeout:25];
(
  way["highway"="path"]["mtb:scale"](around:10000,39.7392,-104.9903);
  way["highway"="path"]["bicycle"="yes"](around:10000,39.7392,-104.9903);
);
out geom;
"""

# Hiking trails
hiking_query = """
[out:json][timeout:25];
(
  way["highway"="path"]["hiking"="yes"](around:10000,39.7392,-104.9903);
  relation["type"="route"]["route"="hiking"](around:10000,39.7392,-104.9903);
);
out geom;
"""
```

**Using Overpy Library (Alternative)**:
```python
import overpy

async def query_osm_trails_overpy(lat: float, lon: float, radius: int = 10000) -> list:
    """Query OSM using overpy library."""
    api = overpy.Overpass()
    
    query = f"""
    (
      way["highway"="path"]["mtb:scale"](around:{radius},{lat},{lon});
      way["highway"="path"]["hiking"="yes"](around:{radius},{lat},{lon});
    );
    out geom;
    """
    
    result = api.query(query)
    
    trails = []
    for way in result.ways:
        trail = {
            "name": way.tags.get("name", "Unnamed Trail"),
            "difficulty": way.tags.get("mtb:scale"),
            "surface": way.tags.get("surface"),
            "nodes": [(node.lat, node.lon) for node in way.nodes]
        }
        trails.append(trail)
    
    return trails
```

#### 2. OSMnx Python Library (Recommended for Network Analysis)

**Installation**: `pip install osmnx`

**Usage**:
```python
import osmnx as ox

# Get trail network for an area
def get_trail_network(place: str, activity: str = "hiking") -> dict:
    """Get trail network from OSM."""
    # Custom filter for trails
    custom_filter = '["highway"~"path|footway"]["hiking"~"yes|designated"]'
    
    if activity == "mountain_biking":
        custom_filter = '["highway"~"path"]["mtb:scale"]'
    
    G = ox.graph_from_place(place, custom_filter=custom_filter, network_type="walk")
    
    # Convert to GeoJSON
    nodes, edges = ox.graph_to_gdfs(G)
    
    return {
        "nodes": nodes.to_dict("records"),
        "edges": edges.to_dict("records")
    }
```

#### 3. Nominatim API (Geocoding)

**Base URL**: `https://nominatim.openstreetmap.org/search`

**Usage**:
```python
async def geocode_location(location: str) -> dict:
    """Geocode location using OSM Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location,
        "format": "json",
        "limit": 1
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers={"User-Agent": "AdventureAgent/1.0"})
        return response.json()[0] if response.json() else None
```

**Rate Limiting**: 1 request per second (use User-Agent header)

#### 4. Planet OSM Extracts (Bulk Downloads)

**URL**: https://planet.openstreetmap.org/

**Usage**: Download regional extracts for offline processing

---

## OpenTrail.org

**Source**: Community-driven platform  
**License**: Open Database License (ODbL)  
**Coverage**: Varies by region  
**Status**: Active community project

### Access Methods

**Note**: As of research, OpenTrail.org does not appear to have a documented public API. The platform is community-driven and may require:

1. **Direct Contact**: Reach out to the project maintainers for API access
2. **Web Scraping**: If terms of service allow, scrape trail data
3. **Data Exports**: Check if they provide bulk data exports

**Website**: https://opentrail.org

**Recommended Approach**: Monitor their website for API documentation or contact them directly for integration opportunities.

---

## Open MTB Trails

**Source**: Community-driven mountain biking database  
**License**: Open (check website for specific terms)  
**Coverage**: Growing database  
**Status**: Early stages, seeking contributors

### Access Methods

**Note**: Open MTB Trails is in early development and does not currently have a public API.

**Website**: https://www.openmtb.org

**Recommended Approach**:
1. **Contact Project Team**: Reach out via their website for API access or collaboration
2. **Contribute**: Consider contributing to the project to gain early access
3. **Monitor**: Watch for API announcements as the project matures

**Integration Strategy**: This could be a valuable complement to MTB Project data once API access is available.

---

## National Park Service Data

**Source**: National Park Service  
**License**: Public Domain  
**Coverage**: U.S. National Parks  
**Update Frequency**: Varies by park

### Access Methods

#### 1. NPS Data API

**Base URL**: `https://developer.nps.gov/api/v1`

**Authentication**: Requires API key (free registration at https://www.nps.gov/subjects/developer/index.htm)

**Endpoints**:
- Parks: `/parks`
- Alerts: `/alerts`
- Events: `/events`
- News Releases: `/newsreleases`
- Places: `/places`

**Example**:
```python
async def get_nps_trails(park_code: str, api_key: str) -> dict:
    """Get trail information for a national park."""
    url = f"https://developer.nps.gov/api/v1/parks"
    params = {
        "parkCode": park_code,
        "api_key": api_key
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        # Parse trail data from park information
        return data
```

**Note**: The NPS API provides general park information. For detailed trail data, you may need to:
- Scrape individual park websites
- Use NPS DataStore for scientific datasets
- Combine with other sources (USGS, OSM)

#### 2. Recreation.gov API

**Base URL**: `https://www.recreation.gov/api`

**Note**: Recreation.gov API is primarily for reservations and permits, not trail data. However, it can provide:
- Campground locations near trails
- Permit requirements
- Facility information

**Authentication**: May require API key (check recreation.gov developer documentation)

---

## State-Level GIS Datasets

**Source**: Various state agencies  
**License**: Varies by state (often public domain)  
**Coverage**: State-specific  
**Update Frequency**: Varies

### Examples

#### Massachusetts (MassGIS)

**Long Distance Trails Dataset**: Trails longer than 25 miles

**Access**: 
- Website: https://www.mass.gov/info-details/massgis-data-long-distance-trails
- Format: Shapefile, GeoJSON
- Download: Direct download from MassGIS

**Python Implementation**:
```python
import geopandas as gpd

def get_mass_trails() -> gpd.GeoDataFrame:
    """Load Massachusetts long-distance trails."""
    # Download from MassGIS or use local file
    trails = gpd.read_file("path/to/mass_trails.shp")
    return trails
```

#### Other States

Many states provide similar GIS datasets:
- **Colorado**: https://data.colorado.gov/
- **California**: https://data.ca.gov/
- **Oregon**: https://data.oregon.gov/
- **Washington**: https://data.wa.gov/

**Integration Strategy**: 
1. Identify states of interest
2. Search state GIS portals for trail datasets
3. Download and process Shapefiles/GeoJSON
4. Create state-specific tools in `tools.py`

---

## Integration Recommendations

### Priority Order for Implementation

1. **OpenStreetMap (OSM)** - Highest priority
   - Most comprehensive global coverage
   - Real-time updates
   - Well-documented APIs
   - Supports all activity types
   - **Python Libraries**: `osmnx`, `overpy` (Overpass wrapper)

2. **USGS Trails Dataset** - High priority
   - Authoritative government data
   - Good U.S. coverage
   - REST API available
   - **Python Libraries**: `geopandas`, `requests`/`httpx`

3. **NPS Data API** - Medium priority
   - Good for national park context
   - Requires API key (free)
   - Limited to NPS areas

4. **State GIS Datasets** - Medium priority
   - High-quality regional data
   - Requires per-state integration
   - Good for specific regions

5. **OpenTrail.org / Open MTB Trails** - Lower priority
   - Monitor for API availability
   - Good for community-driven data
   - May require direct contact

### Implementation Pattern

Based on the existing codebase structure in `src/agent/tools.py`, here's the recommended pattern:

```python
@tool
def search_trails_osm(
    location: str,
    activity_type: str,
    radius_meters: int = 10000,
    difficulty: Optional[str] = None,
) -> str:
    """Search for trails using OpenStreetMap data.
    
    Args:
        location: Location name or coordinates
        activity_type: Type of activity (mountain_biking, hiking, trail_running)
        radius_meters: Search radius in meters
        difficulty: Optional difficulty filter
        
    Returns:
        JSON string with trail information
    """
    # 1. Geocode location using Nominatim
    # 2. Query Overpass API for trails
    # 3. Filter by activity type and difficulty
    # 4. Return structured JSON matching TrailInfo format
    pass

@tool
def search_trails_usgs(
    location: str,
    state: str,
    activity_type: str,
    bbox: Optional[Dict[str, float]] = None,
) -> str:
    """Search for trails using USGS Trails Dataset.
    
    Args:
        location: Location name
        state: State abbreviation
        activity_type: Type of activity
        bbox: Optional bounding box
        
    Returns:
        JSON string with trail information
    """
    # 1. Query USGS ArcGIS REST API
    # 2. Filter by activity type
    # 3. Return structured JSON matching TrailInfo format
    pass
```

### Python Dependencies

Add to `pyproject.toml`:

```toml
[project.optional-dependencies]
trail-data = [
    "osmnx>=1.6.0",  # OpenStreetMap network analysis
    "overpy>=0.6",   # Overpass API wrapper
    "geopandas>=0.14.0",  # GIS data handling
    "shapely>=2.0",  # Geometric operations
    "fiona>=1.9",    # Shapefile reading
]
```

### Error Handling

All trail data tools should:
1. Handle API rate limits gracefully
2. Provide fallback to other sources
3. Cache results when appropriate
4. Return empty results rather than raising exceptions

### Data Normalization

Create a common `TrailInfo` format (already exists in `state.py`) and normalize data from all sources to this format:

```python
# From state.py
class TrailInfo(TypedDict, total=False):
    name: str
    source: str
    activity_type: str
    difficulty: Optional[str]
    length_miles: Optional[float]
    elevation_gain: Optional[float]
    description: Optional[str]
    url: Optional[str]
    coordinates: Optional[Dict[str, float]]
```

---

## Additional Resources

- **USGS Trails Explorer**: https://www.usgs.gov/national-digital-trails/usgs-trails-explorer
- **OpenStreetMap Wiki**: https://wiki.openstreetmap.org/
- **Overpass API Documentation**: https://wiki.openstreetmap.org/wiki/Overpass_API
- **OSMnx Documentation**: https://osmnx.readthedocs.io/
- **NPS Developer Portal**: https://www.nps.gov/subjects/developer/index.htm

---

## Next Steps

1. **Implement OSM integration** - Start with Overpass API queries
2. **Add USGS integration** - Use ArcGIS REST API
3. **Create unified search function** - Combine multiple sources
4. **Add caching layer** - Reduce API calls
5. **Update trail_agent.py** - Use new data sources
6. **Add tests** - Unit tests for each data source integration

