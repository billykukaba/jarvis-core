from pydantic import BaseModel, Field

from app.goal_tracker.goal_tracker_engine import Goal


class GoalRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    progress: int
    completed: bool = False

    def to_goal(self) -> Goal:
        return Goal(
            title=self.title,
            description=self.description,
            progress=self.progress,
            completed=self.completed,
        )


class ProgressUpdateRequest(BaseModel):
    progress: int


class GoalResponse(BaseModel):
    title: str
    description: str
    progress: int
    completed: bool

    @classmethod
    def from_goal(cls, goal: Goal) -> "GoalResponse":
        return cls(
            title=goal.title,
            description=goal.description,
            progress=goal.progress,
            completed=goal.completed,
        )


class UserGoalsResponse(BaseModel):
    user_id: str
    goals: list[GoalResponse]
