"""FastAPI routes for the PDF Reader Agent.

Reads PDF files and extracts text for Jarvis Documentation Intelligence.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.pdf_reader_agent.pdf_reader_agent_engine import normalize_pdf_id
from app.pdf_reader_agent.schemas import (
    PDFReaderRecord,
    PDFReaderRecordResponse,
    UserPDFReaderAgentResponse,
)
from app.services.engine_registry import pdf_reader_agent_engine

# Router exposed to FastAPI as pdf_reader_agent_router in main.py.
pdf_reader_agent_router = APIRouter(tags=["PDF Reader Agent"])


def parse_path_pdf_id(pdf_id: str) -> str:
    """Decode URL path PDF IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(pdf_id.replace("+", " "))


@pdf_reader_agent_router.post(
    "/pdf_reader_agent/{user_id}",
    response_model=PDFReaderRecordResponse,
    summary="Create PDF reader record",
    description=(
        "Create a new PDF reader record for the specified user. "
        "Reads PDF files and extracts text for Jarvis Documentation Intelligence."
    ),
)
async def create_pdf_reader_record(
    user_id: str,
    request: PDFReaderRecord,
) -> PDFReaderRecordResponse:
    """Create and return a PDF reader record."""
    if pdf_reader_agent_engine.pdf_id_exists(user_id, request.pdf_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF reader record already exists",
        )

    record = pdf_reader_agent_engine.create_record(user_id, request)
    return PDFReaderRecordResponse.from_record(record)


@pdf_reader_agent_router.get(
    "/pdf_reader_agent/{user_id}",
    response_model=UserPDFReaderAgentResponse,
    summary="Get all PDF reader records",
    description=(
        "Return all PDF reader records saved by the specified user. "
        "Reads PDF files and extracts text for Jarvis Documentation Intelligence."
    ),
)
async def get_pdf_reader_records(
    user_id: str,
) -> UserPDFReaderAgentResponse:
    """Return all PDF reader records for a user."""
    records = pdf_reader_agent_engine.get_records(user_id)
    return UserPDFReaderAgentResponse(
        user_id=user_id,
        pdf_reader_records=[
            PDFReaderRecordResponse.from_record(record) for record in records
        ],
    )


@pdf_reader_agent_router.get(
    "/pdf_reader_agent/{user_id}/{pdf_id}",
    response_model=PDFReaderRecordResponse,
    summary="Get one PDF reader record",
    description="Return one PDF reader record identified by PDF ID.",
)
async def get_pdf_reader_record(
    user_id: str,
    pdf_id: str,
) -> PDFReaderRecordResponse:
    """Return a single PDF reader record by ID."""
    decoded_id = parse_path_pdf_id(pdf_id)
    record = pdf_reader_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF reader record not found",
        )

    return PDFReaderRecordResponse.from_record(record)


@pdf_reader_agent_router.put(
    "/pdf_reader_agent/{user_id}/{pdf_id}",
    response_model=PDFReaderRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update PDF reader record",
    description="Replace an existing PDF reader record with updated data.",
)
async def update_pdf_reader_record(
    user_id: str,
    pdf_id: str,
    request: PDFReaderRecord,
) -> PDFReaderRecordResponse:
    """Update and return a PDF reader record."""
    decoded_id = parse_path_pdf_id(pdf_id)

    if normalize_pdf_id(request.pdf_id) != normalize_pdf_id(decoded_id):
        if pdf_reader_agent_engine.pdf_id_exists(user_id, request.pdf_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PDF reader record already exists",
            )

    record = pdf_reader_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF reader record not found",
        )

    return PDFReaderRecordResponse.from_record(record)


@pdf_reader_agent_router.delete(
    "/pdf_reader_agent/{user_id}/{pdf_id}",
    response_model=PDFReaderRecordResponse,
    summary="Delete PDF reader record",
    description="Delete a PDF reader record and return the removed record.",
)
async def delete_pdf_reader_record(
    user_id: str,
    pdf_id: str,
) -> PDFReaderRecordResponse:
    """Delete a PDF reader record and return the deleted item."""
    decoded_id = parse_path_pdf_id(pdf_id)
    record = pdf_reader_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF reader record not found",
        )

    return PDFReaderRecordResponse.from_record(record)
