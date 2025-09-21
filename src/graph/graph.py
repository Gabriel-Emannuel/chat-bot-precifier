from langgraph.graph import StateGraph, START, END

from src.graph.rag import generate_price, generate_product
from src.graph.schema import InputState, OutputState, OverallState
from src.graph.validators import (
    generate_answer,
    generate_category,
    generate_error_message,
    verify_category_state,
)

builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)

builder.add_node("category-node", generate_category)  # type: ignore
builder.add_node("product-node", generate_product)  # type: ignore
builder.add_node("price-node", generate_price)  # type: ignore
builder.add_node("answer-node", generate_answer)  # type: ignore
builder.add_node("error-node", generate_error_message)  # type: ignore

builder.add_edge(START, "category-node")
builder.add_conditional_edges("category-node", verify_category_state)
builder.add_edge("product-node", "price-node")
builder.add_edge("price-node", "answer-node")
builder.add_edge("answer-node", END)
builder.add_edge("error-node", END)

graph = builder.compile()
