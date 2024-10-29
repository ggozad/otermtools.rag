from typing import Any
from uuid import UUID, uuid4

from otermtools.rag.config import Config
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class Embedding(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )
    embedding: list[float] = Field(
        sa_column=Column(Vector(Config.EMBEDDING_VECTOR_DIM))
    )
    meta: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))
