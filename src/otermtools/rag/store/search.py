from typing import Sequence

from otermtools.rag.embedder import Embedder
from otermtools.rag.store.engine import engine
from otermtools.rag.store.models.chunk import Chunk
from sqlmodel import Session, select


async def search(query: str, top_k: int = 10) -> Sequence[Chunk]:

    with Session(engine) as session:
        embedder = Embedder()
        query_embedding = await embedder.embed(query)
        chunks = session.exec(
            select(Chunk)
            .order_by(Chunk.embedding.cosine_distance(query_embedding))  # type: ignore
            .limit(top_k)
        ).all()
        return chunks
