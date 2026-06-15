import asyncio
import httpx

async def test_login_debug():
    """
    Test different login attempts to help diagnose 401 errors.
    Try the credentials that are KNOWN to work first.
    """
    
    # These are the fresh users we just created - they definitely work
    working_credentials = [
        ("alex@gmail.com", "alex123456"),
        ("admin@gmail.com", "admin123456"),
        ("test@gmail.com", "test123456"),
    ]
    
    async with httpx.AsyncClient() as client:
        print("=" * 70)
        print("TESTING KNOWN WORKING CREDENTIALS")
        print("=" * 70)
        
        for email, password in working_credentials:
            print(f"\nTrying: {email} / {password}")
            
            # Test with form-data
            response = await client.post(
                "http://localhost:8000/users/login",
                data={
                    "username": email,
                    "password": password
                }
            )
            
            if response.status_code == 200:
                print(f"✓ SUCCESS with /users/login (form-data)")
                print(f"  Token: {response.json()['access_token'][:30]}...")
            else:
                print(f"✗ FAILED with /users/login: {response.status_code}")
                print(f"  Error: {response.json()['detail']}")
        
        print("\n" + "=" * 70)
        print("COMMON MISTAKES TO CHECK:")
        print("=" * 70)
        print("""
1. ❌ Sending JSON to /users/login (wrong - it expects form-data)
   ✓ Solution: Use form-data instead
   
2. ❌ Using wrong password (different from registration)
   ✓ Solution: Use password you registered with
   
3. ❌ Using JSON endpoint without email field
   ✓ Solution: For /users/login-json, use "email" not "username"
   
4. ❌ Forgetting Bearer prefix in Authorization header
   ✓ Solution: Use "Authorization: Bearer <token>"
   
5. ❌ Typo in email address
   ✓ Solution: Check for spaces or wrong domain
        """)

asyncio.run(test_login_debug())
