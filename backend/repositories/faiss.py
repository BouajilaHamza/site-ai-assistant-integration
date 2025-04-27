from .base import KnowledgeRepository
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from typing import List,Dict


class FaissRepository(KnowledgeRepository):
    def __init__(self,diemnsion):
        """
        Initialize the FaissRepository with the path to the index file.
        """
    def __init__(self, dimension: int, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding_model = HuggingFaceEmbeddings(model_name=embedding_model)
        self.doc_id_to_text = {}
    
    def add_documents(self,documents) -> None:
        """
        Index a list of documents.
        """
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embedding_model)
        else:
            self.vector_store.add_documents(documents)
    
    def retrieve(self,query,k=3) -> List[Dict]:
        """
        Retrieve documents based on a query.
        """
        query_embedding = self.embedding_model.embed_query(query)
        docs = self.vector_store.similarity_search_by_vector(query_embedding, k=k)
        results = []
        for doc in docs:
            results.append({
                'id': doc.metadata['id'],
                'text': doc.page_content,
                'distance': doc.metadata['distance']
            })
        return results
    
    def delete_documents(self, ids: List[str]):
        if self.vector_store is not None:
            self.vector_store.delete(ids)
    
    def save(self, path: str) -> None:
        """
        Save the index to a file.
        """
        if self.vector_store is not None:
            self.vector_store.save_local(path)

    def load(self, path: str) -> None:
        """
        Load the index from a file.
        """
        self.vector_store = FAISS.load_local(path, self.embedding_model)
        
        
            