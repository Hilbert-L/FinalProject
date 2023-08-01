#!/usr/bin/python3
# Run this script when the localhost api is running on port 8000
import requests

url = 'http://0.0.0.0:8000/user/auth/register'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# Create 2000 fake users
for user in range(0, 2001):
    data = {
        "firstname": f"firstname_{user}",
        "lastname": f"lastname_{user}",
        "username": f"fake_user_{user}",
        "email": f"fake_user{user}@example.com",
        "password": "$Test1234",
        "phonenumber": 0
    }

    response = requests.post(url, headers=headers, json=data)
