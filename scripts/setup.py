from ollama import Client
from huggingface_hub import snapshot_download

from dotenv import load_dotenv

from os import getenv, mkdir
from os.path import exists

MODEL_DIR = "models"

load_dotenv()

TRANSCRIPTION_MODEL = str(getenv("TRANSCRIPTION_MODEL"))
OLLAMA_URL = str(getenv("OLLAMA_URL"))
LLM_MODEL = str(getenv("LLM_MODEL"))
EMBEDDING_MODEL = str(getenv("EMBEDDING_MODEL"))

if not exists(MODEL_DIR):
    mkdir(MODEL_DIR)

client = Client(host=OLLAMA_URL)

client.pull(LLM_MODEL)
client.pull(EMBEDDING_MODEL)

snapshot_download(
    TRANSCRIPTION_MODEL, local_dir=f"{MODEL_DIR}/{TRANSCRIPTION_MODEL.replace('/','-')}"
)
