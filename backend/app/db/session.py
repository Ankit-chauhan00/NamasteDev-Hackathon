"""
engine is used to connect to PostgreSQL.
async_session_factory creates a session pooler.
get_db() yields a fresh session per request via FastAPI's dependency system.
"""

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession



engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True, # false in production enable SQL Loggong during developement
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session