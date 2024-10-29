import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from otermtools.rag.api import router as api_router
from otermtools.rag.config import Config
from otermtools.rag.monitor import FileWatcher
from otermtools.rag.store.engine import engine
from sqlmodel import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    fw = FileWatcher([Config.DOCUMENT_DIRECTORY])
    monitor = asyncio.create_task(fw.observe())
    yield
    monitor.cancel()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
