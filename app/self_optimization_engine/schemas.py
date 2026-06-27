"""Pydantic schemas for the Self Optimization Engine."""

from pydantic import BaseModel, ConfigDict, Field


class SelfOptimizationRecord(BaseModel):
    """Self optimization record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "optimization_id": "opt_001",
                    "target_component": "memory_service",
                    "optimization_type": "cache_tuning",
                    "optimization_strategy": "Increase cache TTL and enable lazy eviction",
                    "before_performance_score": 68,
                    "after_performance_score": 89,
                    "optimization_result": "Memory retrieval latency reduced by 35%",
                    "confidence_score": 92,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-05T01:00:00",
                    "updated_at": "2026-06-05T01:20:00",
                }
            ]
        }
    )

    optimization_id: str = Field(
        min_length=1,
        description="Unique self optimization record identifier",
        examples=["opt_001"],
    )
    target_component: str = Field(
        min_length=1,
        description="Jarvis component targeted for optimization",
        examples=["memory_service"],
    )
    optimization_type: str = Field(
        min_length=1,
        description="Type of optimization applied",
        examples=["cache_tuning"],
    )
    optimization_strategy: str = Field(
        min_length=1,
        description="Strategy used to perform the optimization",
        examples=["Increase cache TTL and enable lazy eviction"],
    )
    before_performance_score: int = Field(
        ge=0,
        le=100,
        description="Performance score before optimization",
        examples=[68],
    )
    after_performance_score: int = Field(
        ge=0,
        le=100,
        description="Performance score after optimization",
        examples=[89],
    )
    optimization_result: str = Field(
        min_length=1,
        description="Result of the optimization effort",
        examples=["Memory retrieval latency reduced by 35%"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Confidence score for the optimization analysis",
        examples=[92],
    )
    status: str = Field(
        min_length=1,
        description="Current optimization record status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Optimization progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-05T01:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-05T01:20:00"],
    )


class SelfOptimizationRecordResponse(BaseModel):
    """Self optimization record returned by the API."""

    optimization_id: str
    target_component: str
    optimization_type: str
    optimization_strategy: str
    before_performance_score: int
    after_performance_score: int
    optimization_result: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: SelfOptimizationRecord,
    ) -> "SelfOptimizationRecordResponse":
        """Build an API response from a stored self optimization record."""
        return cls(
            optimization_id=record.optimization_id,
            target_component=record.target_component,
            optimization_type=record.optimization_type,
            optimization_strategy=record.optimization_strategy,
            before_performance_score=record.before_performance_score,
            after_performance_score=record.after_performance_score,
            optimization_result=record.optimization_result,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserSelfOptimizationEngineResponse(BaseModel):
    """All self optimization records for one user."""

    user_id: str
    optimization_records: list[SelfOptimizationRecordResponse]
