from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

DATABASE_URL = "postgresql+asyncpg://postgres.bizjhnrlmecvcsvqufnk:A%40n2004kit2004@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"

async def test():
    engine = create_async_engine(DATABASE_URL)
    async with engine.connect() as conn:
        print("✅ Connected successfully")

asyncio.run(test())