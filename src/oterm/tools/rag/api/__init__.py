from fastapi.routing import APIRouter

from oterm.tools.rag.api import documents, health

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)
router.include_router(documents.router)
