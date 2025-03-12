import functools

from ollama import AsyncClient

from haiku.rag.config import Config


class Embedder(object):

    _model: str = Config.EMBEDDING_MODEL
    _client: AsyncClient

    def __init__(self):
        self._client = AsyncClient(host=Config.OLLAMA_BASE_URL)

    @functools.lru_cache(maxsize=128)
    async def embed(self, text: str) -> list[float]:
        res = await self._client.embeddings(model=self._model, prompt=text)
        return list(res["embedding"])
