from typing import Sequence

from fastapi import APIRouter

from oterm.tools.rag.api.responses import ChunkResponse
from oterm.tools.rag.store.models.chunk import Chunk
from oterm.tools.rag.store.search import search

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/chunks", response_model=Sequence[ChunkResponse])
async def search_chunks(query: str) -> Sequence[Chunk]:
    return await search(query)
