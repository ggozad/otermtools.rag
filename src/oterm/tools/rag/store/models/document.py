from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

from oterm.tools.rag.store.models.chunk import Chunk


class Document(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )
    text: str = Field(nullable=False)
    mimetype: str = Field(nullable=False)
    url: str | None = Field(nullable=True)
    meta: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    chunks: list["Chunk"] = Relationship(back_populates="document", cascade_delete=True)
