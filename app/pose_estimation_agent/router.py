"""FastAPI routes for the Pose Estimation Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.pose_estimation_agent.pose_estimation_agent_engine import normalize_pose_id
from app.pose_estimation_agent.schemas import (
    PoseEstimation,
    PoseEstimationResponse,
    UserPoseEstimationAgentResponse,
)
from app.services.engine_registry import pose_estimation_agent_engine

# Router exposed to FastAPI as pose_estimation_agent_router in main.py.
pose_estimation_agent_router = APIRouter(tags=["Pose Estimation Agent"])


def parse_path_pose_id(pose_id: str) -> str:
    """Decode URL path pose IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(pose_id.replace("+", " "))


@pose_estimation_agent_router.post(
    "/pose_estimation_agent/{user_id}",
    response_model=PoseEstimationResponse,
    summary="Create pose record",
    description="Create a new pose estimation record for the specified user.",
)
async def create_pose_record(
    user_id: str,
    request: PoseEstimation,
) -> PoseEstimationResponse:
    """Create and return a pose estimation record."""
    if pose_estimation_agent_engine.pose_id_exists(user_id, request.pose_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pose record already exists",
        )

    record = pose_estimation_agent_engine.create_record(user_id, request)
    return PoseEstimationResponse.from_pose(record)


@pose_estimation_agent_router.get(
    "/pose_estimation_agent/{user_id}",
    response_model=UserPoseEstimationAgentResponse,
    summary="Get all pose records",
    description="Return all pose estimation records saved by the specified user.",
)
async def get_pose_records(user_id: str) -> UserPoseEstimationAgentResponse:
    """Return all pose estimation records for a user."""
    records = pose_estimation_agent_engine.get_records(user_id)
    return UserPoseEstimationAgentResponse(
        user_id=user_id,
        pose_records=[
            PoseEstimationResponse.from_pose(record) for record in records
        ],
    )


@pose_estimation_agent_router.get(
    "/pose_estimation_agent/{user_id}/{pose_id}",
    response_model=PoseEstimationResponse,
    summary="Get one pose record",
    description="Return one pose estimation record identified by pose ID.",
)
async def get_pose_record(
    user_id: str,
    pose_id: str,
) -> PoseEstimationResponse:
    """Return a single pose estimation record by ID."""
    decoded_id = parse_path_pose_id(pose_id)
    record = pose_estimation_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pose record not found",
        )

    return PoseEstimationResponse.from_pose(record)


@pose_estimation_agent_router.put(
    "/pose_estimation_agent/{user_id}/{pose_id}",
    response_model=PoseEstimationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update pose record",
    description="Replace an existing pose estimation record with updated data.",
)
async def update_pose_record(
    user_id: str,
    pose_id: str,
    request: PoseEstimation,
) -> PoseEstimationResponse:
    """Update and return a pose estimation record."""
    decoded_id = parse_path_pose_id(pose_id)

    if normalize_pose_id(request.pose_id) != normalize_pose_id(decoded_id):
        if pose_estimation_agent_engine.pose_id_exists(user_id, request.pose_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pose record already exists",
            )

    record = pose_estimation_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pose record not found",
        )

    return PoseEstimationResponse.from_pose(record)


@pose_estimation_agent_router.delete(
    "/pose_estimation_agent/{user_id}/{pose_id}",
    response_model=PoseEstimationResponse,
    summary="Delete pose record",
    description="Delete a pose estimation record and return the removed record.",
)
async def delete_pose_record(
    user_id: str,
    pose_id: str,
) -> PoseEstimationResponse:
    """Delete a pose estimation record and return the deleted item."""
    decoded_id = parse_path_pose_id(pose_id)
    record = pose_estimation_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pose record not found",
        )

    return PoseEstimationResponse.from_pose(record)
