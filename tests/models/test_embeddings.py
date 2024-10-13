import numpy as np
from numpy.testing import assert_array_almost_equal
from sqlmodel import Session, select

from oterm.tools.rag.config import Config
from oterm.tools.rag.store.engine import engine
from oterm.tools.rag.store.models.embedding import Embedding
from tests.models.utils import create_random_vector


def test_pgvector_distance(setup_db):

    test_vectors = [
        create_random_vector(Config.EMBEDDING_VECTOR_DIM) for _ in range(100)
    ]

    # Insert vectors into database
    with Session(engine) as session:
        for vector in test_vectors:
            session.add(
                Embedding(embedding=vector.tolist(), meta={"source": "rag_test"})
            )
        session.commit()

    # Pick the first vector as the search vector
    search_vector = test_vectors[0]

    # Test cosine similarity
    with Session(engine) as session:
        data = session.exec(
            select(Embedding)
            .order_by(Embedding.embedding.cosine_distance(search_vector))  # type: ignore
            .limit(10)
        )
        results = data.all()

    # Sort test vectors by cosine distance to search vector
    test_vectors.sort(key=lambda v: 1.0 - np.dot(v, search_vector) / (np.linalg.norm(v) * np.linalg.norm(search_vector)))  # type: ignore

    # Check if the 10 nearest vectors are the same as the first 10 test vectors
    for i in range(10):
        assert_array_almost_equal(results[i].embedding, test_vectors[i])

    # Test L2 similarity
    with Session(engine) as session:
        data = session.exec(
            select(Embedding)
            .order_by(Embedding.embedding.l2_distance(search_vector))  # type: ignore
            .limit(10)
        )
        results = data.all()

    # Sort test vectors by L2 distance to search vector
    test_vectors.sort(key=lambda v: np.linalg.norm(v - search_vector))  # type: ignore

    # Check if the 10 nearest vectors are the same as the first 10 test vectors
    for i in range(10):
        assert_array_almost_equal(results[i].embedding, test_vectors[i])
