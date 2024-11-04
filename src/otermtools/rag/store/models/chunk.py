from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

import numpy
from pgvector.sqlalchemy import Vector
from pydantic import field_serializer
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

from otermtools.rag.config import Config

if TYPE_CHECKING:
    from otermtools.rag.store.models.document import Document


class ChunkBase(SQLModel):
    document_id: UUID = Field(foreign_key="document.id", nullable=False)
    text: str = Field(nullable=False)
    meta: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))


class Chunk(ChunkBase, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )
    document: "Document" = Relationship(back_populates="chunks")
    embedding: list[float] = Field(
        sa_column=Column(Vector(Config.EMBEDDING_VECTOR_DIM))
    )

    @field_serializer("embedding")
    def serialize_embedding(self, embedding: numpy.ndarray) -> list[float]:
        return embedding.tolist()

    # If we want to index text as tsvector, we should add a ts_vector column
    # and add a __table_args__ with an Index like this:
    # __table_args__ = (
    #     Index(
    #         "ix_chunk_tsv",
    #         text("to_tsvector('english', ts_vector)"),
    #         postgresql_using="gin",
    #     ),
    # )
