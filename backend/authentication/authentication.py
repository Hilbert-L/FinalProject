import jwt 
from fastapi import Header
from decouple import config
from jwt import PyJWTError
from typing import Optional, List
from models.UserAuthentication import UserSchema
from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections


users_db : List[UserSchema] = []

# This is in the .env file, it is generate through secrets.token_hex(16)
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# Helper function to generate JWT token
async def generate_token(username: str):
    payload = {"username": username}
    token = await jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# Helper function to verify JWT token 
# def verify_token(token: Annotated[str, Header(...)]):
async def verify_token(token: str = Header(...)):
    try:
        payload = await jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        username = payload.get("username")

        user = users_collections.find_one({"username": username})

        if user and user["isloggedin"]:
            return username 

        return None 
    
    except PyJWTError:
        return None