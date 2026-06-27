"""Vision Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.vision_agent.schemas import VisionRecord

# In-memory vision store keyed by user_id, then image_id.
# Example:
# {
#     "billy": {
#         "img_001": {
#             "image_id": "img_001",
#             "image_file": "office_scene.jpg",
#             "detected_objects": ["desk", "laptop", "chair", "person"],
#             "scene_description": "A person working at a desk in an office.",
#             "confidence_score": 88,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T09:03:00",
#         }
#     }
# }
vision_db: dict[str, dict[str, VisionRecord]] = {}


def normalize_image_id(image_id: str) -> str:
    """Normalize an image ID for case-insensitive, whitespace-tolerant lookups."""
    return image_id.strip().lower()


class VisionAgentEngine:
    """Manage user vision records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def image_id_exists(self, user_id: str, image_id: str) -> bool:
        """Return True if a record for this image ID already exists."""
        with self._lock:
            user_records = vision_db.get(user_id, {})
            return normalize_image_id(image_id) in user_records

    def create_record(self, user_id: str, record: VisionRecord) -> VisionRecord:
        """Create and store a vision record for the given user."""
        with self._lock:
            user_records = vision_db.setdefault(user_id, {})
            user_records[normalize_image_id(record.image_id)] = record

        return record

    def get_records(self, user_id: str) -> list[VisionRecord]:
        """Return all vision records for the given user."""
        with self._lock:
            user_records = vision_db.get(user_id, {})
            return list(user_records.values())

    def get_record(self, user_id: str, image_id: str) -> VisionRecord | None:
        """Return one vision record by ID for the given user."""
        with self._lock:
            user_records = vision_db.get(user_id, {})
            return user_records.get(normalize_image_id(image_id))

    def update_record(
        self,
        user_id: str,
        image_id: str,
        record: VisionRecord,
    ) -> VisionRecord | None:
        """Replace an existing vision record with a new version."""
        with self._lock:
            user_records = vision_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_image_id(image_id)
            if normalized_id not in user_records:
                return None

            new_normalized_id = normalize_image_id(record.image_id)
            if new_normalized_id != normalized_id:
                del user_records[normalized_id]

            user_records[new_normalized_id] = record

        return record

    def delete_record(
        self,
        user_id: str,
        image_id: str,
    ) -> VisionRecord | None:
        """Delete and return a vision record by ID."""
        with self._lock:
            user_records = vision_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_image_id(image_id)
            return user_records.pop(normalized_id, None)
