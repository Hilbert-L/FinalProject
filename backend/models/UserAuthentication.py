from pydantic import BaseModel, Field, EmailStr, constr, validator
from typing import Optional, List
from datetime import datetime
from .CreateCarSpace import CarSpaceReview
from validators.PasswordValidator import PasswordValidator

def get_current_datetime():
    return datetime.now()

class UserRegistrationSchema(BaseModel):
    firstname: str = Field(default=None)
    lastname: str = Field(default=None)
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: constr(min_length=8) = Field(default="$Test1234")
    phonenumber: Optional[int] = Field(default=None)
    @validator('password')
    def validate_password(cls, password):
        if not PasswordValidator.validate_password(password):
            raise ValueError(
                "Password must contain at least 1 special character, 1 capital letter, 1 lowercase letter, and 1 number"
            )
        return password
    
    class Config:
        schema = {
            "sample" : {
                "Firstname": "test",
                "Lastname": "test",
                "Username": "test",
                "Email": "test@hotmail.com",
                "Password": "$Test1234",
                "PhoneNumber": 00000000
            }
        }


class UserSchema(UserRegistrationSchema):
    userid: int = Field(default=None)
    isloggedin: bool = Field(default=None)
    passwordunhashed: str = Field(default=None)
    isactive: bool=Field(default=False)
    isadmin: bool=Field(default=False)
    class Config:
        schema = {
            "sample" : {
            "userid": "1",
            "firstname": "test",
            "lastname": "test",
            "username": "test",
            "email": "test@hotmail.com",
            "password": "$%Test1234",
            "phonenumber": 00000000,
            "isloggedin": True,
            "datecreated": "2000-01-01 15:54:53.845417",
            "passwordunhashed": "$Test1234",
            "isactive": True,
            "isadmin": False
            }
        }

class LoginSchema(BaseModel):
    username: str = Field(default=None)
    password: constr(min_length=8) = Field(default="$Test1234")
    
    class Config:
        schema = {
            "sample" : {
                "Username": "test",
                "Password": "$Test1234"
            }
        }