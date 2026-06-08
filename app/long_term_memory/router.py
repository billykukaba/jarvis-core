from fastapi import APIRouter, HTTPException, status

from app.long_term_memory.schemas import (
    DeleteLongTermMemoryResponse,
    LongTermMemoryRequest,
    LongTermMemoryResponse,
    LongTermMemoryUpdateRequest,
    UserLongTermMemoriesResponse,
)
from app.services.engine_registry import long_term_memory_engine

router = APIRouter(tags=["long-term-memory"])


@router.post("/long-memory/{user_id}", response_model=LongTermMemoryResponse)
async def store_memory(
    user_id: str,
    request: LongTermMemoryRequest,
) -> LongTermMemoryResponse:
    memory = long_term_memory_engine.store_memory(
        user_id=user_id,
        key=request.key,
        value=request.value,
    )
    return LongTermMemoryResponse.from_record(memory)


@router.get("/long-memory/{user_id}", response_model=UserLongTermMemoriesResponse)
async def get_all_memories(user_id: str) -> UserLongTermMemoriesResponse:
    memories = long_term_memory_engine.get_all_memories(user_id)
    return UserLongTermMemoriesResponse(user_id=user_id, memories=memories)


@router.get("/long-memory/{user_id}/{key}", response_model=LongTermMemoryResponse)
async def retrieve_memory(user_id: str, key: str) -> LongTermMemoryResponse:
    memory = long_term_memory_engine.retrieve_memory(user_id, key)
    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Long-term memory not found",
        )

    return LongTermMemoryResponse.from_record(memory)


@router.put("/long-memory/{user_id}/{key}", response_model=LongTermMemoryResponse)
async def update_memory(
    user_id: str,
    key: str,
    request: LongTermMemoryUpdateRequest,
) -> LongTermMemoryResponse:
    memory = long_term_memory_engine.update_memory(
        user_id=user_id,
        key=key,
        value=request.value,
    )
    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Long-term memory not found",
        )

    return LongTermMemoryResponse.from_record(memory)


@router.delete(
    "/long-memory/{user_id}/{key}",
    response_model=DeleteLongTermMemoryResponse,
)
async def delete_memory(user_id: str, key: str) -> DeleteLongTermMemoryResponse:
    memory = long_term_memory_engine.delete_memory(user_id, key)
    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Long-term memory not found",
        )

    return DeleteLongTermMemoryResponse(
        deleted=True,
        memory=LongTermMemoryResponse.from_record(memory),
    )
