"""
Centrailse variable and models can be imported any where
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SYNC_DATABASE_URL: str

    GOOGLE_API_KEY: str

    LLM_MODEL: str = "gemini-3.5-flash"
    FALLBACK_LLM_MODEL: str = "gemini-3.1-flash-lite"

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    JWT_SECRET: str

    

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()  # pyright: ignore[reportCallIssue]