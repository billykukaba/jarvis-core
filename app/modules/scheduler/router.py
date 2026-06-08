from fastapi import APIRouter, HTTPException, status

from app.modules.scheduler.schemas import (
    Schedule,
    ScheduleResponse,
    UserSchedulesResponse,
)
from app.services.engine_registry import scheduler_engine

router = APIRouter(tags=["scheduler"])


@router.post("/scheduler/{user_id}", response_model=ScheduleResponse)
async def create_schedule(user_id: str, request: Schedule) -> ScheduleResponse:
    schedule = scheduler_engine.create_schedule(user_id, request)
    return ScheduleResponse.from_schedule(schedule)


@router.get("/scheduler/{user_id}", response_model=UserSchedulesResponse)
async def get_schedules(user_id: str) -> UserSchedulesResponse:
    schedules = scheduler_engine.get_schedules(user_id)
    return UserSchedulesResponse(
        user_id=user_id,
        schedules=[ScheduleResponse.from_schedule(schedule) for schedule in schedules],
    )


@router.get("/scheduler/{user_id}/{task_title}", response_model=ScheduleResponse)
async def get_schedule(user_id: str, task_title: str) -> ScheduleResponse:
    schedule = scheduler_engine.get_schedule(user_id, task_title)
    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )

    return ScheduleResponse.from_schedule(schedule)


@router.put("/scheduler/{user_id}/{task_title}", response_model=ScheduleResponse)
async def update_schedule(
    user_id: str,
    task_title: str,
    request: Schedule,
) -> ScheduleResponse:
    schedule = scheduler_engine.update_schedule(user_id, task_title, request)
    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )

    return ScheduleResponse.from_schedule(schedule)


@router.delete("/scheduler/{user_id}/{task_title}", response_model=ScheduleResponse)
async def delete_schedule(user_id: str, task_title: str) -> ScheduleResponse:
    schedule = scheduler_engine.delete_schedule(user_id, task_title)
    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )

    return ScheduleResponse.from_schedule(schedule)
