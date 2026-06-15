import asyncio
import httpx

async def test_logins():
    async with httpx.AsyncClient() as client:
        # Test 1: Login with correct format (form data)
        print("=== Test 1: Login with form data (correct format) ===")
        response = await client.post(
            "http://localhost:8000/users/login",
            data={
                "username": "testuser@gmail.com",
                "password": "testpass123"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        
        # Test 2: Try logging in with JSON (incorrect format)
        print("=== Test 2: Login with JSON data (wrong format) ===")
        response = await client.post(
            "http://localhost:8000/users/login",
            json={
                "username": "testuser@gmail.com",
                "password": "testpass123"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}\n")
        
        # Test 3: Login with invalid email format
        print("=== Test 3: Login with invalid email (harounbangura@gmail.com.com) ===")
        response = await client.post(
            "http://localhost:8000/users/login",
            data={
                "username": "harounbangura@gmail.com.com",
                "password": "76544567"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}\n")

asyncio.run(test_logins())
