"""Interests Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.interests.schemas import InterestRecord

# In-memory interest store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "interest": "Machine Learning",
#             "level": "High",
#         }
#     ]
# }
interests_db: dict[str, list[InterestRecord]] = {}


def normalize_interest(interest: str) -> str:
    """Normalize an interest name for case-insensitive, whitespace-tolerant lookups."""
    return interest.strip().lower()


class InterestServiceEngine:
    """Manage user interest records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def interest_exists(self, user_id: str, interest: str) -> bool:
        """Return True if a record for this interest already exists."""
        with self._lock:
            return self._find_record_index(
                interests_db.get(user_id, []),
                interest,
            ) is not None

    def create_record(self, user_id: str, record: InterestRecord) -> InterestRecord:
        """Create and store an interest record for the given user."""
        with self._lock:
            user_records = interests_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[InterestRecord]:
        """Return all interest records for the given user."""
        with self._lock:
            return list(interests_db.get(user_id, []))

    def get_record(self, user_id: str, interest: str) -> InterestRecord | None:
        """Return one interest record by name for the given user."""
        with self._lock:
            return self._find_record(user_id, interest)

    def update_record(
        self,
        user_id: str,
        interest: str,
        record: InterestRecord,
    ) -> InterestRecord | None:
        """Replace an existing interest record with a new version."""
        with self._lock:
            user_records = interests_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, interest)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, interest: str) -> InterestRecord | None:
        """Delete and return an interest record by name."""
        with self._lock:
            user_records = interests_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, interest)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, interest: str) -> InterestRecord | None:
        """Locate an interest record in the user's list by name."""
        user_records = interests_db.get(user_id, [])
        index = self._find_record_index(user_records, interest)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[InterestRecord],
        interest: str,
    ) -> int | None:
        """Return the list index for an interest name, if it exists."""
        normalized_interest = normalize_interest(interest)
        for index, record in enumerate(user_records):
            if normalize_interest(record.interest) == normalized_interest:
                return index
        return None
