from typing import List
from langchain_community.vectorstores import Qdrant
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from backend.repositories.base import KnowledgeRepository
from qdrant_client import QdrantClient

class QdrantRepository(KnowledgeRepository):
    def __init__(self, collection_name: str = "documents"):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.client = QdrantClient(":memory:")  # Use ":memory:" for in-memory Qdrant or change to actual server
        self.collection_name = collection_name
        self.vector_store = None

    def add_documents(self, documents: List[Document]) -> None:
        if self.vector_store is None:
            self.vector_store = Qdrant.from_documents(
                documents=documents,
                embedding=self.embeddings,
                location=":memory:",
                collection_name=self.collection_name,
            )
        else:
            self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        if self.vector_store is None:
            return []
        return self.vector_store.similarity_search(query, k=k)

    def reset_index(self) -> None:
        self.client.delete_collection(self.collection_name)
        self.vector_store = None
