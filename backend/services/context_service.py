from backend.repositories.factory import get_repository
from backend.utils.parsing_utils import extract_sitemap_links
from semantic_chunkers import StatisticalChunker
from semantic_router.encoders import HuggingFaceEncoder
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain.docstore.document import Document
import logging
import nest_asyncio



nest_asyncio.apply()
logger = logging.getLogger(__name__)
vector_repository = get_repository()
encoder = HuggingFaceEncoder(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    max_length=512,
)
chunker = StatisticalChunker(
    encoder=encoder,
    min_split_tokens=100,
    max_split_tokens=500,
    plot_chunks=False,
    enable_statistics=False,
)

def build_chunk(title: str, content: str) -> str:
    """
    Build a chunk with a title and content.

    Args:
        title (str): The title of the document.
        content (str): The content of the chunk.

    Returns:
        str: The formatted chunk with the title.
    """
    return f"# {title}\n{content}"

async def initialize_knowledge_base(base_url_or_path: str,urls_limit=2) -> list[Document]:
    """
    Initializes the knowledge base by loading sitemaps, chunking documents, and adding to vector store.

    Args:
        base_url_or_path (str): URL or local path of sitemap.

    Returns:
        List[Document]: All processed and chunked documents added to the vector store.
    """
    sitemap_urls = extract_sitemap_links(base_url_or_path)
    docs = []
    
    for url in sitemap_urls[:urls_limit]:  # limit for now
        logger.debug(f"Processing sitemap: {url}")
        loader = SitemapLoader(web_path=url, continue_on_failure=True)
        loaded_docs = loader.aload()
        docs.extend(loaded_docs)

    if not docs:
        logger.warning("No documents loaded from sitemap!")
        return []

    logger.debug(f"Total documents loaded: {len(docs)}")

    # Semantic chunking
    page_contents = [doc.page_content for doc in docs]
    chunked_docs = chunker(docs=page_contents)

    final_documents = []
    for doc, chunks in zip(docs, chunked_docs):
        title = doc.metadata.get("title", "Untitled")
        url = doc.metadata.get("url", "No URL")
        language = doc.metadata.get("language", "en")

        for chunk in chunks:
            titled_chunk = build_chunk(title=title, content=chunk.content)
            final_documents.append(
                Document(
                    page_content=titled_chunk,
                    metadata={
                        'url': url,
                        'title': title,
                        'language': language
                    }
                )
            )

    logger.debug(f"Total chunks after semantic chunking: {len(final_documents)}")

    # Add documents to the vector database
    vector_repository.add_documents(final_documents)

    return final_documents
