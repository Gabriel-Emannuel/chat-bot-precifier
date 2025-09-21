from ollama import Client

from time import sleep

from dotenv import load_dotenv

from os import getenv

load_dotenv()

OLLAMA_URL = str(getenv("OLLAMA_URL"))
LLM_MODEL = str(getenv("LLM_MODEL"))
EMBEDDING_MODEL = str(getenv("EMBEDDING_MODEL"))

cliente = Client(host=OLLAMA_URL)

cliente.pull(LLM_MODEL)
cliente.pull(EMBEDDING_MODEL)
