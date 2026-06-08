"""Contact engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.contacts.schemas import Contact

# In-memory contact store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "name": "John Doe",
#             "email": "john@gmail.com",
#             "phone": "+243123456789",
#             "role": "Mentor",
#         }
#     ]
# }
contacts_db: dict[str, list[Contact]] = {}


class ContactEngine:
    """Manage user contacts stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def create_contact(self, user_id: str, contact: Contact) -> Contact:
        """Create and store a contact for the given user."""
        with self._lock:
            user_contacts = contacts_db.setdefault(user_id, [])
            user_contacts.append(contact)

        return contact

    def get_contacts(self, user_id: str) -> list[Contact]:
        """Return all contacts for the given user."""
        with self._lock:
            return list(contacts_db.get(user_id, []))

    def get_contact(self, user_id: str, name: str) -> Contact | None:
        """Return one contact by name for the given user."""
        with self._lock:
            return self._find_contact(user_id, name)

    def update_contact(
        self,
        user_id: str,
        name: str,
        contact: Contact,
    ) -> Contact | None:
        """Replace an existing contact with a new version."""
        with self._lock:
            user_contacts = contacts_db.get(user_id)
            if user_contacts is None:
                return None

            index = self._find_contact_index(user_contacts, name)
            if index is None:
                return None

            user_contacts[index] = contact

        return contact

    def delete_contact(self, user_id: str, name: str) -> Contact | None:
        """Delete and return a contact by name."""
        with self._lock:
            user_contacts = contacts_db.get(user_id)
            if user_contacts is None:
                return None

            index = self._find_contact_index(user_contacts, name)
            if index is None:
                return None

            return user_contacts.pop(index)

    def _find_contact(self, user_id: str, name: str) -> Contact | None:
        """Locate a contact in the user's list by name."""
        user_contacts = contacts_db.get(user_id, [])
        index = self._find_contact_index(user_contacts, name)
        if index is None:
            return None
        return user_contacts[index]

    @staticmethod
    def _find_contact_index(user_contacts: list[Contact], name: str) -> int | None:
        """Return the list index for a contact name, if it exists."""
        normalized_name = name.lower()
        for index, contact in enumerate(user_contacts):
            if contact.name.lower() == normalized_name:
                return index
        return None
