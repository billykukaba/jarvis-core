"""Volunteer Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.volunteer.schemas import VolunteerRecord

# In-memory volunteer store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "organization": "MIT OpenCourseWare",
#             "role": "Content Contributor",
#             "year": 2032,
#         }
#     ]
# }
volunteer_db: dict[str, list[VolunteerRecord]] = {}


def normalize_organization(organization: str) -> str:
    """Normalize an organization name for case-insensitive lookups."""
    return organization.strip().lower()


class VolunteerServiceEngine:
    """Manage user volunteer records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def organization_exists(self, user_id: str, organization: str) -> bool:
        """Return True if a volunteer record for this organization already exists."""
        with self._lock:
            return self._find_record_index(
                volunteer_db.get(user_id, []),
                organization,
            ) is not None

    def create_record(self, user_id: str, record: VolunteerRecord) -> VolunteerRecord:
        """Create and store a volunteer record for the given user."""
        with self._lock:
            user_records = volunteer_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[VolunteerRecord]:
        """Return all volunteer records for the given user."""
        with self._lock:
            return list(volunteer_db.get(user_id, []))

    def get_record(self, user_id: str, organization: str) -> VolunteerRecord | None:
        """Return one volunteer record by organization for the given user."""
        with self._lock:
            return self._find_record(user_id, organization)

    def update_record(
        self,
        user_id: str,
        organization: str,
        record: VolunteerRecord,
    ) -> VolunteerRecord | None:
        """Replace an existing volunteer record with a new version."""
        with self._lock:
            user_records = volunteer_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, organization)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, organization: str) -> VolunteerRecord | None:
        """Delete and return a volunteer record by organization."""
        with self._lock:
            user_records = volunteer_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, organization)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, organization: str) -> VolunteerRecord | None:
        """Locate a volunteer record in the user's list by organization."""
        user_records = volunteer_db.get(user_id, [])
        index = self._find_record_index(user_records, organization)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[VolunteerRecord],
        organization: str,
    ) -> int | None:
        """Return the list index for an organization name, if it exists."""
        normalized_organization = normalize_organization(organization)
        for index, record in enumerate(user_records):
            if normalize_organization(record.organization) == normalized_organization:
                return index
        return None
