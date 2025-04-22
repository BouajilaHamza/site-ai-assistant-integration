from typing import List, Dict
from rich.text import Text
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain_community.document_loaders.sitemap import SitemapLoader
from backend.utils.parsing_utils import extract_sitemap_links
from backend.core.config import settings
from semantic_chunkers import StatisticalChunker
from semantic_router.encoders import HuggingFaceEncoder
import logging

logger = logging.getLogger(__name__)



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

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
        
    def add_documents(self, documents: List[Document]):
        docs = [
            Document(
                page_content=doc.page_content,
                metadata={'url': doc.metadata['url'], 'title': doc.metadata['title']}
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

vector_store = VectorStore()

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

async def initialize_knowledge_base():
    sitemap_urls = extract_sitemap_links(settings.BASE_URL)
    print(len(sitemap_urls))
    docs = []
    for url in sitemap_urls[:2]:
        logger.debug(f"Processing sitemap: {url}")
        loader = SitemapLoader(web_path=url, continue_on_failure=True)
        doc = loader.aload()
        docs.extend(doc)
    print(docs[0])
    logger.debug(f"Total documents loaded: {len(docs)}")
    to_be_chunked = [doc.page_content for doc in docs]
    logger.debug(to_be_chunked[0])
    chunked_docs = chunker(docs=to_be_chunked)

    # Add titles to chunks
    titled_chunks = []
    for doc, chunks in zip(docs, chunked_docs):
        title = doc.metadata.get("title", "Untitled")
        for chunk in chunks:
            titled_chunk = Text(build_chunk(title=title, content=chunk.content))
            titled_chunks.append(titled_chunk)

    logger.debug(f"Total chunks after semantic chunking: {len(titled_chunks)}")
    return titled_chunks
#for chunk in chunked_docs:
#vector_store.add_documents(chunked_docs)
