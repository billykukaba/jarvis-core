"""FastAPI routes for the Certifications Service."""

from fastapi import APIRouter, HTTPException, status

from app.certifications.schemas import (
    Certification,
    CertificationResponse,
    UserCertificationsResponse,
)
from app.services.engine_registry import certification_service_engine

# Router exposed to FastAPI as certifications_router in main.py.
certifications_router = APIRouter(tags=["certifications"])


@certifications_router.post(
    "/certifications/{user_id}",
    response_model=CertificationResponse,
    summary="Create certification record",
    description="Create a new certification record for the specified user.",
)
async def create_certification(
    user_id: str,
    request: Certification,
) -> CertificationResponse:
    """Create and return a certification record."""
    if certification_service_engine.name_exists(user_id, request.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certification already exists",
        )

    certification = certification_service_engine.create_certification(
        user_id,
        request,
    )
    return CertificationResponse.from_certification(certification)


@certifications_router.get(
    "/certifications/{user_id}",
    response_model=UserCertificationsResponse,
    summary="Get all certification records",
    description="Return all certification records saved by the specified user.",
)
async def get_certifications(user_id: str) -> UserCertificationsResponse:
    """Return all certification records for a user."""
    certifications = certification_service_engine.get_certifications(user_id)
    return UserCertificationsResponse(
        user_id=user_id,
        certifications=[
            CertificationResponse.from_certification(certification)
            for certification in certifications
        ],
    )


@certifications_router.get(
    "/certifications/{user_id}/{name}",
    response_model=CertificationResponse,
    summary="Get one certification record",
    description="Return one certification record identified by name.",
)
async def get_certification(user_id: str, name: str) -> CertificationResponse:
    """Return a single certification record by name."""
    certification = certification_service_engine.get_certification(user_id, name)
    if certification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found",
        )

    return CertificationResponse.from_certification(certification)


@certifications_router.put(
    "/certifications/{user_id}/{name}",
    response_model=CertificationResponse,
    summary="Update certification record",
    description="Replace an existing certification record with updated data.",
)
async def update_certification(
    user_id: str,
    name: str,
    request: Certification,
) -> CertificationResponse:
    """Update and return a certification record."""
    if (
        request.name.lower() != name.lower()
        and certification_service_engine.name_exists(user_id, request.name)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certification already exists",
        )

    certification = certification_service_engine.update_certification(
        user_id,
        name,
        request,
    )
    if certification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found",
        )

    return CertificationResponse.from_certification(certification)


@certifications_router.delete(
    "/certifications/{user_id}/{name}",
    response_model=CertificationResponse,
    summary="Delete certification record",
    description="Delete a certification record and return the removed record.",
)
async def delete_certification(user_id: str, name: str) -> CertificationResponse:
    """Delete a certification record and return the deleted item."""
    certification = certification_service_engine.delete_certification(user_id, name)
    if certification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found",
        )

    return CertificationResponse.from_certification(certification)
