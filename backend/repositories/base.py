from abc import ABC, abstractmethod
from typing import List
from langchain.docstore.document import Document

class KnowledgeRepository(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int) -> List[Document]:
        """Retrieve top-k documents given a query."""
        pass

    @abstractmethod
    def reset_index(self) -> None:
        """Reset or delete the current index."""
        pass
