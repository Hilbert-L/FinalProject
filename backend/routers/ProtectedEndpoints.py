from fastapi import APIRouter, Depends, HTTPException, status
from authentication.authentication import verify_user_token, verify_admin_token
from wrappers.wrappers import check_token
from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections

ProtectedRouter = APIRouter()

@ProtectedRouter.get("/protected_user", tags=["Protected Endpoint Examples"])
@check_token
async def protected_route_user(token: str = Depends(verify_user_token)):
    return {"Message": "This is a protected user route"}

@ProtectedRouter.post("/getuserfromtoken", tags=["Protected Endpoint Examples"])
@check_token
async def get_user_from_token(token: str = Depends(verify_user_token)):
    return {"Message": "User token is valid", "username": token}

@ProtectedRouter.get("/protected_admin", tags=["Protected Endpoint Examples"])
@check_token
async def protected_route_admin(token: str = Depends(verify_admin_token)):
    return {"Message": "This is a protected admin route"}

@ProtectedRouter.post("/getadminfromtoken", tags=["Protected Endpoint Examples"])
@check_token
async def get_admin_from_token(token: str = Depends(verify_admin_token)):
    return {"Message": "Admin token is valid", "username": token}