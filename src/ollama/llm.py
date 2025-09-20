from langchain_ollama import ChatOllama

from src.settings import Settings

chat = ChatOllama(base_url=Settings.ollama_url, model=Settings.llm_model)
