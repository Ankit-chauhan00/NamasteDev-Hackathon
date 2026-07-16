"""
Centrailse variable and models can be imported any where
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SYNC_DATABASE_URL: str

    GOOGLE_API_KEY: str

    LLM_MODEL: str = "gemini-2.5-flash"
    FALLBACK_LLM_MODEL: str = "gemini-2.5-flash-lite"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()  # pyright: ignore[reportCallIssue]