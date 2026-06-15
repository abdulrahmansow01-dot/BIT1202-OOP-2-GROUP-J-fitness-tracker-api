import asyncio
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, async_session
from models import User

async def check_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"Total users in database: {len(users)}")
        for user in users:
            print(f"  - ID: {user.id}, Email: {user.email}, Active: {user.is_active}")
            print(f"    Password hash: {user.hashed_password[:50]}...")

asyncio.run(check_users())
