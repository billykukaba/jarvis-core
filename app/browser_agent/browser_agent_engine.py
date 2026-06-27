"""Browser Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.browser_agent.schemas import BrowserSessionRecord

# In-memory browser agent store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "browser_session_id": "session_001",
#             "website_url": "https://docs.python.org/3/",
#             "page_title": "Python 3 Documentation",
#             "page_summary": "Official Python language reference and tutorials.",
#             "visited_pages": [
#                 "https://docs.python.org/3/",
#                 "https://docs.python.org/3/tutorial/",
#             ],
#             "search_query": "python documentation",
#             "browser_status": "active",
#             "confidence_score": 94,
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T18:00:00",
#             "updated_at": "2026-06-04T18:10:00",
#         }
#     ]
# }
browser_agent_db: dict[str, list[BrowserSessionRecord]] = {}


def normalize_browser_session_id(browser_session_id: str) -> str:
    """Normalize a browser session ID for case-insensitive, whitespace-tolerant lookups."""
    return browser_session_id.strip().lower()


class BrowserAgentEngine:
    """Manage user browser session records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def browser_session_id_exists(
        self,
        user_id: str,
        browser_session_id: str,
    ) -> bool:
        """Return True if a record for this browser session ID already exists."""
        with self._lock:
            return self._find_record_index(
                browser_agent_db.get(user_id, []),
                browser_session_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: BrowserSessionRecord,
    ) -> BrowserSessionRecord:
        """Create and store a browser session record for the given user."""
        with self._lock:
            user_records = browser_agent_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[BrowserSessionRecord]:
        """Return all browser session records for the given user."""
        with self._lock:
            return list(browser_agent_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        browser_session_id: str,
    ) -> BrowserSessionRecord | None:
        """Return one browser session record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, browser_session_id)

    def update_record(
        self,
        user_id: str,
        browser_session_id: str,
        record: BrowserSessionRecord,
    ) -> BrowserSessionRecord | None:
        """Replace an existing browser session record with a new version."""
        with self._lock:
            user_records = browser_agent_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, browser_session_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        browser_session_id: str,
    ) -> BrowserSessionRecord | None:
        """Delete and return a browser session record by ID."""
        with self._lock:
            user_records = browser_agent_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, browser_session_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        browser_session_id: str,
    ) -> BrowserSessionRecord | None:
        """Locate a browser session record in the user's list by ID."""
        user_records = browser_agent_db.get(user_id, [])
        index = self._find_record_index(user_records, browser_session_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[BrowserSessionRecord],
        browser_session_id: str,
    ) -> int | None:
        """Return the list index for a browser session ID, if it exists."""
        normalized_id = normalize_browser_session_id(browser_session_id)
        for index, record in enumerate(user_records):
            if normalize_browser_session_id(record.browser_session_id) == normalized_id:
                return index
        return None
