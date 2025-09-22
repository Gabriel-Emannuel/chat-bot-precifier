from transformers import pipeline

from src.settings import Settings

MODEL_DIR = "models"

DEVICE = "cpu"

transcription_pipe = pipeline(
    "automatic-speech-recognition",
    model=f"{MODEL_DIR}/{Settings.transcription_model.replace('/','-')}",
    chunk_length_s=30,
    device=DEVICE,
)
