"""FastAPI routes for the Publications Service."""

from fastapi import APIRouter, HTTPException, status

from app.publications.schemas import (
    Publication,
    PublicationResponse,
    UserPublicationsResponse,
)
from app.services.engine_registry import publication_service_engine

# Router exposed to FastAPI as publications_router in main.py.
publications_router = APIRouter(tags=["publications"])


@publications_router.post(
    "/publications/{user_id}",
    response_model=PublicationResponse,
    summary="Create publication record",
    description="Create a new publication record for the specified user.",
)
async def create_publication(
    user_id: str,
    request: Publication,
) -> PublicationResponse:
    """Create and return a publication record."""
    if publication_service_engine.title_exists(user_id, request.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Publication already exists",
        )

    publication = publication_service_engine.create_publication(user_id, request)
    return PublicationResponse.from_publication(publication)


@publications_router.get(
    "/publications/{user_id}",
    response_model=UserPublicationsResponse,
    summary="Get all publication records",
    description="Return all publication records saved by the specified user.",
)
async def get_publications(user_id: str) -> UserPublicationsResponse:
    """Return all publication records for a user."""
    publications = publication_service_engine.get_publications(user_id)
    return UserPublicationsResponse(
        user_id=user_id,
        publications=[
            PublicationResponse.from_publication(publication)
            for publication in publications
        ],
    )


@publications_router.get(
    "/publications/{user_id}/{title}",
    response_model=PublicationResponse,
    summary="Get one publication record",
    description="Return one publication record identified by title.",
)
async def get_publication(user_id: str, title: str) -> PublicationResponse:
    """Return a single publication record by title."""
    publication = publication_service_engine.get_publication(user_id, title)
    if publication is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publication not found",
        )

    return PublicationResponse.from_publication(publication)


@publications_router.put(
    "/publications/{user_id}/{title}",
    response_model=PublicationResponse,
    summary="Update publication record",
    description="Replace an existing publication record with updated data.",
)
async def update_publication(
    user_id: str,
    title: str,
    request: Publication,
) -> PublicationResponse:
    """Update and return a publication record."""
    if (
        request.title.lower() != title.lower()
        and publication_service_engine.title_exists(user_id, request.title)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Publication already exists",
        )

    publication = publication_service_engine.update_publication(
        user_id,
        title,
        request,
    )
    if publication is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publication not found",
        )

    return PublicationResponse.from_publication(publication)


@publications_router.delete(
    "/publications/{user_id}/{title}",
    response_model=PublicationResponse,
    summary="Delete publication record",
    description="Delete a publication record and return the removed record.",
)
async def delete_publication(user_id: str, title: str) -> PublicationResponse:
    """Delete a publication record and return the deleted item."""
    publication = publication_service_engine.delete_publication(user_id, title)
    if publication is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publication not found",
        )

    return PublicationResponse.from_publication(publication)
