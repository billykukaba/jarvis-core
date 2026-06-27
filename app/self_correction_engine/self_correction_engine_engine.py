"""Self Correction Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.self_correction_engine.schemas import SelfCorrectionRecord

# In-memory self correction store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "correction_id": "corr_001",
#             "error_source": "reasoning_engine",
#             "error_description": "Incorrect date calculation in response",
#             "correction_strategy": "Re-run reasoning with validated date context",
#             "corrected_output": "The event occurs on June 15, 2026, not June 5.",
#             "confidence_score": 94,
#             "correction_status": "applied",
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-05T02:00:00",
#             "updated_at": "2026-06-05T02:10:00",
#         }
#     ]
# }
self_correction_engine_db: dict[str, list[SelfCorrectionRecord]] = {}


def normalize_correction_id(correction_id: str) -> str:
    """Normalize a correction ID for case-insensitive, whitespace-tolerant lookups."""
    return correction_id.strip().lower()


class SelfCorrectionEngine:
    """Manage user self correction records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def correction_id_exists(self, user_id: str, correction_id: str) -> bool:
        """Return True if a record for this correction ID already exists."""
        with self._lock:
            return self._find_record_index(
                self_correction_engine_db.get(user_id, []),
                correction_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: SelfCorrectionRecord,
    ) -> SelfCorrectionRecord:
        """Create and store a self correction record for the given user."""
        with self._lock:
            user_records = self_correction_engine_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[SelfCorrectionRecord]:
        """Return all self correction records for the given user."""
        with self._lock:
            return list(self_correction_engine_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        correction_id: str,
    ) -> SelfCorrectionRecord | None:
        """Return one self correction record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, correction_id)

    def update_record(
        self,
        user_id: str,
        correction_id: str,
        record: SelfCorrectionRecord,
    ) -> SelfCorrectionRecord | None:
        """Replace an existing self correction record with a new version."""
        with self._lock:
            user_records = self_correction_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, correction_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        correction_id: str,
    ) -> SelfCorrectionRecord | None:
        """Delete and return a self correction record by ID."""
        with self._lock:
            user_records = self_correction_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, correction_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        correction_id: str,
    ) -> SelfCorrectionRecord | None:
        """Locate a self correction record in the user's list by ID."""
        user_records = self_correction_engine_db.get(user_id, [])
        index = self._find_record_index(user_records, correction_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[SelfCorrectionRecord],
        correction_id: str,
    ) -> int | None:
        """Return the list index for a correction ID, if it exists."""
        normalized_id = normalize_correction_id(correction_id)
        for index, record in enumerate(user_records):
            if normalize_correction_id(record.correction_id) == normalized_id:
                return index
        return None
