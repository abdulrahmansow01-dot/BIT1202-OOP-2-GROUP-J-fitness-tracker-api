import asyncio
from sqlalchemy import select
from database import async_session
from models import User
from auth import verify_password, get_password_hash

async def debug_password():
    async with async_session() as session:
        # Get the test user
        result = await session.execute(select(User).where(User.email == "testuser@gmail.com"))
        user = result.scalars().first()
        
        if not user:
            print("❌ User not found!")
            return
        
        print(f"User: {user.email}")
        print(f"User is_active: {user.is_active}")
        print(f"Hashed password: {user.hashed_password}")
        
        # Test password
        test_password = "testpass123"
        is_valid = verify_password(test_password, user.hashed_password)
        print(f"\nPassword '{test_password}' is valid: {is_valid}")
        
        # Test wrong password
        wrong_password = "wrongpass"
        is_valid_wrong = verify_password(wrong_password, user.hashed_password)
        print(f"Password '{wrong_password}' is valid: {is_valid_wrong}")
        
        # Let's also check all users
        print("\n=== ALL USERS ===")
        result = await session.execute(select(User))
        all_users = result.scalars().all()
        for u in all_users:
            print(f"- {u.email}: is_active={u.is_active}")

asyncio.run(debug_password())
