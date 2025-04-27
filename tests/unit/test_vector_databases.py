import pytest
from unittest.mock import Mock
from langchain.docstore.document import Document
from backend.repositories.faiss import FaissRepository

@pytest.fixture
def faiss_repository():
    repo = FaissRepository(embedding_model="sentence-transformers/all-MiniLM-L6-v2")
    return repo


@pytest.fixture
def documents():
    return [
        Document(page_content="This is a test document.", metadata={"id": "doc1"}),
        Document(page_content="This is another test document.", metadata={"id": "doc2"}),
    ]

def test_init(faiss_repository):
    assert faiss_repository.embedding_model.model_name == "sentence-transformers/all-MiniLM-L6-v2"
    assert faiss_repository.doc_id_to_text == {}

def test_add_documents(faiss_repository, documents):
    faiss_repository.add_documents(documents)
    assert faiss_repository.vector_store is not None

# def test_add_documents_existing_vector_store(faiss_repository, documents):
#     faiss_repository.add_documents(documents)
#     new_documents = [
#         Document(page_content="This is a new test document.", metadata={"id": "doc3"}),
#         Document(page_content="This is another new test document.", metadata={"id": "doc4"}),
#     ]
#     faiss_repository.add_documents(new_documents)
#     assert len(faiss_repository.vector_store.documents) == 4

# def test_retrieve(faiss_repository, documents):
#     faiss_repository.add_documents(documents)
#     query = "test document"
#     results = faiss_repository.retrieve(query)
#     assert len(results) == 2
#     assert all("id" in result and "text" in result and "distance" in result for result in results)

# def test_retrieve_no_results(faiss_repository, documents):
#     faiss_repository.add_documents(documents)
#     query = "non-existent document"
#     results = faiss_repository.retrieve(query)
#     assert len(results) == 0

# def test_delete_documents(faiss_repository, documents):
#     faiss_repository.add_documents(documents)
#     ids = ["doc1", "doc2"]
#     faiss_repository.delete_documents(ids)
#     assert len(faiss_repository.vector_store.documents) == 0

# def test_save(faiss_repository, documents):
#     faiss_repository.add_documents(documents)
#     path = "test_index.faiss"
#     faiss_repository.save(path)
#     assert faiss_repository.vector_store.exists(path)

# def test_load(faiss_repository, documents):
#     faiss_repository.add_documents(documents)
#     path = "test_index.faiss"
#     faiss_repository.save(path)
#     new_repository = FaissRepository(embedding_model="sentence-transformers/all-MiniLM-L6-v2")
#     new_repository.load(path)
#     assert new_repository.vector_store is not None

# def test_add_documents_faiss_exception(faiss_repository, documents):
#     with pytest.raises(Exception):
#         faiss_repository.vector_store = Mock(side_effect=Exception("Test exception"))
#         faiss_repository.add_documents(documents)