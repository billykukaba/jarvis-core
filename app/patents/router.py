"""FastAPI routes for the Patents Service."""

from fastapi import APIRouter, HTTPException, status

from app.patents.schemas import (
    Patent,
    PatentResponse,
    UserPatentsResponse,
)
from app.services.engine_registry import patent_service_engine

# Router exposed to FastAPI as patents_router in main.py.
patents_router = APIRouter(tags=["patents"])


@patents_router.post(
    "/patents/{user_id}",
    response_model=PatentResponse,
    summary="Create patent record",
    description="Create a new patent record for the specified user.",
)
async def create_patent(
    user_id: str,
    request: Patent,
) -> PatentResponse:
    """Create and return a patent record."""
    if patent_service_engine.title_exists(user_id, request.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patent already exists",
        )

    patent = patent_service_engine.create_patent(user_id, request)
    return PatentResponse.from_patent(patent)


@patents_router.get(
    "/patents/{user_id}",
    response_model=UserPatentsResponse,
    summary="Get all patent records",
    description="Return all patent records saved by the specified user.",
)
async def get_patents(user_id: str) -> UserPatentsResponse:
    """Return all patent records for a user."""
    patents = patent_service_engine.get_patents(user_id)
    return UserPatentsResponse(
        user_id=user_id,
        patents=[PatentResponse.from_patent(patent) for patent in patents],
    )


@patents_router.get(
    "/patents/{user_id}/{title}",
    response_model=PatentResponse,
    summary="Get one patent record",
    description="Return one patent record identified by title.",
)
async def get_patent(user_id: str, title: str) -> PatentResponse:
    """Return a single patent record by title."""
    patent = patent_service_engine.get_patent(user_id, title)
    if patent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patent not found",
        )

    return PatentResponse.from_patent(patent)


@patents_router.put(
    "/patents/{user_id}/{title}",
    response_model=PatentResponse,
    summary="Update patent record",
    description="Replace an existing patent record with updated data.",
)
async def update_patent(
    user_id: str,
    title: str,
    request: Patent,
) -> PatentResponse:
    """Update and return a patent record."""
    if (
        request.title.lower() != title.lower()
        and patent_service_engine.title_exists(user_id, request.title)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patent already exists",
        )

    patent = patent_service_engine.update_patent(user_id, title, request)
    if patent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patent not found",
        )

    return PatentResponse.from_patent(patent)


@patents_router.delete(
    "/patents/{user_id}/{title}",
    response_model=PatentResponse,
    summary="Delete patent record",
    description="Delete a patent record and return the removed record.",
)
async def delete_patent(user_id: str, title: str) -> PatentResponse:
    """Delete a patent record and return the deleted item."""
    patent = patent_service_engine.delete_patent(user_id, title)
    if patent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patent not found",
        )

    return PatentResponse.from_patent(patent)
