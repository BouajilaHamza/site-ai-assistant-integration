from decouple import config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    GROQ_API_KEY: str = config('GROQ_API_KEY',cast=str)
    COMET_ML_API_KEY: str = config('COMET_ML_API_KEY',cast=str)
    COMET_ML_PROJECT_NAME: str = config('COMET_ML_PROJECT_NAME',cast=str)
    COMET_ML_WORKSPACE: str = config('COMET_ML_WORKSPACE',cast=str)

    class Config:
        env_file = ".env"

settings = Settings()