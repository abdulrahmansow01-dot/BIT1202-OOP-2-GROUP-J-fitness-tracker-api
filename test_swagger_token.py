import asyncio
import httpx

async def test_swagger_auth():
    async with httpx.AsyncClient() as client:
        print("Testing Admin credentials for Swagger UI...\n")
        
        # Test the exact credentials
        response = await client.post(
            "http://localhost:8000/users/login",
            data={
                "username": "admin@gmail.com",
                "password": "567876678"
            }
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Credentials are VALID\n")
            print(f"Access Token:")
            print(f"{data['access_token']}\n")
            print(f"Token Type: {data['token_type']}\n")
            print("In Swagger UI:")
            print("1. Enter this in the password/token field")
            print("2. Leave client_id and client_secret empty")
        else:
            print(f"\n✗ Error: {response.json()}")

asyncio.run(test_swagger_auth())
