from fastapi import APIRouter
from models.UserAuthentication import UserSchema
from mongodbconnect.mongodb_connect import users_collections, admin_collections, car_space_review_collections, car_space_collections
import json

GeneralRouter = APIRouter()

@GeneralRouter.get("/", tags=["Test Route"])
async def test():
    return {"Message": "Test Route"}

@GeneralRouter.get("/users", tags=["Information"])
async def get_users():
    # users = list(users_collections.find())
    user_cursor = users_collections.find({})
    users = []
    for document in user_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        users.append(document_dict)
    return {"users": users}

@GeneralRouter.get("/admins", tags=["Information"])
async def get_admins():
    admin_cursor = admin_collections.find({})
    admins = []
    for document in admin_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        admins.append(document_dict)
    return {"admins": admins}

@GeneralRouter.get("/carspace", tags=["Information"])
async def get_car_spaces():
    carspace_cursor = car_space_collections.find({})
    carspaces = []
    for document in carspace_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        carspaces.append(document_dict)
    return {"car_spaces": carspaces}

@GeneralRouter.get("/carspacereviews", tags=["Information"])
async def get_car_space_reviews():
    carspace_review_cursor = car_space_review_collections.find()
    carspace_reviews = []
    for document in carspace_review_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        carspace_reviews.append(document_dict)
    return {"carspace_reviews": carspace_reviews}