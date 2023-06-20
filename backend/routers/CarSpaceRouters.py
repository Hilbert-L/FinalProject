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
from decouple import config
from datetime import datetime
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

    new_car_space = CarSpaceSchema(
        UserName=stored_user["username"],
        CarSpaceId=num_car_spaces,
        DateCreated=datetime.now(),
        Title=stored_user["title"],
        FirstName=stored_user["firstname"],
        LastName=stored_user["lastname"],
        Email=stored_user["email"],
        PhoneNumber=stored_user["phonenumber"],
        Address=create_car_space.Address,
        Suburb=create_car_space.Suburb,
        Postcode=create_car_space.Postcode,
        Width=create_car_space.Width,
        Breadth=create_car_space.Breadth,
        SpaceType=create_car_space.SpaceType,
        AccessKeyRequired=create_car_space.AccessKeyRequired,
        VehicleSize=create_car_space.VehicleSize,
        Currency=create_car_space.Currency,
        Price=create_car_space.Price,
        Frequency=create_car_space.Frequency,
        Pictures=create_car_space.Pictures,
        Reviews=[]
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
        "UserName" : str(token), 
        "CarSpaceId" : str(update_car_space.CarSpaceId),
    }

    update_info = {}

    Outcome = {
        "Message": "Car Space Updated Successfully",
        "Address": "Address is unchanged",
        "Postcode": "Postcode is unchanged",
        "Suburb": "Suburb is unchanged",
        "Width": "Width is unchanged",
        "Breadth": "Breadth is unchanged",
        "SpaceType": "Space Type is unchanged",
        "AccessKeyRequired": "Access Key required is unchanged",
        "VehicleSize": "Vehicle Size is unchanged",
        "Currency": "Currency is unchanged",
        "Price": "Price is unchanged",
        "Frequency": "Frequency is unchanged",
    }

    if update_car_space.NewAddress is not None:
        update_info["NewAddress"] = update_car_space.NewAddress
        Outcome["Address"] = "Address has been updated"


    if update_car_space.NewPostcode is not None:
        update_info["Postcode"] = update_car_space.NewPostcode
        Outcome["Postcode"] = "Postcode has been updated"


    if update_car_space.NewSuburb is not None:
        update_info["Suburb"] = update_car_space.NewSuburb
        Outcome["Suburb"] = "Suburb has been updated"


    if update_car_space.NewWidth is not None:
        update_info["Width"] = update_car_space.NewWidth
        Outcome["Width"] = "Width has been updated"


    if update_car_space.NewBreadth is not None:
        update_info["Breadth"] = update_car_space.NewBreadth
        Outcome["Breadth"] = "Breadth has been updated"


    if update_car_space.NewSpacetype is not None:
        update_info["SpaceType"] = update_car_space.NewSpacetype
        Outcome["SpaceType"] = "Space Type has been updated"


    if update_car_space.NewAccessKeyRequired is not None:
        update_info["AccessKeyRequired"] = update_car_space.NewAccessKeyRequired
        Outcome["AccessKeyRequired"] = "Access Key Requirement has been updated"


    if update_car_space.NewVehicleSize is not None:
        update_info["VehicleSize"] = update_car_space.NewVehicleSize
        Outcome["VehicleSize"] = "Vehicle Size has been updated"


    if update_car_space.NewCurrency is not None:
        update_info["Currency"] = update_car_space.NewCurrency
        Outcome["Currency"] = "Currency has been updated"


    if update_car_space.NewPrice is not None:
        update_info["Price"] = update_car_space.NewPrice
        Outcome["Price"] = "Price has been updated"


    if update_car_space.NewFrequency is not None:
        update_info["Frequency"] = update_car_space.NewFrequency
        Outcome["Frequency"] = "Frequency has been updated"

    update = {
        "$set": update_info
    }

    update_results = car_space_collections.update_many(filter, update)

    if update_results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Car space cannot be updated")

    return Outcome

@CarSpaceRouter.post("/carspace/add_image", tags=["Car Spaces"])
@check_token
async def upload_car_space_image(add_image: AddImage, token: str = Depends(verify_user_token)):
    filter = {
        "UserName": str(token),
        "CarSpaceId": str(add_image.CarSpaceId),
    }

    image_str = str(add_image.CarSpaceImage)

    update_results = car_space_collections.update_one(filter, {"$push": {"Pictures": image_str}})
    
    if update_results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Image could not be uploaded")

    return {"Message": "Car Space Image Added Successfully"}
