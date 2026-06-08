"""Pydantic schemas for the Contact Service."""

from pydantic import BaseModel, Field


class Contact(BaseModel):
    """Contact data stored for a user."""

    name: str = Field(min_length=1, description="Contact full name")
    email: str = Field(min_length=1, description="Contact email address")
    phone: str = Field(min_length=1, description="Contact phone number")
    role: str = Field(min_length=1, description="Contact role or relationship")


class ContactResponse(BaseModel):
    """Contact returned by the API."""

    name: str
    email: str
    phone: str
    role: str

    @classmethod
    def from_contact(cls, contact: Contact) -> "ContactResponse":
        """Build an API response from a stored contact."""
        return cls(
            name=contact.name,
            email=contact.email,
            phone=contact.phone,
            role=contact.role,
        )


class UserContactsResponse(BaseModel):
    """All contacts for one user."""

    user_id: str
    contacts: list[ContactResponse]
