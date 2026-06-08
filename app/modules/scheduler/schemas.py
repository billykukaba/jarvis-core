from pydantic import BaseModel, Field


class Schedule(BaseModel):
    task_title: str = Field(min_length=1)
    schedule: str = Field(min_length=1)
    reminder: bool = True


class ScheduleResponse(BaseModel):
    task_title: str
    schedule: str
    reminder: bool

    @classmethod
    def from_schedule(cls, schedule: Schedule) -> "ScheduleResponse":
        return cls(
            task_title=schedule.task_title,
            schedule=schedule.schedule,
            reminder=schedule.reminder,
        )


class UserSchedulesResponse(BaseModel):
    user_id: str
    schedules: list[ScheduleResponse]
