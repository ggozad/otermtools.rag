from fastapi.routing import APIRouter

from haiku.rag.api import documents, health, search

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)
router.include_router(documents.router)
router.include_router(search.router)
