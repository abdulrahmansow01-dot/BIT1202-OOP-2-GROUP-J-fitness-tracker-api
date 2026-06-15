import asyncio
import httpx

async def test_all_existing_users():
    # Known users and test passwords
    users_to_test = [
        ("alex@gmail.com", "alex123"),  # Unknown password, will fail
        ("admin@gmail.com", "admin123"),  # Unknown password, will fail
        ("testuser@gmail.com", "testpass123"),  # Known to work
    ]
    
    async with httpx.AsyncClient() as client:
        print("Testing login with all existing users:\n")
        for email, password in users_to_test:
            response = await client.post(
                "http://localhost:8000/users/login",
                data={
                    "username": email,
                    "password": password
                }
            )
            status = "✓" if response.status_code == 200 else "✗"
            print(f"{status} {email}: {response.status_code}")
            if response.status_code != 200:
                print(f"   Error: {response.json()['detail']}")

asyncio.run(test_all_existing_users())
