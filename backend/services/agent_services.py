from langchain_groq import ChatGroq
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from .vector_store import VectorStore
from backend.core.config import settings
import requests
from bs4 import BeautifulSoup
import asyncio

groq_client = ChatGroq(api_key=settings.GROQ_API_KEY)
vector_store = VectorStore()

# New helper function to extract links from sitemap.xml
def extract_sitemap_links(base_url: str) -> list:
    sitemap_url = base_url.rstrip("/") + "/sitemap.xml"
    try:
        r = requests.get(sitemap_url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text,features="xml")    
            return [loc.text.replace("\r\n", "").strip() for loc in soup.find_all('loc')]
    except Exception as e:
        print(f"Error extracting sitemap: {e}")
    return []


async def initialize_knowledge_base():
    links = extract_sitemap_links(settings.BASE_URL)
    documents = []
    for link in links:
        await asyncio.sleep(25)  # non-blocking sleep
        try:
            loader = FireCrawlLoader(url=link, api_key=settings.FIRECRAWL_API_KEY, mode="scrape")
            docs = await asyncio.to_thread(loader.load)  # run loader.load() without blocking
            documents.extend(docs)
        except Exception as e:
            print(f"Error loading document: {e} {link}")
    vector_store.add_documents(documents)

async def query_knowledge_base(question: str) -> str:
    relevant_docs = vector_store.similarity_search(question)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    
    prompt = f"""Based on the following context:
    {context}
    
    Question: {question}
    Answer:"""
    
    return await groq_client.apredict(prompt)