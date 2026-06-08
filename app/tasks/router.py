"""FastAPI routes for the Task Service."""

from fastapi import APIRouter, HTTPException, status

from app.services.engine_registry import task_engine
from app.tasks.schemas import Task, TaskResponse, UserTasksResponse

# Router exposed to FastAPI as tasks_router in main.py.
tasks_router = APIRouter(tags=["tasks"])


@tasks_router.post(
    "/tasks/{user_id}",
    response_model=TaskResponse,
    summary="Create task",
    description="Create a new task for the specified user.",
)
async def create_task(user_id: str, request: Task) -> TaskResponse:
    """Create and return a task."""
    task = task_engine.create_task(user_id, request)
    return TaskResponse.from_task(task)


@tasks_router.get(
    "/tasks/{user_id}",
    response_model=UserTasksResponse,
    summary="Get all tasks",
    description="Return all tasks saved by the specified user.",
)
async def get_tasks(user_id: str) -> UserTasksResponse:
    """Return all tasks for a user."""
    tasks = task_engine.get_tasks(user_id)
    return UserTasksResponse(
        user_id=user_id,
        tasks=[TaskResponse.from_task(task) for task in tasks],
    )


@tasks_router.get(
    "/tasks/{user_id}/{title}",
    response_model=TaskResponse,
    summary="Get one task",
    description="Return one task identified by its title.",
)
async def get_task(user_id: str, title: str) -> TaskResponse:
    """Return a single task by title."""
    task = task_engine.get_task(user_id, title)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.from_task(task)


@tasks_router.put(
    "/tasks/{user_id}/{title}",
    response_model=TaskResponse,
    summary="Update task",
    description="Replace an existing task with updated data.",
)
async def update_task(user_id: str, title: str, request: Task) -> TaskResponse:
    """Update and return a task."""
    task = task_engine.update_task(user_id, title, request)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.from_task(task)


@tasks_router.delete(
    "/tasks/{user_id}/{title}",
    response_model=TaskResponse,
    summary="Delete task",
    description="Delete a task and return the removed task.",
)
async def delete_task(user_id: str, title: str) -> TaskResponse:
    """Delete a task and return the deleted item."""
    task = task_engine.delete_task(user_id, title)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.from_task(task)
