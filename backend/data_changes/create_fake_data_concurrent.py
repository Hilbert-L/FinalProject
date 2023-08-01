#!/usr/bin/python3
import requests
import googlemaps
import pandas as pd 
import random
from concurrent.futures import ThreadPoolExecutor
import asyncio

# Run this script when the localhost is running on port 8000 for FASTAPI

# Globals

API_KEY = 'AIzaSyB4Bsp9jhz4i39NidfXExaaZV89o8jP5To'
MAX_WORKERS = 50
NUM_FAKE_USERS = 1000

ACCESS_KEY_REQUIRED = [True, False]
SPACE_TYPES = [
    "indoor-lot"
    , "outdoor-lot"
    , "undercover"
    , "outside"
    , "carport"
    , "driveway"
    , "locked-garage"
]

VEHICLE_TYPES = [
   "hatchback"
  , "sedan"
  , "suv"
  , "ev"
  , "ute"
  , "wagon"
  , "van"
  , "bike"
]

create_user_url = 'http://0.0.0.0:8000/user/auth/register'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# Function to create a fake user
async def create_fake_user(user_data):
    global create_user_url
    global headers
    response = requests.post(create_user_url, headers=headers, json=user_data)
    return response


async def create_fake_users():
    tasks = []
    for user in range(0, NUM_FAKE_USERS + 1):
        user_data = {
            "firstname": f"firstname_{user}",
            "lastname": f"lastname_{user}",
            "username": f"fake_user_{user}",
            "email": f"fake_user_{user}@example.com",
            "password": "$Test1234",
            "phonenumber": 0
        }

        task = asyncio.create_task(create_fake_user(user_data))
        tasks.append(task)

    # Wait for all user creation tasks to complete
    await asyncio.gather(*tasks)

    
# # Function to create a fake car space
async def create_fake_carspace(postcode, suburb, result):
    pass
#     # ... (rest of the car space creation code)

#     # Return the car space ID after creation
#     return current_carspace_id

# # Function to create fake reviews
async def create_fake_reviews(postcode, suburb, result, car_space_id):
    pass
#     # ... (rest of the review creation code)
#     pass


# Create 1000 fake users using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    for user in range(0, NUM_FAKE_USERS + 1):
        user_data = {
            "firstname": f"firstname_{user}",
            "lastname": f"lastname_{user}",
            "username": f"fake_user_{user}",
            "email": f"fake_user_{user}@example.com",
            "password": "$Test1234",
            "phonenumber": 0
        }

        future_user = executor.submit(create_fake_user, user_data)

async def main():
    await create_fake_users()

    df = pd.read_csv("australian-postcodes.csv")
    search_combos = list(zip(list(df["Postcode"]), list(df["Suburb"])))

    gmaps = googlemaps.Client(key=API_KEY)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for (postcode, suburb) in search_combos:
            try:
                places = gmaps.places(query=f'{suburb} addresses', type='address', radius=200)['results']
                for result in places:
                    # Submit concurrent tasks for creating car spaces
                    future_carspace = executor.submit(create_fake_carspace, postcode, suburb, result)

                    # Wait for the car space task to complete before moving on to reviews
                    car_space_id = future_carspace.result()
                    
                    # Submit concurrent tasks for creating reviews
                    future_reviews = executor.submit(create_fake_reviews, postcode, suburb, result, car_space_id)
                    # No need to wait for reviews since we are proceeding to the next search_combos iteration
                    
            except KeyError as E:
                print(f"KeyError: Could not get places {E}")
                continue

if __name__ == '__main__':
    asyncio.run(main())