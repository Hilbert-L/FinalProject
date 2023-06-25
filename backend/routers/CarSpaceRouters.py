from base64 import b64encode
from datetime import datetime

from authentication.authentication import verify_user_token
from fastapi import APIRouter, Depends, status, HTTPException
from models.CreateCarSpace import CarSpaceReview, CarSpaceSchema, CreateCarSpaceSchema
from models.UpdateCarSpace import UpdateCarSpace, AddImage
from mongodbconnect.mongodb_connect import users_collections, car_space_review_collections, car_space_collections
from wrappers.wrappers import check_token

CarSpaceRouter = APIRouter()


@CarSpaceRouter.post("/carspace/create_car_space", tags=["Car Spaces"])
@check_token
async def create_car_space(create_car_space: CreateCarSpaceSchema, token: str = Depends(verify_user_token)):
    stored_user = users_collections.find_one({"username": token})

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    num_car_spaces = car_space_collections.count_documents({})

    if create_car_space.Pictures:
        carspace_pictures = [b64encode(base64_str.encode("utf-8")) for base64_str in create_car_space.Pictures]

    else:
        carspace_pictures = None

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
        Pictures=carspace_pictures,
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
        "UserName": str(token),
        "CarSpaceId": str(update_car_space.CarSpaceId),
    }

    update_info = {}
    Outcome = {}
    for key, value in update_car_space.dict().items():
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
        "UserName": str(token),
        "CarSpaceId": str(data.CarSpaceId),
    }
    file = data.CarSpaceImage
    contents = await file.read()
    # Convert file to base64 string
    base64_str = b64encode(contents).decode("utf-8")

    update_results = car_space_collections.update_one(filter, {"$push": {"Pictures": base64_str}})

    if update_results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Image could not be added")

    return {"Car Space Image Added Successfully": file.filename}