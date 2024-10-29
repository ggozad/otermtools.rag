from otermtools.rag.config import Config
from otermtools.rag.store.engine import engine
from otermtools.rag.store.models.embedding import Embedding
from sqlmodel import Session, select

from tests.models.utils import create_random_vector


def test_meta_filtering(setup_db):

    test_vector = create_random_vector(Config.EMBEDDING_VECTOR_DIM)

    metas = [
        {"source": "rag_test", "id": "1"},
        {"source": "rag_test", "foo": {"bar": "baz"}, "id": "2"},
        {"source": "rag_test", "foo": {"bar": "qux"}, "id": "3"},
        {"source": "rag_test", "foo": 42, "id": "4"},
    ]

    # Insert vectors into database
    with Session(engine) as session:
        for meta in metas:
            session.add(Embedding(embedding=test_vector.tolist(), meta=meta))

        session.commit()

    # Test filtering by meta key value
    with Session(engine) as session:
        data = session.exec(select(Embedding).filter(Embedding.meta["foo"] == "42"))
        results = data.all()
    assert len(results) == 1
    assert results[0].meta["id"] == "4"

    # Test filtering by nested meta key value
    with Session(engine) as session:
        data = session.exec(
            select(Embedding).filter(Embedding.meta["foo"]["bar"] == '"baz"')  # type: ignore
        )
        results = data.all()
    assert len(results) == 1
    assert results[0].meta["id"] == "2"

    # Test filtering by meta key existence
    with Session(engine) as session:
        data = session.exec(select(Embedding).filter(Embedding.meta.has_key("foo")))  # type: ignore
        results = data.all()
    assert len(results) == 3
    assert all("foo" in result.meta for result in results)

    # Test filtering by nested meta key existence
    with Session(engine) as session:
        data = session.exec(
            select(Embedding).filter(Embedding.meta["foo"].has_key("bar"))
        )
        results = data.all()
    assert len(results) == 2
    assert all(
        "foo" in result.meta and "bar" in result.meta["foo"] for result in results
    )

    # Test multiple filters
    with Session(engine) as session:
        data = session.exec(
            select(Embedding).filter(
                Embedding.meta["foo"] == "42", Embedding.meta["id"] == '"4"'
            )
        )
        results = data.all()
    assert len(results) == 1
    assert results[0].meta["id"] == "4"
