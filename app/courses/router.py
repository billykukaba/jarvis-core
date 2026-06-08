"""FastAPI routes for the Courses Service (Module 58)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.courses.course_service_engine import normalize_title
from app.courses.schemas import (
    CourseRecord,
    CourseRecordResponse,
    UserCoursesResponse,
)
from app.services.engine_registry import course_service_engine

# Router exposed to FastAPI as courses_router in main.py.
courses_router = APIRouter(tags=["courses"])


def parse_path_title(title: str) -> str:
    """Decode URL path titles so spaces work in GET, PUT, and DELETE."""
    return unquote(title.replace("+", " "))


@courses_router.post(
    "/courses/{user_id}",
    response_model=CourseRecordResponse,
    summary="Create course record",
    description="Create a new online course record for the specified user.",
)
async def create_course_record(
    user_id: str,
    request: CourseRecord,
) -> CourseRecordResponse:
    """Create and return a course record."""
    if course_service_engine.title_exists(user_id, request.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course already exists",
        )

    record = course_service_engine.create_record(user_id, request)
    return CourseRecordResponse.from_record(record)


@courses_router.get(
    "/courses/{user_id}",
    response_model=UserCoursesResponse,
    summary="Get all course records",
    description="Return all course records saved by the specified user.",
)
async def get_course_records(user_id: str) -> UserCoursesResponse:
    """Return all course records for a user."""
    records = course_service_engine.get_records(user_id)
    return UserCoursesResponse(
        user_id=user_id,
        courses=[CourseRecordResponse.from_record(record) for record in records],
    )


@courses_router.get(
    "/courses/{user_id}/{title}",
    response_model=CourseRecordResponse,
    summary="Get one course record",
    description="Return one course record identified by title.",
)
async def get_course_record(user_id: str, title: str) -> CourseRecordResponse:
    """Return a single course record by title."""
    decoded_title = parse_path_title(title)
    record = course_service_engine.get_record(user_id, decoded_title)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    return CourseRecordResponse.from_record(record)


@courses_router.put(
    "/courses/{user_id}/{title}",
    response_model=CourseRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update course record",
    description="Replace an existing course record with updated data.",
)
async def update_course_record(
    user_id: str,
    title: str,
    request: CourseRecord,
) -> CourseRecordResponse:
    """Update and return a course record."""
    decoded_title = parse_path_title(title)

    # Allow keeping the same title while changing platform/year.
    if normalize_title(request.title) != normalize_title(decoded_title):
        if course_service_engine.title_exists(user_id, request.title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course already exists",
            )

    record = course_service_engine.update_record(user_id, decoded_title, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    return CourseRecordResponse.from_record(record)


@courses_router.delete(
    "/courses/{user_id}/{title}",
    response_model=CourseRecordResponse,
    summary="Delete course record",
    description="Delete a course record and return the removed record.",
)
async def delete_course_record(user_id: str, title: str) -> CourseRecordResponse:
    """Delete a course record and return the deleted item."""
    decoded_title = parse_path_title(title)
    record = course_service_engine.delete_record(user_id, decoded_title)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    return CourseRecordResponse.from_record(record)
