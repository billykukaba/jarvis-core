"""Licenses Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.licenses.schemas import LicenseRecord

# In-memory license store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "name": "Professional Engineer License",
#             "issuer": "Massachusetts Board",
#             "year": 2032,
#         }
#     ]
# }
licenses_db: dict[str, list[LicenseRecord]] = {}


def normalize_name(name: str) -> str:
    """Normalize a license name for case-insensitive, whitespace-tolerant lookups."""
    return name.strip().lower()


class LicenseServiceEngine:
    """Manage user license records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def name_exists(self, user_id: str, name: str) -> bool:
        """Return True if a license with this name already exists."""
        with self._lock:
            return self._find_record_index(
                licenses_db.get(user_id, []),
                name,
            ) is not None

    def create_record(self, user_id: str, record: LicenseRecord) -> LicenseRecord:
        """Create and store a license record for the given user."""
        with self._lock:
            user_records = licenses_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[LicenseRecord]:
        """Return all license records for the given user."""
        with self._lock:
            return list(licenses_db.get(user_id, []))

    def get_record(self, user_id: str, name: str) -> LicenseRecord | None:
        """Return one license record by name for the given user."""
        with self._lock:
            return self._find_record(user_id, name)

    def update_record(
        self,
        user_id: str,
        name: str,
        record: LicenseRecord,
    ) -> LicenseRecord | None:
        """Replace an existing license record with a new version."""
        with self._lock:
            user_records = licenses_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, name)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, name: str) -> LicenseRecord | None:
        """Delete and return a license record by name."""
        with self._lock:
            user_records = licenses_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, name)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, name: str) -> LicenseRecord | None:
        """Locate a license record in the user's list by name."""
        user_records = licenses_db.get(user_id, [])
        index = self._find_record_index(user_records, name)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[LicenseRecord],
        name: str,
    ) -> int | None:
        """Return the list index for a license name, if it exists."""
        normalized_name = normalize_name(name)
        for index, record in enumerate(user_records):
            if normalize_name(record.name) == normalized_name:
                return index
        return None
