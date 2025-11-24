"""Geographic information specialist agent."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate

from agent.config import Config
from agent.models import create_llm
from agent.tools import calculate_distance, get_coordinates
from agent.utils import invoke_tool_async


class GeoAgent:
    """Agent specialized in geographic information and location data."""

    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        """Initialize the Geo agent."""
        self.llm = create_llm(
            agent_name="geo",
            model_name=model_name,
            temperature=temperature if temperature is not None else 0.3,
        )

        self.system_prompt = """You are an expert in geographic information for adventure planning.
You specialize in:
- Location geocoding and coordinates
- Distance calculations between points
- Route planning and navigation
- Regional geography (US states, Canadian provinces)
- Elevation profiles and terrain analysis
- Geographic context for adventure planning

Provide accurate geographic information for adventure planning."""

    async def get_location_info(
        self, location_name: str, context: str = ""
    ) -> Dict[str, Any]:
        """Get comprehensive location information."""
        # Use tool to get coordinates - wrap in thread to avoid blocking
        coord_data = await invoke_tool_async(get_coordinates, {"location_name": location_name})

        try:
            coords = (
                json.loads(coord_data) if isinstance(coord_data, str) else coord_data
            )

            # Enhance with LLM analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                (
                    "human",
                    """Context: {context}
Location: {location_name}

Coordinate Data: {coord_data}

Analyze and enhance this location information. Provide:
1. Accurate coordinates
2. Region and state/province
3. Geographic context (terrain, elevation, climate)
4. Nearby points of interest
5. Access routes and transportation
6. Geographic considerations for adventure planning

