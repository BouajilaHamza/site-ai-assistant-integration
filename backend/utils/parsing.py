# from datetime import datetime
# from typing import Dict, List
# from langchain_community.tools.tavily_search import TavilySearchResults
# from fastapi import HTTPException
# from backend.core.config import settings
# # In-memory cache for search results
# content_cache: Dict[str, Dict] = {}

# async def fetch_site_content(domain: str) -> List[Dict]:
#     try:
#         search_tool = TavilySearchResults(tavily_api_key=settings.TAVILY_API_KEY)
#         search_query = f"site:{domain}"
#         results = search_tool.invoke({"query": search_query})
        
#         return results
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching content: {str(e)} {settings.TAVILY_API_KEY}")

# async def process_search_results(results: List[Dict]):
#     for result in results:
#         url = result.get('url', '')
#         if url:
#             content_cache[url] = {
#                 "content": result.get('content', ''),
#                 "title": result.get('title', ''),
#                 "last_refreshed": datetime.now().isoformat()
#             }

# async def refresh_cache():
#     domain = settings.TARGET_DOMAIN
#     results = await fetch_site_content(domain)
#     await process_search_results(results)