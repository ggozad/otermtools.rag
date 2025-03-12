from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from haiku.rag.api.responses import ChunkResponse, DocumentResponse
from haiku.rag.store.engine import engine
from haiku.rag.store.models.chunk import Chunk
from haiku.rag.store.models.document import Document

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=Sequence[DocumentResponse])
def documents(
    offset: int = 0, limit: int = Query(default=100, le=100)
) -> Sequence[Document]:
    with Session(engine) as session:
        return session.exec(select(Document).offset(offset).limit(limit)).all()


@router.get("/{document_id}", response_model=DocumentResponse)
def document(document_id: UUID) -> Document | None:
    with Session(engine) as session:
        return session.get(Document, document_id)


@router.delete("/{document_id}")
def delete_document(document_id: UUID):
    with Session(engine) as session:
        document = session.get(Document, document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        session.delete(document)
        session.commit()


@router.get("/{document_id}/chunks", response_model=Sequence[ChunkResponse])
def document_chunks(document_id: UUID) -> Sequence[Chunk]:
    with Session(engine) as session:
        chunks = session.exec(
            select(Chunk).where(Chunk.document_id == document_id)
        ).all()
        if not chunks:
            raise HTTPException(status_code=404, detail="Document not found")
        return chunks
