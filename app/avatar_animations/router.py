"""FastAPI routes for the Avatar Animation Engine (Module 64)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.avatar_animations.avatar_animation_service_engine import normalize_animation
from app.avatar_animations.schemas import (
    AvatarAnimationRecord,
    AvatarAnimationRecordResponse,
    UserAvatarAnimationsResponse,
)
from app.services.engine_registry import avatar_animation_service_engine

# Router exposed to FastAPI as avatar_animations_router in main.py.
avatar_animations_router = APIRouter(tags=["avatar_animations"])


def parse_path_animation(animation: str) -> str:
    """Decode URL path animation names so spaces work in GET, PUT, and DELETE."""
    return unquote(animation.replace("+", " "))


@avatar_animations_router.post(
    "/avatar_animations/{user_id}",
    response_model=AvatarAnimationRecordResponse,
    summary="Create avatar animation record",
    description="Create a new avatar animation record for the specified user.",
)
async def create_avatar_animation_record(
    user_id: str,
    request: AvatarAnimationRecord,
) -> AvatarAnimationRecordResponse:
    """Create and return an avatar animation record."""
    if avatar_animation_service_engine.animation_exists(
        user_id,
        request.animation,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Animation already exists",
        )

    record = avatar_animation_service_engine.create_record(user_id, request)
    return AvatarAnimationRecordResponse.from_record(record)


@avatar_animations_router.get(
    "/avatar_animations/{user_id}",
    response_model=UserAvatarAnimationsResponse,
    summary="Get all avatar animation records",
    description="Return all avatar animation records saved by the specified user.",
)
async def get_avatar_animation_records(
    user_id: str,
) -> UserAvatarAnimationsResponse:
    """Return all avatar animation records for a user."""
    records = avatar_animation_service_engine.get_records(user_id)
    return UserAvatarAnimationsResponse(
        user_id=user_id,
        avatar_animations=[
            AvatarAnimationRecordResponse.from_record(record)
            for record in records
        ],
    )


@avatar_animations_router.get(
    "/avatar_animations/{user_id}/{animation}",
    response_model=AvatarAnimationRecordResponse,
    summary="Get one avatar animation record",
    description="Return one avatar animation record identified by animation name.",
)
async def get_avatar_animation_record(
    user_id: str,
    animation: str,
) -> AvatarAnimationRecordResponse:
    """Return a single avatar animation record by name."""
    decoded_animation = parse_path_animation(animation)
    record = avatar_animation_service_engine.get_record(
        user_id,
        decoded_animation,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animation not found",
        )

    return AvatarAnimationRecordResponse.from_record(record)


@avatar_animations_router.put(
    "/avatar_animations/{user_id}/{animation}",
    response_model=AvatarAnimationRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update avatar animation record",
    description="Replace an existing avatar animation record with updated data.",
)
async def update_avatar_animation_record(
    user_id: str,
    animation: str,
    request: AvatarAnimationRecord,
) -> AvatarAnimationRecordResponse:
    """Update and return an avatar animation record."""
    decoded_animation = parse_path_animation(animation)

    # Allow keeping the same animation while changing duration.
    if normalize_animation(request.animation) != normalize_animation(
        decoded_animation
    ):
        if avatar_animation_service_engine.animation_exists(
            user_id,
            request.animation,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Animation already exists",
            )

    record = avatar_animation_service_engine.update_record(
        user_id,
        decoded_animation,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animation not found",
        )

    return AvatarAnimationRecordResponse.from_record(record)


@avatar_animations_router.delete(
    "/avatar_animations/{user_id}/{animation}",
    response_model=AvatarAnimationRecordResponse,
    summary="Delete avatar animation record",
    description="Delete an avatar animation record and return the removed record.",
)
async def delete_avatar_animation_record(
    user_id: str,
    animation: str,
) -> AvatarAnimationRecordResponse:
    """Delete an avatar animation record and return the deleted item."""
    decoded_animation = parse_path_animation(animation)
    record = avatar_animation_service_engine.delete_record(
        user_id,
        decoded_animation,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animation not found",
        )

    return AvatarAnimationRecordResponse.from_record(record)
