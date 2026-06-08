"""FastAPI routes for the Skills Service."""

from fastapi import APIRouter, HTTPException, status

from app.services.engine_registry import skill_service_engine
from app.skills.schemas import Skill, SkillResponse, UserSkillsResponse

# Router exposed to FastAPI as skills_router in main.py.
skills_router = APIRouter(tags=["skills"])


@skills_router.post(
    "/skills/{user_id}",
    response_model=SkillResponse,
    summary="Create skill record",
    description="Create a new skill record for the specified user.",
)
async def create_skill(user_id: str, request: Skill) -> SkillResponse:
    """Create and return a skill record."""
    if skill_service_engine.skill_exists(user_id, request.skill):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill already exists",
        )

    skill = skill_service_engine.create_skill(user_id, request)
    return SkillResponse.from_skill(skill)


@skills_router.get(
    "/skills/{user_id}",
    response_model=UserSkillsResponse,
    summary="Get all skill records",
    description="Return all skill records saved by the specified user.",
)
async def get_skills(user_id: str) -> UserSkillsResponse:
    """Return all skill records for a user."""
    skills = skill_service_engine.get_skills(user_id)
    return UserSkillsResponse(
        user_id=user_id,
        skills=[SkillResponse.from_skill(skill) for skill in skills],
    )


@skills_router.get(
    "/skills/{user_id}/{skill}",
    response_model=SkillResponse,
    summary="Get one skill record",
    description="Return one skill record identified by skill name.",
)
async def get_skill(user_id: str, skill: str) -> SkillResponse:
    """Return a single skill record by skill name."""
    record = skill_service_engine.get_skill(user_id, skill)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    return SkillResponse.from_skill(record)


@skills_router.put(
    "/skills/{user_id}/{skill}",
    response_model=SkillResponse,
    summary="Update skill record",
    description="Replace an existing skill record with updated data.",
)
async def update_skill(
    user_id: str,
    skill: str,
    request: Skill,
) -> SkillResponse:
    """Update and return a skill record."""
    if (
        request.skill.lower() != skill.lower()
        and skill_service_engine.skill_exists(user_id, request.skill)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill already exists",
        )

    record = skill_service_engine.update_skill(user_id, skill, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    return SkillResponse.from_skill(record)


@skills_router.delete(
    "/skills/{user_id}/{skill}",
    response_model=SkillResponse,
    summary="Delete skill record",
    description="Delete a skill record and return the removed record.",
)
async def delete_skill(user_id: str, skill: str) -> SkillResponse:
    """Delete a skill record and return the deleted item."""
    record = skill_service_engine.delete_skill(user_id, skill)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    return SkillResponse.from_skill(record)
