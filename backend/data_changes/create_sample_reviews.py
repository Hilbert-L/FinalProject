#!/usr/bin/python3
from pymongo import MongoClient
import os 
import json
import random
import re 
import asyncio
from concurrent.futures import ThreadPoolExecutor

NUM_FAKE_USERS = 2000
MongoDBUser = "GenericUser"
MongoDBPassword = "$Gdaymate123"
MongoDBCluster = "atlascluster"
connectionString = f"mongodb+srv://{MongoDBUser}:{MongoDBPassword}@{MongoDBCluster}.ksdmto3.mongodb.net/?retryWrites=true"
client = MongoClient(connectionString)
# Access the project database
car_reservations_db = client["CarSpaceReservations"]

car_space_review_collections = car_reservations_db["CarSpaceReviews"]
car_space_collections = car_reservations_db["CarSpaces"]

car_space_collection_cursor = car_space_collections.find({})

def create_car_space_review(document):
    global NUM_FAKE_USERS
    global car_space_review_collections

    document_str = json.dumps(document, default=str)
    document_dict = json.loads(document_str)
    username = document["username"]
    if re.match("^fake_user_[0-9]+$", username):
        try:
            carspace_owner_id = document_dict["username"].split("fake_user_")[1]
            carspace_id = document_dict["carspaceid"]
            num_reviews = random.randint(0, 50)
            reviewer_ids = [val for val in range(NUM_FAKE_USERS + 1) if val != carspace_owner_id]

            for review in range (num_reviews):
                reviewer_id = random.choice(reviewer_ids)

                review_payload = {
                    "reviewer_username" : f"fake_user_{reviewer_id}",
                    "carspaceid": carspace_id,
                    "ownerusername": f"fake_user_{carspace_owner_id}",
                    "overall": random.randint(0, 5),
                    "location": random.randint(0, 5),
                    "cleanliness": random.randint(0, 5),
                    "easeofaccess": random.randint(0, 5),
                    "communication": random.randint(0, 5),
                    "writtenfeedback": f"Fake Review from fake_user {reviewer_id}"
                }
                car_space_review_collections.insert_one({**review_payload})
                print("Car space has been added")

        except Exception as E:
            print(f"Exception occured: {E}")

async def main():
    with ThreadPoolExecutor(max_workers=2000) as executor:
        executor.map(create_car_space_review, car_space_collection_cursor)


if __name__ == '__main__':
    asyncio.run(main())