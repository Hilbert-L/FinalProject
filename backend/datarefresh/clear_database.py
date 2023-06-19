#!/usr/bin/python3
from mongodbconnect.mongodb_connect import client, car_reservations_db
client.drop_database(car_reservations_db)