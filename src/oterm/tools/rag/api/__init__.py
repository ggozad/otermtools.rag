from fastapi.routing import APIRouter

from oterm.tools.rag.api import health

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)