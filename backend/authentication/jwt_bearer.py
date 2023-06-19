from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import time
import jwt 
from decouple import config

# This is in the .env file, it is generate through secrets.token_hex(16)
# ALGORITHM is HS256
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# Function returns the generate tokens (JWTs)
def token_response(token: str):
    return {
        "access token": token
    }

def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 1200
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token['expiry'] >= time.time() else None
    except:
        return {}

class jwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool=True):
        super(jwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request : Request):
        credentials : HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code = 403, details="Invalid or Expired token!")
            return credentials.credentials
        else:
            raise HTTPException(status_code = 403, details="Invalid or Expired Token!")

    def verify_jwt(self, jwtoken : str):
        isTokenValid : bool = False # A False flag
        payload = decodeJWT(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid
