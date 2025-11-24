"""Utility functions for retrieving and managing archived adventure plans."""

from typing import Any, Dict, List

from agent.archive import get_archive_backend


def get_archived_plan(archive_id: str) -> Dict[str, Any] | None:
    """Retrieve an archived adventure plan by ID.
    
    Args:
        archive_id: The archive ID returned when the plan was saved
        
    Returns:
        Archived plan data including full state, or None if not found
        
    Example:
        >>> plan = get_archived_plan("123e4567-e89b-12d3-a456-426614174000")
        >>> print(plan["state"]["adventure_plan"]["title"])
    """
    backend = get_archive_backend()
    if not backend:
        return None
    
    return backend.get_plan(archive_id)


def list_archived_plans(
    user_id: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    """List archived adventure plans.
    
    Args:
        user_id: Optional user ID to filter plans by
        limit: Maximum number of plans to return (default: 100)
        offset: Offset for pagination (default: 0)
        
    Returns:
        List of plan metadata dictionaries with keys:
        - archive_id: Unique identifier for the plan
        - user_id: User ID if provided
        - session_id: Session ID if provided
        - created_at: Timestamp when plan was archived
        - title: Plan title
        - description: Plan description
        - location: Location name
        - activity_type: Type of activity (mountain_biking, hiking, etc.)
        - duration_days: Estimated duration in days
        
    Example:
        >>> plans = list_archived_plans(user_id="user123", limit=10)
        >>> for plan in plans:
        ...     print(f"{plan['title']} - {plan['created_at']}")
    """
    backend = get_archive_backend()
    if not backend:
        return []
    
    return backend.list_plans(user_id=user_id, limit=limit, offset=offset)


def search_archived_plans(
    query: str,
    user_id: str | None = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Search archived adventure plans by title, description, or location.
    
    Args:
        query: Search query string
        user_id: Optional user ID to filter plans by
        limit: Maximum number of plans to return (default: 100)
        
    Returns:
        List of matching plan metadata dictionaries (same format as list_archived_plans)
        
    Example:
        >>> results = search_archived_plans("Colorado mountain biking")
        >>> print(f"Found {len(results)} matching plans")
    """
    backend = get_archive_backend()
    if not backend:
        return []
    
    return backend.search_plans(query=query, user_id=user_id, limit=limit)


def export_plan_to_json(archive_id: str, output_path: str) -> bool:
    """Export an archived plan to a JSON file.
    
    Args:
        archive_id: The archive ID of the plan to export
        output_path: Path to save the JSON file
        
    Returns:
        True if successful, False otherwise
        
    Example:
        >>> export_plan_to_json("123e4567-...", "my_plan.json")
    """
    import json
    
    plan = get_archived_plan(archive_id)
    if not plan:
        return False
    
    try:
        with open(output_path, "w") as f:
            json.dump(plan, f, indent=2, default=str)
        return True
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to export plan: {e}", exc_info=True)
        return False