Return enhanced information in JSON format.""",
                ),
            ])

            messages = prompt.format_messages(
                context=context,
                location_name=location_name,
                coord_data=json.dumps(coords),
            )

            response = await self.llm.ainvoke(messages)
            content = response.content

            # Parse enhanced data with better error handling
            import re

            enhanced = coords  # Default fallback
            
            def clean_json_string(json_str: str) -> str:
                """Clean up common JSON formatting issues."""
                if not json_str:
                    return "{}"
                
                # Remove trailing commas before } or ] - handle all whitespace cases
                # This regex matches: comma, optional whitespace (including newlines), then closing bracket
                # Do this multiple times to handle deeply nested structures
                for _ in range(10):  # Max 10 iterations to avoid infinite loops
                    new_json = re.sub(r',(\s*[}\]])', r'\1', json_str)
                    if new_json == json_str:
                        break
                    json_str = new_json
                
                # Fix single-quoted property names: 'key': -> "key":
                # Handle keys with spaces or special chars: 'my key': -> "my key":
                json_str = re.sub(r"'([^']+)'\s*:", r'"\1":', json_str)
                
                # Fix single-quoted string values: : 'value' -> : "value"
                # Match : 'value' followed by comma, space, newline, or closing brace
                json_str = re.sub(r":\s*'([^']*)'([,\s}\n\]])", r': "\1"\2', json_str)
                
                # Fix unquoted property names - more careful approach
                # Only match at the start of a property (after { or ,)
                # Pattern: { or , whitespace* unquoted-identifier whitespace* :
                def quote_property_name(match):
                    prefix = match.group(1)  # { or ,
                    key = match.group(2).strip()  # the property name
                    # Don't quote if it's already quoted or looks like a number
                    if key.startswith('"') or key.startswith("'"):
                        return match.group(0)
                    if key.replace('.', '').replace('-', '').isdigit():
                        return match.group(0)
                    # Quote the key
                    return f'{prefix}"{key}":'
                
                # Match property names that come after { or , and aren't quoted
                # This pattern is more conservative - only matches at object boundaries
                json_str = re.sub(
                    r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_\s-]*?)(\s*:)',
                    quote_property_name,
                    json_str
                )
                
                # Also handle unquoted keys at the start of the JSON (no preceding { or ,)
                # But be very careful - only match if it's clearly a property name
                json_str = re.sub(
                    r'^(\s*)([a-zA-Z_][a-zA-Z0-9_\s-]*?)(\s*:)',
                    lambda m: f'{m.group(1)}"{m.group(2).strip()}":',
                    json_str,
                    flags=re.MULTILINE
                )
                
                # Remove any control characters that might break JSON parsing
                json_str = ''.join(char for char in json_str if ord(char) >= 32 or char in '\n\r\t')
                
                return json_str
            
            json_match = None
            json_str = None
            try:
                # Try to find JSON in markdown code block first
                json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1).strip()
                else:
                    # Try to find JSON object - use balanced brace matching
                    # Find the first { and try to match balanced braces
                    brace_start = content.find('{')
                    if brace_start != -1:
                        brace_count = 0
                        brace_end = brace_start
                        in_string = False
                        escape_next = False
                        
                        for i, char in enumerate(content[brace_start:], start=brace_start):
                            if escape_next:
                                escape_next = False
                                continue
                            
                            if char == '\\':
                                escape_next = True
                                continue
                            
                            if char == '"' and not escape_next:
                                in_string = not in_string
                                continue
                            
                            if not in_string:
                                if char == '{':
                                    brace_count += 1
                                elif char == '}':
                                    brace_count -= 1
                                    if brace_count == 0:
                                        brace_end = i + 1
                                        break
                        
                        if brace_count == 0:
                            json_str = content[brace_start:brace_end].strip()
                            json_match = type('obj', (object,), {'group': lambda x: json_str})()
                
                if json_str:
                    json_str = clean_json_string(json_str)
                    # Validate JSON is not empty or just whitespace
                    if json_str.strip():
                        enhanced = json.loads(json_str)
                    else:
                        raise json.JSONDecodeError("Empty JSON string", json_str, 0)
            except json.JSONDecodeError as json_err:
                # If JSON parsing fails, try to extract key information from text
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"JSON parsing error in Geo agent for {location_name}: {json_err}")
                # Log a snippet of the problematic JSON for debugging
                if json_str:
                    # Show context around the error position if available
                    error_pos = getattr(json_err, 'pos', None)
                    if error_pos and error_pos < len(json_str):
                        start = max(0, error_pos - 100)
                        end = min(len(json_str), error_pos + 100)
                        snippet = json_str[start:end]
                        logger.debug(f"Problematic JSON around error (pos {error_pos}): ...{snippet}...")
                    else:
                        snippet = json_str[:500] if len(json_str) > 500 else json_str
                        logger.debug(f"Problematic JSON snippet: {snippet}...")
                elif content:
                    snippet = content[:500] if len(content) > 500 else content
                    logger.debug(f"Content snippet: {snippet}...")
                
                # Try to extract coordinates if mentioned in text
                coord_match = re.search(r'["\']?lat["\']?\s*[:=]\s*([-\d.]+)', content, re.IGNORECASE)
                lon_match = re.search(r'["\']?lon["\']?\s*[:=]\s*([-\d.]+)', content, re.IGNORECASE)
                if coord_match and lon_match:
                    enhanced = {
                        "coordinates": {
                            "latitude": float(coord_match.group(1)),
                            "longitude": float(lon_match.group(1))
                        }
                    }
                # Otherwise, use coords from tool as fallback

            return {
                "location": location_name,
                "coordinates": enhanced.get("coordinates", coords.get("coordinates")),
                "region": enhanced.get("region", coords.get("region", "")),
                "country": enhanced.get("country", coords.get("country", "US")),
                "description": enhanced.get("description", ""),
                "geographic_context": enhanced.get("geographic_context", {}),
            }

        except Exception as e:
            print(f"Error in Geo agent: {e}")
            return {
                "location": location_name,
                "coordinates": None,
                "region": "",
                "country": "US",
            }

    async def calculate_route_distance(
        self, points: List[Dict[str, float]]
    ) -> Dict[str, Any]:
        """Calculate distance for a route with multiple points."""
        if len(points) < 2:
            return {"total_distance_miles": 0.0, "segments": []}

        total_distance = 0.0
        segments = []

        for i in range(len(points) - 1):
            distance_data = await invoke_tool_async(
                calculate_distance,
                {
                    "point1": points[i],
                    "point2": points[i + 1],
                }
            )

            try:
                dist_info = (
                    json.loads(distance_data)
                    if isinstance(distance_data, str)
                    else distance_data
                )
                segment_dist = dist_info.get("distance_miles", 0.0)
                total_distance += segment_dist
                segments.append({
                    "from": points[i],
                    "to": points[i + 1],
                    "distance_miles": segment_dist,
                })
            except Exception:
                pass

        return {
            "total_distance_miles": total_distance,
            "segments": segments,
        }

