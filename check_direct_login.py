import httpx

with httpx.Client() as client:
    response = client.post(
        'http://127.0.0.1:8000/users/login',
        data={'username':'admin@gmail.com','password':'567876678'}
    )
    print(response.status_code)
    print(response.text)
