"""Reflection Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.reflection_engine.schemas import ReflectionRecord

# In-memory reflection store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "reflection_id": "reflect_001",
#             "topic": "Conversation Quality",
#             "reflection": "The conversation was productive and goal oriented",
#             "score": 9,
#         }
#     ]
# }
reflection_engine_db: dict[str, list[ReflectionRecord]] = {}


def normalize_reflection_id(reflection_id: str) -> str:
    """Normalize a reflection ID for case-insensitive, whitespace-tolerant lookups."""
    return reflection_id.strip().lower()


class ReflectionEngine:
    """Manage user self-reflection records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def reflection_id_exists(self, user_id: str, reflection_id: str) -> bool:
        """Return True if a record for this reflection ID already exists."""
        with self._lock:
            return self._find_record_index(
                reflection_engine_db.get(user_id, []),
                reflection_id,
            ) is not None

    def create_record(self, user_id: str, record: ReflectionRecord) -> ReflectionRecord:
        """Create and store a reflection record for the given user."""
        with self._lock:
            user_records = reflection_engine_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ReflectionRecord]:
        """Return all reflection records for the given user."""
        with self._lock:
            return list(reflection_engine_db.get(user_id, []))

    def get_record(self, user_id: str, reflection_id: str) -> ReflectionRecord | None:
        """Return one reflection record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, reflection_id)

    def update_record(
        self,
        user_id: str,
        reflection_id: str,
        record: ReflectionRecord,
    ) -> ReflectionRecord | None:
        """Replace an existing reflection record with a new version."""
        with self._lock:
            user_records = reflection_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, reflection_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        reflection_id: str,
    ) -> ReflectionRecord | None:
        """Delete and return a reflection record by ID."""
        with self._lock:
            user_records = reflection_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, reflection_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        reflection_id: str,
    ) -> ReflectionRecord | None:
        """Locate a reflection record in the user's list by ID."""
        user_records = reflection_engine_db.get(user_id, [])
        index = self._find_record_index(user_records, reflection_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ReflectionRecord],
        reflection_id: str,
    ) -> int | None:
        """Return the list index for a reflection ID, if it exists."""
        normalized_id = normalize_reflection_id(reflection_id)
        for index, record in enumerate(user_records):
            if normalize_reflection_id(record.reflection_id) == normalized_id:
                return index
        return None
