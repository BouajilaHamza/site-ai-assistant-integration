from fastapi import APIRouter
from backend.services.validation_services import validate_rag_system

validation_router = APIRouter()

@validation_router.get("/validate")
async def validate_rag():
    # Example data for validation
    retrieved_docs = ["https://example.com/doc1", "https://example.com/doc2"]
    ground_truth_docs = ["https://example.com/doc1"]
    generated_answer = "This is a generated answer."
    reference_answer = "This is the reference answer."

    metrics = await validate_rag_system(retrieved_docs, ground_truth_docs, generated_answer, reference_answer)
    return metrics