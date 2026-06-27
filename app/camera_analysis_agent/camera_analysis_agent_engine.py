"""Camera Analysis Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.camera_analysis_agent.schemas import CameraAnalysisRecord

# In-memory camera analysis store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "camera_id": "camera_001",
#             "camera_file": "living_room_feed.mp4",
#             "detected_scene": "indoor_living_room",
#             "detected_objects": ["sofa", "lamp", "person", "coffee_table"],
#             "camera_summary": "Living room scene with one person seated on the sofa.",
#             "confidence_score": 88,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T10:00:00",
#             "updated_at": "2026-06-04T10:03:00",
#         }
#     ]
# }
camera_analysis_storage: dict[str, list[CameraAnalysisRecord]] = {}


def normalize_camera_id(camera_id: str) -> str:
    """Normalize a camera ID for case-insensitive, whitespace-tolerant lookups."""
    return camera_id.strip().lower()


class CameraAnalysisAgentEngine:
    """Manage user camera analysis records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def camera_id_exists(self, user_id: str, camera_id: str) -> bool:
        """Return True if a record for this camera ID already exists."""
        with self._lock:
            return self._find_record_index(
                camera_analysis_storage.get(user_id, []),
                camera_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: CameraAnalysisRecord,
    ) -> CameraAnalysisRecord:
        """Create and store a camera analysis record for the given user."""
        with self._lock:
            user_records = camera_analysis_storage.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[CameraAnalysisRecord]:
        """Return all camera analysis records for the given user."""
        with self._lock:
            return list(camera_analysis_storage.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        camera_id: str,
    ) -> CameraAnalysisRecord | None:
        """Return one camera analysis record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, camera_id)

    def update_record(
        self,
        user_id: str,
        camera_id: str,
        record: CameraAnalysisRecord,
    ) -> CameraAnalysisRecord | None:
        """Replace an existing camera analysis record with a new version."""
        with self._lock:
            user_records = camera_analysis_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, camera_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        camera_id: str,
    ) -> CameraAnalysisRecord | None:
        """Delete and return a camera analysis record by ID."""
        with self._lock:
            user_records = camera_analysis_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, camera_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        camera_id: str,
    ) -> CameraAnalysisRecord | None:
        """Locate a camera analysis record in the user's list by ID."""
        user_records = camera_analysis_storage.get(user_id, [])
        index = self._find_record_index(user_records, camera_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[CameraAnalysisRecord],
        camera_id: str,
    ) -> int | None:
        """Return the list index for a camera ID, if it exists."""
        normalized_id = normalize_camera_id(camera_id)
        for index, record in enumerate(user_records):
            if normalize_camera_id(record.camera_id) == normalized_id:
                return index
        return None
