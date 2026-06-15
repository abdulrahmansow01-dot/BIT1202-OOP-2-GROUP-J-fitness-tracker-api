import asyncio
from sqlalchemy import select
from database import async_session
from models import User

async def find_admin_user():
    async with async_session() as session:
        # Get all users to see what we have
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        print("All users in database:\n")
        for user in users:
            print(f"ID: {user.id}")
            print(f"  Full Name: {user.full_name}")
            print(f"  Email: {user.email}")
            print(f"  Active: {user.is_active}")
            print(f"  Hash: {user.hashed_password[:50]}...")
            print()

asyncio.run(find_admin_user())
