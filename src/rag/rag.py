from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from src.rag.web import web_search
from src.ollama.embedding import embeddings


def generate_documents_from_web(product_name: str) -> list[Document]:
    """Generate a document list from product name.

    Args:
        product_name (str): product name.

    Returns:
        list[Document]: document list.
    """

    price_web_search = web_search(product_name)

    price_document = Document(price_web_search)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    all_splits = text_splitter.split_documents([price_document])

    return all_splits


def generate_vector_store(documents: list[Document]) -> FAISS:
    """Generate a vector store from document list.

    Args:
        documents (list[Document]): documents.

    Returns:
        FAISS: vector store.
    """

    vectorstore = FAISS.from_documents(documents, embeddings)

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
