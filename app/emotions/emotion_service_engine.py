"""Emotion Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.emotions.schemas import EmotionRecord

# In-memory emotion store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "emotion": "Happy",
#             "intensity": "High",
#         }
#     ]
# }
emotions_db: dict[str, list[EmotionRecord]] = {}


def normalize_emotion(emotion: str) -> str:
    """Normalize an emotion name for case-insensitive, whitespace-tolerant lookups."""
    return emotion.strip().lower()


class EmotionServiceEngine:
    """Manage user emotion records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def emotion_exists(self, user_id: str, emotion: str) -> bool:
        """Return True if a record for this emotion already exists."""
        with self._lock:
            return self._find_record_index(
                emotions_db.get(user_id, []),
                emotion,
            ) is not None

    def create_record(self, user_id: str, record: EmotionRecord) -> EmotionRecord:
        """Create and store an emotion record for the given user."""
        with self._lock:
            user_records = emotions_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[EmotionRecord]:
        """Return all emotion records for the given user."""
        with self._lock:
            return list(emotions_db.get(user_id, []))

    def get_record(self, user_id: str, emotion: str) -> EmotionRecord | None:
        """Return one emotion record by name for the given user."""
        with self._lock:
            return self._find_record(user_id, emotion)

    def update_record(
        self,
        user_id: str,
        emotion: str,
        record: EmotionRecord,
    ) -> EmotionRecord | None:
        """Replace an existing emotion record with a new version."""
        with self._lock:
            user_records = emotions_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, emotion)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, emotion: str) -> EmotionRecord | None:
        """Delete and return an emotion record by name."""
        with self._lock:
            user_records = emotions_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, emotion)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, emotion: str) -> EmotionRecord | None:
        """Locate an emotion record in the user's list by name."""
        user_records = emotions_db.get(user_id, [])
        index = self._find_record_index(user_records, emotion)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[EmotionRecord],
        emotion: str,
    ) -> int | None:
        """Return the list index for an emotion name, if it exists."""
        normalized_emotion = normalize_emotion(emotion)
        for index, record in enumerate(user_records):
            if normalize_emotion(record.emotion) == normalized_emotion:
                return index
        return None
