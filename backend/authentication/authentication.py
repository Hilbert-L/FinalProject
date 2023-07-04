import jwt 
from fastapi import Header
from jwt import PyJWTError
from jwt.exceptions import PyJWTError
from typing import Optional, List
from models.UserAuthentication import UserSchema
from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections
from passlib.context import CryptContext
import os 

# This is in the .env file, it is generate through secrets.token_hex(16)
JWT_SECRET = "2ea7e571df496b58d0cd8cc4c0a329a8"
JWT_ALGORITHM = "HS256"

# Password hashing context
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Helper function to generate JWT token
def generate_token(username: str):
    payload = {"username": username}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# Helper function to verify JWT token 
async def verify_user_token(token: str = Header(...)):
    try:
        payload = jwt.decode(
            token, JWT_SECRET, 
            JWT_ALGORITHM)
        username = payload.get("username")

        user = users_collections.find_one({"username": username})
        if user is not None and user["isloggedin"] and user["isactive"]:
            return username 
        return None 
    
    except PyJWTError as e:
        print(f"Error decoding JWT: {e}")
        return None
    

async def verify_admin_token(token: str = Header(...)):
    try:
        payload = jwt.decode(
            token, JWT_SECRET, 
            algorithms=[JWT_ALGORITHM])
        username = payload.get("username")

        user = admin_collections.find_one({"username": username})
        if user is not None and user["isloggedin"] and user["isactive"]:
            return username 
        return None 
    
    except PyJWTError as e:
        print(f"Error decoding JWT: {e}")
        return None