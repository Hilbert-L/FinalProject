from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, \
    car_space_review_collections, car_space_collections
from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from models.UserAuthentication import UserSchema
from mongodbconnect.mongodb_connect import users_collections, car_space_review_collections, car_space_collections, \
    car_space_image_collections, booking_collections, car_space_id_collections
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from typing import Optional, List
from models.CreateCarSpace import CarSpaceReview, CarSpaceSchema, CreateCarSpaceSchema, Review
from models.UpdateCarSpace import UpdateCarSpace
from wrappers.wrappers import check_token
from passlib.context import CryptContext
from datetime import datetime
from base64 import b64encode
import base64
from authentication.authentication import generate_token, verify_user_token
import json
import os
import io
from PIL import Image
from bson import ObjectId

CarSpaceRouter = APIRouter()


def initialize_collection(collection, initial_id):
    if collection.count_documents({}) == 0:
        collection.insert_one({"id": initial_id})


initialize_collection(car_space_id_collections, 1)


def is_valid_image(base64_img_str):
    # Check if this is a "data URL"
    if base64_img_str.startswith('data:image'):
        # Find the start of the actual image data
        base64_img_str = base64_img_str.split(',', 1)[1]
    try:
        img_data = base64.b64decode(base64_img_str)
        img = Image.open(io.BytesIO(img_data))
        img.verify()  # verify that it is, in fact, an image
        return True
    except Exception:
        return False


@CarSpaceRouter.post("/carspace/create_car_space", tags=["Car Spaces"])
@check_token
async def create_car_space(create_car_space: CreateCarSpaceSchema,token: str = Depends(verify_user_token)):
    stored_user = users_collections.find_one({"username": token})

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")


    num_car_spaces = car_space_id_collections.find_one({"_id": ObjectId("64ba8947a0d25b4ae8a3cd84")})

    new_car_space = CarSpaceSchema(
        username=stored_user["username"],
        carspaceid=num_car_spaces['id'],
        title=create_car_space.title,
        firstname=stored_user["firstname"],
        lastname=stored_user["lastname"],
        email=stored_user["email"],
        phonenumber=stored_user["phonenumber"],
        address=create_car_space.address,
        suburb=create_car_space.suburb,
        postcode=create_car_space.postcode,
        longitude=create_car_space.longitude,
        latitude=create_car_space.latitude,
        width=create_car_space.width,
        breadth=create_car_space.breadth,
        spacetype=create_car_space.spacetype,
        accesskeyrequired=create_car_space.accesskeyrequired,
        vehiclesize=create_car_space.vehiclesize,
        currency=create_car_space.currency,
        price=create_car_space.price,
        frequency=create_car_space.frequency,
    )

    new_car_space_dict = new_car_space.dict()
    car_space_collections.insert_one(dict(new_car_space_dict))
    num_car_spaces['id'] += 1
    car_space_id_collections.update_one({"_id": ObjectId("64ba8947a0d25b4ae8a3cd84")}, {"$set": {"id": num_car_spaces["id"]}})
    return {"Message": "Car Space Added Successfully", "Car Space": new_car_space_dict}

@CarSpaceRouter.post("/carspace/upload_carspace_image/{car_space_id}", tags=["Car Spaces"])
@check_token
async def upload_carspace_image(car_space_id: int, file: UploadFile = File(...),token: str = Depends(verify_user_token)):
    stored_user = users_collections.find_one({"username": token})

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    stored_car_space = car_space_collections.find_one({"carspaceid": car_space_id})

    if stored_car_space is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car space {car_space_id} not found")

    contents = await file.read()
    base64_image = base64.b64encode(contents).decode()

    if not is_valid_image(base64_image):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image format")

    image_uri = f"data:{file.content_type};base64,{base64_image}"

    car_space_collections.update_one(
        {"carspaceid": car_space_id},
        {"$set": {"image": image_uri}}
    )

    return {"Message": "Image uploaded successfully"}


# Will add three attributes: leasing, using and booking
@CarSpaceRouter.put("/carspace/updatecarspace", tags=["Car Spaces"])
@check_token
async def update_car_space(update_car_space: UpdateCarSpace, carspaceid: int, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    filter = {
        "username": str(token),
        "carspaceid": carspaceid,
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


@CarSpaceRouter.post("/carspace/create_review", tags=["Car Spaces"])
@check_token
async def create_car_space_review(car_space_review: Review, carspaceid: int, token: str = Depends(verify_user_token)):
    carspace = car_space_collections.find_one({"carspaceid": carspaceid})
    if carspace is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car space not found.")

    user = users_collections.find_one({"username": token})
    username = user["username"]

    reviews = car_space_review.dict()
    temp = dict()
    temp['reviewerusername'] = username
    temp['carspaceid'] = carspaceid
    new_reviews = {**temp, **reviews}
    car_space_review_collections.insert_one(new_reviews)
    return {"Message": "Car Space Review Added Successfully"}


@CarSpaceRouter.get("/carspace/reviews/get_all_reviews_for_consumer/{username}", tags=["Car Spaces"])
@check_token
async def get_car_space_reviews_for_consumer(username: str, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    review_cursor = car_space_review_collections.find({"reviewerusername": username})
    reviews = []
    for document in review_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        reviews.append(document_dict)
    return {f"Reviews made by user: {username}": reviews}


@CarSpaceRouter.get("/carspace/reviews/get_all_reviews_for_producer/{username}", tags=["Car Spaces"])
@check_token
async def get_car_space_reviews_for_producer(username: str, token: str = Depends(verify_user_token)):
    review_cursor = car_space_review_collections.find({"ownerusername": username})
    reviews = []
    for document in review_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        reviews.append(document_dict)
    return {f"Reviews received by user: {username}": reviews}


@CarSpaceRouter.get("/carspace/reviews/get_car_space_reviews_for_producer_by_carspaceid/{username}/{carspaceid}", tags=["Car Spaces"])
@check_token
async def get_car_space_reviews_for_producer_by_carspaceid(username: str, carspaceid: int, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    review_cursor = car_space_review_collections.find({"ownerusername": username, "carspaceid": carspaceid})
    reviews = []
    for document in review_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        reviews.append(document_dict)
    return {f"Reviews received by user: {username} and carspace: {carspaceid}": reviews}


@CarSpaceRouter.get("/carspace/get_car_space_Info/{username}", tags=["Car Spaces"])
@check_token
async def get_car_space_info(username: str, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    # Find all car spaces created by the user
    car_spaces_cursor = car_space_collections.find({"username": username}, {"_id": 0})

    # Convert cursor to list
    car_spaces = list(car_spaces_cursor)
    result = []
    # For each car space, find all bookings and determine availability
    for car_space in car_spaces:
        # Convert _id to string
        bookings = booking_collections.find({"carspaceid": car_space['carspaceid']})
        booking_times = []
        for booking in bookings:
            start_time = booking['start_date']
            end_time = booking['end_date']
            now = datetime.now()
            if start_time <= now <= end_time:
                car_space['availability'] = 'Not Available Now'
            else:
                car_space['availability'] = 'Available Now'

            booking_times.append({"start_time": start_time, "end_time": end_time})

        # Find all reviews for the car space
        review_cursor = car_space_review_collections.find(
            {"ownerusername": username, "carspaceid": car_space['carspaceid']},
            {"_id": 0, "ownerusername": 0, "carspaceid": 0})
        reviews = []
        for document in review_cursor:
            document_str = json.dumps(document, default=str)
            document_dict = json.loads(document_str)
            reviews.append(document_dict)

        image_cursor = car_space_image_collections.find({"username": username, "carspaceid": car_space['carspaceid']}, {"_id": 0, "username": 0, "carspaceid": 0})
        images = []
        for i in image_cursor:
            for image in i['images']:
                images.append(image['carSpaceImagedata'])

        car_space_info = {
            "Your Car Space Information": car_space,
            "reservation": booking_times if booking_times else "No reservation",
            "reviews": reviews if reviews else "No reviews",
            "car space images": images if images else "No images",
        }

        result.append(car_space_info)

    return result


@CarSpaceRouter.delete("/carspace/deletecarspace/{username}/{carspaceid}", tags=["Car Spaces"])
@check_token
async def delete_car_space_by_id(username: str, carspaceid: int, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    # Check if there are future bookings
    now = datetime.now()

    # If there are future bookings, raise an exception
    if booking_collections.count_documents({"carspaceid": carspaceid, "start_date": {"$gte": now}}) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot delete, there are future bookings for this car space")

    filter = {"username": username, "carspaceid": carspaceid}

    result = car_space_collections.delete_many(filter)
    car_space_image_collections.delete_many(filter)
    car_space_review_collections.delete_many(filter)

    if result.deleted_count > 0:
        return {"message": "Car Space deleted successfully"}
    else:
        return {"message": "Car Space not found"}



@CarSpaceRouter.get("/carspace/get_car_space_booking/{carspaceid}", tags=["Car Spaces"])
@check_token
async def get_car_space_bookings(carspaceid: int, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

        # Convert _id to string
    bookings = booking_collections.find({"carspaceid": carspaceid})
    booking_times = []
    for booking in bookings:
        start_time = booking['start_date']
        end_time = booking['end_date']
        booking_times.append({"start_time": start_time, "end_time": end_time})

    return booking_times


@CarSpaceRouter.get("/user/get_current_reservations", tags=["Car Spaces"])
@check_token
async def get_reservation_count(token: str = Depends(verify_user_token)):
    # Verify user token and get user
    user = users_collections.find_one({"username": token})

    # Check if user exists
    if user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username doesn't exist")


    # Get current time in UTC
    current_time = datetime.utcnow()

    future_reservations_filter = {"provider_username": user['username'], "start_date": {"$gt": current_time}}

    # Get the count of such reservations
    reservation_count = booking_collections.count_documents(future_reservations_filter)

    return {
        "Message": "Reservation Count Retrieved Successfully",
        "Reservation Count": reservation_count
    }


@CarSpaceRouter.post("/carspace/create_car_space_no_token", tags=["Car Spaces"])
async def create_car_space_no_token(fakeuser_id: int, create_car_space: CreateCarSpaceSchema, base64_image: str = None):
    stored_user = users_collections.find_one({"username": f"fake_user_{fakeuser_id}"})

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    num_car_spaces = car_space_id_collections.find_one({"_id": ObjectId("64ba8947a0d25b4ae8a3cd84")})

    new_car_space = CarSpaceSchema(
        username=stored_user["username"],
        carspaceid=num_car_spaces['id'],
        title=create_car_space.title,
        firstname=stored_user["firstname"],
        lastname=stored_user["lastname"],
        email=stored_user["email"],
        phonenumber=stored_user["phonenumber"],
        address=create_car_space.address,
        suburb=create_car_space.suburb,
        postcode=create_car_space.postcode,
        longitude=create_car_space.longitude,
        latitude=create_car_space.latitude,
        width=create_car_space.width,
        breadth=create_car_space.breadth,
        spacetype=create_car_space.spacetype,
        accesskeyrequired=create_car_space.accesskeyrequired,
        vehiclesize=create_car_space.vehiclesize,
        currency=create_car_space.currency,
        price=create_car_space.price,
        frequency=create_car_space.frequency,
    )

    new_car_space_dict = new_car_space.dict()
    new_car_space_dict["image"] = base64_image
    car_space_collections.insert_one(dict(new_car_space_dict))
    carspace_id = num_car_spaces['id']
    num_car_spaces['id'] += 1
    car_space_id_collections.update_one({"_id": ObjectId("64ba8947a0d25b4ae8a3cd84")}, {"$set": {"id": num_car_spaces["id"]}})
    return {"Message": "Car Space Added Successfully", "Car Space": new_car_space_dict, "CarSpaceId": carspace_id}

@CarSpaceRouter.post("/carspace/create_review_no_token", tags=["Car Spaces"])
async def create_car_space_review_no_token(fakeuser_id: int, car_space_review: Review, carspaceid: int):
    carspace = car_space_collections.find_one({"carspaceid": carspaceid})
    if carspace is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car space not found.")

    user = users_collections.find_one({"username": f"fake_user_{fakeuser_id}"})
    username = user["username"]

    reviews = car_space_review.dict()
    temp = dict()
    temp['reviewerusername'] = username
    temp['carspaceid'] = carspaceid
    new_reviews = {**temp, **reviews}
    car_space_review_collections.insert_one(new_reviews)
    return {"Message": "Car Space Review Added Successfully"}
