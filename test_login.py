import asyncio
import httpx

async def test_login():
    # First register a user
    async with httpx.AsyncClient() as client:
        print("=== REGISTERING USER ===")
        response = await client.post(
            "http://localhost:8000/users/register",
            json={
                "full_name": "Test User",
                "email": "testuser@gmail.com",
                "password": "testpass123"
            }
        )
        print(f"Register Status: {response.status_code}")
        print(f"Register Response: {response.json()}")
        
        print("\n=== LOGGING IN ===")
        # Now try to login
        response = await client.post(
            "http://localhost:8000/users/login",
            data={
                "username": "testuser@gmail.com",
                "password": "testpass123"
            }
        )
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {response.json()}")

asyncio.run(test_login())
