from pathlib import Path

import pytest
from datasets import Dataset, DatasetDict, load_dataset
from sqlmodel import Session, select

from oterm.tools.rag.store.engine import engine
from oterm.tools.rag.store.models.document import Document
from oterm.tools.rag.store.models.embedding import Embedding


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
def qa_corpus() -> Dataset:
    ds: DatasetDict = load_dataset("google-research-datasets/natural_questions", "dev")  # type: ignore
    return ds.get("validation")  # type: ignore


@pytest.fixture(scope="session")
def qa_corpus_html_documents(qa_corpus) -> list[str]:
    documents = []
    for i in range(100):
        documents.append(qa_corpus[i])
    return [document["document"]["html"] for document in documents]


@pytest.fixture(scope="session")
def test_files() -> Path:
    return Path(__file__).parent / "data"
