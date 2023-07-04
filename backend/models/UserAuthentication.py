from pydantic import BaseModel, Field, EmailStr, constr, validator
from typing import Optional, List
from datetime import datetime
from .CreateCarSpace import CarSpaceReview
from authentication.password_validator import PasswordValidator
import re

def get_current_datetime():
    return datetime.now()

class BankAccountSchema(BaseModel):
    id: str = Field(default=None)
    bsb: Optional[str] = Field(default=None)
    accountnumber: Optional[str] = Field(default=None)
    expiry_date: Optional[str] = Field(default=None)
    ccv: Optional[str] = Field(default=None)

    @validator('bsb')
    def validate_bsb(cls, bsb):
        # BSB should be in the format XXX-XXX
        if bsb and not re.match(r'^\d{3}-\d{3}$', bsb):
            raise ValueError('Invalid BSB format. It should be XXX-XXX.')
        return bsb

    @validator('accountnumber')
    def validate_account_number(cls, num):
        # Account number should be in the format XXXX XXXX
        if num and not re.match(r'^\d{4} \d{4}$', num):
            raise ValueError('Invalid account number format. It should be XXXX XXXX.')
        return num

    @validator('expiry_date')
    def validate_expiry_date(cls, date):
        # Expiry date should be in the format MM/YY
        if date and not re.match(r'^(0[1-9]|1[0-2])/(0[0-9]|[1-9][0-9])$', date):
            raise ValueError('Invalid expiry date format. It should be MM/YY.')
        return date

    @validator('ccv')
    def validate_ccv(cls, ccv):
        # CCV should be a 3 digits string
        if ccv and not re.match(r'^\d{3}$', ccv):
            raise ValueError('Invalid CCV. It should be a 3 digits string.')
        return ccv

    class Config:
        schema = {
            "sample" : {
                "BankAccount": {
                    "BSB": "123-456",
                    "AccountNumber": "1234 5678",
                    "ExpiryDate": "01/23",
                    "CCV": "123"
                }
            }
        }


class UserRegistrationSchema(BaseModel):
    firstname: str = Field(default=None)
    lastname: str = Field(default=None)
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: constr(min_length=8) = Field(default="$Test1234")
    phonenumber: Optional[int] = Field(default=None)
    bankaccount: List[BankAccountSchema] = Field(default=None)

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
                "BankAccount": {
                    "BSB": "123-456",
                    "AccountNumber": "1234 5678",
                    "ExpiryDate": "01/23",
                    "CCV": "123"
                }
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
                "BankAccount": {
                    "AccountID": "1",
                    "BSB": "123-456",
                    "AccountNumber": "1234 5678",
                    "ExpiryDate": "01/23",
                    "CCV": "123"
                },
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