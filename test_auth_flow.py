import asyncio
from database import async_session
from crud import get_user_by_email
from auth import authenticate_user

async def test_auth_flow():
    async with async_session() as session:
        email = "testuser@gmail.com"
        password = "testpass123"
        
        print(f"Testing authentication for {email}")
        print(f"Password: {password}\n")
        
        # Step 1: Get user by email
        print("Step 1: Get user by email...")
        user = await get_user_by_email(session, email)
        if user:
            print(f"✓ User found: {user.email}, is_active={user.is_active}")
        else:
            print(f"✗ User not found")
            return
        
        # Step 2: Authenticate user
        print("\nStep 2: Authenticate user...")
        auth_user = await authenticate_user(session, email, password)
        if auth_user:
            print(f"✓ Authentication successful!")
            print(f"  Email: {auth_user.email}")
            print(f"  Active: {auth_user.is_active}")
        else:
            print(f"✗ Authentication failed!")
            
        # Step 3: Try with wrong password
        print("\nStep 3: Authenticate with wrong password...")
        auth_user_wrong = await authenticate_user(session, email, "wrongpass")
        if auth_user_wrong:
            print(f"✓ Authentication successful (should be false!)")
        else:
            print(f"✓ Authentication correctly rejected wrong password")

asyncio.run(test_auth_flow())
