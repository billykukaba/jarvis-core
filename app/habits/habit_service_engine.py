"""Habit Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.habits.schemas import Habit

# In-memory habit store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "name": "Learn English",
#             "frequency": "daily",
#             "streak": 5,
#             "completed_today": False,
#         }
#     ]
# }
habits_db: dict[str, list[Habit]] = {}


class HabitServiceEngine:
    """Manage user habits stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def create_habit(self, user_id: str, habit: Habit) -> Habit:
        """Create and store a habit for the given user."""
        with self._lock:
            user_habits = habits_db.setdefault(user_id, [])
            user_habits.append(habit)

        return habit

    def get_habits(self, user_id: str) -> list[Habit]:
        """Return all habits for the given user."""
        with self._lock:
            return list(habits_db.get(user_id, []))

    def get_habit(self, user_id: str, name: str) -> Habit | None:
        """Return one habit by name for the given user."""
        with self._lock:
            return self._find_habit(user_id, name)

    def update_habit(self, user_id: str, name: str, habit: Habit) -> Habit | None:
        """Replace an existing habit with a new version."""
        with self._lock:
            user_habits = habits_db.get(user_id)
            if user_habits is None:
                return None

            index = self._find_habit_index(user_habits, name)
            if index is None:
                return None

            user_habits[index] = habit

        return habit

    def delete_habit(self, user_id: str, name: str) -> Habit | None:
        """Delete and return a habit by name."""
        with self._lock:
            user_habits = habits_db.get(user_id)
            if user_habits is None:
                return None

            index = self._find_habit_index(user_habits, name)
            if index is None:
                return None

            return user_habits.pop(index)

    def _find_habit(self, user_id: str, name: str) -> Habit | None:
        """Locate a habit in the user's list by name."""
        user_habits = habits_db.get(user_id, [])
        index = self._find_habit_index(user_habits, name)
        if index is None:
            return None
        return user_habits[index]

    @staticmethod
    def _find_habit_index(user_habits: list[Habit], name: str) -> int | None:
        """Return the list index for a habit name, if it exists."""
        normalized_name = name.lower()
        for index, habit in enumerate(user_habits):
            if habit.name.lower() == normalized_name:
                return index
        return None
