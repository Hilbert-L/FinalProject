from pymongo import MongoClient
import os 

MongoDBUser = os.getenv("MONGODB_USER")
MongoDBPassword = "$Gdaymate123"
MongoDBCluster = os.getenv("MONGODB_CLUSTER_NAME")
connectionString = f"mongodb+srv://{MongoDBUser}:{MongoDBPassword}@{MongoDBCluster}.ksdmto3.mongodb.net/?retryWrites=true"
client = MongoClient(connectionString)

# Access the project database
car_reservations_db = client["CarSpaceReservations"]
users_collections = car_reservations_db["Users"]
admin_collections = car_reservations_db["Admins"]
car_space_collections = car_reservations_db["CarSpaces"]
car_space_review_collections = car_reservations_db["CarSpaceReviews"]
car_space_image_collections = car_reservations_db["CarSpaceImages"]
bank_information_collections = car_reservations_db["BankInformation"]
transaction_information_collections = car_reservations_db["TransactionInformation"]