"""Emotional Intelligence Tracker Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.emotional_intelligence_tracker.schemas import EmotionalIntelligenceRecord

# In-memory EQ store keyed by user_id, then eq_id.
# Example:
# {
#     "billy": {
#         "eq_001": {
#             "eq_id": "eq_001",
#             "self_awareness": 80,
#             "self_regulation": 75,
#             "empathy": 90,
#             "social_skills": 85,
#             "motivation": 88,
#             "overall_eq": 84,
#         }
#     }
# }
emotional_intelligence_tracker_db: dict[str, dict[str, EmotionalIntelligenceRecord]] = {}


def normalize_eq_id(eq_id: str) -> str:
    """Normalize an EQ ID for case-insensitive, whitespace-tolerant lookups."""
    return eq_id.strip().lower()


class EmotionalIntelligenceTrackerEngine:
    """Manage user emotional intelligence records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def eq_id_exists(self, user_id: str, eq_id: str) -> bool:
        """Return True if a record for this EQ ID already exists."""
        with self._lock:
            user_records = emotional_intelligence_tracker_db.get(user_id, {})
            return normalize_eq_id(eq_id) in user_records

    def create_record(
        self,
        user_id: str,
        record: EmotionalIntelligenceRecord,
    ) -> EmotionalIntelligenceRecord:
        """Create and store an EQ record for the given user."""
        with self._lock:
            user_records = emotional_intelligence_tracker_db.setdefault(user_id, {})
            user_records[normalize_eq_id(record.eq_id)] = record

        return record

    def get_records(self, user_id: str) -> list[EmotionalIntelligenceRecord]:
        """Return all EQ records for the given user."""
        with self._lock:
            user_records = emotional_intelligence_tracker_db.get(user_id, {})
            return list(user_records.values())

    def get_record(
        self,
        user_id: str,
        eq_id: str,
    ) -> EmotionalIntelligenceRecord | None:
        """Return one EQ record by ID for the given user."""
        with self._lock:
            user_records = emotional_intelligence_tracker_db.get(user_id, {})
            return user_records.get(normalize_eq_id(eq_id))

    def update_record(
        self,
        user_id: str,
        eq_id: str,
        record: EmotionalIntelligenceRecord,
    ) -> EmotionalIntelligenceRecord | None:
        """Replace an existing EQ record with a new version."""
        with self._lock:
            user_records = emotional_intelligence_tracker_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_eq_id(eq_id)
            if normalized_id not in user_records:
                return None

            new_normalized_id = normalize_eq_id(record.eq_id)
            if new_normalized_id != normalized_id:
                del user_records[normalized_id]

            user_records[new_normalized_id] = record

        return record

    def delete_record(
        self,
        user_id: str,
        eq_id: str,
    ) -> EmotionalIntelligenceRecord | None:
        """Delete and return an EQ record by ID."""
        with self._lock:
            user_records = emotional_intelligence_tracker_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_eq_id(eq_id)
            return user_records.pop(normalized_id, None)
