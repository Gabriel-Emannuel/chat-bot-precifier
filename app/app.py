from fastapi import FastAPI

from app.requests import PriceRequestDto
from app.responses import PriceResponseDto
from src.graph.graph import graph

app = FastAPI()


@app.post("/get-price")
def get_price(price_request: PriceRequestDto) -> PriceResponseDto:
    answer = graph.invoke(price_request.model_dump())  # type: ignore
    return PriceResponseDto(answer=answer["answer"])
