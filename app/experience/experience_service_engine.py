"""Experience Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.experience.schemas import Experience

# In-memory experience store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "company": "OpenAI",
#             "position": "AI Engineer",
#             "start_year": 2031,
#             "end_year": 2035,
#         }
#     ]
# }
experience_db: dict[str, list[Experience]] = {}


class ExperienceServiceEngine:
    """Manage user work experience records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def company_exists(self, user_id: str, company: str) -> bool:
        """Return True if an experience record for this company already exists."""
        with self._lock:
            return self._find_experience_index(
                experience_db.get(user_id, []),
                company,
            ) is not None

    def create_experience(self, user_id: str, experience: Experience) -> Experience:
        """Create and store an experience record for the given user."""
        with self._lock:
            user_experience = experience_db.setdefault(user_id, [])
            user_experience.append(experience)

        return experience

    def get_experience_list(self, user_id: str) -> list[Experience]:
        """Return all experience records for the given user."""
        with self._lock:
            return list(experience_db.get(user_id, []))

    def get_experience(self, user_id: str, company: str) -> Experience | None:
        """Return one experience record by company for the given user."""
        with self._lock:
            return self._find_experience(user_id, company)

    def update_experience(
        self,
        user_id: str,
        company: str,
        experience: Experience,
    ) -> Experience | None:
        """Replace an existing experience record with a new version."""
        with self._lock:
            user_experience = experience_db.get(user_id)
            if user_experience is None:
                return None

            index = self._find_experience_index(user_experience, company)
            if index is None:
                return None

            user_experience[index] = experience

        return experience

    def delete_experience(self, user_id: str, company: str) -> Experience | None:
        """Delete and return an experience record by company."""
        with self._lock:
            user_experience = experience_db.get(user_id)
            if user_experience is None:
                return None

            index = self._find_experience_index(user_experience, company)
            if index is None:
                return None

            return user_experience.pop(index)

    def _find_experience(self, user_id: str, company: str) -> Experience | None:
        """Locate an experience record in the user's list by company."""
        user_experience = experience_db.get(user_id, [])
        index = self._find_experience_index(user_experience, company)
        if index is None:
            return None
        return user_experience[index]

    @staticmethod
    def _find_experience_index(
        user_experience: list[Experience],
        company: str,
    ) -> int | None:
        """Return the list index for a company, if it exists."""
        normalized_company = company.lower()
        for index, record in enumerate(user_experience):
            if record.company.lower() == normalized_company:
                return index
        return None
