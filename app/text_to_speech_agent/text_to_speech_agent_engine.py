"""Text To Speech Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.text_to_speech_agent.schemas import TextToSpeechRecord

# In-memory TTS store keyed by user_id, then tts_id.
# Example:
# {
#     "billy": {
#         "tts_001": {
#             "tts_id": "tts_001",
#             "input_text": "Welcome to the quarterly review meeting.",
#             "output_audio_file": "welcome_message.mp3",
#             "language": "en-US",
#             "voice_name": "Aria",
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T09:02:00",
#         }
#     }
# }
text_to_speech_db: dict[str, dict[str, TextToSpeechRecord]] = {}


def normalize_tts_id(tts_id: str) -> str:
    """Normalize a TTS ID for case-insensitive, whitespace-tolerant lookups."""
    return tts_id.strip().lower()


class TextToSpeechAgentEngine:
    """Manage user text-to-speech records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def tts_id_exists(self, user_id: str, tts_id: str) -> bool:
        """Return True if a record for this TTS ID already exists."""
        with self._lock:
            user_records = text_to_speech_db.get(user_id, {})
            return normalize_tts_id(tts_id) in user_records

    def create_record(
        self,
        user_id: str,
        record: TextToSpeechRecord,
    ) -> TextToSpeechRecord:
        """Create and store a TTS record for the given user."""
        with self._lock:
            user_records = text_to_speech_db.setdefault(user_id, {})
            user_records[normalize_tts_id(record.tts_id)] = record

        return record

    def get_records(self, user_id: str) -> list[TextToSpeechRecord]:
        """Return all TTS records for the given user."""
        with self._lock:
            user_records = text_to_speech_db.get(user_id, {})
            return list(user_records.values())

    def get_record(self, user_id: str, tts_id: str) -> TextToSpeechRecord | None:
        """Return one TTS record by ID for the given user."""
        with self._lock:
            user_records = text_to_speech_db.get(user_id, {})
            return user_records.get(normalize_tts_id(tts_id))

    def update_record(
        self,
        user_id: str,
        tts_id: str,
        record: TextToSpeechRecord,
    ) -> TextToSpeechRecord | None:
        """Replace an existing TTS record with a new version."""
        with self._lock:
            user_records = text_to_speech_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_tts_id(tts_id)
            if normalized_id not in user_records:
                return None

            new_normalized_id = normalize_tts_id(record.tts_id)
            if new_normalized_id != normalized_id:
                del user_records[normalized_id]

            user_records[new_normalized_id] = record

        return record

    def delete_record(
        self,
        user_id: str,
        tts_id: str,
    ) -> TextToSpeechRecord | None:
        """Delete and return a TTS record by ID."""
        with self._lock:
            user_records = text_to_speech_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_tts_id(tts_id)
            return user_records.pop(normalized_id, None)
