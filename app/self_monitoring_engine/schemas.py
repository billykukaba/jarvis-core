"""Pydantic schemas for the Self Monitoring Engine."""

from pydantic import BaseModel, ConfigDict, Field


class SelfMonitoringRecord(BaseModel):
    """Self monitoring record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "monitoring_id": "monitor_001",
                    "system_component": "memory_service",
                    "health_status": "degraded",
                    "detected_issue": "Elevated memory usage detected",
                    "performance_score": 72,
                    "risk_level": 45,
                    "recommended_action": "Restart memory cache and review retention policy",
                    "status": "active",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T23:00:00",
                    "updated_at": "2026-06-04T23:10:00",
                }
            ]
        }
    )

    monitoring_id: str = Field(
        min_length=1,
        description="Unique self monitoring record identifier",
        examples=["monitor_001"],
    )
    system_component: str = Field(
        min_length=1,
        description="Jarvis system component being monitored",
        examples=["memory_service"],
    )
    health_status: str = Field(
        min_length=1,
        description="Current health status of the system component",
        examples=["degraded"],
    )
    detected_issue: str = Field(
        min_length=1,
        description="Issue detected during monitoring",
        examples=["Elevated memory usage detected"],
    )
    performance_score: int = Field(
        ge=0,
        le=100,
        description="Performance score of the monitored component",
        examples=[72],
    )
    risk_level: int = Field(
        ge=0,
        le=100,
        description="Risk level associated with the detected issue",
        examples=[45],
    )
    recommended_action: str = Field(
        min_length=1,
        description="Recommended action to resolve the detected issue",
        examples=["Restart memory cache and review retention policy"],
    )
    status: str = Field(
        min_length=1,
        description="Current monitoring record status",
        examples=["active"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Monitoring progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T23:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T23:10:00"],
    )


class SelfMonitoringRecordResponse(BaseModel):
    """Self monitoring record returned by the API."""

    monitoring_id: str
    system_component: str
    health_status: str
    detected_issue: str
    performance_score: int
    risk_level: int
    recommended_action: str
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: SelfMonitoringRecord,
    ) -> "SelfMonitoringRecordResponse":
        """Build an API response from a stored self monitoring record."""
        return cls(
            monitoring_id=record.monitoring_id,
            system_component=record.system_component,
            health_status=record.health_status,
            detected_issue=record.detected_issue,
            performance_score=record.performance_score,
            risk_level=record.risk_level,
            recommended_action=record.recommended_action,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserSelfMonitoringEngineResponse(BaseModel):
    """All self monitoring records for one user."""

    user_id: str
    monitoring_records: list[SelfMonitoringRecordResponse]
