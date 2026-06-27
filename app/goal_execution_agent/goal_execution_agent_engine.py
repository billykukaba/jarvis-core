"""Goal Execution Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.goal_execution_agent.schemas import GoalExecutionRecord

# In-memory goal execution store keyed by user_id, then goal_id.
# Example:
# {
#     "billy": {
#         "goal_001": {
#             "goal_id": "goal_001",
#             "goal_name": "Launch MVP",
#             "goal_description": "Ship the minimum viable product to production",
#             "execution_steps": [
#                 "Finalize scope",
#                 "Implement core features",
#                 "Deploy to production",
#             ],
#             "current_step": "Implement core features",
#             "completion_percentage": 45,
#             "priority_level": 1,
#             "status": "in_progress",
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T10:30:00",
#         }
#     }
# }
goal_execution_agent_db: dict[str, dict[str, GoalExecutionRecord]] = {}


def normalize_goal_id(goal_id: str) -> str:
    """Normalize a goal ID for case-insensitive, whitespace-tolerant lookups."""
    return goal_id.strip().lower()


class GoalExecutionAgentEngine:
    """Manage user goal execution records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def goal_id_exists(self, user_id: str, goal_id: str) -> bool:
        """Return True if a record for this goal ID already exists."""
        with self._lock:
            user_records = goal_execution_agent_db.get(user_id, {})
            return normalize_goal_id(goal_id) in user_records

    def create_record(
        self,
        user_id: str,
        record: GoalExecutionRecord,
    ) -> GoalExecutionRecord:
        """Create and store a goal execution record for the given user."""
        with self._lock:
            user_records = goal_execution_agent_db.setdefault(user_id, {})
            user_records[normalize_goal_id(record.goal_id)] = record

        return record

    def get_records(self, user_id: str) -> list[GoalExecutionRecord]:
        """Return all goal execution records for the given user."""
        with self._lock:
            user_records = goal_execution_agent_db.get(user_id, {})
            return list(user_records.values())

    def get_record(self, user_id: str, goal_id: str) -> GoalExecutionRecord | None:
        """Return one goal execution record by ID for the given user."""
        with self._lock:
            user_records = goal_execution_agent_db.get(user_id, {})
            return user_records.get(normalize_goal_id(goal_id))

    def update_record(
        self,
        user_id: str,
        goal_id: str,
        record: GoalExecutionRecord,
    ) -> GoalExecutionRecord | None:
        """Replace an existing goal execution record with a new version."""
        with self._lock:
            user_records = goal_execution_agent_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_goal_id(goal_id)
            if normalized_id not in user_records:
                return None

            new_normalized_id = normalize_goal_id(record.goal_id)
            if new_normalized_id != normalized_id:
                del user_records[normalized_id]

            user_records[new_normalized_id] = record

        return record

    def delete_record(
        self,
        user_id: str,
        goal_id: str,
    ) -> GoalExecutionRecord | None:
        """Delete and return a goal execution record by ID."""
        with self._lock:
            user_records = goal_execution_agent_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_goal_id(goal_id)
            return user_records.pop(normalized_id, None)
