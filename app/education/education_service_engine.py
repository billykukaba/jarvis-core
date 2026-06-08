"""Education Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.education.schemas import EducationRecord

# In-memory education store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "institution": "MIT",
#             "degree": "Bachelor of Computer Science",
#             "field": "Artificial Intelligence",
#             "start_year": 2027,
#             "end_year": 2031,
#         }
#     ]
# }
education_db: dict[str, list[EducationRecord]] = {}


class EducationServiceEngine:
    """Manage user education records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def institution_exists(self, user_id: str, institution: str) -> bool:
        """Return True if an education record for this institution already exists."""
        with self._lock:
            return self._find_record_index(
                education_db.get(user_id, []),
                institution,
            ) is not None

    def create_record(self, user_id: str, record: EducationRecord) -> EducationRecord:
        """Create and store an education record for the given user."""
        with self._lock:
            user_records = education_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[EducationRecord]:
        """Return all education records for the given user."""
        with self._lock:
            return list(education_db.get(user_id, []))

    def get_record(self, user_id: str, institution: str) -> EducationRecord | None:
        """Return one education record by institution for the given user."""
        with self._lock:
            return self._find_record(user_id, institution)

    def update_record(
        self,
        user_id: str,
        institution: str,
        record: EducationRecord,
    ) -> EducationRecord | None:
        """Replace an existing education record with a new version."""
        with self._lock:
            user_records = education_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, institution)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, institution: str) -> EducationRecord | None:
        """Delete and return an education record by institution."""
        with self._lock:
            user_records = education_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, institution)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, institution: str) -> EducationRecord | None:
        """Locate an education record in the user's list by institution."""
        user_records = education_db.get(user_id, [])
        index = self._find_record_index(user_records, institution)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[EducationRecord],
        institution: str,
    ) -> int | None:
        """Return the list index for an institution, if it exists."""
        normalized_institution = institution.lower()
        for index, record in enumerate(user_records):
            if record.institution.lower() == normalized_institution:
                return index
        return None
