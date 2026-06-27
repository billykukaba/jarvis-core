"""Object Tracking Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.object_tracking_agent.schemas import ObjectTracking

# In-memory object tracking store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "tracking_id": "track_001",
#             "video_file": "warehouse_feed.mp4",
#             "tracked_object": "forklift",
#             "tracking_status": "active",
#             "confidence_score": 87,
#             "status": "in_progress",
#             "progress_percentage": 65,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T09:05:00",
#         }
#     ]
# }
object_tracking_storage: dict[str, list[ObjectTracking]] = {}


def normalize_tracking_id(tracking_id: str) -> str:
    """Normalize a tracking ID for case-insensitive, whitespace-tolerant lookups."""
    return tracking_id.strip().lower()


class ObjectTrackingAgentEngine:
    """Manage user object tracking records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def tracking_id_exists(self, user_id: str, tracking_id: str) -> bool:
        """Return True if a record for this tracking ID already exists."""
        with self._lock:
            return self._find_record_index(
                object_tracking_storage.get(user_id, []),
                tracking_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: ObjectTracking,
    ) -> ObjectTracking:
        """Create and store an object tracking record for the given user."""
        with self._lock:
            user_records = object_tracking_storage.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ObjectTracking]:
        """Return all object tracking records for the given user."""
        with self._lock:
            return list(object_tracking_storage.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        tracking_id: str,
    ) -> ObjectTracking | None:
        """Return one object tracking record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, tracking_id)

    def update_record(
        self,
        user_id: str,
        tracking_id: str,
        record: ObjectTracking,
    ) -> ObjectTracking | None:
        """Replace an existing object tracking record with a new version."""
        with self._lock:
            user_records = object_tracking_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, tracking_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        tracking_id: str,
    ) -> ObjectTracking | None:
        """Delete and return an object tracking record by ID."""
        with self._lock:
            user_records = object_tracking_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, tracking_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        tracking_id: str,
    ) -> ObjectTracking | None:
        """Locate an object tracking record in the user's list by ID."""
        user_records = object_tracking_storage.get(user_id, [])
        index = self._find_record_index(user_records, tracking_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ObjectTracking],
        tracking_id: str,
    ) -> int | None:
        """Return the list index for a tracking ID, if it exists."""
        normalized_id = normalize_tracking_id(tracking_id)
        for index, record in enumerate(user_records):
            if normalize_tracking_id(record.tracking_id) == normalized_id:
                return index
        return None
