"""Avatar Animation Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.avatar_animations.schemas import AvatarAnimationRecord

# In-memory avatar animation store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "animation": "Wave",
#             "duration": "2 seconds",
#         }
#     ]
# }
avatar_animations_db: dict[str, list[AvatarAnimationRecord]] = {}


def normalize_animation(animation: str) -> str:
    """Normalize an animation name for case-insensitive, whitespace-tolerant lookups."""
    return animation.strip().lower()


class AvatarAnimationServiceEngine:
    """Manage user avatar animation records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def animation_exists(self, user_id: str, animation: str) -> bool:
        """Return True if a record for this animation already exists."""
        with self._lock:
            return self._find_record_index(
                avatar_animations_db.get(user_id, []),
                animation,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: AvatarAnimationRecord,
    ) -> AvatarAnimationRecord:
        """Create and store an avatar animation record for the given user."""
        with self._lock:
            user_records = avatar_animations_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[AvatarAnimationRecord]:
        """Return all avatar animation records for the given user."""
        with self._lock:
            return list(avatar_animations_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        animation: str,
    ) -> AvatarAnimationRecord | None:
        """Return one avatar animation record by name for the given user."""
        with self._lock:
            return self._find_record(user_id, animation)

    def update_record(
        self,
        user_id: str,
        animation: str,
        record: AvatarAnimationRecord,
    ) -> AvatarAnimationRecord | None:
        """Replace an existing avatar animation record with a new version."""
        with self._lock:
            user_records = avatar_animations_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, animation)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        animation: str,
    ) -> AvatarAnimationRecord | None:
        """Delete and return an avatar animation record by name."""
        with self._lock:
            user_records = avatar_animations_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, animation)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        animation: str,
    ) -> AvatarAnimationRecord | None:
        """Locate an avatar animation record in the user's list by name."""
        user_records = avatar_animations_db.get(user_id, [])
        index = self._find_record_index(user_records, animation)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[AvatarAnimationRecord],
        animation: str,
    ) -> int | None:
        """Return the list index for an animation name, if it exists."""
        normalized_animation = normalize_animation(animation)
        for index, record in enumerate(user_records):
            if normalize_animation(record.animation) == normalized_animation:
                return index
        return None
