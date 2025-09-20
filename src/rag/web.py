from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document

from re import search

END_SEARCH_PATTERN = r"(Ooops......... não encontramos resultados para sua busca)"

RETAILS_PATTERN = r"(Magazine Luiza|Casas Bahia|Americanas|Extra)"


def __generate_url(product_name: str, page: int) -> str:
    """Generate the url to web search.

    Args:
        product_name (str): product name.
        page (int): page on web search.

    Returns:
        str: url to web search.
    """

    return f"https://www.zoom.com.br/search?q={product_name.replace(' ','%20')}&hitsPerPage=48&page={page}"


def __filter_retails(contents: str) -> str:
    """Filter the offers from the web search by the retails.

    Args:
        contents (str): contents from web search.

    Returns:
        str: contents filtered by retails.
    """

    offers = contents.splitlines()

    return "\n".join([offer for offer in offers if search(RETAILS_PATTERN, offer)])


def web_search(product_name: str) -> str:
    """web search the product name and return the price research.

    Args:
        product_name (str): product name.

    Returns:
        str: price research.
    """

    web_page = 1
    is_page_final = False
    final_contents: str = str()

    while not is_page_final:

        web_search = WebBaseLoader(__generate_url(product_name, web_page))
        [document] = web_search.load()

        all_contents = document.page_content

        if search(pattern=END_SEARCH_PATTERN, string=all_contents):
            is_page_final = True
            continue

        final_contents += "\n" + __filter_retails(all_contents)
        web_page += 1

    return final_contents
