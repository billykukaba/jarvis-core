from pydantic import BaseModel, Field

from app.task_manager.task_manager_engine import Task


class TaskRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    status: str = Field(min_length=1)
    priority: str = Field(min_length=1)
    completed: bool = False

    def to_task(self) -> Task:
        return Task(
            title=self.title,
            description=self.description,
            status=self.status,
            priority=self.priority,
            completed=self.completed,
        )


class TaskStatusUpdateRequest(BaseModel):
    status: str = Field(min_length=1)


class TaskResponse(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    completed: bool

    @classmethod
    def from_task(cls, task: Task) -> "TaskResponse":
        return cls(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            completed=task.completed,
        )


class UserTasksResponse(BaseModel):
    user_id: str
    tasks: list[TaskResponse]
