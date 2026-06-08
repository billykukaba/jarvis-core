from __future__ import annotations

from dataclasses import dataclass, replace
from threading import Lock


@dataclass(frozen=True)
class LearningSkill:
    skill_name: str
    level: str
    progress: int


class LearningTrackerEngine:
    def __init__(self) -> None:
        self._skills: dict[str, dict[str, LearningSkill]] = {}
        self._lock = Lock()

    def add_skill(self, user_id: str, skill: LearningSkill) -> LearningSkill:
        with self._lock:
            user_skills = self._skills.setdefault(user_id, {})
            user_skills[skill.skill_name.lower()] = skill

        return skill

    def get_skills(self, user_id: str) -> list[LearningSkill]:
        with self._lock:
            return list(self._skills.get(user_id, {}).values())

    def get_skill(self, user_id: str, skill_name: str) -> LearningSkill | None:
        with self._lock:
            return self._skills.get(user_id, {}).get(skill_name.lower())

    def update_progress(
        self,
        user_id: str,
        skill_name: str,
        progress: int,
    ) -> LearningSkill | None:
        with self._lock:
            user_skills = self._skills.get(user_id)
            if user_skills is None:
                return None

            skill = user_skills.get(skill_name.lower())
            if skill is None:
                return None

            updated_skill = replace(skill, progress=progress)
            user_skills[skill_name.lower()] = updated_skill

        return updated_skill
