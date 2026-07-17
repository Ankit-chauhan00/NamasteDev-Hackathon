"""
LLM Setup
using this gemini model as this is free and i dont have tokens
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

google_api_key = settings.GOOGLE_API_KEY
google_llm = settings.LLM_MODEL
google_fallback_llm = settings.FALLBACK_LLM_MODEL


extraction_model = ChatGoogleGenerativeAI(
    model=google_llm,
)

reasoning_model = ChatGoogleGenerativeAI(
    model=google_fallback_llm,
)
