from fastapi import APIRouter, HTTPException, status

from app.personality.schemas import PersonalityRequest, PersonalityResponse
from app.services.engine_registry import personality_engine

router = APIRouter(tags=["personality"])


@router.post("/personality/{user_id}", response_model=PersonalityResponse)
async def create_personality_profile(
    user_id: str,
    request: PersonalityRequest,
) -> PersonalityResponse:
    profile = personality_engine.create_profile(user_id, request.to_profile())
    return PersonalityResponse.from_profile(user_id, profile)


@router.get("/personality/{user_id}", response_model=PersonalityResponse)
async def get_personality_profile(user_id: str) -> PersonalityResponse:
    profile = personality_engine.get_profile(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personality profile not found",
        )

    return PersonalityResponse.from_profile(user_id, profile)


@router.put("/personality/{user_id}", response_model=PersonalityResponse)
async def update_personality_profile(
    user_id: str,
    request: PersonalityRequest,
) -> PersonalityResponse:
    profile = personality_engine.update_profile(user_id, request.to_profile())
    return PersonalityResponse.from_profile(user_id, profile)
