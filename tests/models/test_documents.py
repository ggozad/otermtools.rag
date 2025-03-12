import pytest
from sqlmodel import Session

from haiku.rag.store.engine import engine
from haiku.rag.store.models.document import Document


@pytest.mark.asyncio
async def test_document_chunking(setup_db, qa_corpus):
    with Session(engine) as session:
        document = Document(
            text=qa_corpus[0]["context"],
            uri="",
            mimetype="text/plain",
            meta={"source": "rag_test"},
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
