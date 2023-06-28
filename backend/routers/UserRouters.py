from fastapi import APIRouter, Depends, status, HTTPException, Header
from mongodbconnect.mongodb_connect import users_collections
from models.UserAuthentication import UserRegistrationSchema, UserSchema, LoginSchema
from models.UpdateUserInfo import UpdatePassword, UpdatePersonalDetails
from wrappers.wrappers import check_token
from authentication.authentication import generate_token, verify_user_token, pwd_context

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

    # Create a new user instance 
    new_user = UserSchema(
        userId=num_users, 
        title=userRegistrationSchema.title,
        firstname=userRegistrationSchema.firstname,
        lastname=userRegistrationSchema.lastname,
        username=userRegistrationSchema.username,
        email=userRegistrationSchema.email,
        password=hashed_password,
        phonenumber=userRegistrationSchema.phonenumber,
        profilepicture=userRegistrationSchema.profilepicture,
        isloggedin="True",
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
    
    if stored_user["isloggedin"] == "True":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already logged in")


    users_collections.update_one(filter, {"$set": {"isloggedin": "True"}})

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
    users_collections.update_one({"username": username}, {"$set": {"isloggedin": "False"}})

    return {"Message": "Logout Successfully"}


@UserRouter.put("/user/change_password", tags=["Users"])
@check_token
async def change_password(password_update: UpdatePassword, token: str = Depends(verify_user_token)):
    stored_user = users_collections.find_one({"username": password_update.username})

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")

    if not pwd_context.verify(password_update.currentPassword, stored_user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")
    
    new_hashed_password = pwd_context.hash(password_update.newPassword)
    update = {"$set": {"password": new_hashed_password}}
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
        "Title": "Unchanged",
        "First Name": "Unchanged",
        "Last Name": "Unchanged",
        "Profile Picture": "Unchanged",
    }

    if personal_update.newEmail is not None:
        update_info["email"] = personal_update.newEmail
        outcome["Email"] = "Email has been updated"
    
    if personal_update.newTitle is not None:
        update_info["title"] = personal_update.newTitle
        outcome["Title"] = "Title has been updated"
    
    if personal_update.newFirstName is not None:
        update_info["firstname"] = personal_update.newFirstName
        outcome["First Name"] = "First Name has been updated"

    if personal_update.newLastName is not None:
        update_info["lastname"] = personal_update.newLastName
        outcome["Last Name"] = "Last Name has been updated"

    if personal_update.newProfilePic is not None:
        update_info["profilepicture"] = personal_update.newProfilePic
        outcome["Profile Picture"] = "Profile Picture has been updated"

    update = {"$set": update_info}
    update_results = users_collections.update_many({"username": personal_update.username}, update)

    if update_results.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot update user information")

    return outcome
