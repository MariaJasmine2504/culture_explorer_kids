from pydantic import BaseModel, field_validator
from typing import Optional

class CultureQuery(BaseModel):
    country_or_culture: str
    my_culture: Optional[str] = None

    @field_validator('country_or_culture')
    @classmethod
    def non_empty(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("Please enter a country or culture.")
        if len(v) > 60:
            raise ValueError("Keep it short (max 60 chars).")
        return v

    @field_validator('my_culture')
    @classmethod
    def trim_optional(cls, v: Optional[str]):
        return v.strip() if v else v
