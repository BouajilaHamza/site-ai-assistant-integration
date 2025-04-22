from backend.evaluation.utils import evaluation_task
from fastapi import APIRouter
from pydantic import BaseModel

evaluation_router = APIRouter()

class EvaluateRequest(BaseModel):
    query: str
    llm_response: str



@evaluation_router.post("/evaluate")
async def evaluate_query(request: EvaluateRequest):
    """
    Evaluate a query using the RAG system and return metrics.
    """
    result = evaluation_task({"query": request.query, "llm_response": request.llm_response})
    return result