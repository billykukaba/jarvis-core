"""Certifications Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.certifications.schemas import Certification

# In-memory certification store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "name": "AWS Certified Developer",
#             "organization": "Amazon",
#             "year": 2032,
#         }
#     ]
# }
certifications_db: dict[str, list[Certification]] = {}


class CertificationServiceEngine:
    """Manage user certification records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def name_exists(self, user_id: str, name: str) -> bool:
        """Return True if a certification with this name already exists."""
        with self._lock:
            return self._find_certification_index(
                certifications_db.get(user_id, []),
                name,
            ) is not None

    def create_certification(
        self,
        user_id: str,
        certification: Certification,
    ) -> Certification:
        """Create and store a certification for the given user."""
        with self._lock:
            user_certifications = certifications_db.setdefault(user_id, [])
            user_certifications.append(certification)

        return certification

    def get_certifications(self, user_id: str) -> list[Certification]:
        """Return all certifications for the given user."""
        with self._lock:
            return list(certifications_db.get(user_id, []))

    def get_certification(self, user_id: str, name: str) -> Certification | None:
        """Return one certification by name for the given user."""
        with self._lock:
            return self._find_certification(user_id, name)

    def update_certification(
        self,
        user_id: str,
        name: str,
        certification: Certification,
    ) -> Certification | None:
        """Replace an existing certification with a new version."""
        with self._lock:
            user_certifications = certifications_db.get(user_id)
            if user_certifications is None:
                return None

            index = self._find_certification_index(user_certifications, name)
            if index is None:
                return None

            user_certifications[index] = certification

        return certification

    def delete_certification(self, user_id: str, name: str) -> Certification | None:
        """Delete and return a certification by name."""
        with self._lock:
            user_certifications = certifications_db.get(user_id)
            if user_certifications is None:
                return None

            index = self._find_certification_index(user_certifications, name)
            if index is None:
                return None

            return user_certifications.pop(index)

    def _find_certification(self, user_id: str, name: str) -> Certification | None:
        """Locate a certification in the user's list by name."""
        user_certifications = certifications_db.get(user_id, [])
        index = self._find_certification_index(user_certifications, name)
        if index is None:
            return None
        return user_certifications[index]

    @staticmethod
    def _find_certification_index(
        user_certifications: list[Certification],
        name: str,
    ) -> int | None:
        """Return the list index for a certification name, if it exists."""
        normalized_name = name.lower()
        for index, certification in enumerate(user_certifications):
            if certification.name.lower() == normalized_name:
                return index
        return None
