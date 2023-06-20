from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List

class CarSpaceReview(BaseModel):
    OwnerUserName: str = Field(default=None)
    CarSpaceId: str = Field(default=None)
    ReviewerUserName: str = Field(default=None)
    Overall: str = Field(default=None)
    Location: str = Field(default=None)
    Cleanliness: str = Field(default=None)
    EaseOfAccess: str = Field(default=None)
    Communication: str = Field(default=None)
    WrittenFeedback: Optional[str] = Field(default=None)
    class Config:
        schema = {
            "sample": {
                "carspaceowner": "test",
                "carspaceid": "1",
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
    DateCreated: datetime = datetime.now()
    Title: str = Field(default=None)
    Address: str = Field(default=None)
    Suburb: str = Field(default=None)
    Postcode: str = Field(default=None)
    Width: Optional[str] = Field(default=None)
    Breadth: Optional[str] = Field(default=None)
    SpaceType: Optional[str] = Field(default=None)
    AccessKeyRequired: Optional[str] = Field(default=None)
    VehicleSize: Optional[str] = Field(default=None)
    Currency: str = Field(default=None)
    Price: str = Field(default=None)
    Frequency: str = Field(default=None)
    Pictures: List[str] = Field(default=None)
    class Config:
        schema = {
            "sample": {
                "datecreated": "2000-01-01 15:54:53.845417",
                "title": "test",
                "address": "test",
                "suburb": "test",
                "postcode": "test",
                "width": "test",
                "breadth": "test",
                "spacetype": "test",
                "accesskeyrequired": "False",
                "vehiclesize": "Large",
                "currency": "AUD",
                "price": "100",
                "frequency": "Daily",
                "pictures":"test"
            }
        }


class CarSpaceSchema(BaseModel):
    UserName: str = Field(default=None)
    CarSpaceId: str = Field(default=None)
    DateCreated: datetime = datetime.now()
    Title: str = Field(default=None)
    FirstName: str = Field(default=None)
    LastName: str = Field(default=None)
    Email: EmailStr = Field(default=None)
    PhoneNumber: str = Field(default=None)
    Address: str = Field(default=None)
    Suburb: str = Field(default=None)
    Postcode: str = Field(default=None)
    Width: Optional[str] = Field(default=None)
    Breadth: Optional[str] = Field(default=None)
    SpaceType: Optional[str] = Field(default=None)
    AccessKeyRequired: Optional[str] = Field(default=None)
    VehicleSize: Optional[str] = Field(default=None)
    Currency: str = Field(default=None)
    Price: str = Field(default=None)
    Frequency: str = Field(default=None)
    Pictures: List[str] = Field(default=None)
    Reviews: List[CarSpaceReview] = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "username": "test",
                "carspaceid": "10",
                "datecreated": "2000-01-01 15:54:53.845417",
                "title": "Mr",
                "firstname": "test",
                "lastname": "test",
                "email": "test@hotmail.com",
                "phonenumber": "test",
                "address": "test",
                "suburb": "test",
                "postcode": "1234",
                "width": "test",
                "breadth": "test",
                "spacetype": "test",
                "accesskeyrequired": "False",
                "vehiclesize": "Large",
                "currency": "AUD",
                "price": "100",
                "frequency": "Daily",
                "pictures":[]
            }
        }
