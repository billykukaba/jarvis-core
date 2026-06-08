"""FastAPI routes for the Experience Service."""

from fastapi import APIRouter, HTTPException, status

from app.experience.schemas import (
    Experience,
    ExperienceResponse,
    UserExperienceResponse,
)
from app.services.engine_registry import experience_service_engine

# Router exposed to FastAPI as experience_router in main.py.
experience_router = APIRouter(tags=["experience"])


@experience_router.post(
    "/experience/{user_id}",
    response_model=ExperienceResponse,
    summary="Create experience record",
    description="Create a new work experience record for the specified user.",
)
async def create_experience(
    user_id: str,
    request: Experience,
) -> ExperienceResponse:
    """Create and return an experience record."""
    if experience_service_engine.company_exists(user_id, request.company):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Experience already exists",
        )

    experience = experience_service_engine.create_experience(user_id, request)
    return ExperienceResponse.from_experience(experience)


@experience_router.get(
    "/experience/{user_id}",
    response_model=UserExperienceResponse,
    summary="Get all experience records",
    description="Return all work experience records saved by the specified user.",
)
async def get_experience_records(user_id: str) -> UserExperienceResponse:
    """Return all experience records for a user."""
    records = experience_service_engine.get_experience_list(user_id)
    return UserExperienceResponse(
        user_id=user_id,
        experience=[
            ExperienceResponse.from_experience(record) for record in records
        ],
    )


@experience_router.get(
    "/experience/{user_id}/{company}",
    response_model=ExperienceResponse,
    summary="Get one experience record",
    description="Return one work experience record identified by company.",
)
async def get_experience_record(
    user_id: str,
    company: str,
) -> ExperienceResponse:
    """Return a single experience record by company."""
    experience = experience_service_engine.get_experience(user_id, company)
    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found",
        )

    return ExperienceResponse.from_experience(experience)


@experience_router.put(
    "/experience/{user_id}/{company}",
    response_model=ExperienceResponse,
    summary="Update experience record",
    description="Replace an existing work experience record with updated data.",
)
async def update_experience_record(
    user_id: str,
    company: str,
    request: Experience,
) -> ExperienceResponse:
    """Update and return an experience record."""
    if (
        request.company.lower() != company.lower()
        and experience_service_engine.company_exists(user_id, request.company)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Experience already exists",
        )

    experience = experience_service_engine.update_experience(
        user_id,
        company,
        request,
    )
    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found",
        )

    return ExperienceResponse.from_experience(experience)


@experience_router.delete(
    "/experience/{user_id}/{company}",
    response_model=ExperienceResponse,
    summary="Delete experience record",
    description="Delete a work experience record and return the removed record.",
)
async def delete_experience_record(
    user_id: str,
    company: str,
) -> ExperienceResponse:
    """Delete an experience record and return the deleted item."""
    experience = experience_service_engine.delete_experience(user_id, company)
    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found",
        )

    return ExperienceResponse.from_experience(experience)
