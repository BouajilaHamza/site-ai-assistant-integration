from fastapi.routing import APIRouter
from backend.api.handlers.agents import agents_router

router = APIRouter()


router.include_router(agents_router, prefix="/agents", tags=["agents"])