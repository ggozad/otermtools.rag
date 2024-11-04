from ollama._types import Parameters, Property, Tool, ToolFunction

from otermtools.rag.store.search import vector_search

RAGTool = Tool(
    type="function",
    function=ToolFunction(
        name="rag",
        description="Function to search the RAG knowledge base. Returns chumks of documents that might be relevant to the query.",
        parameters=Parameters(
            type="object",
            properties={
                "query": Property(type="string", description="The query execute.")
            },
            required=["query"],
        ),
    ),
)


async def rag_command(query="") -> str:
    chunks = await vector_search(query, top_k=1)
    response = "\n".join([chunk.text for chunk in chunks])
    return response
