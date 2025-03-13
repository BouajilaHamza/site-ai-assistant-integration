from typing import List, Dict
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
        
    def add_documents(self, documents: List[Dict[str, str]]):
        docs = [
            Document(
                page_content=doc['content'],
                metadata={'url': doc['url'], 'title': doc['title']}
            )
            for doc in documents
        ]
        
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(docs, self.embeddings)
        else:
            self.vector_store.add_documents(docs)
            
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        if self.vector_store is None:
            return []
        return self.vector_store.similarity_search(query, k=k)
