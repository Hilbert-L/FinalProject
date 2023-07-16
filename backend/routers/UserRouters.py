import base64
from fastapi import APIRouter, Depends, status, HTTPException, Header, UploadFile, File
from mongodbconnect.mongodb_connect import users_collections, car_space_collections, bank_information_collections, transaction_information_collections
from models.UserAuthentication import UserRegistrationSchema, UserSchema, LoginSchema
from models.UpdateUserInfo import UpdatePassword, UpdatePersonalDetails
from wrappers.wrappers import check_token
from authentication.authentication import generate_token, verify_user_token, pwd_context
import json 
import os 
from typing import Optional
import io
from PIL import Image

UserRouter = APIRouter()

@UserRouter.post("/user/auth/register", tags=["Users"])
async def register(userRegistrationSchema: UserRegistrationSchema): 
    stored_user = users_collections.find_one({"username": userRegistrationSchema.username})
    if stored_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    
    stored_email = users_collections.find_one({"email": userRegistrationSchema.email})
    if stored_email is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    hashed_password = pwd_context.hash(userRegistrationSchema.password)
    
    num_users = users_collections.count_documents({})
    # # Create a new user instance 
    new_user = UserSchema(
        userid=num_users, 
        firstname=userRegistrationSchema.firstname,
        lastname=userRegistrationSchema.lastname,
        username=userRegistrationSchema.username,
        email=userRegistrationSchema.email,
        password=hashed_password,
        passwordunhashed=userRegistrationSchema.password,
        phonenumber=userRegistrationSchema.phonenumber,
        isloggedin=True,
        isactive=True,
        isadmin=False
    )

    new_user_dict = new_user.dict()
    users_collections.insert_one(new_user_dict)
    token = generate_token(new_user.username)
    return {"Message": "User Registered Successfully", "token": token, "user": new_user}



@UserRouter.post("/user/auth/login", tags=["Users"])
async def login(UserLogin: LoginSchema): 
    filter={"username": UserLogin.username}
    stored_user = users_collections.find_one(filter)

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username doesn't exist")

    # Verify the password
    if not pwd_context.verify(UserLogin.password, stored_user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user name or password")
    
    if stored_user["isloggedin"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already logged in")

    if not stored_user["isactive"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User has been deactivated")

    users_collections.update_one(filter, {"$set": {"isloggedin": True}})

    # Generate and return a JWT token
    token = generate_token(UserLogin.username)
    return {"Message": "User Login Successfully", "token": token}


@UserRouter.post("/user/auth/logout", tags=["Users"])
async def logout(token: str = Header(...)):
    username = await verify_user_token(token)

    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")

    stored_user = users_collections.find_one({"username": username})
    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")

    # Updated user login status
    users_collections.update_one({"username": username}, {"$set": {"isloggedin": False}})

    return {"Message": "Logout Successfully"}


@UserRouter.put("/user/change_password", tags=["Users"])
@check_token
async def change_password(password_update: UpdatePassword, token: str = Depends(verify_user_token)):
    stored_user = users_collections.find_one({"username": password_update.username})

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")

    if not pwd_context.verify(password_update.currentPassword, stored_user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")
    
    if password_update.currentPassword == password_update.newPassword:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="Password is unchanged")
    
    new_hashed_password = pwd_context.hash(password_update.newPassword)
    update = {"$set": {"password": new_hashed_password, "passwordunhashed": password_update.newPassword}}
    update_results = users_collections.update_one({"username": password_update.username}, update)
    
    if update_results.modified_count != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot update password")

    return {"Message": "Password Changed Successfully"}

@UserRouter.put("/user/update_personal_details", tags=["Users"])
@check_token
async def change_personal_details(personal_update: UpdatePersonalDetails, token: str = Depends(verify_user_token)):
    update_info = {}
    outcome = {
        "Message": "Details Changed Successfully",
        "Email": "Unchanged",
        "First Name": "Unchanged",
        "Last Name": "Unchanged",
        "Phone Number": "Unchanged",
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


    update = {"$set": update_info}
    update_results = users_collections.update_many({"username": personal_update.username}, update)

    if update_results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot update user information")

    carspace_update = {"$set": update_info}
    update_car_spaces = car_space_collections.update_many({"username": personal_update.username}, carspace_update)
    outcome["Car Spaces Updated"] = update_car_spaces.modified_count

    return outcome


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

@UserRouter.post("/user/upload_profile_picture", tags=["Users"])
@check_token
async def upload_profile_picture(token: str = Depends(verify_user_token),base64_image: str = None):
    filter = {"username": token}
    user = users_collections.find_one(filter)

    if user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username doesn't exist")

    if not base64_image:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No image provided")

    if not is_valid_image(base64_image):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image format")

    update_results = users_collections.update_one(filter, {"$set": {"image": base64_image}})

    if update_results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot update profile picture")

    return {"Message": "User Profile Picture Updated"}

@UserRouter.get("/user/get_current_user", tags=["Users"])
@check_token
async def get_current_user(token: str = Depends(verify_user_token)):
    user = users_collections.find_one({"username": token})
    user_dict = json.loads(json.dumps(user, default=str))

    if user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username doesn't exist")

    bank_accounts_cursor = bank_information_collections.find({"username": token})
    bank_accounts = []
    for document in bank_accounts_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        bank_accounts.append(document_dict)
    
    payments_received_cursor = transaction_information_collections.find({"payerusername": token})
    payments = []
    for document in payments_received_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        payments.append(document_dict)
    
    receiver_received_cursor = transaction_information_collections.find({"receiverusername": token})
    money_received = []
    for document in receiver_received_cursor:
            document_str = json.dumps(document, default=str)
            document_dict = json.loads(document_str)
            money_received.append(document_dict)
        
    return {
        "Message": "User Information Retrieved Successfully",
        "User Info": user_dict,
        "Bank Accounts": bank_accounts,
        "Payments": payments,
        "Money Received": money_received
    }