"""Pose Estimation Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.pose_estimation_agent.schemas import PoseEstimation

# In-memory pose estimation store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "pose_id": "pose_001",
#             "image_file": "yoga_pose.jpg",
#             "detected_pose": "warrior_ii",
#             "confidence_score": 88,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T09:02:00",
#         }
#     ]
# }
pose_estimation_storage: dict[str, list[PoseEstimation]] = {}


def normalize_pose_id(pose_id: str) -> str:
    """Normalize a pose ID for case-insensitive, whitespace-tolerant lookups."""
    return pose_id.strip().lower()


class PoseEstimationAgentEngine:
    """Manage user pose estimation records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def pose_id_exists(self, user_id: str, pose_id: str) -> bool:
        """Return True if a record for this pose ID already exists."""
        with self._lock:
            return self._find_record_index(
                pose_estimation_storage.get(user_id, []),
                pose_id,
            ) is not None

    def create_record(self, user_id: str, record: PoseEstimation) -> PoseEstimation:
        """Create and store a pose estimation record for the given user."""
        with self._lock:
            user_records = pose_estimation_storage.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[PoseEstimation]:
        """Return all pose estimation records for the given user."""
        with self._lock:
            return list(pose_estimation_storage.get(user_id, []))

    def get_record(self, user_id: str, pose_id: str) -> PoseEstimation | None:
        """Return one pose estimation record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, pose_id)

    def update_record(
        self,
        user_id: str,
        pose_id: str,
        record: PoseEstimation,
    ) -> PoseEstimation | None:
        """Replace an existing pose estimation record with a new version."""
        with self._lock:
            user_records = pose_estimation_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, pose_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        pose_id: str,
    ) -> PoseEstimation | None:
        """Delete and return a pose estimation record by ID."""
        with self._lock:
            user_records = pose_estimation_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, pose_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        pose_id: str,
    ) -> PoseEstimation | None:
        """Locate a pose estimation record in the user's list by ID."""
        user_records = pose_estimation_storage.get(user_id, [])
        index = self._find_record_index(user_records, pose_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[PoseEstimation],
        pose_id: str,
    ) -> int | None:
        """Return the list index for a pose ID, if it exists."""
        normalized_id = normalize_pose_id(pose_id)
        for index, record in enumerate(user_records):
            if normalize_pose_id(record.pose_id) == normalized_id:
                return index
        return None
