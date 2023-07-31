#!/usr/bin/python3
from pymongo import MongoClient
import os 
import requests 
import googlemaps 
import pandas as pd 
import random

# Global Lists for random values to generate
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

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# Run this script when the localhost api is running on port 8000
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
                lat = result['geometry']['location']['lat']
                lng = result['geometry']['location']['lng']

                random_id = random.randint(0, 2000)

                url = f'http://0.0.0.0:8000/carspace/create_car_space_no_token?fakeuser_id={random_id}'

                data = {
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

                requests.post(url, headers=headers, json=data)

            except KeyError as E:
                print(f"KeyError: Could not get place information: {E}")
                continue
            
    except KeyError as E:
        print(f"KeyError: Could not get places {E}")
        continue