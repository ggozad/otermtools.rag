from typing import Sequence

from fastapi import APIRouter
from otermtools.rag.api.responses import ChunkResponse
from otermtools.rag.store.models.chunk import Chunk
from otermtools.rag.store.search import search

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/chunks", response_model=Sequence[ChunkResponse])
async def search_chunks(query: str) -> Sequence[Chunk]:
    return await search(query)
