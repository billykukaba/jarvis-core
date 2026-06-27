"""Activity Recognition Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.activity_recognition_agent.schemas import ActivityRecognition

# In-memory activity recognition store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "activity_id": "activity_001",
#             "video_file": "gym_session.mp4",
#             "detected_activity": "running",
#             "confidence_score": 91,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T09:04:00",
#         }
#     ]
# }
activity_recognition_storage: dict[str, list[ActivityRecognition]] = {}


def normalize_activity_id(activity_id: str) -> str:
    """Normalize an activity ID for case-insensitive, whitespace-tolerant lookups."""
    return activity_id.strip().lower()


class ActivityRecognitionAgentEngine:
    """Manage user activity recognition records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def activity_id_exists(self, user_id: str, activity_id: str) -> bool:
        """Return True if a record for this activity ID already exists."""
        with self._lock:
            return self._find_record_index(
                activity_recognition_storage.get(user_id, []),
                activity_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: ActivityRecognition,
    ) -> ActivityRecognition:
        """Create and store an activity recognition record for the given user."""
        with self._lock:
            user_records = activity_recognition_storage.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ActivityRecognition]:
        """Return all activity recognition records for the given user."""
        with self._lock:
            return list(activity_recognition_storage.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        activity_id: str,
    ) -> ActivityRecognition | None:
        """Return one activity recognition record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, activity_id)

    def update_record(
        self,
        user_id: str,
        activity_id: str,
        record: ActivityRecognition,
    ) -> ActivityRecognition | None:
        """Replace an existing activity recognition record with a new version."""
        with self._lock:
            user_records = activity_recognition_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, activity_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        activity_id: str,
    ) -> ActivityRecognition | None:
        """Delete and return an activity recognition record by ID."""
        with self._lock:
            user_records = activity_recognition_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, activity_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        activity_id: str,
    ) -> ActivityRecognition | None:
        """Locate an activity recognition record in the user's list by ID."""
        user_records = activity_recognition_storage.get(user_id, [])
        index = self._find_record_index(user_records, activity_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ActivityRecognition],
        activity_id: str,
    ) -> int | None:
        """Return the list index for an activity ID, if it exists."""
        normalized_id = normalize_activity_id(activity_id)
        for index, record in enumerate(user_records):
            if normalize_activity_id(record.activity_id) == normalized_id:
                return index
        return None
