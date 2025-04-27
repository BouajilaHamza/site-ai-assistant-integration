from langchain.docstore.document import Document
from backend.repositories.qdrant import QdrantRepository

def test_qdrant_add_and_retrieve_documents():
    repo = QdrantRepository()
    docs = [Document(page_content="This is a test."), Document(page_content="More text here.")]
    
    repo.add_documents(docs)
    results = repo.similarity_search("test", k=1)

    assert len(results) == 1
    assert isinstance(results[0], Document)

def test_qdrant_reset_index():
    repo = QdrantRepository()
    docs = [Document(page_content="Another test doc.")]
    
    repo.add_documents(docs)
    repo.reset_index()

    results = repo.similarity_search("Another", k=1)
    assert results == []
