"""User Timeline Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.user_timeline_engine.schemas import UserTimelineRecord

# In-memory user timeline store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "timeline_id": "timeline_001",
#             "event_title": "Jarvis Core MVP Completed",
#             "event_description": "Completed the first MVP release of Jarvis Core.",
#             "event_category": "project_milestone",
#             "event_date": "2026-06-05",
#             "related_project": "jarvis_core",
#             "importance_score": 92,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-05T05:00:00",
#             "updated_at": "2026-06-05T05:10:00",
#         }
#     ]
# }
user_timeline_engine_db: dict[str, list[UserTimelineRecord]] = {}


def normalize_timeline_id(timeline_id: str) -> str:
    """Normalize a timeline ID for case-insensitive, whitespace-tolerant lookups."""
    return timeline_id.strip().lower()


class UserTimelineEngine:
    """Manage user timeline records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def timeline_id_exists(self, user_id: str, timeline_id: str) -> bool:
        """Return True if a record for this timeline ID already exists."""
        with self._lock:
            return self._find_record_index(
                user_timeline_engine_db.get(user_id, []),
                timeline_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: UserTimelineRecord,
    ) -> UserTimelineRecord:
        """Create and store a user timeline record for the given user."""
        with self._lock:
            user_records = user_timeline_engine_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[UserTimelineRecord]:
        """Return all user timeline records for the given user."""
        with self._lock:
            return list(user_timeline_engine_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        timeline_id: str,
    ) -> UserTimelineRecord | None:
        """Return one user timeline record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, timeline_id)

    def update_record(
        self,
        user_id: str,
        timeline_id: str,
        record: UserTimelineRecord,
    ) -> UserTimelineRecord | None:
        """Replace an existing user timeline record with a new version."""
        with self._lock:
            user_records = user_timeline_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, timeline_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        timeline_id: str,
    ) -> UserTimelineRecord | None:
        """Delete and return a user timeline record by ID."""
        with self._lock:
            user_records = user_timeline_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, timeline_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        timeline_id: str,
    ) -> UserTimelineRecord | None:
        """Locate a user timeline record in the user's list by ID."""
        user_records = user_timeline_engine_db.get(user_id, [])
        index = self._find_record_index(user_records, timeline_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[UserTimelineRecord],
        timeline_id: str,
    ) -> int | None:
        """Return the list index for a timeline ID, if it exists."""
        normalized_id = normalize_timeline_id(timeline_id)
        for index, record in enumerate(user_records):
            if normalize_timeline_id(record.timeline_id) == normalized_id:
                return index
        return None
