# API Integrations Guide

This document describes the real API integrations implemented in the adventure agent.

## Implemented Integrations

### 1. Geocoding (`get_coordinates`)

**Purpose**: Convert location names to coordinates (lat/lon)

**APIs Used**:
1. **OpenCage Geocoding API** (primary, if `OPENCAGE_API_KEY` is set)
   - URL: `https://api.opencagedata.com/geocode/v1/json`
   - Rate limits: Depends on plan (free tier: 2,500 requests/day)
   - Get API key: https://opencagedata.com/api

2. **Nominatim (OpenStreetMap)** (fallback, free)
   - URL: `https://nominatim.openstreetmap.org/search`
   - Rate limits: 1 request/second (use responsibly)
   - No API key required
   - User-Agent header required

**Usage**:
```python
from agent.tools import get_coordinates

result = get_coordinates.invoke({"location_name": "Colorado"})
# Returns JSON with coordinates, region, country, formatted_address
```

**Error Handling**: Falls back to placeholder data if both APIs fail

---

### 2. Weather Forecast (`get_weather_forecast`)

**Purpose**: Get current and forecasted weather for a location

**APIs Used**:
1. **OpenWeatherMap API** (primary, if `OPENWEATHER_API_KEY` is set)
   - URL: `https://api.openweathermap.org/data/2.5/forecast`
   - Rate limits: Free tier: 60 calls/minute, 1,000,000 calls/month
   - Get API key: https://openweathermap.org/api

2. **Weather.gov API** (fallback, free, US only)
   - URL: `https://api.weather.gov/points/{lat},{lon}`
   - No API key required
   - User-Agent header required
   - Only works for US locations

**Usage**:
```python
from agent.tools import get_weather_forecast

result = get_weather_forecast.invoke({
    "location": "Colorado",
    "dates": ["2024-01-20", "2024-01-21"]
})
# Returns JSON with current weather and daily forecasts
```

**Error Handling**: Falls back to placeholder data if both APIs fail

---

### 3. Trail Search (`search_trails`)

**Purpose**: Find trails near a location using OpenStreetMap data

**APIs Used**:
1. **OpenStreetMap Overpass API** (primary, free)
   - URL: `https://overpass-api.de/api/interpreter`
   - No API key required
   - Searches for trails, paths, and routes within ~10km radius
   - Returns trails tagged with highway types: path, track, footway, bridleway, cycleway

**Usage**:
```python
from agent.tools import search_trails

result = search_trails.invoke({
    "location": "Colorado",
    "activity_type": "mountain_biking",
    "source": "osm",
    "difficulty": "intermediate"
})
# Returns JSON with trail information
```

**Note**: Adventure Projects (MTB Project, Hiking Project, Trail Run Project) don't have public APIs, so we use OpenStreetMap data as the primary source.

**Error Handling**: Falls back to placeholder data if API fails

---

### 4. Distance Calculation (`calculate_distance`)

**Purpose**: Calculate distance between two geographic points

**Implementation**: Haversine formula (great-circle distance)
- No external API required
- Accurate for most use cases
- Earth radius: 3,958.8 miles

**Usage**:
```python
from agent.tools import calculate_distance

result = calculate_distance.invoke({
    "point1": {"lat": 39.7392, "lon": -104.9903},  # Denver
    "point2": {"lat": 40.0149, "lon": -105.2705}   # Boulder
})
# Returns JSON with distance in miles and kilometers
```

---

## Configuration

Add API keys to your `.env` file:

```bash
# Optional: For better geocoding (falls back to Nominatim if not set)
OPENCAGE_API_KEY=your_opencage_api_key_here

# Optional: For weather forecasts (falls back to Weather.gov if not set)
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Optional: For hotel/lodging search (campgrounds work without this)
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here

# Optional: For web search (used as fallback for BLM data)
TAVILY_API_KEY=your_tavily_api_key_here
```

