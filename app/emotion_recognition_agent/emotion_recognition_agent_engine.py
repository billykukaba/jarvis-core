"""Emotion Recognition Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.emotion_recognition_agent.schemas import EmotionRecognition

# In-memory emotion recognition store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "emotion_id": "emotion_001",
#             "image_file": "portrait.jpg",
#             "detected_emotion": "happy",
#             "confidence_score": 89,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T09:01:00",
#         }
#     ]
# }
emotion_recognition_storage: dict[str, list[EmotionRecognition]] = {}


def normalize_emotion_id(emotion_id: str) -> str:
    """Normalize an emotion ID for case-insensitive, whitespace-tolerant lookups."""
    return emotion_id.strip().lower()


class EmotionRecognitionAgentEngine:
    """Manage user emotion recognition records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def emotion_id_exists(self, user_id: str, emotion_id: str) -> bool:
        """Return True if a record for this emotion ID already exists."""
        with self._lock:
            return self._find_record_index(
                emotion_recognition_storage.get(user_id, []),
                emotion_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: EmotionRecognition,
    ) -> EmotionRecognition:
        """Create and store an emotion recognition record for the given user."""
        with self._lock:
            user_records = emotion_recognition_storage.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[EmotionRecognition]:
        """Return all emotion recognition records for the given user."""
        with self._lock:
            return list(emotion_recognition_storage.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        emotion_id: str,
    ) -> EmotionRecognition | None:
        """Return one emotion recognition record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, emotion_id)

    def update_record(
        self,
        user_id: str,
        emotion_id: str,
        record: EmotionRecognition,
    ) -> EmotionRecognition | None:
        """Replace an existing emotion recognition record with a new version."""
        with self._lock:
            user_records = emotion_recognition_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, emotion_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        emotion_id: str,
    ) -> EmotionRecognition | None:
        """Delete and return an emotion recognition record by ID."""
        with self._lock:
            user_records = emotion_recognition_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, emotion_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        emotion_id: str,
    ) -> EmotionRecognition | None:
        """Locate an emotion recognition record in the user's list by ID."""
        user_records = emotion_recognition_storage.get(user_id, [])
        index = self._find_record_index(user_records, emotion_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[EmotionRecognition],
        emotion_id: str,
    ) -> int | None:
        """Return the list index for an emotion ID, if it exists."""
        normalized_id = normalize_emotion_id(emotion_id)
        for index, record in enumerate(user_records):
            if normalize_emotion_id(record.emotion_id) == normalized_id:
                return index
        return None
