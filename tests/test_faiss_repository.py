from langchain.docstore.document import Document
from backend.repositories.faiss import FaissRepository

def test_faiss_add_and_retrieve_documents():
    repo = FaissRepository()
    docs = [Document(page_content="Hello world!"), Document(page_content="Another doc.")]
    
    repo.add_documents(docs)
    results = repo.similarity_search("Hello", k=1)

    assert len(results) == 1
    assert isinstance(results[0], Document)

def test_faiss_reset_index():
    repo = FaissRepository()
    docs = [Document(page_content="Test document.")]
    
    repo.add_documents(docs)
    repo.reset_index()

    results = repo.similarity_search("Test", k=1)
    assert results == []
