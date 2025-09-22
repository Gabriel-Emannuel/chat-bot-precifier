from langchain_core.messages import HumanMessage, SystemMessage

from src.graph.schema import CategoryState, ProductState, PriceState
from src.ollama.llm import chat
from src.rag.rag import (
    generate_vector_store,
    web_search_rag,
    generate_documents_from_web,
)

ASSISTANT_IDENTIFY_PRODUCT = SystemMessage(
    content="""Você é um assistente especializado em identificar qual é o produto especificado para busca de preços a partir da entrada.
    
    Exemplos:
    Entrada: Eu quero o preço de um ar condicionado 5500 btu.
    Saída: ar condicionado 5500 btu.
    
    Entrada: Eu preciso de um novo celular, com o objetivo de poder ligar para meus netos.
    Saída: Celular.
    
    Entrada: Estou procurando um fogão para alimentar minha família, com 4 bocas.
    Saída: Fogão 4 bocas"""
)


def generate_price(product_state: ProductState) -> PriceState:
    """Generate price product from product name and query from user.

    Args:
        product_state (ProductState): product from previous stage.

    Returns:
        PriceState: Same state plus price research.
    """

    documents = generate_documents_from_web(product_state["product"])

    vector_store = generate_vector_store(documents)

    retrieval = web_search_rag(vector_store, 10, product_state["query"])

    assistant_rag = SystemMessage(
        content=f"""Você é um assistente especializado em realizar pesquisas de preço. Responda apenas com o preço e onde comprar.
                                  
                                  Utilize esta base de conhecimento: {retrieval}."""
    )

    user_msg = HumanMessage(product_state["query"])

    answer = chat.invoke([assistant_rag, user_msg])

    price = str(answer.content)

    return {"price": price}


def generate_product(category_state: CategoryState) -> ProductState:
    """Generate product from the query from the user.

    Args:
        category_state (CategoryState): category from previous stage.

    Returns:
        ProductState: Same state plus product identified.
    """
    user_msg = HumanMessage(category_state["query"])

    answer = chat.invoke([ASSISTANT_IDENTIFY_PRODUCT, user_msg])

    product = str(answer.content)

    return {
        "category": category_state["category"],
        "product": product,
        "query": category_state["query"],
    }
