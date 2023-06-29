#!/usr/bin/python3
from pymongo import MongoClient
import os 

MongoDBUser = os.getenv("MONGODB_USER")
MongoDBPassword = "$Gdaymate123"
MongoDBCluster = os.getenv("MONGODB_CLUSTER_NAME")
connectionString = f"mongodb+srv://{MongoDBUser}:{MongoDBPassword}@{MongoDBCluster}.ksdmto3.mongodb.net/?retryWrites=true"
client = MongoClient(connectionString)

print(connectionString)

# Access the project database
car_reservations_db = client["CarSpaceReservations"]
admin_collections = car_reservations_db["Admins"]