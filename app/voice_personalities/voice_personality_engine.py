"""Voice Personality Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.voice_personalities.schemas import VoicePersonalityRecord

# In-memory voice personality store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "personality": "Friendly Assistant",
#             "tone": "Warm",
#             "energy": "High",
#         }
#     ]
# }
voice_personalities_db: dict[str, list[VoicePersonalityRecord]] = {}


def normalize_personality(personality: str) -> str:
    """Normalize a personality name for case-insensitive, whitespace-tolerant lookups."""
    return personality.strip().lower()


class VoicePersonalityEngine:
    """Manage user voice personality records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def personality_exists(self, user_id: str, personality: str) -> bool:
        """Return True if a record for this personality already exists."""
        with self._lock:
            return self._find_record_index(
                voice_personalities_db.get(user_id, []),
                personality,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: VoicePersonalityRecord,
    ) -> VoicePersonalityRecord:
        """Create and store a voice personality record for the given user."""
        with self._lock:
            user_records = voice_personalities_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[VoicePersonalityRecord]:
        """Return all voice personality records for the given user."""
        with self._lock:
            return list(voice_personalities_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        personality: str,
    ) -> VoicePersonalityRecord | None:
        """Return one voice personality record by name for the given user."""
        with self._lock:
            return self._find_record(user_id, personality)

    def update_record(
        self,
        user_id: str,
        personality: str,
        record: VoicePersonalityRecord,
    ) -> VoicePersonalityRecord | None:
        """Replace an existing voice personality record with a new version."""
        with self._lock:
            user_records = voice_personalities_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, personality)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        personality: str,
    ) -> VoicePersonalityRecord | None:
        """Delete and return a voice personality record by name."""
        with self._lock:
            user_records = voice_personalities_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, personality)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        personality: str,
    ) -> VoicePersonalityRecord | None:
        """Locate a voice personality record in the user's list by name."""
        user_records = voice_personalities_db.get(user_id, [])
        index = self._find_record_index(user_records, personality)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[VoicePersonalityRecord],
        personality: str,
    ) -> int | None:
        """Return the list index for a personality name, if it exists."""
        normalized_personality = normalize_personality(personality)
        for index, record in enumerate(user_records):
            if normalize_personality(record.personality) == normalized_personality:
                return index
        return None
