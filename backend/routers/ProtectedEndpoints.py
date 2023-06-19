from fastapi import APIRouter, Depends, HTTPException, status
from authentication.authentication import generate_token, verify_token
from wrappers.wrappers import check_token
from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections

ProtectedRouter = APIRouter()

@ProtectedRouter.get("/protected", tags=["Protected Endpoint Examples"])
@check_token
async def protected_route(token: str = Depends(verify_token)):
    return {"Message": "This is a protected route"}

@ProtectedRouter.post("/getuserfromtoken", tags=["Protected Endpoint Examples"])
@check_token
async def get_user_from_token(token: str = Depends(verify_token), tags=["Dependency"]):
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"access_token": token, "username": username}
