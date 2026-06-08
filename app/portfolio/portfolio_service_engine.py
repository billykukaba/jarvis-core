"""Portfolio Service engine with thread-safe in-memory storage."""



from __future__ import annotations



from threading import Lock



from app.portfolio.schemas import PortfolioRecord



# In-memory portfolio store keyed by user_id.

# Example:

# {

#     "billy": [

#         {

#             "title": "AI Social Network",

#             "url": "https://github.com/billy/funet",

#             "category": "Web Development",

#         }

#     ]

# }

portfolio_db: dict[str, list[PortfolioRecord]] = {}





def normalize_title(title: str) -> str:

    """Normalize a title for case-insensitive, whitespace-tolerant lookups."""

    return title.strip().lower()





class PortfolioServiceEngine:

    """Manage user portfolio records stored in memory."""



    def __init__(self) -> None:

        self._lock = Lock()



    def title_exists(self, user_id: str, title: str) -> bool:

        """Return True if a portfolio item with this title already exists."""

        with self._lock:

            return self._find_record_index(

                portfolio_db.get(user_id, []),

                title,

            ) is not None



    def create_record(self, user_id: str, record: PortfolioRecord) -> PortfolioRecord:

        """Create and store a portfolio record for the given user."""

        with self._lock:

            user_records = portfolio_db.setdefault(user_id, [])

            user_records.append(record)



        return record



    def get_records(self, user_id: str) -> list[PortfolioRecord]:

        """Return all portfolio records for the given user."""

        with self._lock:

            return list(portfolio_db.get(user_id, []))



    def get_record(self, user_id: str, title: str) -> PortfolioRecord | None:

        """Return one portfolio record by title for the given user."""

        with self._lock:

            return self._find_record(user_id, title)



    def update_record(

        self,

        user_id: str,

        title: str,

        record: PortfolioRecord,

    ) -> PortfolioRecord | None:

        """Replace an existing portfolio record with a new version."""

        with self._lock:

            user_records = portfolio_db.get(user_id)

            if user_records is None:

                return None



            index = self._find_record_index(user_records, title)

            if index is None:

                return None



            user_records[index] = record



        return record



    def delete_record(self, user_id: str, title: str) -> PortfolioRecord | None:

        """Delete and return a portfolio record by title."""

        with self._lock:

            user_records = portfolio_db.get(user_id)

            if user_records is None:

                return None



            index = self._find_record_index(user_records, title)

            if index is None:

                return None



            return user_records.pop(index)



    def _find_record(self, user_id: str, title: str) -> PortfolioRecord | None:

        """Locate a portfolio record in the user's list by title."""

        user_records = portfolio_db.get(user_id, [])

        index = self._find_record_index(user_records, title)

        if index is None:

            return None

        return user_records[index]



    @staticmethod

    def _find_record_index(

        user_records: list[PortfolioRecord],

        title: str,

    ) -> int | None:

        """Return the list index for a portfolio title, if it exists."""

        normalized_title = normalize_title(title)

        for index, record in enumerate(user_records):

            if normalize_title(record.title) == normalized_title:

                return index

        return None


