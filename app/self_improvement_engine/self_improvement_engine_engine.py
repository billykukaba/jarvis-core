"""Self Improvement Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.self_improvement_engine.schemas import SelfImprovementRecord

# In-memory self improvement store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "improvement_id": "improve_001",
#             "system_component": "response_generator",
#             "identified_problem": "Response latency increases under high load",
#             "proposed_solution": "Add response caching and async batch processing",
#             "expected_benefit": "Reduce average response time by 30%",
#             "priority_level": 85,
#             "implementation_status": "planned",
#             "confidence_score": 88,
#             "status": "active",
#             "progress_percentage": 25,
#             "created_at": "2026-06-05T00:00:00",
#             "updated_at": "2026-06-05T00:15:00",
#         }
#     ]
# }
self_improvement_engine_db: dict[str, list[SelfImprovementRecord]] = {}


def normalize_improvement_id(improvement_id: str) -> str:
    """Normalize an improvement ID for case-insensitive, whitespace-tolerant lookups."""
    return improvement_id.strip().lower()


class SelfImprovementEngine:
    """Manage user self improvement records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def improvement_id_exists(self, user_id: str, improvement_id: str) -> bool:
        """Return True if a record for this improvement ID already exists."""
        with self._lock:
            return self._find_record_index(
                self_improvement_engine_db.get(user_id, []),
                improvement_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: SelfImprovementRecord,
    ) -> SelfImprovementRecord:
        """Create and store a self improvement record for the given user."""
        with self._lock:
            user_records = self_improvement_engine_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[SelfImprovementRecord]:
        """Return all self improvement records for the given user."""
        with self._lock:
            return list(self_improvement_engine_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        improvement_id: str,
    ) -> SelfImprovementRecord | None:
        """Return one self improvement record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, improvement_id)

    def update_record(
        self,
        user_id: str,
        improvement_id: str,
        record: SelfImprovementRecord,
    ) -> SelfImprovementRecord | None:
        """Replace an existing self improvement record with a new version."""
        with self._lock:
            user_records = self_improvement_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, improvement_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        improvement_id: str,
    ) -> SelfImprovementRecord | None:
        """Delete and return a self improvement record by ID."""
        with self._lock:
            user_records = self_improvement_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, improvement_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        improvement_id: str,
    ) -> SelfImprovementRecord | None:
        """Locate a self improvement record in the user's list by ID."""
        user_records = self_improvement_engine_db.get(user_id, [])
        index = self._find_record_index(user_records, improvement_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[SelfImprovementRecord],
        improvement_id: str,
    ) -> int | None:
        """Return the list index for an improvement ID, if it exists."""
        normalized_id = normalize_improvement_id(improvement_id)
        for index, record in enumerate(user_records):
            if normalize_improvement_id(record.improvement_id) == normalized_id:
                return index
        return None
