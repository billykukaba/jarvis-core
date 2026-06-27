"""Pydantic schemas for the Spreadsheet Reader Agent."""

from pydantic import BaseModel, ConfigDict, Field


class SpreadsheetReaderRecord(BaseModel):
    """Spreadsheet reader record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "spreadsheet_id": "sheet_001",
                    "spreadsheet_file": "sales_report_2025.xlsx",
                    "document_title": "Sales Report 2025",
                    "sheet_count": 3,
                    "detected_sheets": ["Summary", "Q1 Sales", "Q2 Sales"],
                    "extracted_data": "Region,Revenue,Units\nNorth,125000,420\nSouth,98000,310",
                    "summary": "Quarterly sales data with regional breakdown.",
                    "language": "en",
                    "confidence_score": 93,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T15:00:00",
                    "updated_at": "2026-06-04T15:06:00",
                }
            ]
        }
    )

    spreadsheet_id: str = Field(
        min_length=1,
        description="Unique spreadsheet reader record identifier",
        examples=["sheet_001"],
    )
    spreadsheet_file: str = Field(
        min_length=1,
        description="Spreadsheet file name or path",
        examples=["sales_report_2025.xlsx"],
    )
    document_title: str = Field(
        min_length=1,
        description="Title of the spreadsheet document",
        examples=["Sales Report 2025"],
    )
    sheet_count: int = Field(
        ge=0,
        description="Total number of worksheets in the spreadsheet",
        examples=[3],
    )
    detected_sheets: list[str] = Field(
        min_length=1,
        description="Worksheet names detected in the spreadsheet",
        examples=[["Summary", "Q1 Sales", "Q2 Sales"]],
    )
    extracted_data: str = Field(
        min_length=1,
        description="Structured data extracted from the spreadsheet",
        examples=["Region,Revenue,Units\nNorth,125000,420\nSouth,98000,310"],
    )
    summary: str = Field(
        min_length=1,
        description="Summary of the spreadsheet content",
        examples=["Quarterly sales data with regional breakdown."],
    )
    language: str = Field(
        min_length=1,
        description="Detected language of the spreadsheet content",
        examples=["en"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Spreadsheet reading and extraction confidence score",
        examples=[93],
    )
    status: str = Field(
        min_length=1,
        description="Current spreadsheet reading status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Spreadsheet reading progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T15:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T15:06:00"],
    )


class SpreadsheetReaderRecordResponse(BaseModel):
    """Spreadsheet reader record returned by the API."""

    spreadsheet_id: str
    spreadsheet_file: str
    document_title: str
    sheet_count: int
    detected_sheets: list[str]
    extracted_data: str
    summary: str
    language: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: SpreadsheetReaderRecord,
    ) -> "SpreadsheetReaderRecordResponse":
        """Build an API response from a stored spreadsheet reader record."""
        return cls(
            spreadsheet_id=record.spreadsheet_id,
            spreadsheet_file=record.spreadsheet_file,
            document_title=record.document_title,
            sheet_count=record.sheet_count,
            detected_sheets=record.detected_sheets,
            extracted_data=record.extracted_data,
            summary=record.summary,
            language=record.language,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserSpreadsheetReaderAgentResponse(BaseModel):
    """All spreadsheet reader records for one user."""

    user_id: str
    spreadsheet_reader_records: list[SpreadsheetReaderRecordResponse]
