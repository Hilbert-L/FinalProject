#!/usr/bin/python3
from pymongo import MongoClient
import os 


MongoDBUser = "GenericUser"
MongoDBPassword = "$Gdaymate123"
MongoDBCluster = "atlascluster"
connectionString = f"mongodb+srv://{MongoDBUser}:{MongoDBPassword}@{MongoDBCluster}.ksdmto3.mongodb.net/?retryWrites=true"
client = MongoClient(connectionString)
car_reservations_db = client["CarSpaceReservations"]
users_collections = car_reservations_db["Users"]
car_space_collections = car_reservations_db["CarSpaces"]


delete_query = {"username": {"$regex": "fake_user_[0-9]+"}}
users_collections.delete_many(delete_query)
# car_space_collections.delete_many(delete_query)