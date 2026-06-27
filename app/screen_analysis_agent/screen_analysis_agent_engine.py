"""Screen Analysis Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.screen_analysis_agent.schemas import ScreenAnalysisRecord

# In-memory screen analysis store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "screen_id": "screen_001",
#             "screenshot_file": "desktop_capture.png",
#             "detected_application": "Visual Studio Code",
#             "screen_summary": "Developer workspace with code editor and terminal open.",
#             "detected_elements": ["editor", "sidebar", "terminal", "status_bar"],
#             "confidence_score": 92,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T09:02:00",
#         }
#     ]
# }
screen_analysis_storage: dict[str, list[ScreenAnalysisRecord]] = {}


def normalize_screen_id(screen_id: str) -> str:
    """Normalize a screen ID for case-insensitive, whitespace-tolerant lookups."""
    return screen_id.strip().lower()


class ScreenAnalysisAgentEngine:
    """Manage user screen analysis records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def screen_id_exists(self, user_id: str, screen_id: str) -> bool:
        """Return True if a record for this screen ID already exists."""
        with self._lock:
            return self._find_record_index(
                screen_analysis_storage.get(user_id, []),
                screen_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: ScreenAnalysisRecord,
    ) -> ScreenAnalysisRecord:
        """Create and store a screen analysis record for the given user."""
        with self._lock:
            user_records = screen_analysis_storage.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ScreenAnalysisRecord]:
        """Return all screen analysis records for the given user."""
        with self._lock:
            return list(screen_analysis_storage.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        screen_id: str,
    ) -> ScreenAnalysisRecord | None:
        """Return one screen analysis record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, screen_id)

    def update_record(
        self,
        user_id: str,
        screen_id: str,
        record: ScreenAnalysisRecord,
    ) -> ScreenAnalysisRecord | None:
        """Replace an existing screen analysis record with a new version."""
        with self._lock:
            user_records = screen_analysis_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, screen_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        screen_id: str,
    ) -> ScreenAnalysisRecord | None:
        """Delete and return a screen analysis record by ID."""
        with self._lock:
            user_records = screen_analysis_storage.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, screen_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        screen_id: str,
    ) -> ScreenAnalysisRecord | None:
        """Locate a screen analysis record in the user's list by ID."""
        user_records = screen_analysis_storage.get(user_id, [])
        index = self._find_record_index(user_records, screen_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ScreenAnalysisRecord],
        screen_id: str,
    ) -> int | None:
        """Return the list index for a screen ID, if it exists."""
        normalized_id = normalize_screen_id(screen_id)
        for index, record in enumerate(user_records):
            if normalize_screen_id(record.screen_id) == normalized_id:
                return index
        return None
