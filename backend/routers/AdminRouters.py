from fastapi import APIRouter, Depends, status, HTTPException, Header
from mongodbconnect.mongodb_connect import admin_collections
from models.UserAuthentication import UserRegistrationSchema, UserSchema, LoginSchema
from models.UpdateUserInfo import UpdatePassword, UpdatePersonalDetails
from wrappers.wrappers import check_token
from passlib.context import CryptContext
from decouple import config
from datetime import datetime
from authentication.authentication import generate_token, verify_admin_token, pwd_context

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
        userId=num_users, 
        firstname=userRegistrationSchema.firstname,
        lastname=userRegistrationSchema.lastname,
        username=userRegistrationSchema.username,
        email=userRegistrationSchema.email,
        password=hashed_password,
        phonenumber=userRegistrationSchema.phonenumber,
        profilepicture=userRegistrationSchema.profilepicture,
        isloggedin="False",
        passwordunhashed=str(userRegistrationSchema.password),
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
    
    if stored_user["isloggedin"] == "True":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already logged in")

    updateLoginStatus = {"$set": {"isloggedin": "True"}}

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

    updateLogoutStatus = {"$set": {"isloggedin": "False"}}

    # Updated user login status
    admin_collections.update_one({"username": username}, updateLogoutStatus)

    return {"Message": "Logout Successfully"}


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
        "Profile Picture": "Unchanged",
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


    if personal_update.newProfilePic is not None:
        update_info["profilepicture"] = personal_update.newProfilePic
        outcome["Profile Picture"] = "Profile Picture has been updated"

    filter = {"username" : personal_update.username}
    update = {"$set": update_info}
    update_results = admin_collections.update_many(filter, update)

    if update_results.modified_count != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot update user information")

    return outcome
