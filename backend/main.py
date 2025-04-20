from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.services.agent_services import initialize_knowledge_base
from backend.api.router import router
from dotenv import load_dotenv
import nest_asyncio
load_dotenv()



def lifespan(app: FastAPI):
    nest_asyncio.apply()
    initialize_knowledge_base()
    yield



app = FastAPI(
    title="Knowledge Base API",
    description="API for managing and querying a knowledge base.",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

# Add base template route
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

