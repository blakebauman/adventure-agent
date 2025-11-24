"""Data archiving system for adventure plans.

This module provides functionality to archive completed adventure plans
for future retrieval and analysis.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

from agent.config import Config
from agent.state import AdventureState


class ArchiveBackend:
    """Base class for archive storage backends."""

    def save_plan(self, state: AdventureState, metadata: Dict[str, Any] | None = None) -> str:
        """Save an adventure plan and return archive ID.
        
        Args:
            state: The complete adventure state
            metadata: Optional metadata (user_id, session_id, etc.)
            
        Returns:
            Archive ID for retrieving the plan later
        """
        raise NotImplementedError

    def get_plan(self, archive_id: str) -> Dict[str, Any] | None:
        """Retrieve an archived plan by ID.
        
        Args:
            archive_id: The archive ID
            
        Returns:
            Archived plan data or None if not found
        """
        raise NotImplementedError

    def list_plans(
        self,
        user_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List archived plans with optional filtering.
        
        Args:
            user_id: Optional user ID to filter by
            limit: Maximum number of plans to return
            offset: Offset for pagination
            
        Returns:
            List of plan metadata (not full plans)
        """
        raise NotImplementedError

    def search_plans(
        self,
        query: str,
        user_id: str | None = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Search archived plans by title, description, or location.
        
        Args:
            query: Search query string
            user_id: Optional user ID to filter by
            limit: Maximum number of plans to return
            
        Returns:
            List of matching plan metadata
        """
        raise NotImplementedError


class SQLiteArchiveBackend(ArchiveBackend):
    """SQLite-based archive backend."""

    def __init__(self, db_path: str = "adventure_archive.db"):
        """Initialize SQLite archive backend.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create plans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adventure_plans (
                archive_id TEXT PRIMARY KEY,
                user_id TEXT,
                session_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                title TEXT,
                description TEXT,
                location TEXT,
                activity_type TEXT,
                duration_days INTEGER,
                state_json TEXT,
                metadata_json TEXT
            )
        """)
        
        # Create indexes for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_id ON adventure_plans(user_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at ON adventure_plans(created_at)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_activity_type ON adventure_plans(activity_type)
        """)
        
        # Full-text search index (SQLite FTS5)
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS adventure_plans_fts USING fts5(
                archive_id,
                title,
                description,
                location,
                content='adventure_plans',
                content_rowid='rowid'
            )
        """)
        
        conn.commit()
        conn.close()

    def save_plan(self, state: AdventureState, metadata: Dict[str, Any] | None = None) -> str:
        """Save plan to SQLite database."""
        archive_id = str(uuid4())
        metadata = metadata or {}
        
        # Extract plan information for metadata
        plan = state.get("adventure_plan", {})
        title = plan.get("title", "Untitled Adventure Plan")
        description = plan.get("description", "")
        location = ""
        if plan.get("location"):
            loc = plan["location"]
            location = loc.get("name", "") or loc.get("region", "")
        
        user_prefs = state.get("user_preferences", {})
        activity_type = user_prefs.get("activity_type", "unknown")
        duration_days = plan.get("estimated_duration_days") or user_prefs.get("duration_days")
        
        user_id = metadata.get("user_id", "")
        session_id = metadata.get("session_id", "")
        
        # Serialize state and metadata
        state_json = json.dumps(state, default=str)
        metadata_json = json.dumps(metadata, default=str)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert into main table
            cursor.execute("""
                INSERT INTO adventure_plans (
                    archive_id, user_id, session_id, title, description,
                    location, activity_type, duration_days, state_json, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                archive_id, user_id, session_id, title, description,
                location, activity_type, duration_days, state_json, metadata_json
            ))
            
            # Update FTS index
            cursor.execute("""
                INSERT INTO adventure_plans_fts (
                    rowid, archive_id, title, description, location
                ) VALUES (
                    (SELECT rowid FROM adventure_plans WHERE archive_id = ?),
                    ?, ?, ?, ?
                )
            """, (archive_id, archive_id, title, description, location))
            
            conn.commit()
        finally:
            conn.close()
        
        return archive_id

    def get_plan(self, archive_id: str) -> Dict[str, Any] | None:
        """Retrieve plan from SQLite database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM adventure_plans WHERE archive_id = ?
        """, (archive_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            "archive_id": row["archive_id"],
            "user_id": row["user_id"],
            "session_id": row["session_id"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "title": row["title"],
            "description": row["description"],
            "location": row["location"],
            "activity_type": row["activity_type"],
            "duration_days": row["duration_days"],
            "state": json.loads(row["state_json"]),
            "metadata": json.loads(row["metadata_json"]) if row["metadata_json"] else {},
        }

    def list_plans(
        self,
        user_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List archived plans."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute("""
                SELECT archive_id, user_id, session_id, created_at, title,
                       description, location, activity_type, duration_days
                FROM adventure_plans
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (user_id, limit, offset))
        else:
            cursor.execute("""
                SELECT archive_id, user_id, session_id, created_at, title,
                       description, location, activity_type, duration_days
                FROM adventure_plans
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "archive_id": row["archive_id"],
                "user_id": row["user_id"],
                "session_id": row["session_id"],
                "created_at": row["created_at"],
                "title": row["title"],
                "description": row["description"],
                "location": row["location"],
                "activity_type": row["activity_type"],
                "duration_days": row["duration_days"],
            }
            for row in rows
        ]

    def search_plans(
        self,
        query: str,
        user_id: str | None = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Search plans using full-text search."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Build search query
        search_query = f"{query}*"  # Prefix search
        
        if user_id:
            cursor.execute("""
                SELECT p.archive_id, p.user_id, p.session_id, p.created_at,
                       p.title, p.description, p.location, p.activity_type, p.duration_days
                FROM adventure_plans p
                JOIN adventure_plans_fts fts ON p.archive_id = fts.archive_id
                WHERE fts.adventure_plans_fts MATCH ? AND p.user_id = ?
                ORDER BY p.created_at DESC
                LIMIT ?
            """, (search_query, user_id, limit))
        else:
            cursor.execute("""
                SELECT p.archive_id, p.user_id, p.session_id, p.created_at,
                       p.title, p.description, p.location, p.activity_type, p.duration_days
                FROM adventure_plans p
                JOIN adventure_plans_fts fts ON p.archive_id = fts.archive_id
                WHERE fts.adventure_plans_fts MATCH ?
                ORDER BY p.created_at DESC
                LIMIT ?
            """, (search_query, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "archive_id": row["archive_id"],
                "user_id": row["user_id"],
                "session_id": row["session_id"],
                "created_at": row["created_at"],
                "title": row["title"],
                "description": row["description"],
                "location": row["location"],
                "activity_type": row["activity_type"],
                "duration_days": row["duration_days"],
            }
            for row in rows
        ]


class JSONFileArchiveBackend(ArchiveBackend):
    """JSON file-based archive backend (simple, no database required)."""

    def __init__(self, archive_dir: str = "adventure_archive"):
        """Initialize JSON file archive backend.
        
        Args:
            archive_dir: Directory to store archived plans
        """
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.archive_dir / "index.json"
        self._init_index()

    def _init_index(self):
        """Initialize index file."""
        if not self.index_file.exists():
            with open(self.index_file, "w") as f:
                json.dump({"plans": []}, f, indent=2)

    def _load_index(self) -> Dict[str, Any]:
        """Load index file."""
        with open(self.index_file) as f:
            return json.load(f)

    def _save_index(self, index: Dict[str, Any]):
        """Save index file."""
        with open(self.index_file, "w") as f:
            json.dump(index, f, indent=2)

    def save_plan(self, state: AdventureState, metadata: Dict[str, Any] | None = None) -> str:
        """Save plan to JSON file."""
        archive_id = str(uuid4())
        metadata = metadata or {}
        
        # Extract plan information
        plan = state.get("adventure_plan", {})
        title = plan.get("title", "Untitled Adventure Plan")
        description = plan.get("description", "")
        location = ""
        if plan.get("location"):
            loc = plan["location"]
            location = loc.get("name", "") or loc.get("region", "")
        
        user_prefs = state.get("user_preferences", {})
        activity_type = user_prefs.get("activity_type", "unknown")
        duration_days = plan.get("estimated_duration_days") or user_prefs.get("duration_days")
        
        # Save plan file
        plan_file = self.archive_dir / f"{archive_id}.json"
        plan_data = {
            "archive_id": archive_id,
            "created_at": datetime.utcnow().isoformat(),
            "user_id": metadata.get("user_id", ""),
            "session_id": metadata.get("session_id", ""),
            "title": title,
            "description": description,
            "location": location,
            "activity_type": activity_type,
            "duration_days": duration_days,
            "state": state,
            "metadata": metadata,
        }
        
        with open(plan_file, "w") as f:
            json.dump(plan_data, f, indent=2, default=str)
        
        # Update index
        index = self._load_index()
        index["plans"].append({
            "archive_id": archive_id,
            "created_at": plan_data["created_at"],
            "user_id": metadata.get("user_id", ""),
            "session_id": metadata.get("session_id", ""),
            "title": title,
            "description": description,
            "location": location,
            "activity_type": activity_type,
            "duration_days": duration_days,
        })
        self._save_index(index)
        
        return archive_id

    def get_plan(self, archive_id: str) -> Dict[str, Any] | None:
        """Retrieve plan from JSON file."""
        plan_file = self.archive_dir / f"{archive_id}.json"
        if not plan_file.exists():
            return None
        
        with open(plan_file) as f:
            return json.load(f)

    def list_plans(
        self,
        user_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List archived plans."""
        index = self._load_index()
        plans = index.get("plans", [])
        
        # Filter by user_id if provided
        if user_id:
            plans = [p for p in plans if p.get("user_id") == user_id]
        
        # Sort by created_at (newest first)
        plans.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # Apply pagination
        return plans[offset : offset + limit]

    def search_plans(
        self,
        query: str,
        user_id: str | None = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Search plans (simple text matching)."""
        index = self._load_index()
        plans = index.get("plans", [])
        
        # Filter by user_id if provided
        if user_id:
            plans = [p for p in plans if p.get("user_id") == user_id]
        
        # Simple text search in title, description, location
        query_lower = query.lower()
        matching = [
            p
            for p in plans
            if query_lower in p.get("title", "").lower()
            or query_lower in p.get("description", "").lower()
            or query_lower in p.get("location", "").lower()
        ]
        
        # Sort by created_at (newest first)
        matching.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return matching[:limit]


def get_archive_backend() -> ArchiveBackend | None:
    """Get configured archive backend based on config.
    
    Returns:
        Archive backend instance or None if archiving is disabled
    """
    archive_type = Config.ARCHIVE_TYPE.lower() if Config.ARCHIVE_TYPE else None
    
    if not archive_type or archive_type == "none":
        return None
    
    if archive_type == "sqlite":
        db_path = Config.ARCHIVE_DB_PATH or "adventure_archive.db"
        return SQLiteArchiveBackend(db_path)
    
    elif archive_type == "json":
        archive_dir = Config.ARCHIVE_DIR or "adventure_archive"
        return JSONFileArchiveBackend(archive_dir)
    
    else:
        # Default to JSON if unknown type
        archive_dir = Config.ARCHIVE_DIR or "adventure_archive"
        return JSONFileArchiveBackend(archive_dir)


def archive_plan(
    state: AdventureState,
    user_id: str | None = None,
    session_id: str | None = None,
) -> str | None:
    """Archive a completed adventure plan.
    
    Args:
        state: The complete adventure state
        user_id: Optional user ID
        session_id: Optional session ID
        
    Returns:
        Archive ID if successful, None if archiving is disabled
    """
    backend = get_archive_backend()
    if not backend:
        return None
    
    metadata = {}
    if user_id:
        metadata["user_id"] = user_id
    if session_id:
        metadata["session_id"] = session_id
    
    try:
        archive_id = backend.save_plan(state, metadata)
        return archive_id
    except Exception as e:
        # Log error but don't fail the workflow
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to archive plan: {e}", exc_info=True)
        return None

