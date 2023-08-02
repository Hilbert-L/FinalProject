import base64
from bson import ObjectId
from fastapi import APIRouter, Depends, status, HTTPException, Header, UploadFile, File
from mongodbconnect.mongodb_connect import admin_collections, users_collections, car_space_image_collections, car_space_review_collections, car_space_collections, transaction_information_collections, booking_collections
from models.UserAuthentication import UserRegistrationSchema, UserSchema, LoginSchema
from models.UpdateUserInfo import UpdatePassword, UpdatePersonalDetails
from models.UpdateCarSpace import UpdateCarSpace
from wrappers.wrappers import check_token
from authentication.authentication import generate_token, verify_admin_token, pwd_context
import os
from typing import Optional
import json
import io
from PIL import Image

AdminRouter = APIRouter()

@AdminRouter.post("/admin/auth/register", tags=["Administrators"])
async def register(userRegistrationSchema: UserRegistrationSchema):
    stored_user = admin_collections.find_one({"username": userRegistrationSchema.username})

    if stored_user is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        
    stored_email = admin_collections.find_one({"email": userRegistrationSchema.email})
    
    if stored_email is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    hashed_password = pwd_context.hash(userRegistrationSchema.password)
    
    num_users = admin_collections.count_documents({})

    # # Create a new user instance 
    new_user = UserSchema(
        userid=num_users, 
        firstname=userRegistrationSchema.firstname,
        lastname=userRegistrationSchema.lastname,
        username=userRegistrationSchema.username,
        email=userRegistrationSchema.email,
        password=hashed_password,
        phonenumber=userRegistrationSchema.phonenumber,
        isloggedin=True,
        passwordunhashed=str(userRegistrationSchema.password),
        isactive=True,
        isadmin=True
    )

    new_user_dict = new_user.dict()
    admin_collections.insert_one(new_user_dict)
    token = generate_token(new_user.username)
    return {"Message": "Admin Registered Successfully", "token": token, "user": new_user}


