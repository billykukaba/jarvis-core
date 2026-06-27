"""FastAPI routes for the Skill Evolution Engine (Module 60)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.skill_evolution_engine.schemas import (
    SkillEvolution,
    SkillEvolutionResponse,
    UserSkillEvolutionEngineResponse,
)
from app.skill_evolution_engine.skill_evolution_engine import normalize_evolution_id
from app.services.engine_registry import skill_evolution_engine

# Router exposed to FastAPI as skill_evolution_engine_router in main.py.
skill_evolution_engine_router = APIRouter(tags=["Skill Evolution Engine"])


def parse_path_evolution_id(evolution_id: str) -> str:
    """Decode URL path evolution IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(evolution_id.replace("+", " "))


@skill_evolution_engine_router.post(
    "/skill_evolution_engine/{user_id}",
    response_model=SkillEvolutionResponse,
    summary="Create skill evolution record",
    description="Create a new skill evolution record for the specified user.",
)
async def create_skill_evolution_record(
    user_id: str,
    request: SkillEvolution,
) -> SkillEvolutionResponse:
    """Create and return a skill evolution record."""
    if skill_evolution_engine.evolution_id_exists(user_id, request.evolution_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Evolution already exists",
        )

    record = skill_evolution_engine.create_record(user_id, request)
    return SkillEvolutionResponse.from_evolution(record)


@skill_evolution_engine_router.get(
    "/skill_evolution_engine/{user_id}",
    response_model=UserSkillEvolutionEngineResponse,
    summary="Get all skill evolution records",
    description="Return all skill evolution records saved by the specified user.",
)
async def get_skill_evolution_records(
    user_id: str,
) -> UserSkillEvolutionEngineResponse:
    """Return all skill evolution records for a user."""
    records = skill_evolution_engine.get_records(user_id)
    return UserSkillEvolutionEngineResponse(
        user_id=user_id,
        skill_evolutions=[
            SkillEvolutionResponse.from_evolution(record) for record in records
        ],
    )


@skill_evolution_engine_router.get(
    "/skill_evolution_engine/{user_id}/{evolution_id}",
    response_model=SkillEvolutionResponse,
    summary="Get one skill evolution record",
    description="Return one skill evolution record identified by evolution ID.",
)
async def get_skill_evolution_record(
    user_id: str,
    evolution_id: str,
) -> SkillEvolutionResponse:
    """Return a single skill evolution record by ID."""
    decoded_id = parse_path_evolution_id(evolution_id)
    record = skill_evolution_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evolution not found",
        )

    return SkillEvolutionResponse.from_evolution(record)


@skill_evolution_engine_router.put(
    "/skill_evolution_engine/{user_id}/{evolution_id}",
    response_model=SkillEvolutionResponse,
    status_code=status.HTTP_200_OK,
    summary="Update skill evolution record",
    description="Replace an existing skill evolution record with updated data.",
)
async def update_skill_evolution_record(
    user_id: str,
    evolution_id: str,
    request: SkillEvolution,
) -> SkillEvolutionResponse:
    """Update and return a skill evolution record."""
    decoded_id = parse_path_evolution_id(evolution_id)

    # Allow keeping the same evolution ID while changing other fields.
    if normalize_evolution_id(request.evolution_id) != normalize_evolution_id(
        decoded_id
    ):
        if skill_evolution_engine.evolution_id_exists(user_id, request.evolution_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Evolution already exists",
            )

    record = skill_evolution_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evolution not found",
        )

    return SkillEvolutionResponse.from_evolution(record)


@skill_evolution_engine_router.delete(
    "/skill_evolution_engine/{user_id}/{evolution_id}",
    response_model=SkillEvolutionResponse,
    summary="Delete skill evolution record",
    description="Delete a skill evolution record and return the removed record.",
)
async def delete_skill_evolution_record(
    user_id: str,
    evolution_id: str,
) -> SkillEvolutionResponse:
    """Delete a skill evolution record and return the deleted item."""
    decoded_id = parse_path_evolution_id(evolution_id)
    record = skill_evolution_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evolution not found",
        )

    return SkillEvolutionResponse.from_evolution(record)
