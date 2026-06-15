import asyncio
from database import async_session
from crud import create_user
from schemas import UserCreate
from sqlalchemy import select, delete
from models import User
from auth import get_password_hash

async def reset_users():
    async with async_session() as session:
        # Delete all existing users
        print("Clearing old users...")
        await session.execute(delete(User))
        await session.commit()
        
        # Create fresh test users
        test_users = [
            {"full_name": "Alex Carter", "email": "alex@gmail.com", "password": "alex123456"},
            {"full_name": "Admin User", "email": "admin@gmail.com", "password": "admin123456"},
            {"full_name": "Test User", "email": "test@gmail.com", "password": "test123456"},
        ]
        
        print("\nCreating fresh users:")
        for user_data in test_users:
            user_create = UserCreate(
                full_name=user_data["full_name"],
                email=user_data["email"],
                password=user_data["password"]
            )
            user = await create_user(session, user_create)
            print(f"✓ {user.email} (password: {user_data['password']})")

asyncio.run(reset_users())
