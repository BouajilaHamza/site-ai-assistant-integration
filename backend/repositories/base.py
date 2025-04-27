from abc import ABC , abstractmethod


class KnowledgeRepository(ABC):
    @abstractmethod
    def index_documents(self, documents):
        """
        Index a list of documents.
        """
        pass
    
    
    @abstractmethod
    def retrieve(self,query,k=3):
        """
        Retrieve documents based on a query.
        """
        pass
    
    
    @abstractmethod
    def delete_index(self):
        """
        Delete the index.
        """
        pass