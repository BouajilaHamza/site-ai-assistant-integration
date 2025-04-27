import pytest
from backend.services.context_service import build_chunk, initialize_knowledge_base
from unittest.mock import patch, AsyncMock, MagicMock
from langchain.docstore.document import Document

@pytest.mark.asyncio
async def test_initialize_knowledge_base_success(monkeypatch):
    # Mock extract_sitemap_links
    monkeypatch.setattr(
        "backend.services.context_service.extract_sitemap_links",
        lambda path: ["https://example.com/sitemap.xml"]
    )

    # Mock SitemapLoader
    mock_loader = AsyncMock()
    mock_loader.aload.return_value = [
        Document(page_content="This is a test page.", metadata={"title": "Test Page", "url": "https://example.com"})
    ]

    monkeypatch.setattr(
        "backend.services.context_service.SitemapLoader",
        MagicMock(return_value=mock_loader)
    )

    # Mock chunker output
    monkeypatch.setattr(
        "backend.services.context_service.chunker",
        lambda docs: [[MagicMock(content="chunk1 content"), MagicMock(content="chunk2 content")]]
    )

    # Mock vector repository add_documents
    monkeypatch.setattr(
        "backend.services.context_service.vector_repository",
        MagicMock(add_documents=MagicMock())
    )

    docs = await initialize_knowledge_base(base_url_or_path="https://example.com")

    assert len(docs) == 2
    assert isinstance(docs[0], Document)
    assert "# Test Page" in docs[0].page_content
    assert docs[0].metadata["url"] == "https://example.com"

@pytest.mark.asyncio
async def test_initialize_knowledge_base_empty(monkeypatch):
    # Mock extract_sitemap_links
    monkeypatch.setattr(
        "backend.services.context_service.extract_sitemap_links",
        lambda path: ["https://example.com/empty_sitemap.xml"]
    )

    # Mock SitemapLoader
    mock_loader = AsyncMock()
    mock_loader.aload.return_value = []

    monkeypatch.setattr(
        "backend.services.context_service.SitemapLoader",
        MagicMock(return_value=mock_loader)
    )

    docs = await initialize_knowledge_base(base_url_or_path="https://example.com/empty")

    assert docs == []

def test_build_chunk_formatting():
    title = "My Title"
    content = "This is the content."

    chunk = build_chunk(title, content)

    assert chunk.startswith("# My Title")
    assert "This is the content." in chunk
