from typing import Sequence

from sqlmodel import Session, select

from oterm.tools.rag.embedder import Embedder
from oterm.tools.rag.store.engine import engine
from oterm.tools.rag.store.models.chunk import Chunk


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
