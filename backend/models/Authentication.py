from pydantic import BaseModel, Field, EmailStr 
from typing import Optional, List
from datetime import datetime
from .CreateCarSpace import CarSpaceReview

class UserRegistrationSchema(BaseModel):
    firstname: str = Field(default=None)
    lastname: str = Field(default=None)
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    phonenumber: Optional[str] = Field(default=None)
    profilepicture: Optional[str] = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "Firstname": "test",
                "Lastname": "test",
                "Username": "test",
                "Email": "test@hotmail.com",
                "Password": "test",
                "PhoneNumber": "+614XXXXXXXX",
                "ProfilePicture": "test",
            }
        }

class UserSchema(UserRegistrationSchema):
    userId: int = Field(default=None)
    isloggedin: bool = Field(default=None)
    DateCreated: datetime = datetime.now()
    Reviews: List[CarSpaceReview] = Field(default=None)
    class Config:
            schema = {
                "sample" : {
                    "Firstname": "test",
                    "Lastname": "test",
                    "Username": "test",
                    "Email": "test@hotmail.com",
                    "Password": "test",
                    "ProfilePicture": "test",
                    "userId": "1",
                    "isLoggedin": False,
                    "DateCreated": "2000-01-01 15:54:53.845417",
                    "Reviews": []
                }
            }

class LoginSchema(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "Username": "test",
                "Password": "test"
            }
        }
    

# class UserSchema(BaseModel):
#     userId: int = Field(default=None)
#     firstname: str = Field(default=None)
#     lastname: str = Field(default=None)
#     username: str = Field(default=None)
#     email: EmailStr = Field(default=None)
#     password: str = Field(default=None)
#     phonenumber: Optional[str] = Field(default=None)
#     profilepicture: Optional[str] = Field(default=None)
#     isloggedin: bool = Field(default=None)
#     DateCreated: datetime = datetime.now()
#     Reviews: List[CarSpaceReview] = Field(default=None)
#     class Config:
#         schema = {
#             "sample" : {
#                 "userId": "1",
#                 "Firstname": "test",
#                 "Lastname": "test",
#                 "Username": "test",
#                 "Email": "test@hotmail.com",
#                 "Password": "test",
#                 "ProfilePicture": "test",
#                 "isLoggedin": False,
#                 "DateCreated": "2000-01-01 15:54:53.845417",
#                 "Reviews": []
#             }
#         }
