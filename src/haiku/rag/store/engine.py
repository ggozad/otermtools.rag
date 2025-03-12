from sqlmodel import SQLModel, create_engine

from haiku.rag.config import Config
from haiku.rag.store.models import *  # noqa

engine = create_engine(
    f"postgresql://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@{Config.POSTGRES_HOST}/{Config.POSTGRES_DB}",
    echo=False,
)

SQLModel.metadata.create_all(engine)
