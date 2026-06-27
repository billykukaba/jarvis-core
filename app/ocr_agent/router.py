"""FastAPI routes for the OCR Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.ocr_agent.ocr_agent_engine import normalize_ocr_id
from app.ocr_agent.schemas import (
    OCRRecord,
    OCRRecordResponse,
    UserOCRAgentResponse,
)
from app.services.engine_registry import ocr_agent_engine

# Router exposed to FastAPI as ocr_agent_router in main.py.
ocr_agent_router = APIRouter(tags=["OCR Agent"])


def parse_path_ocr_id(ocr_id: str) -> str:
    """Decode URL path OCR IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(ocr_id.replace("+", " "))


@ocr_agent_router.post(
    "/ocr_agent/{user_id}",
    response_model=OCRRecordResponse,
    summary="Create OCR record",
    description="Create a new OCR record for the specified user.",
)
async def create_ocr_record(
    user_id: str,
    request: OCRRecord,
) -> OCRRecordResponse:
    """Create and return an OCR record."""
    if ocr_agent_engine.ocr_id_exists(user_id, request.ocr_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OCR record already exists",
        )

    record = ocr_agent_engine.create_record(user_id, request)
    return OCRRecordResponse.from_record(record)


@ocr_agent_router.get(
    "/ocr_agent/{user_id}",
    response_model=UserOCRAgentResponse,
    summary="Get all OCR records",
    description="Return all OCR records saved by the specified user.",
)
async def get_ocr_records(user_id: str) -> UserOCRAgentResponse:
    """Return all OCR records for a user."""
    records = ocr_agent_engine.get_records(user_id)
    return UserOCRAgentResponse(
        user_id=user_id,
        ocr_records=[
            OCRRecordResponse.from_record(record) for record in records
        ],
    )


@ocr_agent_router.get(
    "/ocr_agent/{user_id}/{ocr_id}",
    response_model=OCRRecordResponse,
    summary="Get one OCR record",
    description="Return one OCR record identified by OCR ID.",
)
async def get_ocr_record(
    user_id: str,
    ocr_id: str,
) -> OCRRecordResponse:
    """Return a single OCR record by ID."""
    decoded_id = parse_path_ocr_id(ocr_id)
    record = ocr_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OCR record not found",
        )

    return OCRRecordResponse.from_record(record)


@ocr_agent_router.put(
    "/ocr_agent/{user_id}/{ocr_id}",
    response_model=OCRRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update OCR record",
    description="Replace an existing OCR record with updated data.",
)
async def update_ocr_record(
    user_id: str,
    ocr_id: str,
    request: OCRRecord,
) -> OCRRecordResponse:
    """Update and return an OCR record."""
    decoded_id = parse_path_ocr_id(ocr_id)

    if normalize_ocr_id(request.ocr_id) != normalize_ocr_id(decoded_id):
        if ocr_agent_engine.ocr_id_exists(user_id, request.ocr_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OCR record already exists",
            )

    record = ocr_agent_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OCR record not found",
        )

    return OCRRecordResponse.from_record(record)


@ocr_agent_router.delete(
    "/ocr_agent/{user_id}/{ocr_id}",
    response_model=OCRRecordResponse,
    summary="Delete OCR record",
    description="Delete an OCR record and return the removed record.",
)
async def delete_ocr_record(
    user_id: str,
    ocr_id: str,
) -> OCRRecordResponse:
    """Delete an OCR record and return the deleted item."""
    decoded_id = parse_path_ocr_id(ocr_id)
    record = ocr_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OCR record not found",
        )

    return OCRRecordResponse.from_record(record)
