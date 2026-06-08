"""Skills Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.skills.schemas import Skill

# In-memory skills store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "skill": "Python",
#             "level": "Advanced",
#         }
#     ]
# }
skills_db: dict[str, list[Skill]] = {}


class SkillServiceEngine:
    """Manage user skill records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def skill_exists(self, user_id: str, skill: str) -> bool:
        """Return True if a record for this skill already exists."""
        with self._lock:
            return self._find_skill_index(
                skills_db.get(user_id, []),
                skill,
            ) is not None

    def create_skill(self, user_id: str, skill: Skill) -> Skill:
        """Create and store a skill record for the given user."""
        with self._lock:
            user_skills = skills_db.setdefault(user_id, [])
            user_skills.append(skill)

        return skill

    def get_skills(self, user_id: str) -> list[Skill]:
        """Return all skill records for the given user."""
        with self._lock:
            return list(skills_db.get(user_id, []))

    def get_skill(self, user_id: str, skill: str) -> Skill | None:
        """Return one skill record by skill name for the given user."""
        with self._lock:
            return self._find_skill(user_id, skill)

    def update_skill(
        self,
        user_id: str,
        skill: str,
        updated: Skill,
    ) -> Skill | None:
        """Replace an existing skill record with a new version."""
        with self._lock:
            user_skills = skills_db.get(user_id)
            if user_skills is None:
                return None

            index = self._find_skill_index(user_skills, skill)
            if index is None:
                return None

            user_skills[index] = updated

        return updated

    def delete_skill(self, user_id: str, skill: str) -> Skill | None:
        """Delete and return a skill record by skill name."""
        with self._lock:
            user_skills = skills_db.get(user_id)
            if user_skills is None:
                return None

            index = self._find_skill_index(user_skills, skill)
            if index is None:
                return None

            return user_skills.pop(index)

    def _find_skill(self, user_id: str, skill: str) -> Skill | None:
        """Locate a skill record in the user's list by skill name."""
        user_skills = skills_db.get(user_id, [])
        index = self._find_skill_index(user_skills, skill)
        if index is None:
            return None
        return user_skills[index]

    @staticmethod
    def _find_skill_index(
        user_skills: list[Skill],
        skill: str,
    ) -> int | None:
        """Return the list index for a skill name, if it exists."""
        normalized_skill = skill.lower()
        for index, record in enumerate(user_skills):
            if record.skill.lower() == normalized_skill:
                return index
        return None
