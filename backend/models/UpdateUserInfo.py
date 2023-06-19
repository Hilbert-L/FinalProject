from typing import Optional
from pydantic import BaseModel, Field, EmailStr 

class UpdatePassword(BaseModel):
    username: str = Field(default=None)
    currentPassword: str = Field(default=None)
    newPassword: str = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "Username": "test",
                "CurrentPassword": "test",
                "NewPassword": "newtest"
            }
        }


class UpdateEmail(BaseModel):
    username: str = Field(default=None)
    oldEmail: EmailStr = Field(default=None)
    newEmail: EmailStr = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "Username": "test",
                "OldEmail": "test@hotmail.com",
                "NewEmail": "newtest@hotmail.com"
            }
        }


class UpdateName(BaseModel):
    username: str = Field(default=None)
    oldFirstName: str = Field(default=None)
    oldLastName: str = Field(default=None)
    newFirstName: Optional[str] = Field(default=None)
    newLastName: Optional[str] = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "Username": "test",
                "OldFirstName": "test",
                "OldLastName": "test",
                "NewFirstName": "newtest",
                "NewLastName": "newtest"
            }
        }

class UpdateProfilePicture(BaseModel):
    username: str = Field(default=None)
    oldProfilePic: str = Field(default=None)
    newProfilePic: str = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "Username": "test",
                "OldProfilePic": "string",
                "NewProfilePic": "string"
            }
        }

