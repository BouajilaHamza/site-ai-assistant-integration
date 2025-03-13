from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.parsing import refresh_cache
from backend.api.router import router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


# Startup event
@app.on_event("startup")
async def startup_event():
    await refresh_cache()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
