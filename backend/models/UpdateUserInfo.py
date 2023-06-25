from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from pymongo import MongoClient

# Change this to connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['CarSpace']
app = FastAPI()


class UpdatePassword(BaseModel):
    username: str = Field(default=None)
    currentPassword: str = Field(default=None)
    newPassword: str = Field(default=None)

    class Config:
        schema = {
            "sample": {
                "username": "test",
                "currentPassword": "test",
                "newPassword": "newtest"
            }
        }


class UpdatePersonalDetails(BaseModel):
    username: str = Field(default=None)
    newEmail: Optional[EmailStr] = Field(default=None)
    newTitle: Optional[EmailStr] = Field(default=None)
    newFirstName: Optional[str] = Field(default=None)
    newLastName: Optional[str] = Field(default=None)
    newProfilePic: Optional[str] = Field(default=None)

    class Config:
        schema = {
            "sample": {
                "username": "test",
                "newemail": "test2@hotmail.com",
                "newtitle": "Sir",
                "newfirstname": "test2",
                "newlastname": "test2",
                "newprofilepic": "test2"
            }
        }


@app.put("/users")
async def ChangePassword(password: UpdatePassword):
    user = db["users"].find_one({"username": password.username})
    if not user:
        return {"status": "Error: User does not exist"}
    current_password = user["password"]
    if password.currentPassword != current_password:
        return {"status": "Error: Current password is incorrect"}
    elif password.currentPassword == password.newPassword:
        return {"status": "Error: New password must be different from the current password"}
    else:
        filter = {"username": password.username, "password": password.currentPassword}
        new_password = {"$set": {"password": password.newPassword}}
        result = db["users"].update_one(filter, new_password)
        if result.matched_count > 0:
            return {"status": "Password upadate successfully."}
        else:
            return {"status": "Current password incorrect or user does not exist."}


@app.put("/users")
async def UpdateProfile(profile: UpdatePersonalDetails):
    filter = {"username": profile.username}
    update_details = {"$set": {}}
    for key, value in profile.dict().items():
        if value and key != 'username':
            update_details["$set"][key] = value
    result = db["users"].update_one(filter, update_details)
    if result.matched_count > 0:
        return {"status": "Personal details updated successfully"}
    else:
        return {"status": "User does not exist"}
