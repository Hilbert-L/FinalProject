from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr

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