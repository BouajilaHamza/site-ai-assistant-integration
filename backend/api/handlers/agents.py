from fastapi.routing import APIRouter
from fastapi import HTTPException
from apscheduler.schedulers.background import BackgroundScheduler

from backend.schemas.query_schemas import Query
from backend.utils.parsing import content_cache
from backend.utils.parsing import refresh_cache

agents_router = APIRouter()





@agents_router.post("/agent")
async def query_agent(query: Query):
    if not content_cache:
        raise HTTPException(status_code=400, detail="Cache is empty. Please refresh the cache first.")
    
    # Simple RAG implementation
    relevant_content = ""
    for url, data in content_cache.items():
        if query.question.lower() in data["content"].lower():
            relevant_content += f"\n{data['content'][:500]}"
    
    if not relevant_content:
        return {"response": "No relevant information found."}
    
    # Generate response using Groq
    prompt = f"Based on the following content:\n{relevant_content}\n\nQuestion: {query.question}\nAnswer:"
    # response = await groq_client.generate_response(prompt)
    
    return {"response": prompt}





@agents_router.post("/schedule")
async def schedule_refresh():
    await refresh_cache()
    return {"message": "Cache refresh completed"}

# Set up scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(refresh_cache, 'interval', hours=24)
scheduler.start()

