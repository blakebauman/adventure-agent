# Arizona Adventure Agentic Workflow

## Vision

The **Arizona Adventure Agentic Workflow** is a specialized AI system for planning adventures throughout Arizona. Built by Arizonans, for Arizonans, and anyone who loves exploring the Grand Canyon State.

## Why Arizona?

Arizona is home to:
- **Diverse landscapes**: From Sonoran Desert to pine forests, red rock canyons to mountain peaks
- **World-class trails**: Sedona's MTB trails, Grand Canyon hiking, desert bikepacking routes
- **Rich history**: Mining towns, territorial capitals, Native American heritage
- **Year-round adventure**: Four distinct seasons, each offering unique opportunities
- **Iconic destinations**: Grand Canyon, Sedona, Monument Valley, Saguaro National Park

## Current Location Agents

### Active Agents

1. **Jerome Agent** - Historic mining town, ghost town revival, artistic community
2. **Sedona Agent** - Red rock formations, world-class MTB trails, spiritual vortex sites
3. **Prescott Agent** - Historic territorial capital, Whiskey Row, mountain biking

### Planned Agents (Priority Order)

#### High Priority
- **Flagstaff** - Mountain town, San Francisco Peaks, Grand Canyon gateway
- **Phoenix** - Valley of the Sun, desert trails, urban mountain biking
- **Tucson** - Sonoran Desert, Saguaro National Park, mountain biking

#### Medium Priority
- **Bisbee** - Historic mining town, arts community, Mule Mountains
- **Page** - Lake Powell, Antelope Canyon, Horseshoe Bend
- **Williams** - Route 66, Grand Canyon gateway, mountain biking
- **Cottonwood** - Verde Valley, wine country, Old Town
- **Payson** - Mogollon Rim, Tonto National Forest, mountain biking

#### Lower Priority
- **Show Low** - White Mountains, Ponderosa pine forests
- **Pinetop-Lakeside** - White Mountains, lakes, outdoor recreation

## Arizona Regions

### Northern Arizona
- **Cities**: Flagstaff, Sedona, Prescott, Jerome, Williams, Page
- **Features**: High elevation, pine forests, red rock country, Grand Canyon
- **Activities**: Mountain biking, hiking, skiing, Grand Canyon exploration

### Central Arizona
- **Cities**: Phoenix, Scottsdale, Tempe, Mesa, Payson
- **Features**: Valley of the Sun, desert, urban mountain biking
- **Activities**: Desert trails, urban MTB, Sonoran Desert exploration

### Southern Arizona
- **Cities**: Tucson, Bisbee, Tombstone, Sierra Vista
- **Features**: Sonoran Desert, Saguaro National Park, border region
- **Activities**: Desert hiking, mountain biking, border region exploration

### Eastern Arizona
- **Cities**: Show Low, Pinetop-Lakeside, Springerville
- **Features**: White Mountains, high elevation, pine forests
- **Activities**: Mountain biking, hiking, fishing, winter sports

### Western Arizona
- **Cities**: Lake Havasu City, Kingman, Bullhead City
- **Features**: Colorado River, desert, water recreation
- **Activities**: Water sports, desert trails, Route 66

## System Features

### Arizona-First Design
- Defaults to Arizona context when location not specified
- Automatically detects Arizona cities/towns
- Routes to location-specific agents when available
- Enhances all outputs with Arizona-specific knowledge

### Location Agent Architecture
- Each Arizona city/town can have its own specialized agent
- Agents provide:
  - Local history and culture
  - Specific trails and routes
  - Local businesses and services
  - Regional context and connections
  - Practical tips for visitors

### Comprehensive Adventure Planning
- Mountain biking (world-class trails in Sedona, Flagstaff, etc.)
- Hiking (Grand Canyon, red rock country, desert)
- Trail running (mountain and desert trails)
- Bikepacking (Arizona Trail, desert routes)
- Cultural tourism (mining towns, Native American sites)
- Photography (iconic landscapes, sunsets, red rocks)

## Adding New Arizona Location Agents

See [LOCATION_AGENTS_ARCHITECTURE.md](./LOCATION_AGENTS_ARCHITECTURE.md) for detailed instructions.

Quick steps:
1. Create agent file inheriting from `LocationAgentBase`
2. Populate Arizona-specific knowledge base
3. Register in graph
4. Add to `arizona_registry.py`

## Roadmap

### Phase 1: Foundation (Current)
- ✅ Base architecture for location agents
- ✅ Jerome, Sedona, Prescott agents
- ✅ Arizona registry system
- ✅ Arizona-first orchestrator

### Phase 2: Major Cities (Next)
- Flagstaff agent
- Phoenix agent
- Tucson agent

### Phase 3: Regional Coverage
- Medium priority cities
- Regional route planning
- Multi-city adventures

### Phase 4: Advanced Features
- Arizona Trail integration
- Seasonal recommendations
- Event calendar integration
- Community contributions

## Contributing

We welcome contributions! Areas of focus:
- New location agents for Arizona cities/towns
- Enhanced knowledge bases for existing agents
- Arizona-specific trail data
- Local business directories
- Historical and cultural information

## Resources

- [Arizona Trail](https://aztrail.org/)
- [Arizona State Parks](https://azstateparks.com/)
- [Arizona Office of Tourism](https://www.visitarizona.com/)
- [Arizona Mountain Bike Association](https://www.azmba.org/)

