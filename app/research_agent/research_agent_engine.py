"""Research Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.research_agent.schemas import ResearchRecord

# In-memory research store keyed by user_id, then research_id.
# Example:
# {
#     "billy": {
#         "res_001": {
#             "research_id": "res_001",
#             "research_topic": "AI Safety Trends",
#             "description": "Survey recent developments in AI safety research",
#             "sources": ["https://example.com/paper-a", "https://example.com/report-b"],
#             "findings": ["Increased focus on alignment", "Growing regulatory interest"],
#             "reliability_score": 85,
#             "status": "in_progress",
#             "progress_percentage": 60,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T10:30:00",
#         }
#     }
# }
research_agent_db: dict[str, dict[str, ResearchRecord]] = {}


def normalize_research_id(research_id: str) -> str:
    """Normalize a research ID for case-insensitive, whitespace-tolerant lookups."""
    return research_id.strip().lower()


class ResearchAgentEngine:
    """Manage user research records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def research_id_exists(self, user_id: str, research_id: str) -> bool:
        """Return True if a record for this research ID already exists."""
        with self._lock:
            user_records = research_agent_db.get(user_id, {})
            return normalize_research_id(research_id) in user_records

    def create_record(self, user_id: str, record: ResearchRecord) -> ResearchRecord:
        """Create and store a research record for the given user."""
        with self._lock:
            user_records = research_agent_db.setdefault(user_id, {})
            user_records[normalize_research_id(record.research_id)] = record

        return record

    def get_records(self, user_id: str) -> list[ResearchRecord]:
        """Return all research records for the given user."""
        with self._lock:
            user_records = research_agent_db.get(user_id, {})
            return list(user_records.values())

    def get_record(self, user_id: str, research_id: str) -> ResearchRecord | None:
        """Return one research record by ID for the given user."""
        with self._lock:
            user_records = research_agent_db.get(user_id, {})
            return user_records.get(normalize_research_id(research_id))

    def update_record(
        self,
        user_id: str,
        research_id: str,
        record: ResearchRecord,
    ) -> ResearchRecord | None:
        """Replace an existing research record with a new version."""
        with self._lock:
            user_records = research_agent_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_research_id(research_id)
            if normalized_id not in user_records:
                return None

            new_normalized_id = normalize_research_id(record.research_id)
            if new_normalized_id != normalized_id:
                del user_records[normalized_id]

            user_records[new_normalized_id] = record

        return record

    def delete_record(
        self,
        user_id: str,
        research_id: str,
    ) -> ResearchRecord | None:
        """Delete and return a research record by ID."""
        with self._lock:
            user_records = research_agent_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_research_id(research_id)
            return user_records.pop(normalized_id, None)
