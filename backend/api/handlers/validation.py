from backend.services.validation_services import validate_rag_system
from fastapi import APIRouter
from typing import List

validation_router = APIRouter()


@validation_router.post("/validate")
async def validate_rag(retrieved_docs: List[str], ground_truth_docs: List[str],
                        generated_answer: str, reference_answer: str):
    """
    Validate the RAG system by calculating retrieval and LLM metrics.
    """
    metrics = await validate_rag_system(retrieved_docs, ground_truth_docs, generated_answer, reference_answer)
    return metrics

