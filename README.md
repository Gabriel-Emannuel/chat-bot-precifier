# Chatbot to help digitally illiterate people find the best prices in retail stores

The goal of this repository is to create a proof-of-concept chatbot to help people without online knowledge search for prices. The idea is to use Langchain and Langgraph to build a chain of instructions for an LLM and provide good results to the user.

The final Langgraph architecture of the project is:

<img src="assets/graph.png" alt="Langgraph architecture">

Explanation:
* Category Node: First node, identifies whether the user's query is valid and in which category it can be classified;
* Error Node: Simple error message if the classified category is invalid;
* Product Node: Product identifier for online price searches;
* Price Node: Online price searches;
* Response Node: Final node to add the source URL to the final response.

# Launch Locally

If your Docker Compose version is higher than v2, it's best to update Ollama first and then the application. In any case, if you're having trouble compiling, give it a try.

# Local Evaluation

The RAG system evaluation is available in the [`eval.md`] file!