"""Spreadsheet Reader Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.spreadsheet_reader_agent.schemas import SpreadsheetReaderRecord

# In-memory spreadsheet reader store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "spreadsheet_id": "sheet_001",
#             "spreadsheet_file": "sales_report_2025.xlsx",
#             "document_title": "Sales Report 2025",
#             "sheet_count": 3,
#             "detected_sheets": ["Summary", "Q1 Sales", "Q2 Sales"],
#             "extracted_data": "Region,Revenue,Units\nNorth,125000,420\nSouth,98000,310",
#             "summary": "Quarterly sales data with regional breakdown.",
#             "language": "en",
#             "confidence_score": 93,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T15:00:00",
#             "updated_at": "2026-06-04T15:06:00",
#         }
#     ]
# }
spreadsheet_reader_db: dict[str, list[SpreadsheetReaderRecord]] = {}


def normalize_spreadsheet_id(spreadsheet_id: str) -> str:
    """Normalize a spreadsheet ID for case-insensitive, whitespace-tolerant lookups."""
    return spreadsheet_id.strip().lower()


class SpreadsheetReaderAgentEngine:
    """Manage user spreadsheet reader records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def spreadsheet_id_exists(self, user_id: str, spreadsheet_id: str) -> bool:
        """Return True if a record for this spreadsheet ID already exists."""
        with self._lock:
            return self._find_record_index(
                spreadsheet_reader_db.get(user_id, []),
                spreadsheet_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: SpreadsheetReaderRecord,
    ) -> SpreadsheetReaderRecord:
        """Create and store a spreadsheet reader record for the given user."""
        with self._lock:
            user_records = spreadsheet_reader_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[SpreadsheetReaderRecord]:
        """Return all spreadsheet reader records for the given user."""
        with self._lock:
            return list(spreadsheet_reader_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        spreadsheet_id: str,
    ) -> SpreadsheetReaderRecord | None:
        """Return one spreadsheet reader record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, spreadsheet_id)

    def update_record(
        self,
        user_id: str,
        spreadsheet_id: str,
        record: SpreadsheetReaderRecord,
    ) -> SpreadsheetReaderRecord | None:
        """Replace an existing spreadsheet reader record with a new version."""
        with self._lock:
            user_records = spreadsheet_reader_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, spreadsheet_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        spreadsheet_id: str,
    ) -> SpreadsheetReaderRecord | None:
        """Delete and return a spreadsheet reader record by ID."""
        with self._lock:
            user_records = spreadsheet_reader_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, spreadsheet_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        spreadsheet_id: str,
    ) -> SpreadsheetReaderRecord | None:
        """Locate a spreadsheet reader record in the user's list by ID."""
        user_records = spreadsheet_reader_db.get(user_id, [])
        index = self._find_record_index(user_records, spreadsheet_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[SpreadsheetReaderRecord],
        spreadsheet_id: str,
    ) -> int | None:
        """Return the list index for a spreadsheet ID, if it exists."""
        normalized_id = normalize_spreadsheet_id(spreadsheet_id)
        for index, record in enumerate(user_records):
            if normalize_spreadsheet_id(record.spreadsheet_id) == normalized_id:
                return index
        return None
