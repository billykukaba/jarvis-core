"""Face Recognition Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.face_recognition_agent.schemas import FaceRecognition

# In-memory face recognition store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "face_id": "face_001",
#             "image_file": "portrait.jpg",
#             "person_name": "Alice Johnson",
#             "confidence_score": 94,
#             "status": "recognized",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T09:01:00",
#         }
#     ]
# }
face_recognition_storage: dict[str, list[FaceRecognition]] = {}


def normalize_face_id(face_id: str) -> str:
    """Normalize a face ID for case-insensitive, whitespace-tolerant lookups."""
    return face_id.strip().lower()


class FaceRecognitionAgentEngine:
    """Manage user face recognition records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def face_id_exists(self, user_id: str, face_id: str) -> bool:
        """Return True if a record for this face ID already exists."""
        with self._lock:
            return self._find_record_index(
                face_recognition_storage.get(user_id, []),
                face_id,
            ) is not None

    def create_record(self, user_id: str, record: FaceRecognition) -> FaceRecognition:
        """Create and store a face recognition record for the given user."""
        with self._lock:
            user_records = face_recognition_storage.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[FaceRecognition]:
        """Return all face recognition records for the given user."""
        with self._lock:
            return list(face_recognition_storage.get(user_id, []))

    def get_record(self, user_id: str, face_id: str) -> FaceRecognition | None:
        """Return one face recognition record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, face_id)

    def update_record(
        self,
        user_id: str,
        face_id: str,
        record: FaceRecognition,
    ) -> FaceRecognition | None:
        """Replace an existing face recognition record with a new version."""
        with self._lock:
            user_records = face_recognition_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, face_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        face_id: str,
    ) -> FaceRecognition | None:
        """Delete and return a face recognition record by ID."""
        with self._lock:
            user_records = face_recognition_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, face_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        face_id: str,
    ) -> FaceRecognition | None:
        """Locate a face recognition record in the user's list by ID."""
        user_records = face_recognition_storage.get(user_id, [])
        index = self._find_record_index(user_records, face_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[FaceRecognition],
        face_id: str,
    ) -> int | None:
        """Return the list index for a face ID, if it exists."""
        normalized_id = normalize_face_id(face_id)
        for index, record in enumerate(user_records):
            if normalize_face_id(record.face_id) == normalized_id:
                return index
        return None
