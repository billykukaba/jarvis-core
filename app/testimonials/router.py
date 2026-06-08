"""FastAPI routes for the Testimonials Service (Module 61)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.testimonials.schemas import (
    TestimonialRecord,
    TestimonialRecordResponse,
    UserTestimonialsResponse,
)
from app.testimonials.testimonial_service_engine import normalize_name
from app.services.engine_registry import testimonial_service_engine

# Router exposed to FastAPI as testimonials_router in main.py.
testimonials_router = APIRouter(tags=["testimonials"])


def parse_path_name(name: str) -> str:
    """Decode URL path names so spaces work in GET, PUT, and DELETE."""
    return unquote(name.replace("+", " "))


@testimonials_router.post(
    "/testimonials/{user_id}",
    response_model=TestimonialRecordResponse,
    summary="Create testimonial record",
    description="Create a new testimonial record for the specified user.",
)
async def create_testimonial_record(
    user_id: str,
    request: TestimonialRecord,
) -> TestimonialRecordResponse:
    """Create and return a testimonial record."""
    if testimonial_service_engine.name_exists(user_id, request.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Testimonial already exists",
        )

    record = testimonial_service_engine.create_record(user_id, request)
    return TestimonialRecordResponse.from_record(record)


@testimonials_router.get(
    "/testimonials/{user_id}",
    response_model=UserTestimonialsResponse,
    summary="Get all testimonial records",
    description="Return all testimonial records saved by the specified user.",
)
async def get_testimonial_records(user_id: str) -> UserTestimonialsResponse:
    """Return all testimonial records for a user."""
    records = testimonial_service_engine.get_records(user_id)
    return UserTestimonialsResponse(
        user_id=user_id,
        testimonials=[
            TestimonialRecordResponse.from_record(record) for record in records
        ],
    )


@testimonials_router.get(
    "/testimonials/{user_id}/{name}",
    response_model=TestimonialRecordResponse,
    summary="Get one testimonial record",
    description="Return one testimonial record identified by name.",
)
async def get_testimonial_record(
    user_id: str,
    name: str,
) -> TestimonialRecordResponse:
    """Return a single testimonial record by name."""
    decoded_name = parse_path_name(name)
    record = testimonial_service_engine.get_record(user_id, decoded_name)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial not found",
        )

    return TestimonialRecordResponse.from_record(record)


@testimonials_router.put(
    "/testimonials/{user_id}/{name}",
    response_model=TestimonialRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update testimonial record",
    description="Replace an existing testimonial record with updated data.",
)
async def update_testimonial_record(
    user_id: str,
    name: str,
    request: TestimonialRecord,
) -> TestimonialRecordResponse:
    """Update and return a testimonial record."""
    decoded_name = parse_path_name(name)

    # Allow keeping the same name while changing role/message.
    if normalize_name(request.name) != normalize_name(decoded_name):
        if testimonial_service_engine.name_exists(user_id, request.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Testimonial already exists",
            )

    record = testimonial_service_engine.update_record(
        user_id,
        decoded_name,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial not found",
        )

    return TestimonialRecordResponse.from_record(record)


@testimonials_router.delete(
    "/testimonials/{user_id}/{name}",
    response_model=TestimonialRecordResponse,
    summary="Delete testimonial record",
    description="Delete a testimonial record and return the removed record.",
)
async def delete_testimonial_record(
    user_id: str,
    name: str,
) -> TestimonialRecordResponse:
    """Delete a testimonial record and return the deleted item."""
    decoded_name = parse_path_name(name)
    record = testimonial_service_engine.delete_record(user_id, decoded_name)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial not found",
        )

    return TestimonialRecordResponse.from_record(record)
