from pydantic import BaseModel


class PriceResponseDto(BaseModel):
    answer: str
