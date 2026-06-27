"""Object Detection Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.object_detection_agent.schemas import ObjectDetectionRecord

# In-memory object detection store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "object_id": "object_001",
#             "image_file": "street_scene.jpg",
#             "detected_object": "car",
#             "object_category": "vehicle",
#             "confidence_score": 94,
#             "bounding_box": "120,80,340,260",
#             "object_status": "detected",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T11:00:00",
#             "updated_at": "2026-06-04T11:02:00",
#         }
#     ]
# }
object_detection_db: dict[str, list[ObjectDetectionRecord]] = {}


def normalize_object_id(object_id: str) -> str:
    """Normalize an object ID for case-insensitive, whitespace-tolerant lookups."""
    return object_id.strip().lower()


class ObjectDetectionAgentEngine:
    """Manage user object detection records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def object_id_exists(self, user_id: str, object_id: str) -> bool:
        """Return True if a record for this object ID already exists."""
        with self._lock:
            return self._find_record_index(
                object_detection_db.get(user_id, []),
                object_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: ObjectDetectionRecord,
    ) -> ObjectDetectionRecord:
        """Create and store an object detection record for the given user."""
        with self._lock:
            user_records = object_detection_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ObjectDetectionRecord]:
        """Return all object detection records for the given user."""
        with self._lock:
            return list(object_detection_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        object_id: str,
    ) -> ObjectDetectionRecord | None:
        """Return one object detection record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, object_id)

    def update_record(
        self,
        user_id: str,
        object_id: str,
        record: ObjectDetectionRecord,
    ) -> ObjectDetectionRecord | None:
        """Replace an existing object detection record with a new version."""
        with self._lock:
            user_records = object_detection_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, object_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        object_id: str,
    ) -> ObjectDetectionRecord | None:
        """Delete and return an object detection record by ID."""
        with self._lock:
            user_records = object_detection_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, object_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        object_id: str,
    ) -> ObjectDetectionRecord | None:
        """Locate an object detection record in the user's list by ID."""
        user_records = object_detection_db.get(user_id, [])
        index = self._find_record_index(user_records, object_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ObjectDetectionRecord],
        object_id: str,
    ) -> int | None:
        """Return the list index for an object ID, if it exists."""
        normalized_id = normalize_object_id(object_id)
        for index, record in enumerate(user_records):
            if normalize_object_id(record.object_id) == normalized_id:
                return index
        return None
