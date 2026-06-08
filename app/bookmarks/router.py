"""FastAPI routes for the Bookmark Service."""

from fastapi import APIRouter, HTTPException, status

from app.bookmarks.schemas import Bookmark, BookmarkResponse, UserBookmarksResponse
from app.services.engine_registry import bookmark_engine

# Router exposed to FastAPI as bookmarks_router in main.py.
bookmarks_router = APIRouter(tags=["bookmarks"])


@bookmarks_router.post(
    "/bookmarks/{user_id}",
    response_model=BookmarkResponse,
    summary="Create bookmark",
    description="Create a new bookmark for the specified user.",
)
async def create_bookmark(user_id: str, request: Bookmark) -> BookmarkResponse:
    """Create and return a bookmark."""
    bookmark = bookmark_engine.create_bookmark(user_id, request)
    return BookmarkResponse.from_bookmark(bookmark)


@bookmarks_router.get(
    "/bookmarks/{user_id}",
    response_model=UserBookmarksResponse,
    summary="Get all bookmarks",
    description="Return all bookmarks saved by the specified user.",
)
async def get_bookmarks(user_id: str) -> UserBookmarksResponse:
    """Return all bookmarks for a user."""
    bookmarks = bookmark_engine.get_bookmarks(user_id)
    return UserBookmarksResponse(
        user_id=user_id,
        bookmarks=[BookmarkResponse.from_bookmark(bookmark) for bookmark in bookmarks],
    )


@bookmarks_router.get(
    "/bookmarks/{user_id}/{title}",
    response_model=BookmarkResponse,
    summary="Get bookmark by title",
    description="Return one bookmark identified by its title.",
)
async def get_bookmark(user_id: str, title: str) -> BookmarkResponse:
    """Return a single bookmark by title."""
    bookmark = bookmark_engine.get_bookmark(user_id, title)
    if bookmark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found",
        )

    return BookmarkResponse.from_bookmark(bookmark)


@bookmarks_router.put(
    "/bookmarks/{user_id}/{title}",
    response_model=BookmarkResponse,
    summary="Update bookmark",
    description="Replace an existing bookmark with updated data.",
)
async def update_bookmark(
    user_id: str,
    title: str,
    request: Bookmark,
) -> BookmarkResponse:
    """Update and return a bookmark."""
    bookmark = bookmark_engine.update_bookmark(user_id, title, request)
    if bookmark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found",
        )

    return BookmarkResponse.from_bookmark(bookmark)


@bookmarks_router.delete(
    "/bookmarks/{user_id}/{title}",
    response_model=BookmarkResponse,
    summary="Delete bookmark",
    description="Delete a bookmark and return the removed bookmark.",
)
async def delete_bookmark(user_id: str, title: str) -> BookmarkResponse:
    """Delete a bookmark and return the deleted item."""
    bookmark = bookmark_engine.delete_bookmark(user_id, title)
    if bookmark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found",
        )

    return BookmarkResponse.from_bookmark(bookmark)
