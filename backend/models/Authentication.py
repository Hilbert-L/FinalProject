from pydantic import BaseModel, Field, EmailStr, constr, validator
from typing import Optional, List
from datetime import datetime
from .CreateCarSpace import CarSpaceReview
from authentication.password_validator import PasswordValidator

class UserRegistrationSchema(BaseModel):
    firstname: str = Field(default=None)
    lastname: str = Field(default=None)
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: constr(min_length=8) = Field(default=None)
    phonenumber: Optional[int] = Field(default=None)
    profilepicture: Optional[str] = Field(default=None)
    
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
                "PhoneNumber": 00000000,
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
                    "Password": "$Test1234",
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
                "Password": "$Test1234"
            }
        }
    