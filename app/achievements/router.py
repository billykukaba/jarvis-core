"""FastAPI routes for the Achievement Service."""

from fastapi import APIRouter, HTTPException, status

from app.achievements.schemas import (
    Achievement,
    AchievementResponse,
    UserAchievementsResponse,
)
from app.services.engine_registry import achievement_service_engine

# Router exposed to FastAPI as achievements_router in main.py.
achievements_router = APIRouter(tags=["achievements"])


@achievements_router.post(
    "/achievements/{user_id}",
    response_model=AchievementResponse,
    summary="Create achievement",
    description="Create a new achievement for the specified user.",
)
async def create_achievement(
    user_id: str,
    request: Achievement,
) -> AchievementResponse:
    """Create and return an achievement."""
    if achievement_service_engine.title_exists(user_id, request.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Achievement title already exists",
        )

    achievement = achievement_service_engine.create_achievement(user_id, request)
    return AchievementResponse.from_achievement(achievement)


@achievements_router.get(
    "/achievements/{user_id}",
    response_model=UserAchievementsResponse,
    summary="Get all achievements",
    description="Return all achievements saved by the specified user.",
)
async def get_achievements(user_id: str) -> UserAchievementsResponse:
    """Return all achievements for a user."""
    achievements = achievement_service_engine.get_achievements(user_id)
    return UserAchievementsResponse(
        user_id=user_id,
        achievements=[
            AchievementResponse.from_achievement(achievement)
            for achievement in achievements
        ],
    )


@achievements_router.get(
    "/achievements/{user_id}/{title}",
    response_model=AchievementResponse,
    summary="Get one achievement",
    description="Return one achievement identified by its title.",
)
async def get_achievement(user_id: str, title: str) -> AchievementResponse:
    """Return a single achievement by title."""
    achievement = achievement_service_engine.get_achievement(user_id, title)
    if achievement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found",
        )

    return AchievementResponse.from_achievement(achievement)


@achievements_router.put(
    "/achievements/{user_id}/{title}",
    response_model=AchievementResponse,
    summary="Update achievement",
    description="Replace an existing achievement with updated data.",
)
async def update_achievement(
    user_id: str,
    title: str,
    request: Achievement,
) -> AchievementResponse:
    """Update and return an achievement."""
    if (
        request.title.lower() != title.lower()
        and achievement_service_engine.title_exists(user_id, request.title)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Achievement title already exists",
        )

    achievement = achievement_service_engine.update_achievement(
        user_id,
        title,
        request,
    )
    if achievement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found",
        )

    return AchievementResponse.from_achievement(achievement)


@achievements_router.delete(
    "/achievements/{user_id}/{title}",
    response_model=AchievementResponse,
    summary="Delete achievement",
    description="Delete an achievement and return the removed achievement.",
)
async def delete_achievement(user_id: str, title: str) -> AchievementResponse:
    """Delete an achievement and return the deleted item."""
    achievement = achievement_service_engine.delete_achievement(user_id, title)
    if achievement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found",
        )

    return AchievementResponse.from_achievement(achievement)
