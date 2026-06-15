import asyncio
import httpx

async def test_complete_flow():
    async with httpx.AsyncClient() as client:
        print("=" * 60)
        print("COMPLETE LOGIN TEST FLOW")
        print("=" * 60)
        
        # Register new user
        print("\n1️⃣  REGISTER NEW USER")
        print("-" * 60)
        register_response = await client.post(
            "http://localhost:8000/users/register",
            json={
                "full_name": "Test User 2",
                "email": "testuser2@test.com",
                "password": "password123"
            }
        )
        print(f"Status: {register_response.status_code}")
        if register_response.status_code == 201:
            user_data = register_response.json()
            print(f"✓ User registered: {user_data['email']}")
            print(f"  ID: {user_data['id']}")
            print(f"  Active: {user_data['is_active']}")
        else:
            print(f"✗ Error: {register_response.text}")
            return
        
        # Test login with form data
        print("\n2️⃣  LOGIN WITH FORM DATA (/users/login)")
        print("-" * 60)
        login_response = await client.post(
            "http://localhost:8000/users/login",
            data={
                "username": "testuser2@test.com",
                "password": "password123"
            }
        )
        print(f"Status: {login_response.status_code}")
        if login_response.status_code == 200:
            token_data = login_response.json()
            print(f"✓ Login successful!")
            print(f"  Token: {token_data['access_token'][:40]}...")
            print(f"  Type: {token_data['token_type']}")
            token = token_data['access_token']
        else:
            print(f"✗ Error: {login_response.text}")
            return
        
        # Test login with JSON
        print("\n3️⃣  LOGIN WITH JSON (/users/login-json)")
        print("-" * 60)
        login_json_response = await client.post(
            "http://localhost:8000/users/login-json",
            json={
                "email": "testuser2@test.com",
                "password": "password123"
            }
        )
        print(f"Status: {login_json_response.status_code}")
        if login_json_response.status_code == 200:
            token_data = login_json_response.json()
            print(f"✓ Login successful!")
            print(f"  Token: {token_data['access_token'][:40]}...")
            print(f"  Type: {token_data['token_type']}")
        else:
            print(f"✗ Error: {login_json_response.text}")
        
        # Use token to access protected endpoint
        print("\n4️⃣  USE TOKEN TO ACCESS /users/me")
        print("-" * 60)
        me_response = await client.get(
            "http://localhost:8000/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"Status: {me_response.status_code}")
        if me_response.status_code == 200:
            me_data = me_response.json()
            print(f"✓ Token is valid!")
            print(f"  Current user: {me_data['email']}")
            print(f"  Name: {me_data['full_name']}")
        else:
            print(f"✗ Error: {me_response.text}")

asyncio.run(test_complete_flow())
