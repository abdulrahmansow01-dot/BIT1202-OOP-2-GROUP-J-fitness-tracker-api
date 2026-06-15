import asyncio
import httpx

async def test_fresh_users():
    users = [
        ("alex@gmail.com", "alex123456"),
        ("admin@gmail.com", "admin123456"),
        ("test@gmail.com", "test123456"),
    ]
    
    async with httpx.AsyncClient() as client:
        print("Testing fresh users:\n")
        for email, password in users:
            response = await client.post(
                "http://localhost:8000/users/login",
                data={
                    "username": email,
                    "password": password
                }
            )
            if response.status_code == 200:
                print(f"✓ {email}")
                print(f"  Password: {password}")
                print(f"  Token: {response.json()['access_token'][:40]}...\n")
            else:
                print(f"✗ {email}: {response.status_code}")
                print(f"  Error: {response.json()['detail']}\n")

asyncio.run(test_fresh_users())
