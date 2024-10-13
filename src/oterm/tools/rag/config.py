import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class AppConfig(BaseModel):
    ENV: str = "development"

    COLLECTION_NAME: str = "oterm"

    POSTGRES_DB: str = "rag"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432

    OLLAMA_BASE_URL: str

    LLM_MODEL: str = "llama3.1"
    EMBEDDING_MODEL: str = "mxbai-embed-large"
    EMBEDDING_VECTOR_DIM: int = 1024
    CHUNK_SIZE: int = 256
    CHUNK_OVERLAP: int = 32


# Expose Config object for app to import
Config = AppConfig.model_validate(os.environ)
