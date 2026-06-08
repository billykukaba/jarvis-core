"""FastAPI routes for the Contact Service."""

from fastapi import APIRouter, HTTPException, status

from app.contacts.schemas import Contact, ContactResponse, UserContactsResponse
from app.services.engine_registry import contact_engine

# Router exposed to FastAPI as contacts_router in main.py.
contacts_router = APIRouter(tags=["contacts"])


@contacts_router.post(
    "/contacts/{user_id}",
    response_model=ContactResponse,
    summary="Create contact",
    description="Create a new contact for the specified user.",
)
async def create_contact(user_id: str, request: Contact) -> ContactResponse:
    """Create and return a contact."""
    contact = contact_engine.create_contact(user_id, request)
    return ContactResponse.from_contact(contact)


@contacts_router.get(
    "/contacts/{user_id}",
    response_model=UserContactsResponse,
    summary="Get all contacts",
    description="Return all contacts saved by the specified user.",
)
async def get_contacts(user_id: str) -> UserContactsResponse:
    """Return all contacts for a user."""
    contacts = contact_engine.get_contacts(user_id)
    return UserContactsResponse(
        user_id=user_id,
        contacts=[ContactResponse.from_contact(contact) for contact in contacts],
    )


@contacts_router.get(
    "/contacts/{user_id}/{name}",
    response_model=ContactResponse,
    summary="Get one contact",
    description="Return one contact identified by name.",
)
async def get_contact(user_id: str, name: str) -> ContactResponse:
    """Return a single contact by name."""
    contact = contact_engine.get_contact(user_id, name)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return ContactResponse.from_contact(contact)


@contacts_router.put(
    "/contacts/{user_id}/{name}",
    response_model=ContactResponse,
    summary="Update contact",
    description="Replace an existing contact with updated data.",
)
async def update_contact(
    user_id: str,
    name: str,
    request: Contact,
) -> ContactResponse:
    """Update and return a contact."""
    contact = contact_engine.update_contact(user_id, name, request)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return ContactResponse.from_contact(contact)


@contacts_router.delete(
    "/contacts/{user_id}/{name}",
    response_model=ContactResponse,
    summary="Delete contact",
    description="Delete a contact and return the removed contact.",
)
async def delete_contact(user_id: str, name: str) -> ContactResponse:
    """Delete a contact and return the deleted item."""
    contact = contact_engine.delete_contact(user_id, name)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return ContactResponse.from_contact(contact)
