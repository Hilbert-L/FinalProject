#!/usr/bin/python3
from pymongo import MongoClient
from decouple import config
import click 

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

@click.command()
@click.option('--LogoutUsers', default=True, help='Logout Users from Car Space Database')
@click.option('--GetPasswords', default=True, help='Show the password of all existing users in the Car Space Database')
@click.option('--DeleteAdmins', default=False, help='Delete Database')
@click.option('--DeleteUsers', default=False, help='Delete Database')
@click.option('--DeleteCarSpacesAndReviews', default=False, help='Delete Database')
@click.option('--DeleteDatabase', default=False, help='Delete Database')
@click.option('--LogoutUser', default=False, help='Specify user from the database to logout')
def database_modifications(LogoutUsers, GetPasswords, DeleteAdmins, DeleteUsers, DeleteCarSpacesAndReviews, DeleteDatabase, LogoutUser):

    '''
    A simple script used to make modifications to the existing database that is hosted via mongodb.
    If by default we just do python3 database_modificaations, the script will just set the logout status of all existing users to False
    as well as tell us all the passwords of existing users in the mongodb database.

    --LogoutUsers: Set Logout to True for all users in the collection of the database
    --GetPasswords: Get the passwords of all existing users in the database
    --DeleteAdmins: look at database and clear the admins collections
    --DeleteUsers: Delete Users from users collections
    --DeleteCarSpacesAndReviews: Delete Car spaces and car space reviews from the collections
    --DeleteDatabase: Delete the contents of the database
    --LogoutUser: Set a specific username to logout mode
    '''

    global car_reservations_db, users_collections, admin_collections, car_space_collections, car_space_review_collections

    if LogoutUsers:
        try:
            users_collections.update_many({}, {"$set": {"isloggedin": "False"}})
            print("Successfully Logged out all users!!!")

        except Exception as e:
            print(f"Could not logout users due to error: {e}")

    if GetPasswords:
        try:
            keys = ['username', 'passwordunhashed']
            query = {key: {"$exists": True} for key in keys}
            results = users_collections.find(query)
            for result in results:
                print(f"username: {result['username']}, password: {result['passwordunhashed']}")

            print("Successfully Printed out passwords for all users!!!")
        except Exception as e:
            print(f"Couldn't get passwords for users due to error: {e}")


    if DeleteAdmins:
        try:
            admin_collections.drop()
            print("Successfully Deleted Admins!!!")

        except Exception as e:
            print(f"Could not delete admins due to error: {e}")

    if DeleteUsers:
        try:
            users_collections.drop()
            print("Successfully Deleted Users")

        except Exception as e:
            print(f"Could not delete users due to error: {e}")

    if DeleteCarSpacesAndReviews:
        try:
            car_space_collections.drop()
            car_space_review_collections.drop()
            print("Successfully Deleted Car Space collections and reviews!!!")

        except Exception as e:
            print(f"Could not delete car spaces and reviews due to error: {e}")

    if DeleteDatabase:
        try:
            client.drop_database(car_reservations_db)
            print("Successfully Dropped the database!!!")

        except Exception as e:
            print(f"Could not drop the database due to error: {e}")
    
    if LogoutUser:
        users_collections.update_one({"username": LogoutUser}, {"$set": {"isloggedin": "False"}})
        print(f"successfully logged out user {LogoutUser}!!!")

if __name__ == '__main__':
    database_modifications()