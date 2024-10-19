from uuid import UUID

from oterm.tools.rag.store.models.chunk import ChunkBase
from oterm.tools.rag.store.models.document import DocumentBase


class DocumentResponse(DocumentBase):
    id: UUID


class ChunkResponse(ChunkBase):
    id: UUID
