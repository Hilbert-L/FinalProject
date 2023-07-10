from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections
from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from models.UserAuthentication import UserSchema
from mongodbconnect.mongodb_connect import users_collections, car_space_review_collections, car_space_collections, car_space_image_collections
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from typing import Optional, List
from models.CreateCarSpace import CarSpaceReview, CarSpaceSchema, CreateCarSpaceSchema
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
        width=create_car_space.width,
        breadth=create_car_space.breadth,
        spacetype=create_car_space.spacetype,
        accesskeyrequired=create_car_space.accesskeyrequired,
        vehiclesize=create_car_space.vehiclesize,
        currency=create_car_space.currency,
        price=create_car_space.price,
        frequency=create_car_space.frequency,
        leasing=create_car_space.leasing,
        booking=create_car_space.booking,
        using=create_car_space.using,
    )

    new_car_space_dict = new_car_space.dict()
    car_space_collections.insert_one(dict(new_car_space_dict))
    return {"Message": "Car Space Added Successfully", "Car Space": new_car_space_dict}

# Will add three attributes: leasing, using and booking
@CarSpaceRouter.put("/carspace/updatecarspace", tags=["Car Spaces"])
@check_token
async def update_car_space(update_car_space: UpdateCarSpace, token: str = Depends(verify_user_token)):
    filter = {
        "username" : str(token),
        "carspaceid" : update_car_space.carspaceid,
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
async def create_car_space_review(car_space_review: CarSpaceReview, token: str = Depends(verify_user_token)):
    car_space_review_collections.insert_one(car_space_review.dict())
    return {"Message": "Car Space Review Added Successfully"}


@CarSpaceRouter.get("/carspace/reviews/get_all_reviews_for_consumer/{username}", tags=["Car Spaces"])
@check_token
async def get_car_space_reviews_for_consumer(username: str, token: str = Depends(verify_user_token)):
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
    review_cursor = car_space_review_collections.find({"ownerusername": username, "carspaceid": carspaceid})
    reviews = []
    for document in review_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        reviews.append(document_dict)
    return {f"Reviews received by user: {username} and carspace: {carspaceid}": reviews}

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
async def upload_car_space_image(username: str, carspaceid: int, image: UploadFile = File(None),
                                 base64_image: str = None, token: str = Depends(verify_user_token)):
    if not image and not base64_image:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No image provided")
    carspace_image_info_list = []
    if image:
        carspace_image_info = {}
        image_file_types = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.ico'}
        contents = await image.read()
        file_extension = os.path.splitext(image.filename)[1].lower()

        if file_extension not in image_file_types:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Invalid image file type")

        carspace_image_info["carSpaceImage"] = f"{username}_{image.filename}"
        carspace_image_info["carSpaceID"] = carspaceid
        carspace_image_info["carSpaceImagedata"] = contents
        carspace_image_info["carSpaceImageextension"] = file_extension
        carspace_image_info_list.append(carspace_image_info)

    elif base64_image:
        base64_image = base64_image + '=' * (-len(base64_image) % 4)
        if is_valid_image(base64_image):
            carspace_image_info = {}
            carspace_image_info["carSpaceImage"] = f"{username}_{base64_image}"
            carspace_image_info["carSpaceID"] = carspaceid
            carspace_image_info["carSpaceImagedata"] = base64.b64decode(base64_image)
            carspace_image_info_list.append(carspace_image_info)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid base64 image")

    existing_document = car_space_image_collections.find_one({"username": username, "carspaceid": carspaceid})

    if existing_document:
        # If a document for this user and carspaceid already exists, append new images to the existing list
        car_space_image_collections.update_one(
            {"username": username},
            {"$push": {"images": {"$each": carspace_image_info_list}}}
        )
    else:
        # If no such document exists, create a new one
        car_space_image_collections.insert_one({
            "username": username,
            "carspaceid": carspaceid,
            "images": carspace_image_info_list
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
    carspace_images_cursor = car_space_image_collections.find({"carspaceid": carspaceid, "username": username})
    images = []
    for document in carspace_images_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        images.append(document_dict)
    return {"carspace_images": images}

@CarSpaceRouter.delete("/carspace/delete_image/{username}/{carspaceid}/{imagename}", tags=["Car Spaces"])
@check_token
async def delete_single_car_space_image_for_user_carspace(username: str, carspaceid: int, imagename: str, token: str = Depends(verify_user_token)):
    result = car_space_image_collections.update_one(
        {"username": username, "carspaceid": carspaceid},
        {"$pull": {"images": {"carSpaceImage": imagename}}}
    )

    if result.modified_count == 1:
        return {"message": "Car Space Image deleted successfully"}
    else:
        return {"message": "Car Space Image not found"}
    

@CarSpaceRouter.delete("/carspace/delete_all_images/{username}/{carspaceid}", tags=["Car Spaces"])
@check_token
async def delete_all_car_space_images_for_carspace(username: str, carspaceid: int, token: str = Depends(verify_user_token)):
    result = car_space_image_collections.delete_many({"carspaceid": carspaceid, "username": username})

    if result.deleted_count > 0:
        return {"message": "Car Space Images deleted successfully"}
    else:
        return {"message": "Car Space Image not found"}
    