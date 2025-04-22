from typing import List, Dict
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain_community.document_loaders.sitemap import SitemapLoader
from backend.utils.parsing_utils import extract_sitemap_links
from backend.core.config import settings
from semantic_chunkers import StatisticalChunker
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)



encoder_model = SentenceTransformer("all-MiniLM-L6-v2")

chunker = StatisticalChunker(
    encoder=encoder_model,  # Pass the model directly instead of a dictionary
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
        
    def add_documents(self, documents: List[Dict[str, str]]):
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

async def initialize_knowledge_base():
    sitemap_urls = extract_sitemap_links(settings.BASE_URL)
    docs = []
    for url in sitemap_urls:
        logger.debug(f"Processing sitemap: {url}")
        loader = SitemapLoader(web_path=url,)
        doc = loader.aload()
        docs.extend(doc)
    logger.debug(f"Total documents loaded: {len(docs)}")
    to_be_chunked = [doc.page_content for doc in docs]
    print(to_be_chunked[0])
    chunked_docs = chunker(docs=to_be_chunked)  # Ensure chunker uses the correct encoder
    for chunk in chunked_docs:
        chunk=  Document(
                page_content=chunk,
                metadata={"url": doc.metadata["source"], "title": doc.metadata.get("title", "")}
            )
    logger.debug(f"Total chunks after semantic chunking: {len(chunked_docs)}")
    vector_store.add_documents(chunked_docs)
