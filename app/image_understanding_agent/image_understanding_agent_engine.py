"""Image Understanding Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.image_understanding_agent.schemas import ImageUnderstandingRecord

# In-memory image understanding store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "image_id": "img_001",
#             "image_file": "street_scene.jpg",
#             "scene_description": "A busy urban street with pedestrians and cars.",
#             "detected_objects": ["person", "car", "traffic_light", "building"],
#             "confidence_score": 90,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T09:03:00",
#         }
#     ]
# }
image_understanding_storage: dict[str, list[ImageUnderstandingRecord]] = {}


def normalize_image_id(image_id: str) -> str:
    """Normalize an image ID for case-insensitive, whitespace-tolerant lookups."""
    return image_id.strip().lower()


class ImageUnderstandingAgentEngine:
    """Manage user image understanding records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def image_id_exists(self, user_id: str, image_id: str) -> bool:
        """Return True if a record for this image ID already exists."""
        with self._lock:
            return self._find_record_index(
                image_understanding_storage.get(user_id, []),
                image_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: ImageUnderstandingRecord,
    ) -> ImageUnderstandingRecord:
        """Create and store an image understanding record for the given user."""
        with self._lock:
            user_records = image_understanding_storage.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ImageUnderstandingRecord]:
        """Return all image understanding records for the given user."""
        with self._lock:
            return list(image_understanding_storage.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        image_id: str,
    ) -> ImageUnderstandingRecord | None:
        """Return one image understanding record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, image_id)

    def update_record(
        self,
        user_id: str,
        image_id: str,
        record: ImageUnderstandingRecord,
    ) -> ImageUnderstandingRecord | None:
        """Replace an existing image understanding record with a new version."""
        with self._lock:
            user_records = image_understanding_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, image_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        image_id: str,
    ) -> ImageUnderstandingRecord | None:
        """Delete and return an image understanding record by ID."""
        with self._lock:
            user_records = image_understanding_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, image_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        image_id: str,
    ) -> ImageUnderstandingRecord | None:
        """Locate an image understanding record in the user's list by ID."""
        user_records = image_understanding_storage.get(user_id, [])
        index = self._find_record_index(user_records, image_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ImageUnderstandingRecord],
        image_id: str,
    ) -> int | None:
        """Return the list index for an image ID, if it exists."""
        normalized_id = normalize_image_id(image_id)
        for index, record in enumerate(user_records):
            if normalize_image_id(record.image_id) == normalized_id:
                return index
        return None
