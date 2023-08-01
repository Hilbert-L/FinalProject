#!/usr/bin/python3
from pymongo import MongoClient
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import os 
from typing import Optional
import numpy as np
import pandas as pd 

MongoDBUser = "GenericUser"
MongoDBPassword = "$Gdaymate123"
MongoDBCluster = "atlascluster"
connectionString = f"mongodb+srv://{MongoDBUser}:{MongoDBPassword}@{MongoDBCluster}.ksdmto3.mongodb.net/?retryWrites=true"
client = MongoClient(connectionString)
car_reservations_db = client["CarSpaceReservations"]
users_collections = car_reservations_db["Users"]
car_space_review_collections = car_reservations_db["CarSpaceReviews"]
user_recommended_carspaces = car_reservations_db["RecommendedCarSpaces"]

user_recommended_carspaces.delete_many({})

fields_to_include = ["carspaceid", "reviewer_username", "overall"]
carspace_review_cursor = car_space_review_collections.find({})
filtered_results = [{field: document[field] for field in fields_to_include if field in document} for document in carspace_review_cursor]


df = pd.DataFrame(filtered_results)
df.to_csv("car_space_reviews.csv")
df = df[["carspaceid", "overall", "reviewer_username"]].dropna(subset=["reviewer_username"])
df = df[df["reviewer_username"].str.match("fake_user")]
df["reviewer_id"] = df["reviewer_username"].str.split("fake_user_").str[1].astype(int)
df = df[["carspaceid", "overall", "reviewer_id"]]
df["overall"] = df["overall"].add(1)
df["overall"] = df["overall"].add(1)

reader = Reader(rating_scale=(1, 6))
data = Dataset.load_from_df(df[["reviewer_id", "carspaceid", "overall"]], reader)

model = SVD()

trainset = data.build_full_trainset()
model.fit(trainset)
carspace_ids = df["carspaceid"].unique()

for reviewer_id in range(2001):
    predictions = []
    for carspace_id in carspace_ids:
        prediction = model.predict(reviewer_id, carspace_id)
        predictions.append((carspace_id, prediction.est))

    predictions.sort(key=lambda x: x[1], reverse=True)
    ordered_car_spaces = [int(p[0]) for p in predictions]
    recommender_payload = {
        "username": f"fake_user_{reviewer_id}",
        "ordered_carspaces": ordered_car_spaces
    }
    # Need to convert it to int because you cannot insert numpy.int64
    user_recommended_carspaces.insert_one({**recommender_payload})
    print(f"Successfully inserted for user {reviewer_id}")
