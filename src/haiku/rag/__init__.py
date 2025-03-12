from haiku.rag.tool import RAGTool, rag_command

tools = [
    {
        "tool": RAGTool,
        "callable": rag_command,
    }
]
