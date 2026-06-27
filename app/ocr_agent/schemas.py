"""Pydantic schemas for the OCR Agent."""

from pydantic import BaseModel, ConfigDict, Field


class OCRRecord(BaseModel):
    """OCR record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "ocr_id": "ocr_001",
                    "image_file": "invoice_scan.png",
                    "extracted_text": "Invoice #12345\nTotal: $250.00",
                    "language": "en",
                    "confidence_score": 91,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T09:02:00",
                }
            ]
        }
    )

    ocr_id: str = Field(
        min_length=1,
        description="Unique OCR record identifier",
        examples=["ocr_001"],
    )
    image_file: str = Field(
        min_length=1,
        description="Image file name or path",
        examples=["invoice_scan.png"],
    )
    extracted_text: str = Field(
        min_length=1,
        description="Text extracted from the image",
        examples=["Invoice #12345\nTotal: $250.00"],
    )
    language: str = Field(
        min_length=1,
        description="Detected document language",
        examples=["en"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="OCR extraction confidence score",
        examples=[91],
    )
    status: str = Field(
        min_length=1,
        description="Current OCR processing status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="OCR processing progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T09:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T09:02:00"],
    )


class OCRRecordResponse(BaseModel):
    """OCR record returned by the API."""

    ocr_id: str
    image_file: str
    extracted_text: str
    language: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(cls, record: OCRRecord) -> "OCRRecordResponse":
        """Build an API response from a stored OCR record."""
        return cls(
            ocr_id=record.ocr_id,
            image_file=record.image_file,
            extracted_text=record.extracted_text,
            language=record.language,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserOCRAgentResponse(BaseModel):
    """All OCR records for one user."""

    user_id: str
    ocr_records: list[OCRRecordResponse]
