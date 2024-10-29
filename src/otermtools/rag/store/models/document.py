from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from otermtools.rag.chunker import Chunker
from otermtools.rag.embedder import Embedder
from otermtools.rag.store.models.chunk import Chunk
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel


class DocumentBase(SQLModel):
    text: str = Field(nullable=False)
    mimetype: str = Field(nullable=False)
    uri: str | None = Field(nullable=True)
    meta: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Document(DocumentBase, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )

    chunks: list[Chunk] = Relationship(back_populates="document", cascade_delete=True)

    async def chunk(self, meta={}) -> list[Chunk]:
        # If the document has already been chunked do nothing
        if self.chunks:
            return []
        chunker = Chunker()
        embedder = Embedder()
        chunks = await chunker.chunk(self.text)

        document_chunks = [
            Chunk(
                text=chunk,
                meta={**meta, "chunk_order": i},
                document_id=self.id,
                embedding=await embedder.embed(chunk),
            )
            for i, chunk in enumerate(chunks)
        ]

        return document_chunks
