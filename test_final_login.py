import asyncio
import httpx

async def test_both_login_methods():
    async with httpx.AsyncClient() as client:
        # Test 1: Original form-data endpoint
        print("=== Test 1: /users/login with form-data ===")
        response = await client.post(
            "http://localhost:8000/users/login",
            data={
                "username": "testuser@gmail.com",
                "password": "testpass123"
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Token received: {data['access_token'][:30]}...\n")
        else:
            print(f"✗ Error: {response.json()}\n")
        
        # Test 2: New JSON endpoint
        print("=== Test 2: /users/login-json with JSON body ===")
        response = await client.post(
            "http://localhost:8000/users/login-json",
            json={
                "email": "testuser@gmail.com",
                "password": "testpass123"
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Token received: {data['access_token'][:30]}...\n")
        else:
            print(f"✗ Error: {response.json()}\n")
        
        # Test 3: Wrong password
        print("=== Test 3: Login with wrong password (JSON) ===")
        response = await client.post(
            "http://localhost:8000/users/login-json",
            json={
                "email": "testuser@gmail.com",
                "password": "wrongpassword"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")

asyncio.run(test_both_login_methods())
