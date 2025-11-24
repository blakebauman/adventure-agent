"""Planning and itinerary tools."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from langchain.tools import tool


@tool
def create_itinerary(
    trails: List[Dict[str, Any]],
    start_location: str,
    duration_days: int,
) -> str:
    """Create a day-by-day itinerary for an adventure.

    Args:
        trails: List of trail information
        start_location: Starting location
        duration_days: Number of days

    Returns:
        JSON string with itinerary
    """
    itinerary = []
    for day in range(1, duration_days + 1):
        itinerary.append({
            "day": day,
            "activities": [
                f"Ride trail: {trails[day % len(trails)]['name'] if trails else 'Trail'}",
                "Camp overnight",
            ],
            "distance_miles": 15.0,
        })

    return json.dumps({"itinerary": itinerary})

