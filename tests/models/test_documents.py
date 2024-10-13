import pytest
from sqlmodel import Session

from oterm.tools.rag.converters.html import from_html
from oterm.tools.rag.store.engine import engine
from oterm.tools.rag.store.models.document import Document


@pytest.mark.asyncio
async def test_document_chunking(setup_db, qa_corpus_html_documents):
    with Session(engine) as session:
        html = qa_corpus_html_documents[0]
        text = from_html(html)
        document = Document(
            text=text, url="", mimetype="text/plain", meta={"source": "rag_test"}
        )

        chunks = await document.chunk(meta={"source": "rag_test"})
        document.chunks = chunks
        session.add(document)
        session.commit()

        session.refresh(document)

        assert document.id

        chunks = document.chunks

    assert len(document.chunks) > 1
    assert len(document.text) > 0
    chunks = document.chunks
    chunks.sort(key=lambda x: x.meta["chunk_order"])
    assert document.text.startswith(chunks[0].text)
    assert document.text.endswith(chunks[-1].text)
