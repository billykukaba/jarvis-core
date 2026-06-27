"""FastAPI routes for the Spreadsheet Reader Agent.

Reads Excel spreadsheets, extracts worksheets, tables and structured data
for Jarvis Documentation Intelligence.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.spreadsheet_reader_agent.schemas import (
    SpreadsheetReaderRecord,
    SpreadsheetReaderRecordResponse,
    UserSpreadsheetReaderAgentResponse,
)
from app.spreadsheet_reader_agent.spreadsheet_reader_agent_engine import (
    normalize_spreadsheet_id,
)
from app.services.engine_registry import spreadsheet_reader_agent_engine

# Router exposed to FastAPI as spreadsheet_reader_agent_router in main.py.
spreadsheet_reader_agent_router = APIRouter(tags=["Spreadsheet Reader Agent"])


def parse_path_spreadsheet_id(spreadsheet_id: str) -> str:
    """Decode URL path spreadsheet IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(spreadsheet_id.replace("+", " "))


@spreadsheet_reader_agent_router.post(
    "/spreadsheet_reader_agent/{user_id}",
    response_model=SpreadsheetReaderRecordResponse,
    summary="Create spreadsheet reader record",
    description=(
        "Create a new spreadsheet reader record for the specified user. "
        "Reads Excel spreadsheets, extracts worksheets, tables and structured "
        "data for Jarvis Documentation Intelligence."
    ),
)
async def create_spreadsheet_reader_record(
    user_id: str,
    request: SpreadsheetReaderRecord,
) -> SpreadsheetReaderRecordResponse:
    """Create and return a spreadsheet reader record."""
    if spreadsheet_reader_agent_engine.spreadsheet_id_exists(
        user_id,
        request.spreadsheet_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spreadsheet reader record already exists",
        )

    record = spreadsheet_reader_agent_engine.create_record(user_id, request)
    return SpreadsheetReaderRecordResponse.from_record(record)


@spreadsheet_reader_agent_router.get(
    "/spreadsheet_reader_agent/{user_id}",
    response_model=UserSpreadsheetReaderAgentResponse,
    summary="Get all spreadsheet reader records",
    description=(
        "Return all spreadsheet reader records saved by the specified user. "
        "Reads Excel spreadsheets, extracts worksheets, tables and structured "
        "data for Jarvis Documentation Intelligence."
    ),
)
async def get_spreadsheet_reader_records(
    user_id: str,
) -> UserSpreadsheetReaderAgentResponse:
    """Return all spreadsheet reader records for a user."""
    records = spreadsheet_reader_agent_engine.get_records(user_id)
    return UserSpreadsheetReaderAgentResponse(
        user_id=user_id,
        spreadsheet_reader_records=[
            SpreadsheetReaderRecordResponse.from_record(record)
            for record in records
        ],
    )


@spreadsheet_reader_agent_router.get(
    "/spreadsheet_reader_agent/{user_id}/{spreadsheet_id}",
    response_model=SpreadsheetReaderRecordResponse,
    summary="Get one spreadsheet reader record",
    description="Return one spreadsheet reader record identified by spreadsheet ID.",
)
async def get_spreadsheet_reader_record(
    user_id: str,
    spreadsheet_id: str,
) -> SpreadsheetReaderRecordResponse:
    """Return a single spreadsheet reader record by ID."""
    decoded_id = parse_path_spreadsheet_id(spreadsheet_id)
    record = spreadsheet_reader_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spreadsheet reader record not found",
        )

    return SpreadsheetReaderRecordResponse.from_record(record)


@spreadsheet_reader_agent_router.put(
    "/spreadsheet_reader_agent/{user_id}/{spreadsheet_id}",
    response_model=SpreadsheetReaderRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update spreadsheet reader record",
    description="Replace an existing spreadsheet reader record with updated data.",
)
async def update_spreadsheet_reader_record(
    user_id: str,
    spreadsheet_id: str,
    request: SpreadsheetReaderRecord,
) -> SpreadsheetReaderRecordResponse:
    """Update and return a spreadsheet reader record."""
    decoded_id = parse_path_spreadsheet_id(spreadsheet_id)

    if normalize_spreadsheet_id(request.spreadsheet_id) != normalize_spreadsheet_id(
        decoded_id,
    ):
        if spreadsheet_reader_agent_engine.spreadsheet_id_exists(
            user_id,
            request.spreadsheet_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Spreadsheet reader record already exists",
            )

    record = spreadsheet_reader_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spreadsheet reader record not found",
        )

    return SpreadsheetReaderRecordResponse.from_record(record)


@spreadsheet_reader_agent_router.delete(
    "/spreadsheet_reader_agent/{user_id}/{spreadsheet_id}",
    response_model=SpreadsheetReaderRecordResponse,
    summary="Delete spreadsheet reader record",
    description="Delete a spreadsheet reader record and return the removed record.",
)
async def delete_spreadsheet_reader_record(
    user_id: str,
    spreadsheet_id: str,
) -> SpreadsheetReaderRecordResponse:
    """Delete a spreadsheet reader record and return the deleted item."""
    decoded_id = parse_path_spreadsheet_id(spreadsheet_id)
    record = spreadsheet_reader_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spreadsheet reader record not found",
        )

    return SpreadsheetReaderRecordResponse.from_record(record)
