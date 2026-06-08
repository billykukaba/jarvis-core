"""Conferences Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.conferences.schemas import ConferenceRecord

# In-memory conference store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "title": "AI Summit Keynote",
#             "event": "MIT AI Conference",
#             "year": 2033,
#         }
#     ]
# }
conferences_db: dict[str, list[ConferenceRecord]] = {}


def normalize_title(title: str) -> str:
    """Normalize a title for case-insensitive, whitespace-tolerant lookups."""
    return title.strip().lower()


class ConferenceServiceEngine:
    """Manage user conference records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def title_exists(self, user_id: str, title: str) -> bool:
        """Return True if a conference record with this title already exists."""
        with self._lock:
            return self._find_record_index(
                conferences_db.get(user_id, []),
                title,
            ) is not None

    def create_record(self, user_id: str, record: ConferenceRecord) -> ConferenceRecord:
        """Create and store a conference record for the given user."""
        with self._lock:
            user_records = conferences_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ConferenceRecord]:
        """Return all conference records for the given user."""
        with self._lock:
            return list(conferences_db.get(user_id, []))

    def get_record(self, user_id: str, title: str) -> ConferenceRecord | None:
        """Return one conference record by title for the given user."""
        with self._lock:
            return self._find_record(user_id, title)

    def update_record(
        self,
        user_id: str,
        title: str,
        record: ConferenceRecord,
    ) -> ConferenceRecord | None:
        """Replace an existing conference record with a new version."""
        with self._lock:
            user_records = conferences_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, title)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, title: str) -> ConferenceRecord | None:
        """Delete and return a conference record by title."""
        with self._lock:
            user_records = conferences_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, title)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, title: str) -> ConferenceRecord | None:
        """Locate a conference record in the user's list by title."""
        user_records = conferences_db.get(user_id, [])
        index = self._find_record_index(user_records, title)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ConferenceRecord],
        title: str,
    ) -> int | None:
        """Return the list index for a conference title, if it exists."""
        normalized_title = normalize_title(title)
        for index, record in enumerate(user_records):
            if normalize_title(record.title) == normalized_title:
                return index
        return None
