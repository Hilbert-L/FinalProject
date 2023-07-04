#!/usr/bin/python3
from pymongo import MongoClient
import os 

MongoDBUser = os.getenv("MONGODB_USER")
MongoDBPassword = "$Gdaymate123"
MongoDBCluster = os.getenv("MONGODB_CLUSTER_NAME")
connectionString = f"mongodb+srv://{MongoDBUser}:{MongoDBPassword}@{MongoDBCluster}.ksdmto3.mongodb.net/?retryWrites=true"
client = MongoClient(connectionString)

# Access the project database
car_reservations_db = client["CarSpaceReservations"]
client.drop_database(car_reservations_db)