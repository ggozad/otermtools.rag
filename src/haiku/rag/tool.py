from ollama._types import Tool

from haiku.rag.store.search import vector_search

RAGTool = Tool(
    type="function",
    function=Tool.Function(
        name="rag",
        description="Function to search the RAG knowledge base. Returns chumks of documents that might be relevant to the query.",
        parameters=Tool.Function.Parameters(
            type="object",
            properties={
                "query": Tool.Function.Parameters.Property(
                    type="string", description="The query execute."
                )
            },
            required=["query"],
        ),
    ),
)


async def rag_command(query="") -> str:
    chunks = await vector_search(query, top_k=1)
    response = "\n".join([chunk.text for chunk in chunks])
    return response
