#!/usr/bin/python3 
from pymongo import MongoClient
import os 

MongoDBUser = "GenericUser"
MongoDBPassword = "$Gdaymate123"
MongoDBCluster = "atlascluster"
connectionString = f"mongodb+srv://{MongoDBUser}:{MongoDBPassword}@{MongoDBCluster}.ksdmto3.mongodb.net/?retryWrites=true"
client = MongoClient(connectionString)

# Access the project database
car_reservations_db = client["CarSpaceReservations"]
bank_information_collections = car_reservations_db["BankInformation"]

for userId in range(0, 2001):
    username = f"fake_user_{userId}"
    payload = {
        "username": f"fake_user_{userId}",
        "bankname": "fake_bank",
        "accountname": f"fake_account_{userId}",
        "accountbsb": "123-456",
        "accountnumber": "100000000",
        "cardtitle": f"fake_card_title_{userId}",
        "cardnumber": "0000-0000-0000-0000",
        "cardexpirydate": "12/30",
        "cardccv": "000",
        "balance": 0
    }

    try:
        bank_information_collections.insert_one({**payload})
        print("Account created")

    except Exception as E:
        print(f"Exception occurred: {E}")
