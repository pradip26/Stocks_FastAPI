from pydantic import BaseModel, Field

class IndexDetails(BaseModel):
    indexcode: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
