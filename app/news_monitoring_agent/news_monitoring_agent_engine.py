"""News Monitoring Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.news_monitoring_agent.schemas import NewsMonitoringRecord

# In-memory news monitoring store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "news_id": "news_001",
#             "news_title": "AI Breakthrough in Language Models",
#             "news_source": "Tech Daily",
#             "news_category": "technology",
#             "news_summary": "Researchers announce major advances in multilingual AI models.",
#             "news_url": "https://example.com/ai-breakthrough",
#             "published_date": "2026-06-04",
#             "keywords": ["AI", "language models", "research"],
#             "priority_level": 8,
#             "status": "monitored",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T19:00:00",
#             "updated_at": "2026-06-04T19:05:00",
#         }
#     ]
# }
news_monitoring_db: dict[str, list[NewsMonitoringRecord]] = {}


def normalize_news_id(news_id: str) -> str:
    """Normalize a news ID for case-insensitive, whitespace-tolerant lookups."""
    return news_id.strip().lower()


class NewsMonitoringAgentEngine:
    """Manage user news monitoring records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def news_id_exists(self, user_id: str, news_id: str) -> bool:
        """Return True if a record for this news ID already exists."""
        with self._lock:
            return self._find_record_index(
                news_monitoring_db.get(user_id, []),
                news_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: NewsMonitoringRecord,
    ) -> NewsMonitoringRecord:
        """Create and store a news monitoring record for the given user."""
        with self._lock:
            user_records = news_monitoring_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[NewsMonitoringRecord]:
        """Return all news monitoring records for the given user."""
        with self._lock:
            return list(news_monitoring_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        news_id: str,
    ) -> NewsMonitoringRecord | None:
        """Return one news monitoring record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, news_id)

    def update_record(
        self,
        user_id: str,
        news_id: str,
        record: NewsMonitoringRecord,
    ) -> NewsMonitoringRecord | None:
        """Replace an existing news monitoring record with a new version."""
        with self._lock:
            user_records = news_monitoring_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, news_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        news_id: str,
    ) -> NewsMonitoringRecord | None:
        """Delete and return a news monitoring record by ID."""
        with self._lock:
            user_records = news_monitoring_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, news_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        news_id: str,
    ) -> NewsMonitoringRecord | None:
        """Locate a news monitoring record in the user's list by ID."""
        user_records = news_monitoring_db.get(user_id, [])
        index = self._find_record_index(user_records, news_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[NewsMonitoringRecord],
        news_id: str,
    ) -> int | None:
        """Return the list index for a news ID, if it exists."""
        normalized_id = normalize_news_id(news_id)
        for index, record in enumerate(user_records):
            if normalize_news_id(record.news_id) == normalized_id:
                return index
        return None
