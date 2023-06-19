from fastapi import APIRouter, Depends, status, HTTPException
from mongodbconnect.mongodb_connect import car_reservations_db, users_collections, admin_collections, car_space_review_collections, car_space_collections
from models.UserAuthentication import UserRegistrationSchema, UserSchema, LoginSchema, LogoutSchema
from models.UpdateUserInfo import UpdatePassword, UpdateEmail, UpdateName, UpdateProfilePicture
from wrappers.wrappers import check_token
from passlib.context import CryptContext
from decouple import config
from datetime import datetime
from authentication.authentication import generate_token, verify_token

# Password hashing context
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

UserRouter = APIRouter()

@UserRouter.post("/user/auth/register", tags=["User Authentication"])
async def register(userRegistrationSchema: UserRegistrationSchema): 
    stored_user = users_collections.find_one({"username": userRegistrationSchema.username})
    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    hashed_password = pwd_context.hash(userRegistrationSchema.password)
    
    # Create a new user instance 
    new_user = UserSchema(
        userId=len(list(users_collections.find())), 
        firstname=userRegistrationSchema.firstname,
        lastname=userRegistrationSchema.lastname,
        username=userRegistrationSchema.lastname,
        email=userRegistrationSchema.email,
        password=hashed_password,
        phonenumber=userRegistrationSchema.phonenumber,
        profilepicture=userRegistrationSchema.profilepicture,
        isloggedin=False,
        datecreated = datetime.now(),
    )

    new_user_dict = new_user.dict()
    users_collections.insert_one(new_user_dict)
    token = generate_token(new_user.username)
    return {"Message": "User Registered Successfully", "token": token}


@UserRouter.post("/user/auth/login", tags=["User Authentication"])
def login(UserLogin: LoginSchema): 
    filter={"username": UserLogin.username}
    stored_user = users_collections.find_one(filter)

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    # Verify the password
    if not pwd_context.verify(UserLogin.password, stored_user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user name or password")
    
    if stored_user["isloggedin"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already logged in")

    updateLoginStatus = {"$set": {"isloggedin": True}}

    users_collections.update_one(filter, updateLoginStatus)

    # Generate and return a JWT token
    token = generate_token(UserLogin.username)
    return {"Message": "User Login Successfully", "token": token}


@UserRouter.post("/user/auth/logout", tags=["User Authentication"])
async def logout(token: str = Depends(verify_token)):
    username = verify_token(token)

    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")

    stored_user = users_collections.find_one({"username": username})
    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")

    updateLogoutStatus = {"$set": {"isloggedin": False}}

    # Updated user login status
    users_collections.update_one({"username": username}, updateLogoutStatus)

    return {"Message": "Logout Successfully"}


@UserRouter.put("/user/change_password", tags=["Update User Profile"])
@check_token
async def change_password(password_update: UpdatePassword, token: str = Depends(verify_token)):
    filter = {"username": password_update.username}
    stored_user = users_collections.find_one(filter)

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")

    if not pwd_context.verify(password_update.currentPassword, stored_user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")
    
    new_hashed_password = pwd_context.hash(password_update.newPassword)
    update = {"$set": {"password": new_hashed_password}}
    update_results = users_collections.update_one(filter, update)
    
    if update_results.modified_count != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot update password")

    return {"Message": "Password Changed Successfully"}


@UserRouter.put("/user/change_email", tags=["Update User Profile"])
@check_token
async def change_email(email_update: UpdateEmail, token: str = Depends(verify_token)):
    filter = {"username": email_update.username, "email": email_update.oldEmail}
    update = {"$set": {"email": email_update.newEmail}}
    stored_user = users_collections.update_one(filter, update)

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    return {"Message": "Email Changed Successfully"}


@UserRouter.put("/user/change_name", tags=["Update User Profile"])
@check_token
async def change_name(name_update: UpdateName, token: str = Depends(verify_token)):
    filter = {
        "username": name_update.username, 
        "firstname": name_update.oldFirstName,
        "lastname": name_update.oldLastName
    }
    update = {
        "$set": {
            "firstname": name_update.newFirstName,
            "lastname": name_update.newLastName
        }
    }

    update_results = users_collections.update_one(filter, update)
    
    if update_results.modified_count != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot update password")

    outcome = {}
    outcome["Message"] = "User Exists"
    outcome["First Name"] = "Not Changed"
    outcome["Last Name"] = "Not Changed"

    if name_update.newFirstName is not None:
        outcome["First Name"] = f"Changed to {name_update.newFirstName}"

    if name_update.newLastName is not None:
        outcome["Last Name"] = f"Changed to {name_update.newLastName}"

    return outcome

@UserRouter.put("/user/change_profile_picture", tags=["Update User Profile"])
@check_token
async def change_profile_picture(profile_picture_update: UpdateProfilePicture, token: str = Depends(verify_token)):
    filter = {
        "username": profile_picture_update.username, 
    }
    update = {
        "$set": {
        "profilepicture": profile_picture_update.newProfilePic, 
        }
    }

    update_results = users_collections.update_one(filter, update)
    
    if update_results.modified_count != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    if profile_picture_update.newProfilePic is not None:
        outcome = {"Outcome": "Profile Picture Changed Successfully"}

    else:
        outcome = {"Outcome": "No Profile Picture for update"}    

    return outcome