from otermtools.rag.config import Config
from otermtools.rag.store.models import *  # noqa
from sqlmodel import SQLModel, create_engine

engine = create_engine(
    f"postgresql://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@{Config.POSTGRES_HOST}/{Config.POSTGRES_DB}",
    echo=False,
)

SQLModel.metadata.create_all(engine)
