"""Pydantic schemas for the Skill Evolution Engine (Module 60)."""

from pydantic import BaseModel, ConfigDict, Field


class SkillEvolution(BaseModel):
    """Skill evolution record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "evolution_id": "evo_001",
                    "skill": "Python",
                    "current_level": 3,
                    "target_level": 5,
                    "status": "in_progress",
                }
            ]
        }
    )

    evolution_id: str = Field(
        min_length=1,
        description="Unique skill evolution identifier",
        examples=["evo_001"],
    )
    skill: str = Field(
        min_length=1,
        description="Skill name being evolved",
        examples=["Python"],
    )
    current_level: int = Field(
        ge=0,
        description="Current skill level",
        examples=[3],
    )
    target_level: int = Field(
        ge=0,
        description="Target skill level",
        examples=[5],
    )
    status: str = Field(
        min_length=1,
        description="Evolution status",
        examples=["in_progress"],
    )


class SkillEvolutionResponse(BaseModel):
    """Skill evolution record returned by the API."""

    evolution_id: str
    skill: str
    current_level: int
    target_level: int
    status: str

    @classmethod
    def from_evolution(cls, evolution: SkillEvolution) -> "SkillEvolutionResponse":
        """Build an API response from a stored skill evolution record."""
        return cls(
            evolution_id=evolution.evolution_id,
            skill=evolution.skill,
            current_level=evolution.current_level,
            target_level=evolution.target_level,
            status=evolution.status,
        )


class UserSkillEvolutionEngineResponse(BaseModel):
    """All skill evolution records for one user."""

    user_id: str
    skill_evolutions: list[SkillEvolutionResponse]
