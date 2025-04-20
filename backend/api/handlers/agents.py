from fastapi.routing import APIRouter
from fastapi import HTTPException
from apscheduler.schedulers.background import BackgroundScheduler

from backend.schemas.query_schemas import Query
from backend.services.agent_services import query_knowledge_base
from backend.services.vector_store import initialize_knowledge_base
agents_router = APIRouter()



@agents_router.post("/schedule")
async def schedule_refresh():
    await initialize_knowledge_base()
    return {"message": "Knowledge base refresh completed"}



@agents_router.post("/api/chat")
async def chat_endpoint(message: Query):
    try:
        # Add your AI logic here
        response = await query_knowledge_base(message.message)
        print(f"Response: {response}")
        return {"response": response, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Set up scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(initialize_knowledge_base, 'interval', hours=24)
scheduler.start()

