from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from threading import Lock


@dataclass(frozen=True)
class LearnedSkill:
    user_id: str
    learned_skill: str
    status: str = "learned"


class LearningEngine:
    def __init__(self, storage_path: Path | None = None) -> None:
        self._storage_path = storage_path or Path("data/learning.json")
        self._lock = Lock()
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_storage_file()

    def learn_skill(self, user_id: str, skill: str) -> LearnedSkill:
        normalized_skill = skill.strip()

        with self._lock:
            learning = self._read_learning()
            skills = learning.setdefault(user_id, [])
            if normalized_skill.lower() not in {item.lower() for item in skills}:
                skills.append(normalized_skill)
            self._write_learning(learning)

        return LearnedSkill(user_id=user_id, learned_skill=normalized_skill)

    def get_skills(self, user_id: str) -> list[str]:
        with self._lock:
            learning = self._read_learning()
            return list(learning.get(user_id, []))

    def _ensure_storage_file(self) -> None:
        if not self._storage_path.exists():
            self._storage_path.write_text("{}", encoding="utf-8")

    def _read_learning(self) -> dict[str, list[str]]:
        try:
            with self._storage_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            return {}

        if not isinstance(data, dict):
            return {}

        return {
            str(user_id): [str(skill) for skill in skills if skill]
            for user_id, skills in data.items()
            if isinstance(skills, list)
        }

    def _write_learning(self, learning: dict[str, list[str]]) -> None:
        temporary_path = self._storage_path.with_suffix(".tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(learning, file, indent=2)

        temporary_path.replace(self._storage_path)
