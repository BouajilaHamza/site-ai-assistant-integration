from typing import Literal
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    COMET_ML_API_KEY: str
    COMET_ML_PROJECT_NAME: str
    COMET_ML_WORKSPACE: str
    VECTOR_BACKEND: Literal["FAISS", "QDRANT"] = "FAISS"
    class Config:
        env_file = ".env"

settings = Settings()
