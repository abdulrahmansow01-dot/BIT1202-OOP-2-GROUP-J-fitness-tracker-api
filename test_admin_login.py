import asyncio
import httpx

async def test_admin_user():
    """
    Test various possible email addresses for the Admin user
    """
    
    # Possible emails the user might have registered with
    possible_emails = [
        "admin@gmail.com",
        "Admin@gmail.com",
        "admin",
        "Admin",
        "admin@example.com",
        "admin@test.com",
    ]
    
    password = "567876678"
    
    async with httpx.AsyncClient() as client:
        print("Testing login with password: 567876678\n")
        print("Trying different possible emails/usernames:\n")
        
        for username in possible_emails:
            response = await client.post(
                "http://localhost:8000/users/login",
                data={
                    "username": username,
                    "password": password
                }
            )
            
            status_icon = "✓" if response.status_code == 200 else "✗"
            print(f"{status_icon} {username}: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  SUCCESS! Token: {response.json()['access_token'][:40]}...\n")
            elif response.status_code == 401:
                print(f"  (wrong credentials)\n")
            else:
                print(f"  Error: {response.json()['detail']}\n")

asyncio.run(test_admin_user())
