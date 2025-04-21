from backend.services.validation_services import validate_rag_system, evaluation_task
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

validation_router = APIRouter()

class EvaluateRequest(BaseModel):
    query: str
    llm_response: str

@validation_router.post("/validate")
async def validate_rag(retrieved_docs: List[str], ground_truth_docs: List[str],
                        generated_answer: str, reference_answer: str):
    """
    Validate the RAG system by calculating retrieval and LLM metrics.
    """
    metrics = await validate_rag_system(retrieved_docs, ground_truth_docs, generated_answer, reference_answer)
    return metrics

@validation_router.post("/evaluate")
async def evaluate_query(request: EvaluateRequest):
    """
    Evaluate a query using the RAG system and return metrics.
    """
    result = evaluation_task({"query": request.query, "llm_response": request.llm_response})
    return result