import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from haiku.rag.api import router as api_router
from haiku.rag.config import Config
from haiku.rag.monitor import FileWatcher
from haiku.rag.store.engine import engine


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
