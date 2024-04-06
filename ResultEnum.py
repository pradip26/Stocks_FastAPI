from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

#ref URL for enum : https://www.getorchestra.io/guides/fastapi-enum-classes-using-python-enum-for-field-values

class resultEnum(Enum):
    ALL = 'all'
    RECENT = 'recent'

class ResultInfo(BaseModel):
    symbol: str | None = Field(
        default=None, title="The description of the item", max_length=300
    ),
    result_type: Optional[resultEnum] = Field(default=resultEnum.ALL,validate_default=True)
