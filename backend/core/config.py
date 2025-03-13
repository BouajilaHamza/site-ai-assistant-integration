from decouple import config
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    GROQ_API_KEY: str = config('GROQ_API_KEY',cast=str)
    TAVILY_API_KEY: str = config('TAVILY_API_KEY',cast=str)
    TARGET_DOMAIN: str = config('TARGET_DOMAIN',cast=str)



settings = Settings()