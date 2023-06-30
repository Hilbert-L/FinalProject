from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections
from fastapi import APIRouter, Depends, status, HTTPException
from models.UserAuthentication import UserSchema
from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from typing import Optional, List
from models.CreateCarSpace import CarSpaceReview, CarSpaceSchema, CreateCarSpaceSchema
from models.UpdateCarSpace import UpdateCarSpace, AddImage
from wrappers.wrappers import check_token
from passlib.context import CryptContext
from datetime import datetime
from base64 import b64encode
from authentication.authentication import generate_token, verify_user_token
import json 

CarSpaceRouter = APIRouter()

@CarSpaceRouter.post("/carspace/create_car_space", tags=["Car Spaces"])
@check_token
async def create_car_space(create_car_space: CreateCarSpaceSchema, token: str = Depends(verify_user_token)):
    
    stored_user = users_collections.find_one({"username": token})

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")
    
    num_car_spaces = car_space_collections.count_documents({})

    if create_car_space.pictures:
        carspace_pictures = [b64encode(base64_str.encode("utf-8")) for base64_str in create_car_space.Pictures]

    else:
        carspace_pictures = None

    new_car_space = CarSpaceSchema(
        username=stored_user["username"],
        carspaceid=num_car_spaces,
        title=create_car_space.title,
        firstname=stored_user["firstname"],
        lastname=stored_user["lastname"],
        email=stored_user["email"],
        phonenumber=stored_user["phonenumber"],
        address=create_car_space.address,
        suburb=create_car_space.suburb,
        postcode=create_car_space.postcode,
        width=create_car_space.width,
        breadth=create_car_space.breadth,
        spacetype=create_car_space.spacetype,
        accesskeyrequired=create_car_space.accesskeyrequired,
        vehiclesize=create_car_space.vehiclesize,
        currency=create_car_space.currency,
        price=create_car_space.price,
        frequency=create_car_space.frequency,
        pictures=carspace_pictures,
        reviews=[]
    )
    
    new_car_space_dict = new_car_space.dict()
    car_space_collections.insert_one(dict(new_car_space_dict))
    return {"Message": "Car Space Added Successfully", "Car Space": new_car_space_dict}

@CarSpaceRouter.post("/carspace/create_review", tags=["Car Spaces"])
@check_token
async def create_car_space_review(car_space_review: CarSpaceReview, token: str = Depends(verify_user_token)):
    car_space_review_collections.insert_one(car_space_review.dict())
    return {"Message": "Car Space Review Added Successfully"}


@CarSpaceRouter.put("/carspace/updatecarspace", tags=["Car Spaces"])
@check_token
async def update_car_space(update_car_space: UpdateCarSpace, token: str = Depends(verify_user_token)):
    filter = {
        "username" : str(token),
        "carspaceid" : str(update_car_space.carspaceid),
    }

    update_info = {}
    Outcome = {}
    for key, value in update_car_space.dict().items():
        if key == "carspaceid":
            continue
        if value is None:
            Outcome[key] = key + " is unchanged"
        else:
            update_info[key] = value
            Outcome[key] = key + " has been updated"

    update = {
        "$set": update_info
    }

    update_results = car_space_collections.update_one(filter, update)

    if update_results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Car space cannot be updated")

    return Outcome

@CarSpaceRouter.post("/carspace/add_image", tags=["Car Spaces"])
@check_token
async def add_car_space_image(data: AddImage, token: str = Depends(verify_user_token)):
    filter = {
        "username": str(token),
        "carspaceid": str(data.CarSpaceId),
    }
    file = data.CarSpaceImage
    contents = await file.read()
    # Convert file to base64 string
    base64_str = b64encode(contents).decode("utf-8")

    update_results = car_space_collections.update_one(filter, {"$push": {"pictures": base64_str}})

    if update_results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Image could not be added")

    return {"Car Space Image Added Successfully": file.filename}
