from backend.repositories.faiss import FaissRepository
from backend.repositories.qdrant import QdrantRepository
from backend.repositories.base import KnowledgeRepository
from backend.core.config import settings  # <- use your Settings class

def get_repository() -> KnowledgeRepository:
    """
    Factory to select the vector database backend based on environment variable.

    Returns:
        KnowledgeRepository: An instance of the selected repository.
    """
    backend = settings.VECTOR_BACKEND.upper()

    if backend == "FAISS":
        return FaissRepository()
    elif backend == "QDRANT":
        return QdrantRepository()
    else:
        raise ValueError(f"Unsupported VECTOR_BACKEND: {backend}")
