"""FastAPI routes for the Languages Service."""

from fastapi import APIRouter, HTTPException, status

from app.languages.schemas import (
    Language,
    LanguageResponse,
    UserLanguagesResponse,
)
from app.services.engine_registry import language_service_engine

# Router exposed to FastAPI as languages_router in main.py.
languages_router = APIRouter(tags=["languages"])


@languages_router.post(
    "/languages/{user_id}",
    response_model=LanguageResponse,
    summary="Create language record",
    description="Create a new language proficiency record for the specified user.",
)
async def create_language(
    user_id: str,
    request: Language,
) -> LanguageResponse:
    """Create and return a language record."""
    if language_service_engine.language_exists(user_id, request.language):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language already exists",
        )

    language = language_service_engine.create_language(user_id, request)
    return LanguageResponse.from_language(language)


@languages_router.get(
    "/languages/{user_id}",
    response_model=UserLanguagesResponse,
    summary="Get all language records",
    description="Return all language records saved by the specified user.",
)
async def get_languages(user_id: str) -> UserLanguagesResponse:
    """Return all language records for a user."""
    languages = language_service_engine.get_languages(user_id)
    return UserLanguagesResponse(
        user_id=user_id,
        languages=[
            LanguageResponse.from_language(language) for language in languages
        ],
    )


@languages_router.get(
    "/languages/{user_id}/{language}",
    response_model=LanguageResponse,
    summary="Get one language record",
    description="Return one language record identified by language name.",
)
async def get_language(user_id: str, language: str) -> LanguageResponse:
    """Return a single language record by language name."""
    record = language_service_engine.get_language(user_id, language)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Language not found",
        )

    return LanguageResponse.from_language(record)


@languages_router.put(
    "/languages/{user_id}/{language}",
    response_model=LanguageResponse,
    summary="Update language record",
    description="Replace an existing language record with updated data.",
)
async def update_language(
    user_id: str,
    language: str,
    request: Language,
) -> LanguageResponse:
    """Update and return a language record."""
    if (
        request.language.lower() != language.lower()
        and language_service_engine.language_exists(user_id, request.language)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language already exists",
        )

    record = language_service_engine.update_language(user_id, language, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Language not found",
        )

    return LanguageResponse.from_language(record)


@languages_router.delete(
    "/languages/{user_id}/{language}",
    response_model=LanguageResponse,
    summary="Delete language record",
    description="Delete a language record and return the removed record.",
)
async def delete_language(user_id: str, language: str) -> LanguageResponse:
    """Delete a language record and return the deleted item."""
    record = language_service_engine.delete_language(user_id, language)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Language not found",
        )

    return LanguageResponse.from_language(record)
