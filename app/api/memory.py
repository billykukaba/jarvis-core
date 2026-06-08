from fastapi import APIRouter, HTTPException, status

from app.models.memory import MemoryRequest, MemoryResponse, UserMemoriesResponse
from app.services.engine_registry import memory_engine

router = APIRouter(tags=["memory"])


@router.post("/memory/{user_id}", response_model=MemoryResponse)
async def remember(user_id: str, request: MemoryRequest) -> MemoryResponse:
    record = memory_engine.remember(user_id, request.key, request.value)
    return MemoryResponse.from_record(record)


@router.get("/memory/{user_id}/{key}", response_model=MemoryResponse)
async def recall(user_id: str, key: str) -> MemoryResponse:
    record = memory_engine.recall(user_id, key)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    return MemoryResponse.from_record(record)


@router.get("/memory/{user_id}", response_model=UserMemoriesResponse)
async def get_all_memories(user_id: str) -> UserMemoriesResponse:
    memories = memory_engine.get_all_memories(user_id)
    return UserMemoriesResponse(user_id=user_id, memories=memories)
