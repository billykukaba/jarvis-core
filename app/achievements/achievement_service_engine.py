"""Achievement Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.achievements.schemas import Achievement

# In-memory achievement store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "title": "MIT Admission",
#             "description": "Accepted into MIT",
#             "date": "2027-08-01",
#             "level": "major",
#         }
#     ]
# }
achievements_db: dict[str, list[Achievement]] = {}


class AchievementServiceEngine:
    """Manage user achievements stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def title_exists(self, user_id: str, title: str) -> bool:
        """Return True if an achievement with this title already exists."""
        with self._lock:
            return self._find_achievement_index(
                achievements_db.get(user_id, []),
                title,
            ) is not None

    def create_achievement(self, user_id: str, achievement: Achievement) -> Achievement:
        """Create and store an achievement for the given user."""
        with self._lock:
            user_achievements = achievements_db.setdefault(user_id, [])
            user_achievements.append(achievement)

        return achievement

    def get_achievements(self, user_id: str) -> list[Achievement]:
        """Return all achievements for the given user."""
        with self._lock:
            return list(achievements_db.get(user_id, []))

    def get_achievement(self, user_id: str, title: str) -> Achievement | None:
        """Return one achievement by title for the given user."""
        with self._lock:
            return self._find_achievement(user_id, title)

    def update_achievement(
        self,
        user_id: str,
        title: str,
        achievement: Achievement,
    ) -> Achievement | None:
        """Replace an existing achievement with a new version."""
        with self._lock:
            user_achievements = achievements_db.get(user_id)
            if user_achievements is None:
                return None

            index = self._find_achievement_index(user_achievements, title)
            if index is None:
                return None

            user_achievements[index] = achievement

        return achievement

    def delete_achievement(self, user_id: str, title: str) -> Achievement | None:
        """Delete and return an achievement by title."""
        with self._lock:
            user_achievements = achievements_db.get(user_id)
            if user_achievements is None:
                return None

            index = self._find_achievement_index(user_achievements, title)
            if index is None:
                return None

            return user_achievements.pop(index)

    def _find_achievement(self, user_id: str, title: str) -> Achievement | None:
        """Locate an achievement in the user's list by title."""
        user_achievements = achievements_db.get(user_id, [])
        index = self._find_achievement_index(user_achievements, title)
        if index is None:
            return None
        return user_achievements[index]

    @staticmethod
    def _find_achievement_index(
        user_achievements: list[Achievement],
        title: str,
    ) -> int | None:
        """Return the list index for an achievement title, if it exists."""
        normalized_title = title.lower()
        for index, achievement in enumerate(user_achievements):
            if achievement.title.lower() == normalized_title:
                return index
        return None
