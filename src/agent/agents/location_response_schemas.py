"""Structured output schemas for location agents.

This module defines Pydantic models for structured responses from location agents,
following LangChain best practices for predictable, validated output.
"""

from __future__ import annotations

from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field, field_validator


class LocationOverview(BaseModel):
    """Overview information about a location."""

    name: str
    coordinates: Dict[str, float] | None = None  # Made optional with fallback
    elevation: int | None = None  # Made optional
    region: str
    nickname: str | None = None
    proximity: Dict[str, Dict[str, Any]] | None = None
    
    @field_validator("coordinates", mode="before")
    @classmethod
    def ensure_coordinates(cls, v: Any) -> Dict[str, float] | None:
        """Ensure coordinates is a dict with lat/lon or latitude/longitude."""
        if v is None:
            return None
        if isinstance(v, dict):
            # Normalize coordinate keys
            if "lat" in v and "lon" in v:
                return {"latitude": float(v["lat"]), "longitude": float(v["lon"])}
            elif "latitude" in v and "longitude" in v:
                return {"latitude": float(v["latitude"]), "longitude": float(v["longitude"])}
            return v
        return None


class OutdoorActivity(BaseModel):
    """Information about an outdoor activity."""

    activity_type: str
    description: str
    famous_trails: List[str] = Field(default_factory=list)
    difficulty_range: str | None = None  # Made optional
    best_seasons: str | None = None
    warnings: List[str] | None = None
    additional_info: Dict[str, Any] | None = None
    
    @field_validator("famous_trails", mode="before")
    @classmethod
    def transform_trails(cls, v: Any) -> List[str]:
        """Transform famous_trails from dicts to strings if needed."""
        if not v:
            return []
        if isinstance(v, list):
            return [
                item.get("name", str(item)) if isinstance(item, dict) else str(item)
                for item in v
            ]
        return [str(v)]


class Attraction(BaseModel):
    """Information about an attraction."""

    name: str
    type: str = Field(description="Type of attraction: natural, cultural, recreation, etc.")
    description: str | None = None
    highlights: List[str] | None = None


class Business(BaseModel):
    """Information about a local business."""

    name: str
    type: str
    description: str | None = None
    highlights: List[str] | None = None


class PracticalInfo(BaseModel):
    """Practical information for visitors."""

    parking: str | None = None
    permits: str | None = None
    best_times: str | None = None
    weather: Dict[str, Any] | str | None = None  # Allow string or dict
    access: str | None = None
    considerations: List[str] | None = None
    
    @field_validator("weather", mode="before")
    @classmethod
    def transform_weather(cls, v: Any) -> Dict[str, Any] | str | None:
        """Transform weather from string to dict if needed."""
        if v is None:
            return None
        if isinstance(v, str):
            return {"description": v}
        return v


class LocationGuideResponse(BaseModel):
    """Structured response format for location agents.

    This schema ensures consistent, validated output from all location agents.
    """

    location: str
    location_name: str
    is_match: bool
    overview: LocationOverview
    outdoor_activities: List[OutdoorActivity] = Field(default_factory=list)
    key_attractions: List[Attraction] = Field(default_factory=list)
    businesses: Dict[str, List[Business]] = Field(
        default_factory=dict,
        description="Businesses organized by category: restaurants, accommodations, shops, etc.",
    )
    practical_info: PracticalInfo
    recommendations: List[str] = Field(default_factory=list)
    tools_used: List[str] = Field(default_factory=list)
    location_knowledge: Dict[str, Any] | None = None
    enhanced_info: Dict[str, Any] | None = None
    error: str | None = None

