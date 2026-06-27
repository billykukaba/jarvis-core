"""Autonomous Research Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.autonomous_research_engine.schemas import AutonomousResearchRecord

# In-memory autonomous research store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "research_id": "research_001",
#             "research_goal": "Analyze emerging AI regulation trends",
#             "research_topic": "AI policy",
#             "research_plan": "Scan news, browse official sources, summarize findings",
#             "used_agents": [
#                 "browser_agent",
#                 "news_monitoring_agent",
#                 "website_automation_agent",
#             ],
#             "visited_sources": [
#                 "https://example.com/ai-policy",
#                 "https://news.example.com/ai-regulation",
#             ],
#             "research_summary": "Global AI regulation is accelerating across major regions.",
#             "final_conclusion": "Compliance frameworks are becoming mandatory within 24 months.",
#             "confidence_score": 91,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T21:00:00",
#             "updated_at": "2026-06-04T21:30:00",
#         }
#     ]
# }
autonomous_research_engine_db: dict[str, list[AutonomousResearchRecord]] = {}


def normalize_research_id(research_id: str) -> str:
    """Normalize a research ID for case-insensitive, whitespace-tolerant lookups."""
    return research_id.strip().lower()


class AutonomousResearchEngine:
    """Manage user autonomous research records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def research_id_exists(self, user_id: str, research_id: str) -> bool:
        """Return True if a record for this research ID already exists."""
        with self._lock:
            return self._find_record_index(
                autonomous_research_engine_db.get(user_id, []),
                research_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: AutonomousResearchRecord,
    ) -> AutonomousResearchRecord:
        """Create and store an autonomous research record for the given user."""
        with self._lock:
            user_records = autonomous_research_engine_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[AutonomousResearchRecord]:
        """Return all autonomous research records for the given user."""
        with self._lock:
            return list(autonomous_research_engine_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        research_id: str,
    ) -> AutonomousResearchRecord | None:
        """Return one autonomous research record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, research_id)

    def update_record(
        self,
        user_id: str,
        research_id: str,
        record: AutonomousResearchRecord,
    ) -> AutonomousResearchRecord | None:
        """Replace an existing autonomous research record with a new version."""
        with self._lock:
            user_records = autonomous_research_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, research_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        research_id: str,
    ) -> AutonomousResearchRecord | None:
        """Delete and return an autonomous research record by ID."""
        with self._lock:
            user_records = autonomous_research_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, research_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        research_id: str,
    ) -> AutonomousResearchRecord | None:
        """Locate an autonomous research record in the user's list by ID."""
        user_records = autonomous_research_engine_db.get(user_id, [])
        index = self._find_record_index(user_records, research_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[AutonomousResearchRecord],
        research_id: str,
    ) -> int | None:
        """Return the list index for a research ID, if it exists."""
        normalized_id = normalize_research_id(research_id)
        for index, record in enumerate(user_records):
            if normalize_research_id(record.research_id) == normalized_id:
                return index
        return None
