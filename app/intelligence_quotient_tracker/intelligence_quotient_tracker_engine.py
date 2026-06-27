"""Intelligence Quotient Tracker Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.intelligence_quotient_tracker.schemas import IntelligenceQuotientRecord

# In-memory IQ store keyed by user_id, then iq_id.
# Example:
# {
#     "billy": {
#         "iq_001": {
#             "iq_id": "iq_001",
#             "iq_score": 128,
#             "classification": "Very Superior",
#             "test_date": "2026-06-04",
#         }
#     }
# }
intelligence_quotient_tracker_db: dict[str, dict[str, IntelligenceQuotientRecord]] = {}


def normalize_iq_id(iq_id: str) -> str:
    """Normalize an IQ ID for case-insensitive, whitespace-tolerant lookups."""
    return iq_id.strip().lower()


class IntelligenceQuotientTrackerEngine:
    """Manage user IQ records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def iq_id_exists(self, user_id: str, iq_id: str) -> bool:
        """Return True if a record for this IQ ID already exists."""
        with self._lock:
            user_records = intelligence_quotient_tracker_db.get(user_id, {})
            return normalize_iq_id(iq_id) in user_records

    def create_record(
        self,
        user_id: str,
        record: IntelligenceQuotientRecord,
    ) -> IntelligenceQuotientRecord:
        """Create and store an IQ record for the given user."""
        with self._lock:
            user_records = intelligence_quotient_tracker_db.setdefault(user_id, {})
            user_records[normalize_iq_id(record.iq_id)] = record

        return record

    def get_records(self, user_id: str) -> list[IntelligenceQuotientRecord]:
        """Return all IQ records for the given user."""
        with self._lock:
            user_records = intelligence_quotient_tracker_db.get(user_id, {})
            return list(user_records.values())

    def get_record(
        self,
        user_id: str,
        iq_id: str,
    ) -> IntelligenceQuotientRecord | None:
        """Return one IQ record by ID for the given user."""
        with self._lock:
            user_records = intelligence_quotient_tracker_db.get(user_id, {})
            return user_records.get(normalize_iq_id(iq_id))

    def update_record(
        self,
        user_id: str,
        iq_id: str,
        record: IntelligenceQuotientRecord,
    ) -> IntelligenceQuotientRecord | None:
        """Replace an existing IQ record with a new version."""
        with self._lock:
            user_records = intelligence_quotient_tracker_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_iq_id(iq_id)
            if normalized_id not in user_records:
                return None

            new_normalized_id = normalize_iq_id(record.iq_id)
            if new_normalized_id != normalized_id:
                del user_records[normalized_id]

            user_records[new_normalized_id] = record

        return record

    def delete_record(
        self,
        user_id: str,
        iq_id: str,
    ) -> IntelligenceQuotientRecord | None:
        """Delete and return an IQ record by ID."""
        with self._lock:
            user_records = intelligence_quotient_tracker_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_iq_id(iq_id)
            return user_records.pop(normalized_id, None)
