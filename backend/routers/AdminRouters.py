import base64

from fastapi import APIRouter, Depends, status, HTTPException, Header, UploadFile, File
from mongodbconnect.mongodb_connect import admin_collections, users_collections, car_space_image_collections, car_space_review_collections
from models.UserAuthentication import UserRegistrationSchema, UserSchema, LoginSchema
from models.UpdateUserInfo import UpdatePassword, UpdatePersonalDetails
from wrappers.wrappers import check_token
from authentication.authentication import generate_token, verify_admin_token, pwd_context
import os
from typing import Optional
import json 

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

     
@AdminRouter.post("/admin/upload_profile_picture", tags=["Administrators"])
@check_token
async def upload_profile_picture(token: str = Depends(verify_admin_token), image: Optional[UploadFile] = File(None),
                                 base64_image: str = None):
    filter = {"username": token}
    admin = admin_collections.find_one(filter)

    if admin is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Admin doesn't exist")

    if not image and not base64_image:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No image provided")

    update_info = {}
    if image:
        image_file_types = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.ico'}
        contents = await image.read()
        file_extension = os.path.splitext(image.filename)[1].lower()

        if file_extension not in image_file_types:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Invalid image file type")

        update_info["profileImage"] = image.filename
        update_info["profileImagedata"] = contents
        update_info["profileImageextension"] = file_extension
    elif base64_image:
        try:
            update_info["profileImage"] = image.filename
            update_info["profileImagedata"] = base64.b64decode(base64_image)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid base64 image")

    update_results = admin_collections.update_one(filter, {"$set" : update_info})

    if update_results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot update profile picture")

    return {
        "Message": "Admin Profile Picture Updated",
    }


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
    return {"Message", f"User {username} has been activated"}


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
    

@AdminRouter.delete("/admin/carspaceimage/{username}", tags=["Administrators"], description="Delete car space a producer for a particular producer")
@check_token
async def delete_car_space_image_for_producer(username: str, token: str = Depends(verify_admin_token)):
    result = car_space_image_collections.delete_many({"username": username})

    if result.deleted_count > 0:
        return {"message": "Car Space Image(s) deleted successfully"}
    else:
        return {"message": "Car Space Image not found"}

@AdminRouter.delete("/admin/carspaceimage/{username}/{carspaceid}", tags=["Administrators"], description="Delete car space a producer for a carspace owned by a particular producer")
@check_token
async def delete_car_space_image_for_producer_carspace(username: str, carspaceid: int, token: str = Depends(verify_admin_token)):
    result = car_space_image_collections.delete_many({"username": username, "carspaceid": carspaceid})

    if result.deleted_count > 0:
        return {"message": "Car Space Image(s) deleted successfully"}
    else:
        return {"message": "Car Space Image not found"}


@AdminRouter.delete("/admin/carspaceimage/{username}/{carspaceid}/{image}", tags=["Administrators"], description="Delete car space a producer for a particular image in a carspace owned by a particular producer")
@check_token
async def delete_car_space_image_for_producer_carspace(username: str, carspaceid: int, image: str, token: str = Depends(verify_admin_token)):
    result = car_space_image_collections.delete_many({"username": username, "carspaceid": carspaceid, "imagename": image})

    if result.deleted_count > 0:
        return {"message": "Car Space Image(s) deleted successfully"}
    else:
        return {"message": "Car Space Image not found"}