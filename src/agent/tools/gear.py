"""Gear and product recommendation tools."""

from __future__ import annotations

import json
from typing import List

from langchain.tools import tool


@tool
def recommend_gear(
    adventure_type: str,
    duration_days: int,
    skill_level: str,
    gear_owned: List[str] | None = None,
) -> str:
    """Recommend gear and products for an adventure.

    Args:
        adventure_type: Type of adventure
        duration_days: Duration in days
        skill_level: User skill level
        gear_owned: List of gear user already owns

    Returns:
        JSON string with gear recommendations
    """
    recommendations = [
        {
            "name": "Mountain Bike Helmet",
            "category": "safety",
            "description": "Essential safety gear",
            "affiliate_url": "https://example.com/affiliate/helmet",
            "essential": True,
        },
        {
            "name": "Bikepacking Bags",
            "category": "bikepacking",
            "description": "For multi-day adventures",
            "affiliate_url": "https://example.com/affiliate/bags",
            "essential": duration_days > 1,
        },
    ]

    return json.dumps({"recommendations": recommendations})


@tool
def search_gear_products(
    category: str, price_range: str | None = None
) -> str:
    """Search for specific gear products.

    Args:
        category: Product category
        price_range: Price range filter

    Returns:
        JSON string with product options
    """
    return json.dumps({
        "products": [
            {
                "name": f"{category} Product",
                "category": category,
                "price_range": price_range or "$50-200",
                "affiliate_url": f"https://example.com/affiliate/{category}",
            }
        ]
    })

