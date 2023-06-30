from fastapi import APIRouter, Depends
from models.UserAuthentication import UserSchema
from mongodbconnect.mongodb_connect import users_collections, admin_collections, car_space_review_collections, car_space_collections
import json
from wrappers.wrappers import check_token
from authentication.authentication import verify_admin_token

GeneralRouter = APIRouter()

@GeneralRouter.get("/", tags=["Test Route"])
async def test():
    return {"Message": "Test Route"}

@GeneralRouter.get("/users", tags=["Admin Information"])
@check_token
async def get_users(token: str = Depends(verify_admin_token)):
    # users = list(users_collections.find())
    user_cursor = users_collections.find({})
    users = []
    for document in user_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        users.append(document_dict)
    return {"users": users}

@GeneralRouter.get("/admins", tags=["Admin Information"])
@check_token
async def get_admins(token: str = Depends(verify_admin_token)):
    admin_cursor = admin_collections.find({})
    admins = []
    for document in admin_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        admins.append(document_dict)
    return {"admins": admins}

@GeneralRouter.get("/carspace", tags=["Admin Information"])
@check_token
async def get_car_spaces(token: str = Depends(verify_admin_token)):
    carspace_cursor = car_space_collections.find({})
    carspaces = []
    for document in carspace_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        carspaces.append(document_dict)
    return {"car_spaces": carspaces}

@GeneralRouter.get("/carspacereviews", tags=["Admin Information"])
@check_token
async def get_car_space_reviews(token: str = Depends(verify_admin_token)):
    carspace_review_cursor = car_space_review_collections.find()
    carspace_reviews = []
    for document in carspace_review_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        carspace_reviews.append(document_dict)
    return {"carspace_reviews": carspace_reviews}