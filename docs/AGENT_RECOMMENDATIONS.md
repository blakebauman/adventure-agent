# Agent Implementation Status

This document outlines the current status of agents in the adventure planning service.

## Implemented Agents (Active in Graph)

### Core Planning Agents
- **Orchestrator Agent**: Routes requests and manages workflow
- **Geo Agent**: Geographic information, coordinates, and location data
- **Trail Agent**: MTB Project, Hiking Project, Trail Run Project
- **Planning Agent**: Itinerary creation and logistics

### Land Management & Regulations
- **BLM Agent**: Bureau of Land Management lands, access, and regulations
- **Permits Agent**: Permit requirements, regulations, and access restrictions

### Safety & Conditions
- **Weather Agent**: Real-time weather, trail conditions, and seasonal information
- **Safety Agent**: Safety information, emergency contacts, and risk assessment

### Logistics & Services
- **Accommodation Agent**: Hotels, campgrounds, and lodging
- **Transportation Agent**: Parking, shuttles, public transit, and transportation logistics
- **Food Agent**: Food options, resupply points, water sources, and local recommendations

### Community & Culture
- **Community Agent**: Local clubs, events, and community resources
- **Historical Agent**: Historical sites, cultural significance, and local history

### Enhancement Agents
- **Gear Agent**: Product recommendations with affiliate links
- **Photography Agent**: Best photo spots, scenic viewpoints, and media resources

## Agents Not Currently in Graph

The following agents are implemented as classes but are not currently wired into the graph workflow:

- **Route Planning Agent**: RideWithGPS, Strava (exists but not in graph)
- **Bikepacking Agent**: Bikepacking.com, Bikepacking Roots (exists but not in graph)
- **Advocacy Agent**: IMBA, Adventure Cycling Association (exists but not in graph)

These agents can be added to the graph in `src/agent/graph.py` if needed.

## Additional Data Sources

### Trail-Specific Resources
- **Trailforks** (trailforks.com) - Comprehensive mountain bike trail database
- **AllTrails** (alltrails.com) - Popular hiking and trail running resource
- **Komoot** (komoot.com) - Route planning with turn-by-turn navigation

### Regional Resources
- **Colorado Trail Foundation** - For Colorado Trail specific information
- **Arizona Trail Association** - For AZT specific information
- **Pacific Crest Trail Association** - For PCT information
- **Continental Divide Trail Coalition** - For CDT information

### Gear & Equipment
- **REI Co-op** - Gear reviews and recommendations
- **Backcountry.com** - Gear and expert advice
- **Outdoor Gear Lab** - Detailed gear reviews

