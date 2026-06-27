"""FastAPI routes for the Scene Understanding Agent.

Understands complete scenes and environments for Jarvis Vision Intelligence.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.scene_understanding_agent.scene_understanding_agent_engine import (
    normalize_scene_id,
)
from app.scene_understanding_agent.schemas import (
    SceneUnderstandingRecord,
    SceneUnderstandingRecordResponse,
    UserSceneUnderstandingAgentResponse,
)
from app.services.engine_registry import scene_understanding_agent_engine

# Router exposed to FastAPI as scene_understanding_agent_router in main.py.
scene_understanding_agent_router = APIRouter(tags=["Scene Understanding Agent"])


def parse_path_scene_id(scene_id: str) -> str:
    """Decode URL path scene IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(scene_id.replace("+", " "))


@scene_understanding_agent_router.post(
    "/scene_understanding_agent/{user_id}",
    response_model=SceneUnderstandingRecordResponse,
    summary="Create scene understanding record",
    description=(
        "Create a new scene understanding record for the specified user. "
        "Understands complete scenes and environments for Jarvis Vision Intelligence."
    ),
)
async def create_scene_understanding_record(
    user_id: str,
    request: SceneUnderstandingRecord,
) -> SceneUnderstandingRecordResponse:
    """Create and return a scene understanding record."""
    if scene_understanding_agent_engine.scene_id_exists(user_id, request.scene_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scene understanding record already exists",
        )

    record = scene_understanding_agent_engine.create_record(user_id, request)
    return SceneUnderstandingRecordResponse.from_record(record)


@scene_understanding_agent_router.get(
    "/scene_understanding_agent/{user_id}",
    response_model=UserSceneUnderstandingAgentResponse,
    summary="Get all scene understanding records",
    description=(
        "Return all scene understanding records saved by the specified user. "
        "Understands complete scenes and environments for Jarvis Vision Intelligence."
    ),
)
async def get_scene_understanding_records(
    user_id: str,
) -> UserSceneUnderstandingAgentResponse:
    """Return all scene understanding records for a user."""
    records = scene_understanding_agent_engine.get_records(user_id)
    return UserSceneUnderstandingAgentResponse(
        user_id=user_id,
        scene_understanding_records=[
            SceneUnderstandingRecordResponse.from_record(record) for record in records
        ],
    )


@scene_understanding_agent_router.get(
    "/scene_understanding_agent/{user_id}/{scene_id}",
    response_model=SceneUnderstandingRecordResponse,
    summary="Get one scene understanding record",
    description="Return one scene understanding record identified by scene ID.",
)
async def get_scene_understanding_record(
    user_id: str,
    scene_id: str,
) -> SceneUnderstandingRecordResponse:
    """Return a single scene understanding record by ID."""
    decoded_id = parse_path_scene_id(scene_id)
    record = scene_understanding_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scene understanding record not found",
        )

    return SceneUnderstandingRecordResponse.from_record(record)


@scene_understanding_agent_router.put(
    "/scene_understanding_agent/{user_id}/{scene_id}",
    response_model=SceneUnderstandingRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update scene understanding record",
    description="Replace an existing scene understanding record with updated data.",
)
async def update_scene_understanding_record(
    user_id: str,
    scene_id: str,
    request: SceneUnderstandingRecord,
) -> SceneUnderstandingRecordResponse:
    """Update and return a scene understanding record."""
    decoded_id = parse_path_scene_id(scene_id)

    if normalize_scene_id(request.scene_id) != normalize_scene_id(decoded_id):
        if scene_understanding_agent_engine.scene_id_exists(user_id, request.scene_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scene understanding record already exists",
            )

    record = scene_understanding_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scene understanding record not found",
        )

    return SceneUnderstandingRecordResponse.from_record(record)


@scene_understanding_agent_router.delete(
    "/scene_understanding_agent/{user_id}/{scene_id}",
    response_model=SceneUnderstandingRecordResponse,
    summary="Delete scene understanding record",
    description="Delete a scene understanding record and return the removed record.",
)
async def delete_scene_understanding_record(
    user_id: str,
    scene_id: str,
) -> SceneUnderstandingRecordResponse:
    """Delete a scene understanding record and return the deleted item."""
    decoded_id = parse_path_scene_id(scene_id)
    record = scene_understanding_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scene understanding record not found",
        )

    return SceneUnderstandingRecordResponse.from_record(record)
