"""FastAPI routes for the Self Evaluation Engine."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.self_evaluation_engine.schemas import (
    SelfEvaluationRecord,
    SelfEvaluationRecordResponse,
    UserSelfEvaluationEngineResponse,
)
from app.self_evaluation_engine.self_evaluation_engine import normalize_evaluation_id
from app.services.engine_registry import self_evaluation_engine

# Router exposed to FastAPI as self_evaluation_engine_router in main.py.
self_evaluation_engine_router = APIRouter(tags=["Self Evaluation Engine"])


def parse_path_evaluation_id(evaluation_id: str) -> str:
    """Decode URL path evaluation IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(evaluation_id.replace("+", " "))


@self_evaluation_engine_router.post(
    "/self_evaluation_engine/{user_id}",
    response_model=SelfEvaluationRecordResponse,
    summary="Create self evaluation record",
    description="Create a new self-evaluation record for the specified user.",
)
async def create_self_evaluation_record(
    user_id: str,
    request: SelfEvaluationRecord,
) -> SelfEvaluationRecordResponse:
    """Create and return a self-evaluation record."""
    if self_evaluation_engine.evaluation_id_exists(user_id, request.evaluation_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Evaluation already exists",
        )

    record = self_evaluation_engine.create_record(user_id, request)
    return SelfEvaluationRecordResponse.from_record(record)


@self_evaluation_engine_router.get(
    "/self_evaluation_engine/{user_id}",
    response_model=UserSelfEvaluationEngineResponse,
    summary="Get all self evaluation records",
    description="Return all self-evaluation records saved by the specified user.",
)
async def get_self_evaluation_records(
    user_id: str,
) -> UserSelfEvaluationEngineResponse:
    """Return all self-evaluation records for a user."""
    records = self_evaluation_engine.get_records(user_id)
    return UserSelfEvaluationEngineResponse(
        user_id=user_id,
        self_evaluations=[
            SelfEvaluationRecordResponse.from_record(record) for record in records
        ],
    )


@self_evaluation_engine_router.get(
    "/self_evaluation_engine/{user_id}/{evaluation_id}",
    response_model=SelfEvaluationRecordResponse,
    summary="Get one self evaluation record",
    description="Return one self-evaluation record identified by evaluation ID.",
)
async def get_self_evaluation_record(
    user_id: str,
    evaluation_id: str,
) -> SelfEvaluationRecordResponse:
    """Return a single self-evaluation record by ID."""
    decoded_id = parse_path_evaluation_id(evaluation_id)
    record = self_evaluation_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found",
        )

    return SelfEvaluationRecordResponse.from_record(record)


@self_evaluation_engine_router.put(
    "/self_evaluation_engine/{user_id}/{evaluation_id}",
    response_model=SelfEvaluationRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update self evaluation record",
    description="Replace an existing self-evaluation record with updated data.",
)
async def update_self_evaluation_record(
    user_id: str,
    evaluation_id: str,
    request: SelfEvaluationRecord,
) -> SelfEvaluationRecordResponse:
    """Update and return a self-evaluation record."""
    decoded_id = parse_path_evaluation_id(evaluation_id)

    # Allow keeping the same evaluation ID while changing category/score/feedback.
    if normalize_evaluation_id(request.evaluation_id) != normalize_evaluation_id(
        decoded_id
    ):
        if self_evaluation_engine.evaluation_id_exists(user_id, request.evaluation_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Evaluation already exists",
            )

    record = self_evaluation_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found",
        )

    return SelfEvaluationRecordResponse.from_record(record)


@self_evaluation_engine_router.delete(
    "/self_evaluation_engine/{user_id}/{evaluation_id}",
    response_model=SelfEvaluationRecordResponse,
    summary="Delete self evaluation record",
    description="Delete a self-evaluation record and return the removed record.",
)
async def delete_self_evaluation_record(
    user_id: str,
    evaluation_id: str,
) -> SelfEvaluationRecordResponse:
    """Delete a self-evaluation record and return the deleted item."""
    decoded_id = parse_path_evaluation_id(evaluation_id)
    record = self_evaluation_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found",
        )

    return SelfEvaluationRecordResponse.from_record(record)
