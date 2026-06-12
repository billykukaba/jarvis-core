"""FastAPI routes for the Facial Expression Service (Module 63)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.facial_expressions.facial_expression_service_engine import normalize_expression
from app.facial_expressions.schemas import (
    FacialExpressionRecord,
    FacialExpressionRecordResponse,
    UserFacialExpressionsResponse,
)
from app.services.engine_registry import facial_expression_service_engine

# Router exposed to FastAPI as facial_expressions_router in main.py.
facial_expressions_router = APIRouter(tags=["facial_expressions"])


def parse_path_expression(expression: str) -> str:
    """Decode URL path expression names so spaces work in GET, PUT, and DELETE."""
    return unquote(expression.replace("+", " "))


@facial_expressions_router.post(
    "/facial_expressions/{user_id}",
    response_model=FacialExpressionRecordResponse,
    summary="Create facial expression record",
    description="Create a new facial expression record for the specified user.",
)
async def create_facial_expression_record(
    user_id: str,
    request: FacialExpressionRecord,
) -> FacialExpressionRecordResponse:
    """Create and return a facial expression record."""
    if facial_expression_service_engine.expression_exists(
        user_id,
        request.expression,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expression already exists",
        )

    record = facial_expression_service_engine.create_record(user_id, request)
    return FacialExpressionRecordResponse.from_record(record)


@facial_expressions_router.get(
    "/facial_expressions/{user_id}",
    response_model=UserFacialExpressionsResponse,
    summary="Get all facial expression records",
    description="Return all facial expression records saved by the specified user.",
)
async def get_facial_expression_records(
    user_id: str,
) -> UserFacialExpressionsResponse:
    """Return all facial expression records for a user."""
    records = facial_expression_service_engine.get_records(user_id)
    return UserFacialExpressionsResponse(
        user_id=user_id,
        facial_expressions=[
            FacialExpressionRecordResponse.from_record(record)
            for record in records
        ],
    )


@facial_expressions_router.get(
    "/facial_expressions/{user_id}/{expression}",
    response_model=FacialExpressionRecordResponse,
    summary="Get one facial expression record",
    description="Return one facial expression record identified by expression name.",
)
async def get_facial_expression_record(
    user_id: str,
    expression: str,
) -> FacialExpressionRecordResponse:
    """Return a single facial expression record by name."""
    decoded_expression = parse_path_expression(expression)
    record = facial_expression_service_engine.get_record(
        user_id,
        decoded_expression,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expression not found",
        )

    return FacialExpressionRecordResponse.from_record(record)


@facial_expressions_router.put(
    "/facial_expressions/{user_id}/{expression}",
    response_model=FacialExpressionRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update facial expression record",
    description="Replace an existing facial expression record with updated data.",
)
async def update_facial_expression_record(
    user_id: str,
    expression: str,
    request: FacialExpressionRecord,
) -> FacialExpressionRecordResponse:
    """Update and return a facial expression record."""
    decoded_expression = parse_path_expression(expression)

    # Allow keeping the same expression while changing avatar_state.
    if normalize_expression(request.expression) != normalize_expression(
        decoded_expression
    ):
        if facial_expression_service_engine.expression_exists(
            user_id,
            request.expression,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Expression already exists",
            )

    record = facial_expression_service_engine.update_record(
        user_id,
        decoded_expression,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expression not found",
        )

    return FacialExpressionRecordResponse.from_record(record)


@facial_expressions_router.delete(
    "/facial_expressions/{user_id}/{expression}",
    response_model=FacialExpressionRecordResponse,
    summary="Delete facial expression record",
    description="Delete a facial expression record and return the removed record.",
)
async def delete_facial_expression_record(
    user_id: str,
    expression: str,
) -> FacialExpressionRecordResponse:
    """Delete a facial expression record and return the deleted item."""
    decoded_expression = parse_path_expression(expression)
    record = facial_expression_service_engine.delete_record(
        user_id,
        decoded_expression,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expression not found",
        )

    return FacialExpressionRecordResponse.from_record(record)
