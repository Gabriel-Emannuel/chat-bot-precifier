from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from src.rag.web import web_search
from src.ollama.embedding import embeddings


def generate_vector_store(product_name: str) -> FAISS:
    """Generate a vector store from product name.

    Args:
        product_name (str): product name.

    Returns:
        FAISS: vector store.
    """

    price_web_search = web_search(product_name)

    price_document = Document(price_web_search)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    all_splits = text_splitter.split_documents([price_document])

    vectorstore = FAISS.from_documents(all_splits, embeddings)

    return vectorstore


def web_search_rag(vectorstore: FAISS, k: int, query: str) -> str:
    """Web search the query from the user on vectorstore from prices.

    Args:
        vectorstore (FAISS): vector store with all search.
        k (int): Define how many items will be on the search.
        query (str): query from user.

    Returns:
        str: The result from the web search from rag.
    """

    retrieval = vectorstore.similarity_search(query, k)

    all_contents = [document.page_content for document in retrieval]

    return "\n\n".join(all_contents)
