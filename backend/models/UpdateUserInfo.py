from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field, constr, validator
from pydantic.networks import EmailStr
from authentication.password_validator import PasswordValidator
from models.UserAuthentication import BankAccountSchema
class UpdatePassword(BaseModel):
    username: str = Field(default=None)
    currentPassword: constr(min_length=8) = Field(default=None)
    newPassword: constr(min_length=8) = Field(default=None)

    @validator('currentPassword')
    def validate_password(cls, password):
        if not PasswordValidator.validate_password(password):
            raise ValueError(
                "Password must contain at least 1 special character, 1 capital letter, 1 lowercase letter, and 1 number"
            )
        return password
    
    @validator('newPassword')
    def validate_passwords(cls, newPassword, values, **kwargs):
        password = values.get('password')
        if newPassword == password:
            raise ValueError("New password must be different from the current password")
        
        if not PasswordValidator.validate_password(newPassword):
            raise ValueError(
                "New password must contain at least 1 special character, 1 capital letter, 1 lowercase letter, and 1 number"
            )
        
        return newPassword
    
    class Config:
        schema = {
            "sample": {
                "username": "test",
                "currentPassword": "$Test1234",
                "newPassword": "$NewTest1234"
            }
        }


class UpdatePersonalDetails(BaseModel):
    username: str = Field(default=None)
    newEmail: Optional[EmailStr] = Field(default=None)
    newFirstName: Optional[str] = Field(default=None)
    newLastName: Optional[str] = Field(default=None)
    newPhoneNumber: Optional[int] = Field(default=None) 

    class Config:
        schema = {
            "sample": {
                "username": "test",
                "newemail": "test2@hotmail.com",
                "newfirstname": "test2",
                "newlastname": "test2",
                "newPhoneNumber": 0000000,
            }
        }

class UpdateBankAccount(BaseModel):
    username: str = Field(default=None)
    newbankaccount: BankAccountSchema = Field(default=None)

    class Config:
        schema = {
            "sample": {
                "username": "test",
                "newBankAccount": {
                    "bsb": "123-456",
                    "account_number": "1234 5678",
                    "expiry_date": "01/25",
                    "ccv": "465"
                }
            }
        }