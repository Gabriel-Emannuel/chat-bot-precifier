from fastapi import FastAPI, UploadFile

from app.requests import PriceRequestDto
from app.responses import PriceResponseDto
from src.graph.graph import graph
from src.transformers.transcription import transcription_pipe
from src.utils import save_temp_file, remove_temp_file

app = FastAPI()


@app.post("/get-price")
def get_price(price_request: PriceRequestDto) -> PriceResponseDto:
    answer = graph.invoke(price_request.model_dump())  # type: ignore
    return PriceResponseDto(answer=answer["answer"])


@app.post("/get-price-audio")
def get_price_audio(price: UploadFile) -> PriceResponseDto:
    file_path = save_temp_file(price)
    transcription = transcription_pipe(file_path)
    remove_temp_file(file_path)
    answer = graph.invoke({"query": transcription["transcription"]["text"]})  # type: ignore
    return PriceResponseDto(answer=answer["answer"])
