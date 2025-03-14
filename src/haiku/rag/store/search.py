from typing import Sequence

from sqlmodel import Session, select

from haiku.rag.embedder import Embedder
from haiku.rag.reranker import rerank
from haiku.rag.store.engine import engine
from haiku.rag.store.models.chunk import Chunk


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
            .filter(Chunk.text.match(query, postgresql_regconfig="english"))  # type: ignore
            .limit(top_k)
        ).all()

        return chunks


async def search(
    query: str, top_k: int = 10, threshold=0.0
) -> Sequence[tuple[Chunk, float]]:
    k_search = await keyword_search(query, top_k)
    v_search = await vector_search(query, top_k)
    chunks = list(set(list(k_search) + list(v_search)))
    reranked = rerank(
        query, [chunk.text for chunk in chunks], top_k=top_k, threshold=threshold
    )
    print([chunk.text for chunk in chunks])

    return [
        (
            chunks[ranked.index],
            ranked.score,
        )
        for ranked in reranked
    ]
