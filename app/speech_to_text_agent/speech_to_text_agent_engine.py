"""Speech To Text Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.speech_to_text_agent.schemas import SpeechRecord

# In-memory speech store keyed by user_id, then speech_id.
# Example:
# {
#     "billy": {
#         "speech_001": {
#             "speech_id": "speech_001",
#             "audio_file": "meeting_recording.wav",
#             "detected_language": "en-US",
#             "transcription": "Welcome to the quarterly review meeting.",
#             "confidence_score": 92,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T09:05:00",
#         }
#     }
# }
speech_to_text_db: dict[str, dict[str, SpeechRecord]] = {}


def normalize_speech_id(speech_id: str) -> str:
    """Normalize a speech ID for case-insensitive, whitespace-tolerant lookups."""
    return speech_id.strip().lower()


class SpeechToTextAgentEngine:
    """Manage user speech-to-text records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def speech_id_exists(self, user_id: str, speech_id: str) -> bool:
        """Return True if a record for this speech ID already exists."""
        with self._lock:
            user_records = speech_to_text_db.get(user_id, {})
            return normalize_speech_id(speech_id) in user_records

    def create_record(self, user_id: str, record: SpeechRecord) -> SpeechRecord:
        """Create and store a speech record for the given user."""
        with self._lock:
            user_records = speech_to_text_db.setdefault(user_id, {})
            user_records[normalize_speech_id(record.speech_id)] = record

        return record

    def get_records(self, user_id: str) -> list[SpeechRecord]:
        """Return all speech records for the given user."""
        with self._lock:
            user_records = speech_to_text_db.get(user_id, {})
            return list(user_records.values())

    def get_record(self, user_id: str, speech_id: str) -> SpeechRecord | None:
        """Return one speech record by ID for the given user."""
        with self._lock:
            user_records = speech_to_text_db.get(user_id, {})
            return user_records.get(normalize_speech_id(speech_id))

    def update_record(
        self,
        user_id: str,
        speech_id: str,
        record: SpeechRecord,
    ) -> SpeechRecord | None:
        """Replace an existing speech record with a new version."""
        with self._lock:
            user_records = speech_to_text_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_speech_id(speech_id)
            if normalized_id not in user_records:
                return None

            new_normalized_id = normalize_speech_id(record.speech_id)
            if new_normalized_id != normalized_id:
                del user_records[normalized_id]

            user_records[new_normalized_id] = record

        return record

    def delete_record(
        self,
        user_id: str,
        speech_id: str,
    ) -> SpeechRecord | None:
        """Delete and return a speech record by ID."""
        with self._lock:
            user_records = speech_to_text_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_speech_id(speech_id)
            return user_records.pop(normalized_id, None)
