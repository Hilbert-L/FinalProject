#!/usr/bin/python3
import requests
import googlemaps
import pandas as pd 
import random

# Run this script when the localhost api is running on port 8000

# Global USED
NUM_FAKE_USERS = 2000
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

# Create 2000 fake users
for user in range(0, NUM_FAKE_USERS + 1):
    user_data = {
        "firstname": f"firstname_{user}",
        "lastname": f"lastname_{user}",
        "username": f"fake_user_{user}",
        "email": f"fake_user_{user}@example.com",
        "password": "$Test1234",
        "phonenumber": 0
    }

    response = requests.post(create_user_url, headers=headers, json=user_data)

df = pd.read_csv("australian-postcodes.csv")
search_combos = list(zip(list(df["Postcode"]), list(df["Suburb"])))

api_key = 'AIzaSyB4Bsp9jhz4i39NidfXExaaZV89o8jP5To'
gmaps = googlemaps.Client(key=api_key)

for (postcode, suburb) in search_combos:
    try:
        places = gmaps.places(query=f'{suburb} addresses', type='address', radius=200)['results']
        for result in places:
            try:
                address = result['formatted_address']

                if "australia" not in address.lower():
                    continue

                lat = result['geometry']['location']['lat']
                lng = result['geometry']['location']['lng']

                # This will be the car space owner
                carspace_owner_id = random.randint(0, NUM_FAKE_USERS)

                carspace_url = f'http://0.0.0.0:8000/carspace/create_car_space_no_token?fakeuser_id={carspace_owner_id}'

                carspace_data = {
                    "title": "string",
                    "address": address,
                    "suburb": suburb,
                    "postcode": postcode,
                    "longitude": lng,
                    "latitude": lat,
                    "width": round(random.uniform(2.4, 2.7), 2),
                    "breadth": round(random.uniform(4.8, 5.4), 2),
                    "spacetype": random.choice(SPACE_TYPES),
                    "accesskeyrequired": random.choice(ACCESS_KEY_REQUIRED),
                    "vehiclesize": random.choice(VEHICLE_TYPES),
                    "currency": "AUD",
                    "price": random.uniform(10, 50),
                    "frequency": "daily"
                }

                response = requests.post(carspace_url, headers=headers, json=carspace_data)
                current_carspace_id = response.json()["CarSpaceId"]

                num_reviews = random.randint(0, 100)

                # This will be the potential reviewers which cannot be the carspace owner
                reviewer_ids = [val for val in range(NUM_FAKE_USERS + 1) if val != carspace_owner_id]

                for review in range(num_reviews):
                    reviewer_id = random.choice(reviewer_ids)

                    carspace_review_url = f'http://0.0.0.0:8000/carspace/create_review_no_token?fakeuser_id={reviewer_id}'

                    carspace_review_data = {
                        "ownerusername": f"fake_user_{carspace_owner_id}",
                        "overall": random.randint(0, 5),
                        "location": random.randint(0, 5),
                        "cleanliness": random.randint(0, 5),
                        "easeofaccess": random.randint(0, 5),
                        "communication": random.randint(0, 5),
                        "writtenfeedback": f"Fake Review from fake_user{reviewer_id}"
                    }

                    requests.post(carspace_review_url, headers=headers, json=carspace_review_data)

            except KeyError as E:
                print(f"KeyError: Could not get place information: {E}")
                continue
            
    except KeyError as E:
        print(f"KeyError: Could not get places {E}")
        continue