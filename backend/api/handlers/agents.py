from fastapi.routing import APIRouter
from fastapi import HTTPException
from apscheduler.schedulers.background import BackgroundScheduler

from backend.schemas.query_schemas import Query
from backend.services.agent_services import initialize_knowledge_base, query_knowledge_base

agents_router = APIRouter()

@agents_router.post("/agent")
async def query_agent(query: Query):
    try:
        response = await query_knowledge_base(query.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@agents_router.post("/schedule")
async def schedule_refresh():
    await initialize_knowledge_base()
    return {"message": "Knowledge base refresh completed"}

# Set up scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(initialize_knowledge_base, 'interval', hours=24)
scheduler.start()

