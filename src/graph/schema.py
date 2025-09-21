from typing import TypedDict


class InputState(TypedDict):
    query: str


class CategoryState(TypedDict):
    query: str
    category: str


class ProductState(TypedDict):
    query: str
    category: str
    product: str


class PriceState(TypedDict):
    price: str


class OutputState(TypedDict):
    answer: str


class OverallState(TypedDict):
    query: str
    category: str
    product: str
    price: str
    answer: str
