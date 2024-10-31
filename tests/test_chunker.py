import pytest
from datasets import Dataset

from otermtools.rag.chunker import Chunker


@pytest.mark.asyncio
async def test_chunker(qa_corpus: Dataset):
    chunks = await Chunker().chunk(qa_corpus[0]["context"])

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
