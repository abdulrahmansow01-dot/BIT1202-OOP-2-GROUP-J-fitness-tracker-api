import asyncio
import httpx

async def test_register():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/users/register",
            json={
                "full_name": "haroun bamgura",
                "email": "harounbangura@gmail.com.com",
                "password": "76544567"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

asyncio.run(test_register())
