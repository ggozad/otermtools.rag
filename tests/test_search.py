import pytest
from otermtools.rag.reader import FileReader
from otermtools.rag.store.engine import engine
from otermtools.rag.store.models.document import Document
from otermtools.rag.store.search import search
from sqlmodel import Session


@pytest.mark.asyncio
async def test_search(setup_db, qa_corpus_html_documents):
    with Session(engine) as session:
        for html in qa_corpus_html_documents[:3]:
            text = FileReader().from_html(html)
            document = Document(
                text=text, uri="", mimetype="text/plain", meta={"source": "rag_test"}
            )

            chunks = await document.chunk(meta={"source": "rag_test"})
            document.chunks = chunks
            session.add(document)
            session.commit()
            session.refresh(document)

    search_results = await search(
        "How many persons does the US senate consist of?", top_k=3
    )
    assert "The United States Senate consists of 100 members" in search_results[0].text
    assert (
        search_results[0].document_id
        == search_results[1].document_id
        == search_results[2].document_id
    )

    search_results = await search(
        "Who worked initally on the wave–particle duality theory?", top_k=3
    )
    assert "Max Planck" in search_results[0].text
    assert "Einstein" in search_results[0].text
    assert "Louis de Broglie" in search_results[0].text
    assert (
        search_results[0].document_id
        == search_results[1].document_id
        == search_results[2].document_id
    )
