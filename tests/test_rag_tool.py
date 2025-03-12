import pytest
from ollama import Client, Message
from sqlmodel import Session

from haiku.rag.config import Config
from haiku.rag.store.engine import engine
from haiku.rag.store.models.document import Document
from haiku.rag.tool import RAGTool, rag_command


@pytest.mark.asyncio
async def test_rag_tool(setup_db, qa_corpus):
    with Session(engine) as session:

        documents = qa_corpus[:3]
        for doc in documents:
            document = Document(
                text=doc["context"],
                uri="",
                mimetype="text/plain",
                meta={"source": "rag_test"},
            )

            chunks = await document.chunk(meta={"source": "rag_test"})
            document.chunks = chunks
            session.add(document)
            session.commit()
            session.refresh(document)

    client = Client(host=Config.OLLAMA_BASE_URL)
    messages = [
        Message(
            role="system",
            content="You are provided with a database of text documents. Use the tools at your disposal to search for relevant information and answer the user's questions. Answer the questions as accurately as possible, if cannot answer, say so.",
        ),
        Message(
            role="user",
            content="What is the Berry Export Summary 2028 and what is its purpose?",
        ),
    ]
    response = client.chat(
        Config.LLM_MODEL,
        messages=messages,
        tools=[RAGTool],
    )
    message = response.get("message")
    assert message.get("role") == "assistant"  # type: ignore
    assert message.get("content") == ""  # type: ignore
    tool_calls = message.get("tool_calls")  # type: ignore
    assert len(tool_calls) == 1
    tool_call = tool_calls[0]
    assert tool_call.get("function").get("name") == "rag"
    query = tool_call.get("function").get("arguments").get("query")
    assert "Berry Export" in query

    tool_response = await rag_command(query)
    messages.append(Message(role="tool", content=tool_response))
    response = client.chat(
        model=Config.LLM_MODEL,
        messages=messages,
        tools=[RAGTool],
        options={"temperature": 0.0},
    )
    message = response.get("message").get("content")  # type: ignore
    assert "Australian" in message
