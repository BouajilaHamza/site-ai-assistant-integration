from decouple import config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str = config('GROQ_API_KEY',cast=str)
    TAVILY_API_KEY: str = config('TAVILY_API_KEY',cast=str)
    BASE_URL: str = config('BASE_URL',cast=str)
    FIRECRAWL_API_KEY: str = config('FIRECRAWL_API_KEY',cast=str)

    class Config:
        env_file = ".env"

settings = Settings()