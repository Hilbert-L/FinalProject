from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections
from fastapi import APIRouter, Depends, status, HTTPException
from models.UserAuthentication import UserSchema
from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from typing import Optional, List
from models.CreateCarSpace import CarSpaceReview, CarSpaceSchema, CreateCarSpaceSchema
from models.UpdateCarSpace import UpdateCarSpaceAddress, UpdateCarSpaceDimensions, UpdateCarSpacePrice
from wrappers.wrappers import check_token
from passlib.context import CryptContext
from decouple import config
from datetime import datetime
from authentication.authentication import generate_token, verify_token

CarSpaceRouter = APIRouter()

@CarSpaceRouter.post("/carspace/create_car_space", tags=["Car Spaces"])
@check_token
def create_car_space(create_car_space: CreateCarSpaceSchema, token: str = Depends(verify_token)):
    
    stored_user = users_collections.find({"username": create_car_space.UserName})

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    # Find the user by username
    user_car_spaces = list(car_space_collections.find({"UserName": create_car_space.UserName}))
    
    new_car_space = CarSpaceSchema(
        UserName=create_car_space.UserName,
        CarSpaceId=len(user_car_spaces),
        DateCreated=datetime.now(),
        Title=create_car_space.Title,
        FirstName=create_car_space.FirstName,
        LastName=create_car_space.LastName,
        Email=create_car_space.Email,
        PhoneNumber=create_car_space.PhoneNumber,
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
    )
    
    new_car_space_dict = new_car_space.dict()
    car_space_collections.insert_one(new_car_space_dict)
    return {"Message": "Car Space Added Successfully"}

@CarSpaceRouter.post("/carspace/create_review", tags=["Car Spaces"])
@check_token
def create_car_space_review(car_space_review: CarSpaceReview, token: str = Depends(verify_token)):
    car_space_review_collections.insert_one(car_space_review.dict())
    return {"Message": "Car Space Review Added Successfully"}


@CarSpaceRouter.put("/carspace/update_location", tags=["Car Spaces"])
@check_token
def update_car_space_address(update_space_address: UpdateCarSpaceAddress, token: str = Depends(verify_token)):
    filter = {
        "UserName" : update_space_address.UserName, 
        "CarSpaceId" : update_space_address.CarSpaceId,
        "Address" : update_space_address.OldAddress,
        "PostCode" : update_space_address.OldPostcode,
        "Suburb" : update_space_address.OldSuburb    
    }

    update = {
        "$set": {
            "Address" : update_space_address.NewAddress,
            "Postcode" : update_space_address.NewPostcode,
            "Suburb" : update_space_address.NewSuburb    
        }
    }
    
    car_space_collections.update_many(filter, update)
    
    Outcome = {
        "Message": "Car Space Updated Successfully",
        "Address": "Address is unchanged",
        "Postcode": "Postcode is unchanged",
        "Suburb": "Suburb is unchanged"
        }
    
    if update_space_address.NewAddress is not None:
        Outcome["Address"] = "Address Updated Succesfully"
    
    if update_space_address.NewSuburb is not None:
        Outcome["Suburb"] = "Suburb Updated Succesfully"
    
    if update_space_address.NewPostcode is not None:
        Outcome["Postcode"] = "Postcode Updated Succesfully"

    return Outcome
    

@CarSpaceRouter.put("/carspace/update_space_dimensions", tags=["Car Spaces"])
@check_token
def update_car_space_details(update_space_dimensions: UpdateCarSpaceDimensions, token: str = Depends(verify_token)):
    filter = {
        "UserName" : update_space_dimensions.UserName, 
        "CarSpaceId" : update_space_dimensions.CarSpaceId,
        "Width": update_space_dimensions.OldWidth,
        "Breadth": update_space_dimensions.OldBreadth,
        "SpaceType": update_space_dimensions.OldSpacetype,
        "AccessKeyRequired": update_space_dimensions.OldAccessKeyRequired,
        "VehicleSize": update_space_dimensions.OldVehicleSize
    }
    update = {
        "$set": {
        "Width": update_space_dimensions.NewWidth,
        "Breadth": update_space_dimensions.NewBreadth,
        "SpaceType": update_space_dimensions.NewSpacetype,
        "AccessKeyRequired": update_space_dimensions.NewAccessKeyRequired,
        "VehicleSize": update_space_dimensions.NewVehicleSize
        }
    }
    
    results = car_space_collections.update_many(filter, update)
    
    if results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't update car space details")

    Outcome = {
        "Message": "Car Space Updated Successfully",
        "Width": "Width is unchanged",
        "Breadth": "Breadth is unchanged",
        "SpaceType": "Space Type is unchanged",
        "AccessKeyRequired": "Access Key required is unchanged",
        "VehicleSize": "Vehicle Size is unchanged",
    }
    
    if update_space_dimensions.NewWidth is not None:
        Outcome["Width"] = "Width has been updated"

    if update_space_dimensions.NewBreadth is not None:
        Outcome["Breadth"] = "Breadth has been updated"

    if update_space_dimensions.NewSpacetype is not None:
        Outcome["Space Type"] = "Space Type has been updated"

    if update_space_dimensions.NewAccessKeyRequired is not None:
        Outcome["AccessKeyRequired"] = "Access Key has been updated"

    if update_space_dimensions.NewVehicleSize is not None:
        Outcome["VehicleSize"] = "Vehicle Size has been updated"

    return Outcome


@CarSpaceRouter.put("/carspace/update_space_price", tags=["Car Spaces"])
@check_token
def update_car_space_price(update_car_space_price: UpdateCarSpacePrice, token: str = Depends(verify_token)):
    filter = {
        "UserName" : update_car_space_price.UserName, 
        "CarSpaceId" : update_car_space_price.CarSpaceId,
        "Currency" : update_car_space_price.OldCurrency,
        "Price": update_car_space_price.OldPrice,
        "Frequency": update_car_space_price.OldFrequency
    }
    update = {
        "$set": {
        "Currency" : update_car_space_price.NewCurrency,
        "Price": update_car_space_price.NewPrice,
        "Frequency": update_car_space_price.NewFrequency
        }
    }
    
    results = car_space_collections.update_many(filter, update)
    
    if results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't update car space details")
    
    Outcome = {
        "Message": "Car Space Updated Successfully",
        "Currency": "Currency is unchanged",
        "Price": "Price is unchanged",
        "Frequency": "Frequency is unchanged",
    }

    if update_car_space_price.NewCurrency is not None:
        Outcome["Currency"] = "Currency has been updated"
    
    if update_car_space_price.NewFrequency is not None:
        Outcome["Frequency"] = "Payment Frequency has been updated"

    if update_car_space_price.NewPrice is not None:
        Outcome["Price"] = "Price has been updated"

    return Outcome
