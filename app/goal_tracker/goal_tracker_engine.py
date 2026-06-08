from __future__ import annotations

from dataclasses import dataclass, replace
from threading import Lock


@dataclass(frozen=True)
class Goal:
    title: str
    description: str
    progress: int
    completed: bool


class GoalTrackerEngine:
    def __init__(self) -> None:
        self._goals: dict[str, dict[str, Goal]] = {}
        self._lock = Lock()

    def add_goal(self, user_id: str, goal: Goal) -> Goal:
        with self._lock:
            user_goals = self._goals.setdefault(user_id, {})
            user_goals[goal.title.lower()] = goal

        return goal

    def get_goals(self, user_id: str) -> list[Goal]:
        with self._lock:
            return list(self._goals.get(user_id, {}).values())

    def get_goal(self, user_id: str, title: str) -> Goal | None:
        with self._lock:
            return self._goals.get(user_id, {}).get(title.lower())

    def update_progress(self, user_id: str, title: str, progress: int) -> Goal | None:
        with self._lock:
            user_goals = self._goals.get(user_id)
            if user_goals is None:
                return None

            goal = user_goals.get(title.lower())
            if goal is None:
                return None

            updated_goal = replace(goal, progress=progress)
            user_goals[title.lower()] = updated_goal

        return updated_goal

    def mark_completed(self, user_id: str, title: str) -> Goal | None:
        with self._lock:
            user_goals = self._goals.get(user_id)
            if user_goals is None:
                return None

            goal = user_goals.get(title.lower())
            if goal is None:
                return None

            completed_goal = replace(goal, completed=True)
            user_goals[title.lower()] = completed_goal

        return completed_goal
