import pytest
from sqlmodel import Session

from otermtools.rag.store.engine import engine
from otermtools.rag.store.models.document import Document
from otermtools.rag.store.search import search


@pytest.mark.asyncio
async def test_search(setup_db, qa_corpus):
    with Session(engine) as session:
        for doc in qa_corpus[:10]:
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

    search_results = await search(
        "'What is the Berry Export Summary 2028 and what is its purpose?", top_k=1
    )
    assert "strawberry" in search_results[0].text
    assert "raspberry" in search_results[0].text
    assert "blackberry" in search_results[0].text

    search_results = await search(
        "What are the unique features of the Coolands for Twitter app?",
        top_k=3,
    )
    search_results_text = "".join([result.text for result in search_results])
    assert "Avatar Indicator" in search_results_text
    assert "Direct Link" in search_results_text
    assert "Smart Bookmark" in search_results_text
