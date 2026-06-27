"""Skill Evolution Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.skill_evolution_engine.schemas import SkillEvolution

# In-memory skill evolution store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "evolution_id": "evo_001",
#             "skill": "Python",
#             "current_level": 3,
#             "target_level": 5,
#             "status": "in_progress",
#         }
#     ]
# }
skill_evolution_db: dict[str, list[SkillEvolution]] = {}


def normalize_evolution_id(evolution_id: str) -> str:
    """Normalize an evolution ID for case-insensitive, whitespace-tolerant lookups."""
    return evolution_id.strip().lower()


class SkillEvolutionEngine:
    """Manage user skill evolution records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def evolution_id_exists(self, user_id: str, evolution_id: str) -> bool:
        """Return True if a record for this evolution ID already exists."""
        with self._lock:
            return self._find_record_index(
                skill_evolution_db.get(user_id, []),
                evolution_id,
            ) is not None

    def create_record(self, user_id: str, record: SkillEvolution) -> SkillEvolution:
        """Create and store a skill evolution record for the given user."""
        with self._lock:
            user_records = skill_evolution_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[SkillEvolution]:
        """Return all skill evolution records for the given user."""
        with self._lock:
            return list(skill_evolution_db.get(user_id, []))

    def get_record(self, user_id: str, evolution_id: str) -> SkillEvolution | None:
        """Return one skill evolution record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, evolution_id)

    def update_record(
        self,
        user_id: str,
        evolution_id: str,
        record: SkillEvolution,
    ) -> SkillEvolution | None:
        """Replace an existing skill evolution record with a new version."""
        with self._lock:
            user_records = skill_evolution_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, evolution_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        evolution_id: str,
    ) -> SkillEvolution | None:
        """Delete and return a skill evolution record by ID."""
        with self._lock:
            user_records = skill_evolution_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, evolution_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        evolution_id: str,
    ) -> SkillEvolution | None:
        """Locate a skill evolution record in the user's list by ID."""
        user_records = skill_evolution_db.get(user_id, [])
        index = self._find_record_index(user_records, evolution_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[SkillEvolution],
        evolution_id: str,
    ) -> int | None:
        """Return the list index for an evolution ID, if it exists."""
        normalized_id = normalize_evolution_id(evolution_id)
        for index, record in enumerate(user_records):
            if normalize_evolution_id(record.evolution_id) == normalized_id:
                return index
        return None
