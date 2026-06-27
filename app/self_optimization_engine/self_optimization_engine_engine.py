"""Self Optimization Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.self_optimization_engine.schemas import SelfOptimizationRecord

# In-memory self optimization store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "optimization_id": "opt_001",
#             "target_component": "memory_service",
#             "optimization_type": "cache_tuning",
#             "optimization_strategy": "Increase cache TTL and enable lazy eviction",
#             "before_performance_score": 68,
#             "after_performance_score": 89,
#             "optimization_result": "Memory retrieval latency reduced by 35%",
#             "confidence_score": 92,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-05T01:00:00",
#             "updated_at": "2026-06-05T01:20:00",
#         }
#     ]
# }
self_optimization_engine_db: dict[str, list[SelfOptimizationRecord]] = {}


def normalize_optimization_id(optimization_id: str) -> str:
    """Normalize an optimization ID for case-insensitive, whitespace-tolerant lookups."""
    return optimization_id.strip().lower()


class SelfOptimizationEngine:
    """Manage user self optimization records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def optimization_id_exists(self, user_id: str, optimization_id: str) -> bool:
        """Return True if a record for this optimization ID already exists."""
        with self._lock:
            return self._find_record_index(
                self_optimization_engine_db.get(user_id, []),
                optimization_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: SelfOptimizationRecord,
    ) -> SelfOptimizationRecord:
        """Create and store a self optimization record for the given user."""
        with self._lock:
            user_records = self_optimization_engine_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[SelfOptimizationRecord]:
        """Return all self optimization records for the given user."""
        with self._lock:
            return list(self_optimization_engine_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        optimization_id: str,
    ) -> SelfOptimizationRecord | None:
        """Return one self optimization record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, optimization_id)

    def update_record(
        self,
        user_id: str,
        optimization_id: str,
        record: SelfOptimizationRecord,
    ) -> SelfOptimizationRecord | None:
        """Replace an existing self optimization record with a new version."""
        with self._lock:
            user_records = self_optimization_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, optimization_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        optimization_id: str,
    ) -> SelfOptimizationRecord | None:
        """Delete and return a self optimization record by ID."""
        with self._lock:
            user_records = self_optimization_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, optimization_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        optimization_id: str,
    ) -> SelfOptimizationRecord | None:
        """Locate a self optimization record in the user's list by ID."""
        user_records = self_optimization_engine_db.get(user_id, [])
        index = self._find_record_index(user_records, optimization_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[SelfOptimizationRecord],
        optimization_id: str,
    ) -> int | None:
        """Return the list index for an optimization ID, if it exists."""
        normalized_id = normalize_optimization_id(optimization_id)
        for index, record in enumerate(user_records):
            if normalize_optimization_id(record.optimization_id) == normalized_id:
                return index
        return None
