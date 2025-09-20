from langchain_ollama import OllamaEmbeddings

from src.settings import Settings

embeddings = OllamaEmbeddings(
    base_url=Settings.ollama_url, model=Settings.embedding_model
)
