"""Autonomous Action Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.autonomous_action_engine.schemas import AutonomousActionRecord

# In-memory autonomous action store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "action_id": "action_001",
#             "action_goal": "Deploy updated configuration to staging",
#             "action_type": "system_deployment",
#             "target_system": "staging_environment",
#             "required_tools": ["workflow_engine", "website_automation_agent"],
#             "execution_plan": [
#                 "validate configuration",
#                 "run pre-deployment checks",
#                 "apply configuration",
#                 "verify deployment status",
#             ],
#             "execution_result": "Configuration deployed successfully",
#             "risk_level": 35,
#             "approval_required": True,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T22:00:00",
#             "updated_at": "2026-06-04T22:15:00",
#         }
#     ]
# }
autonomous_action_engine_db: dict[str, list[AutonomousActionRecord]] = {}


def normalize_action_id(action_id: str) -> str:
    """Normalize an action ID for case-insensitive, whitespace-tolerant lookups."""
    return action_id.strip().lower()


class AutonomousActionEngine:
    """Manage user autonomous action records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def action_id_exists(self, user_id: str, action_id: str) -> bool:
        """Return True if a record for this action ID already exists."""
        with self._lock:
            return self._find_record_index(
                autonomous_action_engine_db.get(user_id, []),
                action_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: AutonomousActionRecord,
    ) -> AutonomousActionRecord:
        """Create and store an autonomous action record for the given user."""
        with self._lock:
            user_records = autonomous_action_engine_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[AutonomousActionRecord]:
        """Return all autonomous action records for the given user."""
        with self._lock:
            return list(autonomous_action_engine_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        action_id: str,
    ) -> AutonomousActionRecord | None:
        """Return one autonomous action record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, action_id)

    def update_record(
        self,
        user_id: str,
        action_id: str,
        record: AutonomousActionRecord,
    ) -> AutonomousActionRecord | None:
        """Replace an existing autonomous action record with a new version."""
        with self._lock:
            user_records = autonomous_action_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, action_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        action_id: str,
    ) -> AutonomousActionRecord | None:
        """Delete and return an autonomous action record by ID."""
        with self._lock:
            user_records = autonomous_action_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, action_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        action_id: str,
    ) -> AutonomousActionRecord | None:
        """Locate an autonomous action record in the user's list by ID."""
        user_records = autonomous_action_engine_db.get(user_id, [])
        index = self._find_record_index(user_records, action_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[AutonomousActionRecord],
        action_id: str,
    ) -> int | None:
        """Return the list index for an action ID, if it exists."""
        normalized_id = normalize_action_id(action_id)
        for index, record in enumerate(user_records):
            if normalize_action_id(record.action_id) == normalized_id:
                return index
        return None
