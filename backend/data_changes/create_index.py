#!/usr/bin/python3
from pymongo import MongoClient
import os 
import json
import random
import re 
import pymongo
import asyncio
from concurrent.futures import ThreadPoolExecutor

NUM_FAKE_USERS = 2000
MongoDBUser = "GenericUser"
MongoDBPassword = "$Gdaymate123"
MongoDBCluster = "atlascluster"
connectionString = f"mongodb+srv://{MongoDBUser}:{MongoDBPassword}@{MongoDBCluster}.ksdmto3.mongodb.net/?retryWrites=true"
client = MongoClient(connectionString)

car_reservations_db = client["CarSpaceReservations"]
users_collections = car_reservations_db["Users"]
admin_collections = car_reservations_db["Admins"]
car_space_collections = car_reservations_db["CarSpaces"]
car_space_review_collections = car_reservations_db["CarSpaceReviews"]
car_space_image_collections = car_reservations_db["CarSpaceImages"]
bank_information_collections = car_reservations_db["BankInformation"]
transaction_information_collections = car_reservations_db["TransactionInformation"]
booking_collections = car_reservations_db["BookingInformation"]
booking_id_collections = car_reservations_db["BookingIDs"]
car_space_id_collections = car_reservations_db["CarSpaceIDs"]


users_collections.create_index("username")
car_space_collections.create_index("username")
booking_collections.create_index("carspaceid")
car_space_review_collections.create_index([("ownerusername", pymongo.ASCENDING), ("carspaceid", pymongo.ASCENDING)])
car_space_image_collections.create_index("username")
car_space_collections.create_index([("price", pymongo.ASCENDING), ("spacetype", pymongo.ASCENDING), ("vehiclesize", pymongo)])

