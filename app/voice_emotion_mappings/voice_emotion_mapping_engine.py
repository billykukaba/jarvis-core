"""Voice Emotion Mapping Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.voice_emotion_mappings.schemas import VoiceEmotionMappingRecord

# In-memory voice emotion mapping store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "emotion": "Happy",
#             "voice_style": "Cheerful",
#             "speech_speed": "Normal",
#         }
#     ]
# }
voice_emotion_mappings_db: dict[str, list[VoiceEmotionMappingRecord]] = {}


def normalize_emotion(emotion: str) -> str:
    """Normalize an emotion name for case-insensitive, whitespace-tolerant lookups."""
    return emotion.strip().lower()


class VoiceEmotionMappingEngine:
    """Manage user voice emotion mapping records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def emotion_exists(self, user_id: str, emotion: str) -> bool:
        """Return True if a record for this emotion already exists."""
        with self._lock:
            return self._find_record_index(
                voice_emotion_mappings_db.get(user_id, []),
                emotion,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: VoiceEmotionMappingRecord,
    ) -> VoiceEmotionMappingRecord:
        """Create and store a voice emotion mapping record for the given user."""
        with self._lock:
            user_records = voice_emotion_mappings_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[VoiceEmotionMappingRecord]:
        """Return all voice emotion mapping records for the given user."""
        with self._lock:
            return list(voice_emotion_mappings_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        emotion: str,
    ) -> VoiceEmotionMappingRecord | None:
        """Return one voice emotion mapping record by name for the given user."""
        with self._lock:
            return self._find_record(user_id, emotion)

    def update_record(
        self,
        user_id: str,
        emotion: str,
        record: VoiceEmotionMappingRecord,
    ) -> VoiceEmotionMappingRecord | None:
        """Replace an existing voice emotion mapping record with a new version."""
        with self._lock:
            user_records = voice_emotion_mappings_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, emotion)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        emotion: str,
    ) -> VoiceEmotionMappingRecord | None:
        """Delete and return a voice emotion mapping record by name."""
        with self._lock:
            user_records = voice_emotion_mappings_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, emotion)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        emotion: str,
    ) -> VoiceEmotionMappingRecord | None:
        """Locate a voice emotion mapping record in the user's list by name."""
        user_records = voice_emotion_mappings_db.get(user_id, [])
        index = self._find_record_index(user_records, emotion)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[VoiceEmotionMappingRecord],
        emotion: str,
    ) -> int | None:
        """Return the list index for an emotion name, if it exists."""
        normalized_emotion = normalize_emotion(emotion)
        for index, record in enumerate(user_records):
            if normalize_emotion(record.emotion) == normalized_emotion:
                return index
        return None
