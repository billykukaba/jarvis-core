"""Scene Understanding Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.scene_understanding_agent.schemas import SceneUnderstandingRecord

# In-memory scene understanding store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "scene_id": "scene_001",
#             "image_file": "office_workspace.jpg",
#             "scene_type": "indoor_office",
#             "scene_description": "Modern office with desk, monitor, and natural lighting.",
#             "detected_entities": ["desk", "monitor", "chair", "window", "plant"],
#             "environment_type": "workplace",
#             "confidence_score": 91,
#             "scene_status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T12:00:00",
#             "updated_at": "2026-06-04T12:05:00",
#         }
#     ]
# }
scene_understanding_db: dict[str, list[SceneUnderstandingRecord]] = {}


def normalize_scene_id(scene_id: str) -> str:
    """Normalize a scene ID for case-insensitive, whitespace-tolerant lookups."""
    return scene_id.strip().lower()


class SceneUnderstandingAgentEngine:
    """Manage user scene understanding records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def scene_id_exists(self, user_id: str, scene_id: str) -> bool:
        """Return True if a record for this scene ID already exists."""
        with self._lock:
            return self._find_record_index(
                scene_understanding_db.get(user_id, []),
                scene_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: SceneUnderstandingRecord,
    ) -> SceneUnderstandingRecord:
        """Create and store a scene understanding record for the given user."""
        with self._lock:
            user_records = scene_understanding_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[SceneUnderstandingRecord]:
        """Return all scene understanding records for the given user."""
        with self._lock:
            return list(scene_understanding_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        scene_id: str,
    ) -> SceneUnderstandingRecord | None:
        """Return one scene understanding record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, scene_id)

    def update_record(
        self,
        user_id: str,
        scene_id: str,
        record: SceneUnderstandingRecord,
    ) -> SceneUnderstandingRecord | None:
        """Replace an existing scene understanding record with a new version."""
        with self._lock:
            user_records = scene_understanding_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, scene_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        scene_id: str,
    ) -> SceneUnderstandingRecord | None:
        """Delete and return a scene understanding record by ID."""
        with self._lock:
            user_records = scene_understanding_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, scene_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        scene_id: str,
    ) -> SceneUnderstandingRecord | None:
        """Locate a scene understanding record in the user's list by ID."""
        user_records = scene_understanding_db.get(user_id, [])
        index = self._find_record_index(user_records, scene_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[SceneUnderstandingRecord],
        scene_id: str,
    ) -> int | None:
        """Return the list index for a scene ID, if it exists."""
        normalized_id = normalize_scene_id(scene_id)
        for index, record in enumerate(user_records):
            if normalize_scene_id(record.scene_id) == normalized_id:
                return index
        return None
