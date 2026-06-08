"""FastAPI routes for the Portfolio Service (Module 60)."""



from urllib.parse import unquote



from fastapi import APIRouter, HTTPException, status



from app.portfolio.portfolio_service_engine import normalize_title

from app.portfolio.schemas import (

    PortfolioRecord,

    PortfolioRecordResponse,

    UserPortfolioResponse,

)

from app.services.engine_registry import portfolio_service_engine



# Router exposed to FastAPI as portfolio_router in main.py.

portfolio_router = APIRouter(tags=["portfolio"])





def parse_path_title(title: str) -> str:

    """Decode URL path titles so spaces work in GET, PUT, and DELETE."""

    return unquote(title.replace("+", " "))





@portfolio_router.post(

    "/portfolio/{user_id}",

    response_model=PortfolioRecordResponse,

    summary="Create portfolio record",

    description="Create a new portfolio item record for the specified user.",

)

async def create_portfolio_record(

    user_id: str,

    request: PortfolioRecord,

) -> PortfolioRecordResponse:

    """Create and return a portfolio record."""

    if portfolio_service_engine.title_exists(user_id, request.title):

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Portfolio item already exists",

        )



    record = portfolio_service_engine.create_record(user_id, request)

    return PortfolioRecordResponse.from_record(record)





@portfolio_router.get(

    "/portfolio/{user_id}",

    response_model=UserPortfolioResponse,

    summary="Get all portfolio records",

    description="Return all portfolio item records saved by the specified user.",

)

async def get_portfolio_records(user_id: str) -> UserPortfolioResponse:

    """Return all portfolio records for a user."""

    records = portfolio_service_engine.get_records(user_id)

    return UserPortfolioResponse(

        user_id=user_id,

        portfolio=[

            PortfolioRecordResponse.from_record(record) for record in records

        ],

    )





@portfolio_router.get(

    "/portfolio/{user_id}/{title}",

    response_model=PortfolioRecordResponse,

    summary="Get one portfolio record",

    description="Return one portfolio item record identified by title.",

)

async def get_portfolio_record(

    user_id: str,

    title: str,

) -> PortfolioRecordResponse:

    """Return a single portfolio record by title."""

    decoded_title = parse_path_title(title)

    record = portfolio_service_engine.get_record(user_id, decoded_title)

    if record is None:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Portfolio item not found",

        )



    return PortfolioRecordResponse.from_record(record)





@portfolio_router.put(

    "/portfolio/{user_id}/{title}",

    response_model=PortfolioRecordResponse,

    status_code=status.HTTP_200_OK,

    summary="Update portfolio record",

    description="Replace an existing portfolio item record with updated data.",

)

async def update_portfolio_record(

    user_id: str,

    title: str,

    request: PortfolioRecord,

) -> PortfolioRecordResponse:

    """Update and return a portfolio record."""

    decoded_title = parse_path_title(title)



    # Allow keeping the same title while changing url/category.

    if normalize_title(request.title) != normalize_title(decoded_title):

        if portfolio_service_engine.title_exists(user_id, request.title):

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Portfolio item already exists",

            )



    record = portfolio_service_engine.update_record(

        user_id,

        decoded_title,

        request,

    )

    if record is None:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Portfolio item not found",

        )



    return PortfolioRecordResponse.from_record(record)





@portfolio_router.delete(

    "/portfolio/{user_id}/{title}",

    response_model=PortfolioRecordResponse,

    summary="Delete portfolio record",

    description="Delete a portfolio item record and return the removed record.",

)

async def delete_portfolio_record(

    user_id: str,

    title: str,

) -> PortfolioRecordResponse:

    """Delete a portfolio record and return the deleted item."""

    decoded_title = parse_path_title(title)

    record = portfolio_service_engine.delete_record(user_id, decoded_title)

    if record is None:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Portfolio item not found",

        )



    return PortfolioRecordResponse.from_record(record)


