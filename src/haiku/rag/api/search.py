from typing import Sequence

from fastapi import APIRouter

from haiku.rag.api.responses import ChunkResponse
from haiku.rag.store.models.chunk import Chunk
from haiku.rag.store.search import search

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/chunks", response_model=Sequence[tuple[ChunkResponse, float]])
async def vector_search_chunks(
    query: str, top_k: int = 10, threshold: float = 0.0
) -> Sequence[tuple[Chunk, float]]:
    return await search(query, top_k=top_k, threshold=threshold)
