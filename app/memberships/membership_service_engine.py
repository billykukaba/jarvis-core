"""Memberships Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.memberships.schemas import MembershipRecord

# In-memory membership store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "organization": "IEEE",
#             "role": "Senior Member",
#             "year": 2032,
#         }
#     ]
# }
memberships_db: dict[str, list[MembershipRecord]] = {}


def normalize_organization(organization: str) -> str:
    """Normalize an organization name for case-insensitive lookups."""
    return organization.strip().lower()


class MembershipServiceEngine:
    """Manage user membership records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def organization_exists(self, user_id: str, organization: str) -> bool:
        """Return True if a membership for this organization already exists."""
        with self._lock:
            return self._find_record_index(
                memberships_db.get(user_id, []),
                organization,
            ) is not None

    def create_record(self, user_id: str, record: MembershipRecord) -> MembershipRecord:
        """Create and store a membership record for the given user."""
        with self._lock:
            user_records = memberships_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[MembershipRecord]:
        """Return all membership records for the given user."""
        with self._lock:
            return list(memberships_db.get(user_id, []))

    def get_record(self, user_id: str, organization: str) -> MembershipRecord | None:
        """Return one membership record by organization for the given user."""
        with self._lock:
            return self._find_record(user_id, organization)

    def update_record(
        self,
        user_id: str,
        organization: str,
        record: MembershipRecord,
    ) -> MembershipRecord | None:
        """Replace an existing membership record with a new version."""
        with self._lock:
            user_records = memberships_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, organization)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, organization: str) -> MembershipRecord | None:
        """Delete and return a membership record by organization."""
        with self._lock:
            user_records = memberships_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, organization)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, organization: str) -> MembershipRecord | None:
        """Locate a membership record in the user's list by organization."""
        user_records = memberships_db.get(user_id, [])
        index = self._find_record_index(user_records, organization)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[MembershipRecord],
        organization: str,
    ) -> int | None:
        """Return the list index for an organization name, if it exists."""
        normalized_organization = normalize_organization(organization)
        for index, record in enumerate(user_records):
            if normalize_organization(record.organization) == normalized_organization:
                return index
        return None
