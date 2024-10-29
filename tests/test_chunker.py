import pytest
from otermtools.rag.chunker import Chunker
from otermtools.rag.reader import FileReader


@pytest.mark.asyncio
async def test_chunker(qa_corpus_html_documents: list[str]):
    html = qa_corpus_html_documents[0]  # type: ignore
    text = FileReader().from_html(html)
    chunks = await Chunker().chunk(text)

    # Ensure that the text is split into multiple chunks
    assert len(chunks) > 1

    # Ensure that each chunk corresponds to roughly Config.CHUNK_SIZE tokens
    for chunk in chunks[:-1]:
        encoded_tokens = Chunker.encoder.encode(chunk, disallowed_special=())
        assert len(encoded_tokens) <= Chunker().chunk_size
        assert len(encoded_tokens) > Chunker().chunk_size * 0.9
    # Ensure that the last chunk is less than Config.CHUNK_SIZE tokens
    assert (
        len(Chunker.encoder.encode(chunks[-1], disallowed_special=()))
        < Chunker().chunk_size
    )
