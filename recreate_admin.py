import asyncio
from database import async_session
from models import User
from sqlalchemy import delete, select
from schemas import UserCreate
from crud import create_user
from auth import get_password_hash

async def recreate_your_admin():
    async with async_session() as session:
        # Delete current admin
        print("Deleting the reset admin user...")
        await session.execute(delete(User).where(User.email == "admin@gmail.com"))
        await session.commit()
        
        # Recreate with YOUR credentials
        print("Creating your Admin user with your password...\n")
        
        user_data = UserCreate(
            full_name="Admin",
            email="admin@gmail.com",  # Required for login - email is used as username
            password="567876678"
        )
        
        user = await create_user(session, user_data)
        print(f"✓ User created!")
        print(f"  Full Name: {user.full_name}")
        print(f"  Email: {user.email}")
        print(f"  Password: 567876678")
        print(f"\nTo login use:")
        print(f"  Username: admin@gmail.com")
        print(f"  Password: 567876678")

asyncio.run(recreate_your_admin())
