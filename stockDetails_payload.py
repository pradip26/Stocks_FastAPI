from pydantic import BaseModel, Field

class StockDetails(BaseModel):
    symbol: str | None = Field(
        default=None, title="The description of the item", max_length=300
    ),
    industry: str | None = Field(
        default=None, title="The description of the item", max_length=500
    )
