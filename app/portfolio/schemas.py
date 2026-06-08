"""Pydantic schemas for the Portfolio Service (Module 60)."""



from pydantic import BaseModel, ConfigDict, Field





class PortfolioRecord(BaseModel):

    """Portfolio item record stored for a user."""



    model_config = ConfigDict(

        json_schema_extra={

            "examples": [

                {

                    "title": "AI Social Network",

                    "url": "https://github.com/billy/funet",

                    "category": "Web Development",

                }

            ]

        }

    )



    title: str = Field(

        min_length=1,

        description="Portfolio item title",

        examples=["AI Social Network"],

    )

    url: str = Field(

        min_length=1,

        description="Project or work sample URL",

        examples=["https://github.com/billy/funet"],

    )

    category: str = Field(

        min_length=1,

        description="Portfolio category or type",

        examples=["Web Development"],

    )





class PortfolioRecordResponse(BaseModel):

    """Portfolio item record returned by the API."""



    title: str

    url: str

    category: str



    @classmethod

    def from_record(cls, record: PortfolioRecord) -> "PortfolioRecordResponse":

        """Build an API response from a stored portfolio record."""

        return cls(

            title=record.title,

            url=record.url,

            category=record.category,

        )





class UserPortfolioResponse(BaseModel):

    """All portfolio records for one user."""



    user_id: str

    portfolio: list[PortfolioRecordResponse]


