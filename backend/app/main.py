from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.auth import router as auth_router
from app.api.routes.user_services import router as user_router
from app.schema.input_schema import ChatRequest, ChatResponse
from app.agent.graph import run_agent
from app.core.auth.dependencies import get_current_user
from app.models.user import User

# dont remove this as this import all models
import app.models

app = FastAPI(
    title="AI-personal-Finance-Manager",
    description="Ai powere finance management system",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {
        "status": "running",
        "services": "AI-First CRM - HCP Module"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    result = await run_agent(
        user_message=request.message,
        user_id=str(current_user.id),
        history=request.history,
    )

    return ChatResponse(
        reply=result["reply"],
        tool_calls=result["tool_calls"],
        tool_results=result["tool_results"],
        execution_trace=result["execution_trace"],
    )