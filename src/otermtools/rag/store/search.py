from typing import Sequence

from sqlmodel import Session, select

from otermtools.rag.embedder import Embedder
from otermtools.rag.store.engine import engine
from otermtools.rag.store.models.chunk import Chunk


async def vector_search(query: str, top_k: int = 10) -> Sequence[Chunk]:

    with Session(engine) as session:
        embedder = Embedder()
        query_embedding = await embedder.embed(query)
        chunks = session.exec(
            select(Chunk)
            .order_by(Chunk.embedding.cosine_distance(query_embedding))  # type: ignore
            .limit(top_k)
        ).all()
        return chunks


async def keyword_search(query: str, top_k: int = 10) -> Sequence[Chunk]:

    with Session(engine) as session:

        # We want this:
        #
        # SELECT id, text FROM chunk WHERE to_tsvector(text) @@ plainto_tsquery('english', query) LIMIT 10
        #
        # which is equivalent to:
        #
        # chunks = session.exec(
        #     select(Chunk)
        #     .filter(to_tsvector(Chunk.text).op("@@")(plainto_tsquery("english", query)))
        #     .limit(top_k)
        # ).all()
        #
        # But it seems we can also use the match method:
        chunks = session.exec(
            select(Chunk)
            .filter(Chunk.text.match(query, postgresql_regconfig="english"))
            .limit(top_k)
        ).all()

        return chunks
