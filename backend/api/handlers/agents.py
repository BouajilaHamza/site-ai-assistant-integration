from fastapi.routing import APIRouter
from fastapi import HTTPException

from backend.schemas.query_schemas import Query
from backend.services.agent_services import query_knowledge_base
import logging

logger = logging.getLogger(__name__)
agents_router = APIRouter()

@agents_router.post("/api/chat")
async def chat_endpoint(message: Query):
    try:
        response = await query_knowledge_base(message.message)
        logger.debug(f"Response: {response}")
        return {"response": response, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
