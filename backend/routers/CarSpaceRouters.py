from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections
from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from models.UserAuthentication import UserSchema
from mongodbconnect.mongodb_connect import users_collections, car_space_review_collections, car_space_collections, car_space_image_collections, booking_collections
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

CarSpaceRouter = APIRouter()

@CarSpaceRouter.post("/carspace/create_car_space", tags=["Car Spaces"])
@check_token
async def create_car_space(create_car_space: CreateCarSpaceSchema, token: str = Depends(verify_user_token)):
    
    stored_user = users_collections.find_one({"username": token})

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")
    
    num_car_spaces = car_space_collections.count_documents({})

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
    return {"Message": "Car Space Added Successfully", "Car Space": new_car_space_dict}

# Will add three attributes: leasing, using and booking
@CarSpaceRouter.put("/carspace/updatecarspace", tags=["Car Spaces"])
@check_token
async def update_car_space(update_car_space: UpdateCarSpace, carspaceid: int, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    filter = {
        "username" : str(token),
        "carspaceid" : carspaceid,
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

@CarSpaceRouter.get("/carspace/reviews/get_all_reviews_for_producer/{username}/{carspaceid}", tags=["Car Spaces"])
@check_token
async def get_car_space_reviews_for_producer(username: str, carspaceid: int, token: str = Depends(verify_user_token)):
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
    car_spaces_cursor = car_space_collections.find({"username": username},{"_id": 0})

    # Convert cursor to list
    car_spaces = list(car_spaces_cursor)
    result = []
    # For each car space, find all bookings and determine availability
    for car_space in car_spaces:
        # Convert _id to string
        bookings = booking_collections.find({"carspaceid": car_space['carspaceid'], "status": "Confirmed"})
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
            {"ownerusername": username, "carspaceid": car_space['carspaceid']},{"_id": 0,"ownerusername": 0,"carspaceid": 0})
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

@CarSpaceRouter.post("/carspace/upload_image/{username}/{carspaceid}", tags=["Car Spaces"])
@check_token
async def upload_car_space_image(username: str, carspaceid: int,
                                 base64_image: str = None, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    if not base64_image:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No image provided")

    carspace_image_info_list = []
    if base64_image:
        verify_base64_image = base64_image + '=' * (-len(base64_image) % 4)
        if is_valid_image(verify_base64_image):
            carspace_image_info = {}
            carspace_image_info["carSpaceImagedata"] = base64_image
            carspace_image_info_list.append(carspace_image_info)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid base64 image")

    existing_document = car_space_image_collections.find_one({"username": username, "carspaceid": carspaceid})

    if existing_document:
        # If a document for this user and carspaceid already exists, append new images to the existing list
        image_id = existing_document.get("next_image_id", 1)
        for image_info in carspace_image_info_list:
            image_info["image_id"] = image_id
            image_id += 1
        car_space_image_collections.update_one(
            {"username": username, "carspaceid": carspaceid},
            {"$push": {"images": {"$each": carspace_image_info_list}}, "$set": {"next_image_id": image_id}}
        )
    else:
        # If no such document exists, create a new one
        image_id = 1
        for image_info in carspace_image_info_list:
            image_info["image_id"] = image_id
            image_id += 1
        car_space_image_collections.insert_one({
            "username": username,
            "carspaceid": carspaceid,
            "images": carspace_image_info_list,
            "next_image_id": image_id
        })

    # Update the images in the users_collections
    users_collections.update_one(
        {"username": username},
        {"$push": {"carSpaceImages": {"$each": carspace_image_info_list}}}
    )

    return {"Message": f"Car Space Image uploaded for user: {username} and carspaceid: {carspaceid}"}


@CarSpaceRouter.get("/carspace/get_all_images/{username}/{carspaceid}", tags=["Car Spaces"])
@check_token
async def get_all_car_space_images(username: str, carspaceid: int, token: str = Depends(verify_user_token)):
    users = users_collections.find_one({"username": username})

    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username")

    car_space_images_cursor = car_space_image_collections.find({"carspaceid": carspaceid, "username": username})
    images = []
    for document in car_space_images_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        images.append(document_dict)

    if not images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No images found for the given username and carspaceid")

    return {"carspace_images": images}



@CarSpaceRouter.delete("/carspace/delete_image/{username}/{carspaceid}/{imageid}", tags=["Car Spaces"])
@check_token
async def delete_single_car_space_image_for_user_carspace(username: str, carspaceid: int, imageid: int, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    existing_document = car_space_image_collections.find_one({"username": username, "carspaceid": carspaceid})
    if existing_document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    # Find the image with the given ID
    image_to_delete = None
    for image in existing_document["images"]:
        if image["image_id"] == imageid:
            image_to_delete = image
            break

    if image_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    # Remove the image from the images list
    existing_document["images"].remove(image_to_delete)

    # Update the document in the database
    car_space_image_collections.update_one(
        {"username": username, "carspaceid": carspaceid},
        {"$set": {"images": existing_document["images"]}}
    )

    return {"Message": f"Image with ID {imageid} deleted successfully"}
    

@CarSpaceRouter.delete("/carspace/delete_all_images/{username}/{carspaceid}", tags=["Car Spaces"])
@check_token
async def delete_all_car_space_images_for_carspace(username: str, carspaceid: int, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    result = car_space_image_collections.delete_many({"carspaceid": carspaceid, "username": username})

    if result.deleted_count > 0:
        return {"message": "Car Space Images deleted successfully"}
    else:
        return {"message": "Car Space Image not found"}


@CarSpaceRouter.delete("/carspace/deletecarspace/{username}/{carspaceid}", tags=["Car Spaces"])
@check_token
async def delete_car_space_by_id(username: str, carspaceid: int, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    filter = {"username": username, "carspaceid": carspaceid}

    result = car_space_collections.delete_many(filter)
    car_space_image_collections.delete_many(filter)
    car_space_review_collections.delete_many(filter)

    if result.deleted_count > 0:
        return {"message": "Car Space deleted successfully"}
    else:
        return {"message": "Car Space not found"}