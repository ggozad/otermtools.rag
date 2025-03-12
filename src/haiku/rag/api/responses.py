from uuid import UUID

from haiku.rag.store.models.chunk import ChunkBase
from haiku.rag.store.models.document import DocumentBase


class DocumentResponse(DocumentBase):
    id: UUID


class ChunkResponse(ChunkBase):
    id: UUID
