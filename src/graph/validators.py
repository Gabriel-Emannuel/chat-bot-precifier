from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from re import search
from typing import Literal

from src.graph.schema import InputState, CategoryState, OutputState, PriceState
from src.ollama.llm import chat

PATTERN_INVALID_CATEGORY = r"(Entrada inválida.)"

ASSISTANT_IDENTIFIER_CATEGORY = SystemMessage(
    content="""Você é um assistente especializado em identificar se a entrada recebida é passível de processamento. Para uma entrada ser processada, é necessário que ela possa ser utilizada para buscar preços. Para verificar se uma entrada pode ser usada para buscar preços, verifique se a entrada pode participar das seguintes categorias:
    
    Categorias válidas:
    - Celular;
    - Televisão;
    - Lavador;
    - Notebook;
    - Geladeira;
    - Ar-Condicionado;
    - Fogão;
    - Eletrodomésticos;
    - Eletroportáteis;
    - Informática.
    
    Caso a entrada participe de quaisquer categoria, pode ser considerada uma entrada válida. Se este for o caso, especifique a categoria. Se não, apenas especifique que não é uma entrada válida e não gere uma resposta."""
)

USER_IDENTIFIER_CATEGORY_FEW_SHOT_1 = HumanMessage(
    content="Qual a idade do atual presidente do brasil?"
)

AI_IDENTIFIER_CATEGORY_FEW_SHOT_1 = AIMessage(content="Entrada inválida.")

USER_IDENTIFIER_CATEGORY_FEW_SHOT_2 = HumanMessage(
    content="Qual o preço de um ar condicionado?"
)

AI_IDENTIFIER_CATEGORY_FEW_SHOT_2 = AIMessage(content="Categoria: Ar-condicionado.")

USER_IDENTIFIER_CATEGORY_FEW_SHOT_3 = HumanMessage(content="Qual o preço de um carro?")

AI_IDENTIFIER_CATEGORY_FEW_SHOT_3 = AIMessage(content="Entrada inválida.")

USER_IDENTIFIER_CATEGORY_FEW_SHOT_4 = HumanMessage(content="Qual é o motivo da chuva?")

AI_IDENTIFIER_CATEGORY_FEW_SHOT_4 = AIMessage(content="Entrada inválida.")

PATTERN_URL = r"(www.zoom.com.br)"


def generate_answer(price_state: PriceState) -> OutputState:
    """Generate a response with the source URL of the research

    Args:
        price_state (PriceState): State containing query from user, product and price research.

    Returns:
        OutputState: Answer for the user. This answer has the source URL.
    """
    if search(PATTERN_URL, price_state["price"]):
        return {"answer": price_state["price"]}

    answer = price_state["price"] + "\n" + "Fonte: " + "www.zoom.com.br."

    return {"answer": str(answer)}


def generate_category(input_state: InputState) -> CategoryState:
    """Generate category product from user query.

    Args:
        input_state (InputState): input from the user.

    Returns:
        CategoryState: Same state from the input plus the category.
    """
    user_msg = HumanMessage(content=input_state["query"])

    answer = chat.invoke(
        [
            ASSISTANT_IDENTIFIER_CATEGORY,
            USER_IDENTIFIER_CATEGORY_FEW_SHOT_1,
            AI_IDENTIFIER_CATEGORY_FEW_SHOT_1,
            USER_IDENTIFIER_CATEGORY_FEW_SHOT_2,
            AI_IDENTIFIER_CATEGORY_FEW_SHOT_2,
            USER_IDENTIFIER_CATEGORY_FEW_SHOT_3,
            AI_IDENTIFIER_CATEGORY_FEW_SHOT_3,
            USER_IDENTIFIER_CATEGORY_FEW_SHOT_4,
            AI_IDENTIFIER_CATEGORY_FEW_SHOT_4,
            user_msg,
        ]
    )

    category = str(answer.content)

    return {"query": input_state["query"], "category": category}


def generate_error_message(category_state: CategoryState) -> OutputState:
    """Generate error message for the user. This message is fixed.

    Args:
        category_state (CategoryState): category identified.

    Returns:
        OutputState: answer to the user (error message).
    """

    answer = """Eu não posso resolver o seu pedido, pois eu sou especializado em identificar preços para produtos das seguintes categorias: Celular; Televisão; Lavador; Notebook; Geladeira; Ar-Condicionado; Fogão; Eletrodomésticos; Eletroportáteis; Informática.
    """

    return {"answer": answer}


def verify_category_state(
    category_state: CategoryState,
) -> Literal["error-node", "product-node"]:
    if search(PATTERN_INVALID_CATEGORY, category_state["category"]):
        return "error-node"
    return "product-node"
