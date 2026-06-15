import asyncio
from sqlalchemy import text
from database import engine

async def test_connection():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            print(result.fetchone())
    except Exception as e:
        print(f"Database connection failed: {e}")
        print(f"Error type: {type(e).__name__}")

asyncio.run(test_connection())
