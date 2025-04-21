from fastapi.routing import APIRouter
from backend.api.handlers.agents import agents_router
from backend.api.handlers.validation import validation_router
from backend.api.handlers.evaluation import evaluation_router
router = APIRouter()


router.include_router(agents_router, prefix="/agents", tags=["agents"])
router.include_router(validation_router, prefix="/validation", tags=["validation"])
router.include_router(evaluation_router, prefix="/evaluation", tags=["evaluation"])