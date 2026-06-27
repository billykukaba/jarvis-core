"""FastAPI routes for the Camera Analysis Agent.

Analyze camera feeds, detected scenes, objects, and summaries for Jarvis visual intelligence.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.camera_analysis_agent.camera_analysis_agent_engine import normalize_camera_id
from app.camera_analysis_agent.schemas import (
    CameraAnalysisRecord,
    CameraAnalysisRecordResponse,
    UserCameraAnalysisAgentResponse,
)
from app.services.engine_registry import camera_analysis_agent_engine

# Router exposed to FastAPI as camera_analysis_agent_router in main.py.
camera_analysis_agent_router = APIRouter(tags=["Camera Analysis Agent"])


def parse_path_camera_id(camera_id: str) -> str:
    """Decode URL path camera IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(camera_id.replace("+", " "))


@camera_analysis_agent_router.post(
    "/camera_analysis_agent/{user_id}",
    response_model=CameraAnalysisRecordResponse,
    summary="Create camera analysis record",
    description=(
        "Create a new camera analysis record for the specified user. "
        "Analyze camera feeds, detected scenes, objects, and summaries "
        "for Jarvis visual intelligence."
    ),
)
async def create_camera_analysis_record(
    user_id: str,
    request: CameraAnalysisRecord,
) -> CameraAnalysisRecordResponse:
    """Create and return a camera analysis record."""
    if camera_analysis_agent_engine.camera_id_exists(user_id, request.camera_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Camera analysis record already exists",
        )

    record = camera_analysis_agent_engine.create_record(user_id, request)
    return CameraAnalysisRecordResponse.from_record(record)


@camera_analysis_agent_router.get(
    "/camera_analysis_agent/{user_id}",
    response_model=UserCameraAnalysisAgentResponse,
    summary="Get all camera analysis records",
    description=(
        "Return all camera analysis records saved by the specified user. "
        "Analyze camera feeds, detected scenes, objects, and summaries "
        "for Jarvis visual intelligence."
    ),
)
async def get_camera_analysis_records(
    user_id: str,
) -> UserCameraAnalysisAgentResponse:
    """Return all camera analysis records for a user."""
    records = camera_analysis_agent_engine.get_records(user_id)
    return UserCameraAnalysisAgentResponse(
        user_id=user_id,
        camera_analysis_records=[
            CameraAnalysisRecordResponse.from_record(record) for record in records
        ],
    )


@camera_analysis_agent_router.get(
    "/camera_analysis_agent/{user_id}/{camera_id}",
    response_model=CameraAnalysisRecordResponse,
    summary="Get one camera analysis record",
    description="Return one camera analysis record identified by camera ID.",
)
async def get_camera_analysis_record(
    user_id: str,
    camera_id: str,
) -> CameraAnalysisRecordResponse:
    """Return a single camera analysis record by ID."""
    decoded_id = parse_path_camera_id(camera_id)
    record = camera_analysis_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera analysis record not found",
        )

    return CameraAnalysisRecordResponse.from_record(record)


@camera_analysis_agent_router.put(
    "/camera_analysis_agent/{user_id}/{camera_id}",
    response_model=CameraAnalysisRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update camera analysis record",
    description="Replace an existing camera analysis record with updated data.",
)
async def update_camera_analysis_record(
    user_id: str,
    camera_id: str,
    request: CameraAnalysisRecord,
) -> CameraAnalysisRecordResponse:
    """Update and return a camera analysis record."""
    decoded_id = parse_path_camera_id(camera_id)

    if normalize_camera_id(request.camera_id) != normalize_camera_id(decoded_id):
        if camera_analysis_agent_engine.camera_id_exists(user_id, request.camera_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Camera analysis record already exists",
            )

    record = camera_analysis_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera analysis record not found",
        )

    return CameraAnalysisRecordResponse.from_record(record)


@camera_analysis_agent_router.delete(
    "/camera_analysis_agent/{user_id}/{camera_id}",
    response_model=CameraAnalysisRecordResponse,
    summary="Delete camera analysis record",
    description="Delete a camera analysis record and return the removed record.",
)
async def delete_camera_analysis_record(
    user_id: str,
    camera_id: str,
) -> CameraAnalysisRecordResponse:
    """Delete a camera analysis record and return the deleted item."""
    decoded_id = parse_path_camera_id(camera_id)
    record = camera_analysis_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera analysis record not found",
        )

    return CameraAnalysisRecordResponse.from_record(record)
