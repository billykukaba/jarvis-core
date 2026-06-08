from pydantic import BaseModel, Field

from app.personality.personality_engine import PersonalityProfile


class PersonalityRequest(BaseModel):
    name: str = Field(min_length=1)
    tone: str = Field(min_length=1)
    communication_style: str = Field(min_length=1)
    language: str = Field(min_length=1)
    traits: list[str]

    def to_profile(self) -> PersonalityProfile:
        return PersonalityProfile(
            name=self.name,
            tone=self.tone,
            communication_style=self.communication_style,
            language=self.language,
            traits=self.traits,
        )


class PersonalityResponse(BaseModel):
    user_id: str
    name: str
    tone: str
    communication_style: str
    language: str
    traits: list[str]

    @classmethod
    def from_profile(
        cls,
        user_id: str,
        profile: PersonalityProfile,
    ) -> "PersonalityResponse":
        return cls(
            user_id=user_id,
            name=profile.name,
            tone=profile.tone,
            communication_style=profile.communication_style,
            language=profile.language,
            traits=profile.traits,
        )
