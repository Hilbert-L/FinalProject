from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List

class CarSpaceReview(BaseModel):
    OwnerUserName: str = Field(default=None)
    CarSpaceId: int = Field(default=None)
    ReviewerUserName: str = Field(default=None)
    Overall: int = Field(default=None)
    Location: int = Field(default=None)
    Cleanliness: int = Field(default=None)
    EaseOfAccess: int = Field(default=None)
    Communication: int = Field(default=None)
    WrittenFeedback: Optional[str] = Field(default=None)
    class Config:
        schema = {
            "CarSpaceOwner": "test",
            "CarSpaceId": 1,
            "ReviewerUserName": "test",
            "Overall": 10,
            "Location": 10,
            "Cleanliness": 10,
            "EaseOfAccess": 10,
            "Communication": 10,
            "WrittenFeedback": "test"
        }


class CreateCarSpaceSchema(BaseModel):
    UserName: str = Field(default=None)
    DateCreated: datetime = datetime.now()
    Title: str = Field(default=None)
    FirstName: str = Field(default=None)
    LastName: str = Field(default=None)
    Email: str = Field(default=None)
    PhoneNumber: str = Field(default=None)
    Address: str = Field(default=None)
    Suburb: str = Field(default=None)
    Postcode: str = Field(default=None)
    Width: Optional[str] = Field(default=None)
    Breadth: Optional[str] = Field(default=None)
    SpaceType: Optional[str] = Field(default=None)
    AccessKeyRequired: Optional[bool] = Field(default=None)
    VehicleSize: Optional[str] = Field(default=None)
    Currency: str = Field(default=None)
    Price: int = Field(default=None)
    Frequency: str = Field(default=None)
    Pictures: List[str] = Field(default=None)
    class Config:
        schema = {
            "Username": "test",
            "DateCreated": "2000-01-01 15:54:53.845417",
            "Title": "test",
            "FirstName": "test",
            "LastName": "test",
            "Email": "test",
            "PhoneNumber": "test",
            "Address": "test",
            "Suburb": "test",
            "Postcode": "test",
            "Width": "test",
            "Breadth": "test",
            "SpaceType": "test",
            "AccessKeyRequired": False,
            "VehicleSize": "Large",
            "Currency": "AUD",
            "Price": 100,
            "Frequency": "Daily",
            "Pictures":"test",
        }


class CarSpaceSchema(BaseModel):
    UserName: str = Field(default=None)
    CarSpaceId: int = Field(default=None)
    DateCreated: datetime = datetime.now()
    Title: str = Field(default=None)
    FirstName: str = Field(default=None)
    LastName: str = Field(default=None)
    Email: str = Field(default=None)
    PhoneNumber: str = Field(default=None)
    Address: str = Field(default=None)
    Suburb: str = Field(default=None)
    Postcode: str = Field(default=None)
    Width: Optional[str] = Field(default=None)
    Breadth: Optional[str] = Field(default=None)
    SpaceType: Optional[str] = Field(default=None)
    AccessKeyRequired: Optional[bool] = Field(default=None)
    VehicleSize: Optional[str] = Field(default=None)
    Currency: str = Field(default=None)
    Price: int = Field(default=None)
    Frequency: str = Field(default=None)
    Pictures: List[str] = Field(default=None)
    class Config:
        schema = {
            "Username": "test",
            "CarSpaceId": 1,
            "DateCreated": "2000-01-01 15:54:53.845417",
            "Title": "test",
            "FirstName": "test",
            "LastName": "test",
            "Email": "test",
            "PhoneNumber": "test",
            "Address": "test",
            "Suburb": "test",
            "Postcode": "test",
            "Width": "test",
            "Breadth": "test",
            "SpaceType": "test",
            "AccessKeyRequired": False,
            "VehicleSize": "Large",
            "Currency": "AUD",
            "Price": 100,
            "Frequency": "Daily",
            "Pictures":"test",
        }
