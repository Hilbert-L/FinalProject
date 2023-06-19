import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from typing import Optional, List
from models.UserAuthentication import UserSchema
from models.CreateCarSpace import CarSpaceReview, CarSpaceSchema, CreateCarSpaceSchema
from models.UpdateCarSpace import UpdateCarSpaceAddress, UpdateCarSpaceDimensions, UpdateCarSpacePrice
from wrappers.wrappers import check_token
from passlib.context import CryptContext
from decouple import config
from authentication.authentication import verify_token
from routers.GeneralRouters import GeneralRouter
from routers.ProtectedEndpoints import ProtectedRouter
from routers.UserRouters import UserRouter
from routers.CarSpaceRouters import CarSpaceRouter

# Admins to the database + routes + models
# Write unit tests with pymongo and mock objects
# Create the frontend

app = FastAPI(title=config("projectName"))

app.include_router(GeneralRouter)
app.include_router(ProtectedRouter)
app.include_router(UserRouter)
app.include_router(CarSpaceRouter)

# Can do this instead of CLI (python3 main.py) in which it will run on local host 9000 
# instead of port 8000 (which is entered via uvicorn main:app --reload)
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port = '9000')
