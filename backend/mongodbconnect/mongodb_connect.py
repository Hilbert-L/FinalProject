from pymongo import MongoClient
from decouple import config

MongoDBUser = config("mongodbUser")
MongoDBPassword = config("mongodbPassword")
MongoDBCluster = config("mongodbClusterName")
connectionString = f"mongodb+srv://{MongoDBUser}:{MongoDBPassword}@{MongoDBCluster}.ksdmto3.mongodb.net/?retryWrites=true"
client = MongoClient(connectionString)

# Access the project database
car_reservations_db = client["CarSpaceReservations"]
users_collections = car_reservations_db["Users"]
admin_collections = car_reservations_db["Admins"]
car_space_collections = car_reservations_db["CarSpaces"]
car_space_review_collections = car_reservations_db["CarSpaceReviews"]
