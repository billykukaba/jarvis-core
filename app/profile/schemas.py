from pydantic import BaseModel

from app.profile.profile_engine import UserProfile


class ProfileResponse(BaseModel):
    dream: str
    skills: list[str]
    interests: list[str]
    projects: list[str]

    @classmethod
    def from_profile(cls, profile: UserProfile) -> "ProfileResponse":
        return cls(
            dream=profile.dream,
            skills=profile.skills,
            interests=profile.interests,
            projects=profile.projects,
        )
