from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4


@dataclass(frozen=True)
class GoalRecord:
    id: str
    title: str
    completed: bool
    created_at: datetime


class GoalEngine:
    def __init__(self) -> None:
        self._goals: dict[str, list[GoalRecord]] = {}
        self._lock = Lock()

    def create_goal(self, user_id: str, goal: str) -> GoalRecord:
        record = GoalRecord(
            id=str(uuid4()),
            title=goal.strip(),
            completed=False,
            created_at=self._now(),
        )

        with self._lock:
            self._goals.setdefault(user_id, []).append(record)

        return record

    def get_goals(self, user_id: str) -> list[GoalRecord]:
        with self._lock:
            return list(self._goals.get(user_id, []))

    def complete_goal(self, user_id: str, goal_id: str) -> GoalRecord | None:
        with self._lock:
            goals = self._goals.get(user_id, [])
            for index, goal in enumerate(goals):
                if goal.id == goal_id:
                    completed_goal = replace(goal, completed=True)
                    goals[index] = completed_goal
                    return completed_goal

        return None

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)
