"""FastAPI routes for the Awards Service."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.awards.award_service_engine import normalize_title
from app.awards.schemas import (
    Award,
    AwardResponse,
    UserAwardsResponse,
)
from app.services.engine_registry import award_service_engine

# Router exposed to FastAPI as awards_router in main.py.
awards_router = APIRouter(tags=["awards"])


def parse_path_title(title: str) -> str:
    """Decode URL path titles so spaces work in GET, PUT, and DELETE."""
    # Path segments may use %20 or + for spaces depending on the client.
    return unquote(title.replace("+", " "))


@awards_router.post(
    "/awards/{user_id}",
    response_model=AwardResponse,
    summary="Create award record",
    description="Create a new award record for the specified user.",
)
async def create_award(
    user_id: str,
    request: Award,
) -> AwardResponse:
    """Create and return an award record."""
    # Reject only when another award already has the same normalized title.
    if award_service_engine.title_exists(user_id, request.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Award already exists",
        )

    award = award_service_engine.create_award(user_id, request)
    return AwardResponse.from_award(award)


@awards_router.get(
    "/awards/{user_id}",
    response_model=UserAwardsResponse,
    summary="Get all award records",
    description="Return all award records saved by the specified user.",
)
async def get_awards(user_id: str) -> UserAwardsResponse:
    """Return all award records for a user."""
    awards = award_service_engine.get_awards(user_id)
    return UserAwardsResponse(
        user_id=user_id,
        awards=[AwardResponse.from_award(award) for award in awards],
    )


@awards_router.get(
    "/awards/{user_id}/{title}",
    response_model=AwardResponse,
    summary="Get one award record",
    description="Return one award record identified by title.",
)
async def get_award(user_id: str, title: str) -> AwardResponse:
    """Return a single award record by title."""
    # Decode and normalize the path title before lookup.
    decoded_title = parse_path_title(title)
    award = award_service_engine.get_award(user_id, decoded_title)
    if award is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Award not found",
        )

    return AwardResponse.from_award(award)


@awards_router.put(
    "/awards/{user_id}/{title}",
    response_model=AwardResponse,
    status_code=status.HTTP_200_OK,
    summary="Update award record",
    description="Replace an existing award record with updated data.",
)
async def update_award(
    user_id: str,
    title: str,
    request: Award,
) -> AwardResponse:
    """Update and return an award record."""
    decoded_title = parse_path_title(title)

    # Allow keeping the same title while changing issuer/year.
    # Reject only when renaming to a different title that already exists.
    if normalize_title(request.title) != normalize_title(decoded_title):
        if award_service_engine.title_exists(user_id, request.title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Award already exists",
            )

    award = award_service_engine.update_award(user_id, decoded_title, request)
    if award is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Award not found",
        )

    return AwardResponse.from_award(award)


@awards_router.delete(
    "/awards/{user_id}/{title}",
    response_model=AwardResponse,
    summary="Delete award record",
    description="Delete an award record and return the removed record.",
)
async def delete_award(user_id: str, title: str) -> AwardResponse:
    """Delete an award record and return the deleted item."""
    # Decode and normalize the path title before lookup.
    decoded_title = parse_path_title(title)
    award = award_service_engine.delete_award(user_id, decoded_title)
    if award is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Award not found",
        )

    return AwardResponse.from_award(award)
