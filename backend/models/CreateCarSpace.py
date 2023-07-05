from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from pymongo import MongoClient
from fastapi import FastAPI
from base64 import b64encode

class CarSpaceReview(BaseModel):
    ownerusername: str = Field(default=None)
    carspaceid: int = Field(default=None)
    reviewerusername: str = Field(default=None)
    overall: str = Field(default=None)
    location: str = Field(default=None)
    cleanliness: str = Field(default=None)
    easeofaccess: str = Field(default=None)
    communication: str = Field(default=None)
    writtenfeedback: Optional[str] = Field(default=None)
    class Config:
        schema = {
            "sample": {
                "ownerusername": "test",
                "carspaceid": 10,
                "reviewerusername": "test",
                "overall": "10",
                "location": "10",
                "cleanliness": "10",
                "easeofaccess": "10",
                "communication": "10",
                "writtenfeedback": "test"
            }
        }


class CreateCarSpaceSchema(BaseModel):
    title: str = Field(default=None)
    address: str = Field(default=None)
    suburb: str = Field(default=None)
    postcode: str = Field(default=None)
    width: Optional[str] = Field(default=None)
    breadth: Optional[str] = Field(default=None)
    spacetype: Optional[str] = Field(default=None)
    accesskeyrequired: Optional[bool] = Field(default=None)
    vehiclesize: Optional[str] = Field(default=None)
    currency: str = Field(default=None)
    price: str = Field(default=None)
    frequency: str = Field(default=None)
    leasing: bool = Field(default=None)
    booking: bool = Field(default=None)
    using: Obool = Field(default=None)
    class Config:
        schema = {
            "sample": {
                "title": "test",
                "address": "test",
                "suburb": "test",
                "postcode": "test",
                "width": "test",
                "breadth": "test",
                "spacetype": "test",
                "accesskeyrequired": False,
                "vehiclesize": "Large",
                "currency": "AUD",
                "price": "100",
                "frequency": "Daily",
                "leasing": True,
                "booking": False,
                "using": False,
            }
        }


class CarSpaceSchema(BaseModel):
    username: str = Field(default=None)
    carspaceid: int = Field(default=None)
    title: str = Field(default=None)
    firstname: str = Field(default=None)
    lastname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    phonenumber: Optional[int] = Field(default=None)
    address: str = Field(default=None)
    suburb: str = Field(default=None)
    postcode: str = Field(default=None)
    width: Optional[str] = Field(default=None)
    breadth: Optional[str] = Field(default=None)
    spacetype: Optional[str] = Field(default=None)
    accesskeyrequired: Optional[bool] = Field(default=False)
    vehiclesize: Optional[str] = Field(default=None)
    currency: str = Field(default=None)
    price: str = Field(default=None)
    frequency: str = Field(default=None)
    leasing: bool = Field(default=None)
    booking: bool = Field(default=None)
    using: bool = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "username": "test",
                "carspaceid": 10,
                "datecreated": "2000-01-01 15:54:53.845417",
                "title": "Car space title",
                "firstname": "test",
                "lastname": "test",
                "email": "test@hotmail.com",
                "phonenumber": 00000000000,
                "address": "test",
                "suburb": "test",
                "postcode": "1234",
                "width": "test",
                "breadth": "test",
                "spacetype": "test",
                "accesskeyrequired": False,
                "vehiclesize": "Large",
                "currency": "AUD",
                "price": "100",
                "frequency": "Daily",
                "leasing": True,
                "booking": False,
                "using": False,
            }
        }
