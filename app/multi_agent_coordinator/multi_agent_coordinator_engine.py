"""Multi-Agent Coordinator with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.multi_agent_coordinator.schemas import MultiAgentCoordinatorRecord

# In-memory coordinator store keyed by user_id, then coordinator_id.
# Example:
# {
#     "billy": {
#         "coord_001": {
#             "coordinator_id": "coord_001",
#             "coordinator_name": "Research Squad",
#             "agents": ["analyst", "writer", "reviewer"],
#             "leader_agent": "analyst",
#             "current_task": "Draft quarterly report",
#             "priority_level": 2,
#             "status": "active",
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T10:30:00",
#         }
#     }
# }
multi_agent_coordinator_db: dict[str, dict[str, MultiAgentCoordinatorRecord]] = {}


def normalize_coordinator_id(coordinator_id: str) -> str:
    """Normalize a coordinator ID for case-insensitive, whitespace-tolerant lookups."""
    return coordinator_id.strip().lower()


class MultiAgentCoordinatorEngine:
    """Manage user multi-agent coordinator records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def coordinator_id_exists(self, user_id: str, coordinator_id: str) -> bool:
        """Return True if a record for this coordinator ID already exists."""
        with self._lock:
            user_records = multi_agent_coordinator_db.get(user_id, {})
            return normalize_coordinator_id(coordinator_id) in user_records

    def create_record(
        self,
        user_id: str,
        record: MultiAgentCoordinatorRecord,
    ) -> MultiAgentCoordinatorRecord:
        """Create and store a coordinator record for the given user."""
        with self._lock:
            user_records = multi_agent_coordinator_db.setdefault(user_id, {})
            user_records[normalize_coordinator_id(record.coordinator_id)] = record

        return record

    def get_records(self, user_id: str) -> list[MultiAgentCoordinatorRecord]:
        """Return all coordinator records for the given user."""
        with self._lock:
            user_records = multi_agent_coordinator_db.get(user_id, {})
            return list(user_records.values())

    def get_record(
        self,
        user_id: str,
        coordinator_id: str,
    ) -> MultiAgentCoordinatorRecord | None:
        """Return one coordinator record by ID for the given user."""
        with self._lock:
            user_records = multi_agent_coordinator_db.get(user_id, {})
            return user_records.get(normalize_coordinator_id(coordinator_id))

    def update_record(
        self,
        user_id: str,
        coordinator_id: str,
        record: MultiAgentCoordinatorRecord,
    ) -> MultiAgentCoordinatorRecord | None:
        """Replace an existing coordinator record with a new version."""
        with self._lock:
            user_records = multi_agent_coordinator_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_coordinator_id(coordinator_id)
            if normalized_id not in user_records:
                return None

            new_normalized_id = normalize_coordinator_id(record.coordinator_id)
            if new_normalized_id != normalized_id:
                del user_records[normalized_id]

            user_records[new_normalized_id] = record

        return record

    def delete_record(
        self,
        user_id: str,
        coordinator_id: str,
    ) -> MultiAgentCoordinatorRecord | None:
        """Delete and return a coordinator record by ID."""
        with self._lock:
            user_records = multi_agent_coordinator_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_coordinator_id(coordinator_id)
            return user_records.pop(normalized_id, None)
