from sqlmodel import SQLModel, create_engine

from oterm.tools.rag.config import Config
from oterm.tools.rag.store.models import *  # noqa

engine = create_engine(
    f"postgresql://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@{Config.POSTGRES_HOST}/{Config.POSTGRES_DB}",
    echo=False,
)

SQLModel.metadata.create_all(engine)
