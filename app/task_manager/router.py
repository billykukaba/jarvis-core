from fastapi import APIRouter, HTTPException, status

from app.services.engine_registry import task_manager_engine
from app.task_manager.schemas import (
    TaskRequest,
    TaskResponse,
    TaskStatusUpdateRequest,
    UserTasksResponse,
)

router = APIRouter(tags=["task-manager"])


@router.post("/tasks/{user_id}", response_model=TaskResponse)
async def create_task(user_id: str, request: TaskRequest) -> TaskResponse:
    task = task_manager_engine.create_task(user_id, request.to_task())
    return TaskResponse.from_task(task)


@router.get("/tasks/{user_id}", response_model=UserTasksResponse)
async def get_tasks(user_id: str) -> UserTasksResponse:
    tasks = task_manager_engine.get_tasks(user_id)
    return UserTasksResponse(
        user_id=user_id,
        tasks=[TaskResponse.from_task(task) for task in tasks],
    )


@router.get("/tasks/{user_id}/{title}", response_model=TaskResponse)
async def get_task(user_id: str, title: str) -> TaskResponse:
    task = task_manager_engine.get_task(user_id, title)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.from_task(task)


@router.put("/tasks/{user_id}/{title}/status", response_model=TaskResponse)
async def update_task_status(
    user_id: str,
    title: str,
    request: TaskStatusUpdateRequest,
) -> TaskResponse:
    task = task_manager_engine.update_task_status(
        user_id=user_id,
        title=title,
        status=request.status,
    )
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.from_task(task)


@router.put("/tasks/{user_id}/{title}/complete", response_model=TaskResponse)
async def mark_completed(user_id: str, title: str) -> TaskResponse:
    task = task_manager_engine.mark_completed(user_id, title)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.from_task(task)


@router.delete("/tasks/{user_id}/{title}", response_model=TaskResponse)
async def delete_task(user_id: str, title: str) -> TaskResponse:
    task = task_manager_engine.delete_task(user_id, title)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.from_task(task)
