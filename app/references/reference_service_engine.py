"""References Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.references.schemas import ReferenceRecord

# In-memory reference store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "name": "Dr. Jane Smith",
#             "title": "Professor of AI",
#             "organization": "MIT",
#             "email": "jane.smith@mit.edu",
#         }
#     ]
# }
references_db: dict[str, list[ReferenceRecord]] = {}


def normalize_name(name: str) -> str:
    """Normalize a name for case-insensitive, whitespace-tolerant lookups."""
    return name.strip().lower()


class ReferenceServiceEngine:
    """Manage user reference records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def name_exists(self, user_id: str, name: str) -> bool:
        """Return True if a reference with this name already exists."""
        with self._lock:
            return self._find_record_index(
                references_db.get(user_id, []),
                name,
            ) is not None

    def create_record(self, user_id: str, record: ReferenceRecord) -> ReferenceRecord:
        """Create and store a reference record for the given user."""
        with self._lock:
            user_records = references_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ReferenceRecord]:
        """Return all reference records for the given user."""
        with self._lock:
            return list(references_db.get(user_id, []))

    def get_record(self, user_id: str, name: str) -> ReferenceRecord | None:
        """Return one reference record by name for the given user."""
        with self._lock:
            return self._find_record(user_id, name)

    def update_record(
        self,
        user_id: str,
        name: str,
        record: ReferenceRecord,
    ) -> ReferenceRecord | None:
        """Replace an existing reference record with a new version."""
        with self._lock:
            user_records = references_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, name)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, name: str) -> ReferenceRecord | None:
        """Delete and return a reference record by name."""
        with self._lock:
            user_records = references_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, name)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, name: str) -> ReferenceRecord | None:
        """Locate a reference record in the user's list by name."""
        user_records = references_db.get(user_id, [])
        index = self._find_record_index(user_records, name)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ReferenceRecord],
        name: str,
    ) -> int | None:
        """Return the list index for a reference name, if it exists."""
        normalized_name = normalize_name(name)
        for index, record in enumerate(user_records):
            if normalize_name(record.name) == normalized_name:
                return index
        return None