## Error Handling Strategy

All tools follow this pattern:

1. **Try primary API** (if configured)
2. **Try fallback API** (if available)
3. **Return placeholder data** (if all APIs fail)

This ensures the system continues to function even when external services are unavailable.

## Rate Limiting Considerations

- **Nominatim**: 1 request/second (use responsibly)
- **OpenCage**: Depends on plan (free tier: 2,500 requests/day)
- **OpenWeatherMap**: 60 calls/minute (free tier)
- **Weather.gov**: No official limit, but use responsibly
- **Overpass API**: No official limit, but use responsibly

### 5. BLM Land Search (`search_blm_lands`)

**Purpose**: Find Bureau of Land Management recreation areas and lands

**APIs Used**:
1. **Recreation.gov API** (primary, free)
   - URL: `https://ridb.recreation.gov/api/v1/recareas`
   - No API key required (uses public key)
   - Returns BLM-managed recreation areas

2. **Tavily Web Search** (fallback, if `TAVILY_API_KEY` is set)
   - Searches web for BLM information
   - Used when Recreation.gov doesn't return results

**Usage**:
```python
from agent.tools import search_blm_lands

result = search_blm_lands.invoke({
    "region": "Colorado",
    "activity_type": "mountain_biking"
})
# Returns JSON with BLM land information
```

**Error Handling**: Falls back to placeholder data if APIs fail

---

### 6. Accommodation Search (`search_accommodations`)

**Purpose**: Find accommodations (campgrounds, hotels, hostels) near a location

**APIs Used**:
1. **Recreation.gov API** (for campgrounds, free)
   - URL: `https://ridb.recreation.gov/api/v1/facilities`
   - No API key required
   - Returns campgrounds and campsites

2. **Google Places API** (for hotels/lodging, if `GOOGLE_PLACES_API_KEY` is set)
   - URL: `https://maps.googleapis.com/maps/api/place/nearbysearch/json`
   - Requires API key
   - Returns hotels, hostels, and other lodging
   - Get API key: https://console.cloud.google.com/apis/credentials

**Usage**:
```python
from agent.tools import search_accommodations

# Search for campgrounds
result = search_accommodations.invoke({
    "location": "Colorado",
    "accommodation_type": "campground"
})

# Search for hotels (requires Google Places API key)
result = search_accommodations.invoke({
    "location": "Denver, Colorado",
    "accommodation_type": "hotel",
    "check_in": "2024-06-01",
    "check_out": "2024-06-03"
})
```

**Error Handling**: Falls back to placeholder data if APIs fail

---

## Future Integrations

Planned but not yet implemented:

- **Permit Information**: Recreation.gov API for permit details
- **Trail Conditions**: Community APIs or web scraping
- **Emergency Contacts**: Government databases
- **Food/Restaurants**: Google Places API or Yelp API

## Testing

To test API integrations:

```python
# Test geocoding
from agent.tools import get_coordinates
result = get_coordinates.invoke({"location_name": "Denver, CO"})
print(result)

# Test weather
from agent.tools import get_weather_forecast
result = get_weather_forecast.invoke({"location": "Denver, CO"})
print(result)

# Test trail search
from agent.tools import search_trails
result = search_trails.invoke({
    "location": "Denver, CO",
    "activity_type": "mountain_biking",
    "source": "osm"
})
print(result)
```

## Troubleshooting

### Geocoding returns placeholder data
- Check if location name is valid
- Verify network connectivity
- Check API key if using OpenCage
- Nominatim may be rate-limited (wait 1 second between requests)

### Weather returns placeholder data
- Verify location has valid coordinates
- For US locations, Weather.gov should work without API key
- Check OpenWeatherMap API key if using it
- Verify network connectivity

### Trail search returns placeholder data
- Verify location has valid coordinates
- Check Overpass API status
- Some locations may not have trail data in OpenStreetMap
- Verify network connectivity

