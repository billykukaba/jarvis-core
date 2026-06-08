from fastapi import APIRouter, HTTPException, status

from app.learning_tracker.schemas import (
    LearningProgressRequest,
    LearningSkillRequest,
    LearningSkillResponse,
    UserSkillsResponse,
)
from app.services.engine_registry import learning_tracker_engine

router = APIRouter(tags=["learning-tracker"])


@router.post("/learning/{user_id}", response_model=LearningSkillResponse)
async def add_skill(
    user_id: str,
    request: LearningSkillRequest,
) -> LearningSkillResponse:
    skill = learning_tracker_engine.add_skill(user_id, request.to_skill())
    return LearningSkillResponse.from_skill(skill)


@router.get("/learning/{user_id}", response_model=UserSkillsResponse)
async def get_skills(user_id: str) -> UserSkillsResponse:
    skills = learning_tracker_engine.get_skills(user_id)
    return UserSkillsResponse(
        user_id=user_id,
        skills=[LearningSkillResponse.from_skill(skill) for skill in skills],
    )


@router.get("/learning/{user_id}/{skill_name}", response_model=LearningSkillResponse)
async def get_skill(user_id: str, skill_name: str) -> LearningSkillResponse:
    skill = learning_tracker_engine.get_skill(user_id, skill_name)
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning skill not found",
        )

    return LearningSkillResponse.from_skill(skill)


@router.put(
    "/learning/{user_id}/{skill_name}/progress",
    response_model=LearningSkillResponse,
)
async def update_progress(
    user_id: str,
    skill_name: str,
    request: LearningProgressRequest,
) -> LearningSkillResponse:
    skill = learning_tracker_engine.update_progress(
        user_id=user_id,
        skill_name=skill_name,
        progress=request.progress,
    )
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning skill not found",
        )

    return LearningSkillResponse.from_skill(skill)
