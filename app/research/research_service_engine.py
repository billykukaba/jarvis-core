"""Research Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.research.schemas import ResearchRecord

# In-memory research store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "title": "Neural Network Optimization",
#             "institution": "MIT CSAIL",
#             "year": 2033,
#         }
#     ]
# }
research_db: dict[str, list[ResearchRecord]] = {}


def normalize_title(title: str) -> str:
    """Normalize a title for case-insensitive, whitespace-tolerant lookups."""
    return title.strip().lower()


class ResearchServiceEngine:
    """Manage user research records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def title_exists(self, user_id: str, title: str) -> bool:
        """Return True if a research record with this title already exists."""
        with self._lock:
            return self._find_record_index(
                research_db.get(user_id, []),
                title,
            ) is not None

    def create_record(self, user_id: str, record: ResearchRecord) -> ResearchRecord:
        """Create and store a research record for the given user."""
        with self._lock:
            user_records = research_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ResearchRecord]:
        """Return all research records for the given user."""
        with self._lock:
            return list(research_db.get(user_id, []))

    def get_record(self, user_id: str, title: str) -> ResearchRecord | None:
        """Return one research record by title for the given user."""
        with self._lock:
            return self._find_record(user_id, title)

    def update_record(
        self,
        user_id: str,
        title: str,
        record: ResearchRecord,
    ) -> ResearchRecord | None:
        """Replace an existing research record with a new version."""
        with self._lock:
            user_records = research_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, title)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, title: str) -> ResearchRecord | None:
        """Delete and return a research record by title."""
        with self._lock:
            user_records = research_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, title)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, title: str) -> ResearchRecord | None:
        """Locate a research record in the user's list by title."""
        user_records = research_db.get(user_id, [])
        index = self._find_record_index(user_records, title)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ResearchRecord],
        title: str,
    ) -> int | None:
        """Return the list index for a research title, if it exists."""
        normalized_title = normalize_title(title)
        for index, record in enumerate(user_records):
            if normalize_title(record.title) == normalized_title:
                return index
        return None
