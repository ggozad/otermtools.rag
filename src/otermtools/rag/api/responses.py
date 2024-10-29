from uuid import UUID

from otermtools.rag.store.models.chunk import ChunkBase
from otermtools.rag.store.models.document import DocumentBase


class DocumentResponse(DocumentBase):
    id: UUID


class ChunkResponse(ChunkBase):
    id: UUID
