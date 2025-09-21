from pydantic import BaseModel


class PriceRequestDto(BaseModel):
    query: str
