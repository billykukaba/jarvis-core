"""Cognitive Growth Tracker Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.cognitive_growth_tracker.schemas import CognitiveGrowthRecord

# In-memory cognitive growth store keyed by user_id, then growth_id.
# Example:
# {
#     "billy": {
#         "growth_001": {
#             "growth_id": "growth_001",
#             "cognitive_area": "Reasoning",
#             "previous_score": 40,
#             "current_score": 80,
#             "growth_percentage": 100,
#         }
#     }
# }
cognitive_growth_db: dict[str, dict[str, CognitiveGrowthRecord]] = {}


def normalize_growth_id(growth_id: str) -> str:
    """Normalize a growth ID for case-insensitive, whitespace-tolerant lookups."""
    return growth_id.strip().lower()


class CognitiveGrowthTrackerEngine:
    """Manage user cognitive growth records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def growth_id_exists(self, user_id: str, growth_id: str) -> bool:
        """Return True if a record for this growth ID already exists."""
        with self._lock:
            user_records = cognitive_growth_db.get(user_id, {})
            return normalize_growth_id(growth_id) in user_records

    def create_record(
        self,
        user_id: str,
        record: CognitiveGrowthRecord,
    ) -> CognitiveGrowthRecord:
        """Create and store a cognitive growth record for the given user."""
        with self._lock:
            user_records = cognitive_growth_db.setdefault(user_id, {})
            user_records[normalize_growth_id(record.growth_id)] = record

        return record

    def get_records(self, user_id: str) -> list[CognitiveGrowthRecord]:
        """Return all cognitive growth records for the given user."""
        with self._lock:
            user_records = cognitive_growth_db.get(user_id, {})
            return list(user_records.values())

    def get_record(
        self,
        user_id: str,
        growth_id: str,
    ) -> CognitiveGrowthRecord | None:
        """Return one cognitive growth record by ID for the given user."""
        with self._lock:
            user_records = cognitive_growth_db.get(user_id, {})
            return user_records.get(normalize_growth_id(growth_id))

    def update_record(
        self,
        user_id: str,
        growth_id: str,
        record: CognitiveGrowthRecord,
    ) -> CognitiveGrowthRecord | None:
        """Replace an existing cognitive growth record with a new version."""
        with self._lock:
            user_records = cognitive_growth_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_growth_id(growth_id)
            if normalized_id not in user_records:
                return None

            new_normalized_id = normalize_growth_id(record.growth_id)
            if new_normalized_id != normalized_id:
                del user_records[normalized_id]

            user_records[new_normalized_id] = record

        return record

    def delete_record(
        self,
        user_id: str,
        growth_id: str,
    ) -> CognitiveGrowthRecord | None:
        """Delete and return a cognitive growth record by ID."""
        with self._lock:
            user_records = cognitive_growth_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_growth_id(growth_id)
            return user_records.pop(normalized_id, None)
