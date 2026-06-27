"""Website Automation Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.website_automation_agent.schemas import WebsiteAutomationRecord

# In-memory website automation store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "automation_id": "auto_001",
#             "website_url": "https://example.com/login",
#             "automation_name": "Daily Login Flow",
#             "automation_type": "form_submission",
#             "trigger_action": "scheduled_daily",
#             "execution_steps": [
#                 "navigate to login page",
#                 "fill username field",
#                 "fill password field",
#                 "click submit button",
#             ],
#             "execution_result": "Login completed successfully",
#             "execution_status": "completed",
#             "success_rate": 98,
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T20:00:00",
#             "updated_at": "2026-06-04T20:05:00",
#         }
#     ]
# }
website_automation_db: dict[str, list[WebsiteAutomationRecord]] = {}


def normalize_automation_id(automation_id: str) -> str:
    """Normalize an automation ID for case-insensitive, whitespace-tolerant lookups."""
    return automation_id.strip().lower()


class WebsiteAutomationAgentEngine:
    """Manage user website automation records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def automation_id_exists(self, user_id: str, automation_id: str) -> bool:
        """Return True if a record for this automation ID already exists."""
        with self._lock:
            return self._find_record_index(
                website_automation_db.get(user_id, []),
                automation_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: WebsiteAutomationRecord,
    ) -> WebsiteAutomationRecord:
        """Create and store a website automation record for the given user."""
        with self._lock:
            user_records = website_automation_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[WebsiteAutomationRecord]:
        """Return all website automation records for the given user."""
        with self._lock:
            return list(website_automation_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        automation_id: str,
    ) -> WebsiteAutomationRecord | None:
        """Return one website automation record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, automation_id)

    def update_record(
        self,
        user_id: str,
        automation_id: str,
        record: WebsiteAutomationRecord,
    ) -> WebsiteAutomationRecord | None:
        """Replace an existing website automation record with a new version."""
        with self._lock:
            user_records = website_automation_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, automation_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        automation_id: str,
    ) -> WebsiteAutomationRecord | None:
        """Delete and return a website automation record by ID."""
        with self._lock:
            user_records = website_automation_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, automation_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        automation_id: str,
    ) -> WebsiteAutomationRecord | None:
        """Locate a website automation record in the user's list by ID."""
        user_records = website_automation_db.get(user_id, [])
        index = self._find_record_index(user_records, automation_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[WebsiteAutomationRecord],
        automation_id: str,
    ) -> int | None:
        """Return the list index for an automation ID, if it exists."""
        normalized_id = normalize_automation_id(automation_id)
        for index, record in enumerate(user_records):
            if normalize_automation_id(record.automation_id) == normalized_id:
                return index
        return None
