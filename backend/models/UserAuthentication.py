from pydantic import BaseModel, Field, EmailStr 
from typing import Optional, List
from datetime import datetime

def get_current_datetime():
    return datetime.now()

class UserRegistrationSchema(BaseModel):
    title: str = Field(default=None)
    firstname: str = Field(default=None)
    lastname: str = Field(default=None)
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    phonenumber: Optional[str] = Field(default=None)
    profilepicture: Optional[str] = Field(default=None)
    class Config:
        json_schema_extra = {
            "sample" : {
                "title": "mr",
                "firstname": "test",
                "lastname": "test",
                "username": "test",
                "email": "test@hotmail.com",
                "password": "test",
                "phonenumber": "0000000000",
                "profilepicture": "test",
            }
        }

class UserSchema(UserRegistrationSchema):
    userId: str = Field(default=None)
    isloggedin: str = Field(default=None)
    datecreated: datetime = Field(default_factory=get_current_datetime)
    passwordunhashed: str = Field(default=None)
    class Config:
        json_schema_extra = {
            "sample" : {
                "userid": "1",
                "title": "mr",
                "firstname": "test",
                "lastname": "test",
                "username": "test",
                "email": "test@hotmail.com",
                "password": "test",
                "profilepicture": "test",
                "isloggedin": "False",
                "datecreated": "2000-01-01 15:54:53.845417",
                "passwordunhashed": "test"
            }
        }


class LoginSchema(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    class Config:
        json_schema_extra = {
            "sample" : {
                "username": "test",
                "password": "test",
            }
        }
    
