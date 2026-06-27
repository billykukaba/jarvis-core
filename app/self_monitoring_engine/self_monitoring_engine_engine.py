"""Self Monitoring Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.self_monitoring_engine.schemas import SelfMonitoringRecord

# In-memory self monitoring store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "monitoring_id": "monitor_001",
#             "system_component": "memory_service",
#             "health_status": "degraded",
#             "detected_issue": "Elevated memory usage detected",
#             "performance_score": 72,
#             "risk_level": 45,
#             "recommended_action": "Restart memory cache and review retention policy",
#             "status": "active",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T23:00:00",
#             "updated_at": "2026-06-04T23:10:00",
#         }
#     ]
# }
self_monitoring_engine_db: dict[str, list[SelfMonitoringRecord]] = {}


def normalize_monitoring_id(monitoring_id: str) -> str:
    """Normalize a monitoring ID for case-insensitive, whitespace-tolerant lookups."""
    return monitoring_id.strip().lower()


class SelfMonitoringEngine:
    """Manage user self monitoring records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def monitoring_id_exists(self, user_id: str, monitoring_id: str) -> bool:
        """Return True if a record for this monitoring ID already exists."""
        with self._lock:
            return self._find_record_index(
                self_monitoring_engine_db.get(user_id, []),
                monitoring_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: SelfMonitoringRecord,
    ) -> SelfMonitoringRecord:
        """Create and store a self monitoring record for the given user."""
        with self._lock:
            user_records = self_monitoring_engine_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[SelfMonitoringRecord]:
        """Return all self monitoring records for the given user."""
        with self._lock:
            return list(self_monitoring_engine_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        monitoring_id: str,
    ) -> SelfMonitoringRecord | None:
        """Return one self monitoring record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, monitoring_id)

    def update_record(
        self,
        user_id: str,
        monitoring_id: str,
        record: SelfMonitoringRecord,
    ) -> SelfMonitoringRecord | None:
        """Replace an existing self monitoring record with a new version."""
        with self._lock:
            user_records = self_monitoring_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, monitoring_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        monitoring_id: str,
    ) -> SelfMonitoringRecord | None:
        """Delete and return a self monitoring record by ID."""
        with self._lock:
            user_records = self_monitoring_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, monitoring_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        monitoring_id: str,
    ) -> SelfMonitoringRecord | None:
        """Locate a self monitoring record in the user's list by ID."""
        user_records = self_monitoring_engine_db.get(user_id, [])
        index = self._find_record_index(user_records, monitoring_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[SelfMonitoringRecord],
        monitoring_id: str,
    ) -> int | None:
        """Return the list index for a monitoring ID, if it exists."""
        normalized_id = normalize_monitoring_id(monitoring_id)
        for index, record in enumerate(user_records):
            if normalize_monitoring_id(record.monitoring_id) == normalized_id:
                return index
        return None