@AdminRouter.post("/admin/auth/login", tags=["Administrators"])
async def login(AdminLogin: LoginSchema):
     
    filter={"username": AdminLogin.username}
    stored_user = admin_collections.find_one(filter)

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username doesn't exist")

    # Verify the password
    if not pwd_context.verify(AdminLogin.password, stored_user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user name or password")
    
    if stored_user["isloggedin"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already logged in")

    if not stored_user["isactive"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User has been deactivated")

    updateLoginStatus = {"$set": {"isloggedin": True}}

    admin_collections.update_one(filter, updateLoginStatus)

    # Generate and return a JWT token
    token = generate_token(AdminLogin.username)
    return {"Message": "User Login Successfully", "token": token}


@AdminRouter.post("/admin/auth/logout", tags=["Administrators"])
async def logout(token: str = Header(...)):
    username = await verify_admin_token(token)

    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")

    stored_user = admin_collections.find_one({"username": username})

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")

    updateLogoutStatus = {"$set": {"isloggedin": False}}

    # Updated user login status
    admin_collections.update_one({"username": username}, updateLogoutStatus)

    return {"Message": "Logout Successfully"}

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

@AdminRouter.post("/admin/upload_profile_picture", tags=["Administrators"])
@check_token
async def upload_profile_picture(token: str = Depends(verify_admin_token), file: UploadFile = File(...)):
    filter = {"username": token}
    user = admin_collections.find_one(filter)

    if user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username doesn't exist")

    contents = await file.read()
    base64_image = base64.b64encode(contents).decode()

    if not is_valid_image(base64_image):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image format")

    data_uri = f"data:{file.content_type};base64,{base64_image}"

    update_results = admin_collections.update_one(filter, {"$set": {"image": data_uri}})

    if update_results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot update profile picture")

    return {"Message": "User Profile Picture Updated"}


@AdminRouter.put("/admin/change_password", tags=["Administrators"])
@check_token
async def change_password(password_update: UpdatePassword, token: str = Depends(verify_admin_token)):
    filter = {"username": password_update.username}
    stored_user = admin_collections.find_one(filter)

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")

    if not pwd_context.verify(password_update.currentPassword, stored_user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")
    
    new_hashed_password = pwd_context.hash(password_update.newPassword)
    update = {"$set": {"password": new_hashed_password}}
    update_results = admin_collections.update_one(filter, update)
    
    if update_results.modified_count != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot update password")

    return {"Message": "Password Changed Successfully"}


@AdminRouter.put("/admin/update_personal_details", tags=["Administrators"])
@check_token
async def change_personal_details(personal_update: UpdatePersonalDetails, token: str = Depends(verify_admin_token)):
    update_info = {}
    outcome = {
        "Message": "Details Changed Successfully",
        "Email": "Unchanged",
        "First Name": "Unchanged",
        "Last Name": "Unchanged",
    }

    if personal_update.newEmail is not None:
        update_info["email"] = personal_update.newEmail
        outcome["Email"] = "Email has been updated"
    
    if personal_update.newFirstName is not None:
        update_info["firstname"] = personal_update.newFirstName
        outcome["First Name"] = "First Name has been updated"

    if personal_update.newLastName is not None:
        update_info["lastname"] = personal_update.newLastName
        outcome["Last Name"] = "Last Name has been updated"


    if personal_update.newPhoneNumber is not None:
        update_info["phonenumber"] = personal_update.newPhoneNumber
        outcome["Phone Number"] = "Phone number has been updated"


    filter = {"username" : personal_update.username}
    update = {"$set": update_info}
    update_results = admin_collections.update_many(filter, update)

    if update_results.modified_count != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot update user information")

    return outcome


@AdminRouter.put("/admin/deactivate_user/{username}", tags=["Administrators"])
@check_token
async def deactivate_user(username: str, token: str = Depends(verify_admin_token)):
    filter = {"username": username}
    user = users_collections.find_one(filter)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username does not exist")

    update = {"$set": {"isactive": False}}
    users_collections.update_one(filter, update)
    return {"Message", f"User {username} has been deactivated"}


@AdminRouter.put("/admin/activate_user/{username}", tags=["Administrators"])
@check_token
async def activate_user(username: str, token: str = Depends(verify_admin_token)):
    filter = {"username": username}
    user = users_collections.find_one(filter)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username does not exist")

    update = {"$set": {"isactive": True}}
    users_collections.update_one(filter, update)
    return {"Message": f"User {username} has been activated"}

@AdminRouter.put("/admin/setuserasadmin/{username}", tags=["Administrators"])
@check_token
async def set_user_as_admin(username: str, token: str = Depends(verify_admin_token)):
    filter = {"username": username}
    user = users_collections.find_one(filter)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username does not exist")
    
    admin = admin_collections.find_one(filter)
    update = {"$set": {"isadmin": True}}

    if admin is not None:
        admin_collections.update_one({"username": username}, update)
        users_collections.update_one(filter, update)
    
    else:
        users_collections.update_one(filter, update)
        admin_dict = {}
        for key, value in user.items():
            if isinstance(value, ObjectId):
                admin_dict[key] = str(value)
            else:
                admin_dict[key] = value
        admin_dict["isadmin"] = True
        print(admin_dict)
        admin_collections.insert_one(admin_dict)

    return {"Message": f"{username} is now an admin"}


@AdminRouter.put("/admin/removeuserfromadmin/{username}", tags=["Administrators"])
@check_token
async def unset_user_as_admin(username: str, token: str = Depends(verify_admin_token)):
    filter = {"username": username}
    user_admin = admin_collections.delete_one(filter)

    if user_admin.deleted_count < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username was not an admin previously")
    
    update = {"$set": {"isadmin": False}}
    users_collections.update_one(filter, update)

    return {"Message": f"{username} is no longer an admin"}


@AdminRouter.delete("/admin/carspacereview/consumer/{username}", tags=["Administrators"])
@check_token
async def delete_car_space_reviews_for_consumer(username: str, token: str = Depends(verify_admin_token)):
    result = car_space_review_collections.delete_many({"reviewerusername": username})

    if result.deleted_count < 1:
        return {"Message": f"Could not find username: {username}"}
    else:
        return {"Message": f"Reviews successfully deleted for user: {username}"}
    

@AdminRouter.delete("/admin/carspacereview/consumer/{username}/{carspaceid}", tags=["Administrators"])
@check_token
async def delete_car_space_reviews_for_consumer_carspace(username: str, carspaceid: int, token: str = Depends(verify_admin_token)):
    result = car_space_review_collections.delete_many({"reviewerusername": username, "carspaceid": carspaceid})

    if result.deleted_count < 1:
        return {"Message": f"Could not find username: {username} review for carspace: {carspaceid}"}
    else:
        return {"Message": f"Reviews successfully deleted for user: {username} for carspace: {carspaceid}"}
    

@AdminRouter.delete("/admin/carspacereview/producer/{username}", tags=["Administrators"])
@check_token
async def delete_car_space_reviews_for_producer(username: str, token: str = Depends(verify_admin_token)):
    result = car_space_review_collections.delete_many({"ownerusername": username})

    if result.deleted_count < 1:
        return {"Message": f"Could not find username: {username}"}
    else:
        return {"Message": f"Reviews successfully deleted for user: {username}"}


@AdminRouter.delete("/admin/carspacereview/producer/{username}/{carspaceid}", tags=["Administrators"])
@check_token
async def delete_car_space_reviews_for_producer_carspace(username: str, carspaceid: int, token: str = Depends(verify_admin_token)):
    result = car_space_review_collections.delete_many({"ownerusername": username, "carspaceid": carspaceid})

    if result.deleted_count < 1:
        return {"Message": f"Could not find username: {username} review for carspace: {carspaceid}"}
    else:
        return {"Message": f"Reviews successfully deleted for user: {username} for carspace: {carspaceid}"}
    

# @AdminRouter.delete("/admin/carspaceimage/{username}", tags=["Administrators"], description="Delete car space a producer for a particular producer")
# @check_token
# async def delete_car_space_image_for_producer(username: str, token: str = Depends(verify_admin_token)):
#     result = car_space_image_collections.delete_many({"username": username})
#
#     if result.deleted_count > 0:
#         return {"message": "Car Space Image(s) deleted successfully"}
#     else:
#         return {"message": "Car Space Image not found"}
#
# @AdminRouter.delete("/admin/carspaceimage/{username}/{carspaceid}", tags=["Administrators"], description="Delete car space a producer for a carspace owned by a particular producer")
# @check_token
# async def delete_car_space_image_for_producer_carspace(username: str, carspaceid: int, token: str = Depends(verify_admin_token)):
#     result = car_space_image_collections.delete_many({"username": username, "carspaceid": carspaceid})
#
#     if result.deleted_count > 0:
#         return {"message": "Car Space Image(s) deleted successfully"}
#     else:
#         return {"message": "Car Space Image not found"}
#
#
# @AdminRouter.delete("/admin/carspaceimage/{username}/{carspaceid}/{image}", tags=["Administrators"], description="Delete car space a producer for a particular image in a carspace owned by a particular producer")
# @check_token
# async def delete_car_space_image_for_producer_carspace(username: str, carspaceid: int, image: str, token: str = Depends(verify_admin_token)):
#     result = car_space_image_collections.delete_many({"username": username, "carspaceid": carspaceid, "imagename": image})
#
#     if result.deleted_count > 0:
#         return {"message": "Car Space Image(s) deleted successfully"}
#     else:
#         return {"message": "Car Space Image not found"}
#

@AdminRouter.get("/admin/carspace/getcarspace/{username}", tags=["Administrators"])
@check_token
async def get_car_spaces_by_user(username: str, token: str = Depends(verify_admin_token)):
    filter = {"username": username}
    carspace_cursor = car_space_collections.find({filter})
    carspaces = []
    for document in carspace_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        carspaces.append(document_dict)
    return {f"carspaces for user: {username}": carspaces}

@AdminRouter.get("/admin/carspace/getcarspace/{username}/{carspaceid}", tags=["Administrators"])
@check_token
async def get_car_space_by_id(username: str, carspaceid: int, token: str = Depends(verify_admin_token)):
    filter = {"username": username, "carspaceid": carspaceid}
    carspace_cursor = car_space_collections.find({filter})
    carspaces = []
    []
    for document in carspace_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        carspaces.append(document_dict)
    return {f"carspaces for user: {username} and carspaceid: {carspaceid}": carspaces}
    


# @AdminRouter.delete("/admin/carspace/deletecarspace/{username}", tags=["Administrators"])
# @check_token
# async def delete_car_spaces_by_user(username: str, token: str = Depends(verify_admin_token)):
#     filter = {"username": username}
#
#     result = car_space_collections.delete_many(filter)
#     car_space_image_collections.delete_many(filter)
#     car_space_review_collections.delete_many(filter)
#
#     if result.deleted_count > 0:
#         return {"message": "Car Space deleted successfully"}
#     else:
#         return {"message": "Car Space not found"}


# @AdminRouter.delete("/admin/carspace/deletecarspace/{username}/{carspaceid}", tags=["Administrators"])
# @check_token
# async def delete_car_space_by_id(username: str, carspaceid: int, token: str = Depends(verify_admin_token)):
#     filter = {"username": username, "carspaceid": carspaceid}
#
#     result = car_space_collections.delete_many(filter)
#     car_space_image_collections.delete_many(filter)
#     car_space_review_collections.delete_many(filter)
#
#     if result.deleted_count > 0:
#         return {"message": "Car Space deleted successfully"}
#     else:
#         return {"message": "Car Space not found"}
    

@AdminRouter.put("/admin/carspace/updatecarspace/{username}", tags=["Administrators"])
@check_token
async def update_car_spaces_by_user(username: str, update_car_space: UpdateCarSpace, token: str = Depends(verify_admin_token)):
    filter = {"username": username}
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


@AdminRouter.put("/admin/carspace/updatecarspace/{username}/{carspaceid}", tags=["Administrators"])
@check_token
async def update_car_space_by_id(username: str, carspaceid: int, update_car_space: UpdateCarSpace, token: str = Depends(verify_admin_token)):
    filter = {"username": username, "carspaceid": carspaceid}
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


@AdminRouter.get("/admin/carspace/getcarspacereviews/{username}", tags=["Administrators"])
@check_token
async def get_car_spaces_reviews_by_user(username: str, token: str = Depends(verify_admin_token)):
    filter = {"username": username}
    carspace_cursor = car_space_review_collections.find(filter)
    carspaces = []
    for document in carspace_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        carspaces.append(document_dict)
    return {f"carspaces for user: {username}": carspaces}

@AdminRouter.get("/admin/carspace/getcarspacereviews/{username}/{carspaceid}", tags=["Administrators"])
@check_token
async def get_car_space_reviews_by_id(username: str, carspaceid: int, token: str = Depends(verify_admin_token)):
    filter = {"username": username, "carspaceid": carspaceid}
    carspace_cursor = car_space_review_collections.find(filter)
    carspaces = []
    for document in carspace_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        carspaces.append(document_dict)
    return {f"carspaces for user: {username} and carspaceid: {carspaceid}": carspaces}

@AdminRouter.get("/admin/carspace/get_transections/{username}", tags=["Administrators"])
@check_token
async def get_transections_by_user(username: str, token: str = Depends(verify_admin_token)):
    transactions_cursor = transaction_information_collections.find({
        "$or": [
            {"payerusername": username},
            {"receiverusername": username}
        ]
    })
    transactions = []
    for document in transactions_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        transactions.append({
            "transaction_title": document_dict.get("title"),
            "transaction_id": document_dict.get("id"),
            "payer_username": document_dict.get("payerusername"),
            "receiver_username": document_dict.get("receiverusername"),
            "transaction_time": document_dict.get("transaction_time"),
            "transaction_amount": document_dict.get("amount")
        })
    return {f"transactions for user: {username}": transactions}

@AdminRouter.get("/admin/transactions/get_transactions/{transaction_id}", tags=["Administrators"])
@check_token
async def get_transaction_by_id(transaction_id: int, token: str = Depends(verify_admin_token)):
    transaction_info = transaction_information_collections.find_one({"id": transaction_id})

    if transaction_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    transaction_str = json.dumps(transaction_info, default=str)
    transaction_dict = json.loads(transaction_str)

    return {
        "transaction_title": transaction_dict.get("title"),
        "transaction_id": transaction_dict.get("id"),
        "payer_username": transaction_dict.get("payerusername"),
        "receiver_username": transaction_dict.get("receiverusername"),
        "transaction_time": transaction_dict.get("transaction_time"),
        "transaction_amount": transaction_dict.get("amount")
    }

@AdminRouter.get("/admin/Bookings/get_all_bookings", tags=["Administrators"])
@check_token
async def get_all_bookings(token: str = Depends(verify_admin_token)):
    # verify admin
    admin = admin_collections.find_one({"username": token})
    if admin is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")
    bookings_cursor = booking_collections.find({}, {"_id": 0})  # No filter to get all documents
    bookings = []
    for document in bookings_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        bookings.append(document_dict)
    quantities = len(bookings)
    return {"All Bookings": bookings,
            "Length": quantities
            }
