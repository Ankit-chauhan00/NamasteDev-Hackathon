from fastapi import FastAPI
from app.api.routes.auth import router as auth_router

import app.models

app = FastAPI(
    title="AI-personal-Finance-Manager",
    description="Ai powere finance management system",
    version="1.0.0",
)

app.include_router(auth_router)

