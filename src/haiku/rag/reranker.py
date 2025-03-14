from mxbai_rerank import MxbaiRerankV2
from mxbai_rerank.base import RankResult

from haiku.rag.config import Config

model = MxbaiRerankV2(Config.RERANKING_MODEL)


def rerank(
    query: str,
    documents: list[str],
    top_k: int = 5,
    threshold: float = 0.0,
) -> list[RankResult]:
    ranked = model.rank(query, documents, top_k=top_k)
    if threshold:
        ranked = [r for r in ranked if r.score > threshold]
    return ranked
