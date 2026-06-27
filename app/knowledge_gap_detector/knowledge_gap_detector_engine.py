"""Knowledge Gap Detector Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.knowledge_gap_detector.schemas import KnowledgeGap

# In-memory knowledge gap store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "gap_id": "gap_001",
#             "topic": "FastAPI Middleware",
#             "severity": 8,
#             "recommendation": "Study middleware lifecycle and custom middleware patterns",
#         }
#     ]
# }
knowledge_gap_db: dict[str, list[KnowledgeGap]] = {}


def normalize_gap_id(gap_id: str) -> str:
    """Normalize a gap ID for case-insensitive, whitespace-tolerant lookups."""
    return gap_id.strip().lower()


class KnowledgeGapDetectorEngine:
    """Manage user knowledge gap records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def gap_id_exists(self, user_id: str, gap_id: str) -> bool:
        """Return True if a record for this gap ID already exists."""
        with self._lock:
            return self._find_record_index(
                knowledge_gap_db.get(user_id, []),
                gap_id,
            ) is not None

    def create_record(self, user_id: str, record: KnowledgeGap) -> KnowledgeGap:
        """Create and store a knowledge gap record for the given user."""
        with self._lock:
            user_records = knowledge_gap_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[KnowledgeGap]:
        """Return all knowledge gap records for the given user."""
        with self._lock:
            return list(knowledge_gap_db.get(user_id, []))

    def get_record(self, user_id: str, gap_id: str) -> KnowledgeGap | None:
        """Return one knowledge gap record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, gap_id)

    def update_record(
        self,
        user_id: str,
        gap_id: str,
        record: KnowledgeGap,
    ) -> KnowledgeGap | None:
        """Replace an existing knowledge gap record with a new version."""
        with self._lock:
            user_records = knowledge_gap_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, gap_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, gap_id: str) -> KnowledgeGap | None:
        """Delete and return a knowledge gap record by ID."""
        with self._lock:
            user_records = knowledge_gap_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, gap_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, gap_id: str) -> KnowledgeGap | None:
        """Locate a knowledge gap record in the user's list by ID."""
        user_records = knowledge_gap_db.get(user_id, [])
        index = self._find_record_index(user_records, gap_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[KnowledgeGap],
        gap_id: str,
    ) -> int | None:
        """Return the list index for a gap ID, if it exists."""
        normalized_id = normalize_gap_id(gap_id)
        for index, record in enumerate(user_records):
            if normalize_gap_id(record.gap_id) == normalized_id:
                return index
        return None
