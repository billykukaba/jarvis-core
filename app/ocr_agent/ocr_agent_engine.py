"""OCR Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.ocr_agent.schemas import OCRRecord

# In-memory OCR store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "ocr_id": "ocr_001",
#             "image_file": "invoice_scan.png",
#             "extracted_text": "Invoice #12345\nTotal: $250.00",
#             "language": "en",
#             "confidence_score": 91,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T09:02:00",
#         }
#     ]
# }
ocr_db: dict[str, list[OCRRecord]] = {}


def normalize_ocr_id(ocr_id: str) -> str:
    """Normalize an OCR ID for case-insensitive, whitespace-tolerant lookups."""
    return ocr_id.strip().lower()


class OCRAgentEngine:
    """Manage user OCR records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def ocr_id_exists(self, user_id: str, ocr_id: str) -> bool:
        """Return True if a record for this OCR ID already exists."""
        with self._lock:
            return self._find_record_index(
                ocr_db.get(user_id, []),
                ocr_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: OCRRecord,
    ) -> OCRRecord:
        """Create and store an OCR record for the given user."""
        with self._lock:
            user_records = ocr_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[OCRRecord]:
        """Return all OCR records for the given user."""
        with self._lock:
            return list(ocr_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        ocr_id: str,
    ) -> OCRRecord | None:
        """Return one OCR record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, ocr_id)

    def update_record(
        self,
        user_id: str,
        ocr_id: str,
        record: OCRRecord,
    ) -> OCRRecord | None:
        """Replace an existing OCR record with a new version."""
        with self._lock:
            user_records = ocr_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, ocr_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        ocr_id: str,
    ) -> OCRRecord | None:
        """Delete and return an OCR record by ID."""
        with self._lock:
            user_records = ocr_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, ocr_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        ocr_id: str,
    ) -> OCRRecord | None:
        """Locate an OCR record in the user's list by ID."""
        user_records = ocr_db.get(user_id, [])
        index = self._find_record_index(user_records, ocr_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[OCRRecord],
        ocr_id: str,
    ) -> int | None:
        """Return the list index for an OCR ID, if it exists."""
        normalized_id = normalize_ocr_id(ocr_id)
        for index, record in enumerate(user_records):
            if normalize_ocr_id(record.ocr_id) == normalized_id:
                return index
        return None
