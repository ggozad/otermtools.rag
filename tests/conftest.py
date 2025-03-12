from pathlib import Path

import pytest
from datasets import Dataset, load_from_disk
from sqlmodel import Session, select

from haiku.rag.store.engine import engine
from haiku.rag.store.models.document import Document
from haiku.rag.store.models.embedding import Embedding


@pytest.fixture(scope="function")
def setup_db():
    def delete_test_entries():
        with Session(engine) as session:
            test_entries = session.exec(
                select(Embedding).filter(Embedding.meta["source"] == '"rag_test"')
            ).all()
            test_entries = list(test_entries) + list(
                session.exec(
                    select(Document).filter(Document.meta["source"] == '"rag_test"')
                ).all()
            )

            for entry in test_entries:
                session.delete(entry)
            session.commit()

    delete_test_entries()
    yield
    delete_test_entries()


@pytest.fixture(scope="session")
def qa_corpus() -> list[dict[str, str]]:
    ds: Dataset = load_from_disk(Path(__file__).parent / "data" / "dataset")  # type: ignore

    return ds.to_list()


@pytest.fixture(scope="session")
def test_files() -> Path:
    return Path(__file__).parent / "data"
