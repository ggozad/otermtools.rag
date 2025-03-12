from typing import Sequence

from fastapi import APIRouter

from haiku.rag.api.responses import ChunkResponse
from haiku.rag.store.models.chunk import Chunk
from haiku.rag.store.search import vector_search

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/chunks", response_model=Sequence[ChunkResponse])
async def search_chunks(query: str) -> Sequence[Chunk]:
    return await vector_search(query)
