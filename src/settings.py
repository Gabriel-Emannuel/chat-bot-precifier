from dotenv import load_dotenv

from os import getenv

LLM_MODEL = getenv("LLM_MODEL")

if not LLM_MODEL:
    load_dotenv()

    LLM_MODEL = str(getenv("LLM_MODEL"))

EMBEDDING_MODEL = str(getenv("EMBEDDING_MODEL"))
OLLAMA_URL = str(getenv("OLLAMA_URL"))


class Settings:
    llm_model = LLM_MODEL
    embedding_model = EMBEDDING_MODEL
    ollama_url = OLLAMA_URL
