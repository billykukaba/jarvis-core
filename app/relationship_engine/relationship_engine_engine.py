"""Relationship Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.relationship_engine.schemas import RelationshipRecord

# In-memory relationship store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "relationship_id": "rel_001",
#             "source_entity": "user_billy",
#             "target_entity": "project_jarvis_core",
#             "relationship_type": "owner",
#             "relationship_strength": 95,
#             "relationship_context": "Primary owner and lead developer of the project.",
#             "importance_score": 90,
#             "status": "active",
#             "progress_percentage": 100,
#             "created_at": "2026-06-05T04:00:00",
#             "updated_at": "2026-06-05T04:05:00",
#         }
#     ]
# }
relationship_engine_db: dict[str, list[RelationshipRecord]] = {}


def normalize_relationship_id(relationship_id: str) -> str:
    """Normalize a relationship ID for case-insensitive, whitespace-tolerant lookups."""
    return relationship_id.strip().lower()


class RelationshipEngine:
    """Manage user relationship records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def relationship_id_exists(self, user_id: str, relationship_id: str) -> bool:
        """Return True if a record for this relationship ID already exists."""
        with self._lock:
            return self._find_record_index(
                relationship_engine_db.get(user_id, []),
                relationship_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: RelationshipRecord,
    ) -> RelationshipRecord:
        """Create and store a relationship record for the given user."""
        with self._lock:
            user_records = relationship_engine_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[RelationshipRecord]:
        """Return all relationship records for the given user."""
        with self._lock:
            return list(relationship_engine_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        relationship_id: str,
    ) -> RelationshipRecord | None:
        """Return one relationship record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, relationship_id)

    def update_record(
        self,
        user_id: str,
        relationship_id: str,
        record: RelationshipRecord,
    ) -> RelationshipRecord | None:
        """Replace an existing relationship record with a new version."""
        with self._lock:
            user_records = relationship_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, relationship_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        relationship_id: str,
    ) -> RelationshipRecord | None:
        """Delete and return a relationship record by ID."""
        with self._lock:
            user_records = relationship_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, relationship_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        relationship_id: str,
    ) -> RelationshipRecord | None:
        """Locate a relationship record in the user's list by ID."""
        user_records = relationship_engine_db.get(user_id, [])
        index = self._find_record_index(user_records, relationship_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[RelationshipRecord],
        relationship_id: str,
    ) -> int | None:
        """Return the list index for a relationship ID, if it exists."""
        normalized_id = normalize_relationship_id(relationship_id)
        for index, record in enumerate(user_records):
            if normalize_relationship_id(record.relationship_id) == normalized_id:
                return index
        return None
