import asyncio
from database import engine

async def test():
    try:
        async with engine.begin() as conn:
            print("Connected to database successfully")
    except Exception as e:
        print(f"Error connecting to database: {e}")

asyncio.run(test())
