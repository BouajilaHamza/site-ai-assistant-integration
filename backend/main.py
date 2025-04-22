from backend.services.vector_store import initialize_knowledge_base
from backend.api.router import router
from backend.utils.lang_detect_utils import MODEL_PATH,MODEL_URL

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import nest_asyncio
import aiofiles
import httpx




async def download_model():
    MODEL_PATH.parent.mkdir(exist_ok=True)
    async with httpx.AsyncClient() as client:              # httpx async client :contentReference[oaicite:5]{index=5}
        resp = await client.get(MODEL_URL)
        resp.raise_for_status()
        async with aiofiles.open(MODEL_PATH, "wb") as f:   # aiofiles for non‑blocking file I/O :contentReference[oaicite:6]{index=6}
            await f.write(resp.content)



async def lifespan(app: FastAPI):
    nest_asyncio.apply()
    if not MODEL_PATH.exists():
        await download_model()
    yield

app = FastAPI(
    title="Knowledge Base API",
    description="API for managing and querying a knowledge base.",
    version="1.0.0",
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

