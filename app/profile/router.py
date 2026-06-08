from fastapi import APIRouter

from app.profile.schemas import ProfileResponse
from app.services.engine_registry import profile_engine

router = APIRouter(tags=["profile"])


@router.post("/profile/{user_id}/build", response_model=ProfileResponse)
async def build_profile(user_id: str) -> ProfileResponse:
    profile = profile_engine.build_profile(user_id)
    return ProfileResponse.from_profile(profile)


@router.get("/profile/{user_id}", response_model=ProfileResponse)
async def get_profile(user_id: str) -> ProfileResponse:
    profile = profile_engine.get_profile(user_id)
    return ProfileResponse.from_profile(profile)
