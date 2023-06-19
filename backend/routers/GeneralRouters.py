from fastapi import APIRouter
from models.UserAuthentication import UserSchema
from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections

GeneralRouter = APIRouter()

@GeneralRouter.get("/users", tags=["Information"])
async def get_users():
    users = list(users_collections.find())
    return {"users": users}

@GeneralRouter.get("/admins", tags=["Information"])
async def get_admins():
    admins = list(admin_collections.find())
    return {"admins": admins}

@GeneralRouter.get("/carspace", tags=["Information"])
async def get_car_spaces():
    carspaces = list(car_space_collections.find())
    return {"car_spaces": carspaces}

@GeneralRouter.get("/carspacereviews", tags=["Information"])
async def get_car_space_reviews():
    carspace_reviews = list(car_space_review_collections.find())
    return {"carspace_reviews": carspace_reviews}