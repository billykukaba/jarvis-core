"""Goal Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.goals.schemas import Goal

# In-memory goal store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "title": "MIT Admission",
#             "description": "Get accepted into MIT",
#             "target_date": "2027-08-01",
#             "status": "in_progress",
#         }
#     ]
# }
goals_db: dict[str, list[Goal]] = {}


class GoalServiceEngine:
    """Manage user goals stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def title_exists(self, user_id: str, title: str) -> bool:
        """Return True if a goal with this title already exists."""
        with self._lock:
            return self._find_goal_index(goals_db.get(user_id, []), title) is not None

    def create_goal(self, user_id: str, goal: Goal) -> Goal:
        """Create and store a goal for the given user."""
        with self._lock:
            user_goals = goals_db.setdefault(user_id, [])
            user_goals.append(goal)

        return goal

    def get_goals(self, user_id: str) -> list[Goal]:
        """Return all goals for the given user."""
        with self._lock:
            return list(goals_db.get(user_id, []))

    def get_goal(self, user_id: str, title: str) -> Goal | None:
        """Return one goal by title for the given user."""
        with self._lock:
            return self._find_goal(user_id, title)

    def update_goal(self, user_id: str, title: str, goal: Goal) -> Goal | None:
        """Replace an existing goal with a new version."""
        with self._lock:
            user_goals = goals_db.get(user_id)
            if user_goals is None:
                return None

            index = self._find_goal_index(user_goals, title)
            if index is None:
                return None

            user_goals[index] = goal

        return goal

    def delete_goal(self, user_id: str, title: str) -> Goal | None:
        """Delete and return a goal by title."""
        with self._lock:
            user_goals = goals_db.get(user_id)
            if user_goals is None:
                return None

            index = self._find_goal_index(user_goals, title)
            if index is None:
                return None

            return user_goals.pop(index)

    def _find_goal(self, user_id: str, title: str) -> Goal | None:
        """Locate a goal in the user's list by title."""
        user_goals = goals_db.get(user_id, [])
        index = self._find_goal_index(user_goals, title)
        if index is None:
            return None
        return user_goals[index]

    @staticmethod
    def _find_goal_index(user_goals: list[Goal], title: str) -> int | None:
        """Return the list index for a goal title, if it exists."""
        normalized_title = title.lower()
        for index, goal in enumerate(user_goals):
            if goal.title.lower() == normalized_title:
                return index
        return None
