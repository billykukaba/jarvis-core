from fastapi import APIRouter, HTTPException, status

from app.services.engine_registry import user_state_engine
from app.user_state.schemas import UserStateRequest, UserStateResponse

router = APIRouter(tags=["user_state"])


@router.post("/user-state/{user_id}", response_model=UserStateResponse)
async def set_user_state(
    user_id: str,
    request: UserStateRequest,
) -> UserStateResponse:
    state = user_state_engine.set_state(user_id, request.to_state())
    return UserStateResponse.from_state(user_id, state)


@router.get("/user-state/{user_id}", response_model=UserStateResponse)
async def get_user_state(user_id: str) -> UserStateResponse:
    state = user_state_engine.get_state(user_id)
    if state is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User state not found",
        )

    return UserStateResponse.from_state(user_id, state)
