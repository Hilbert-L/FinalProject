from typing import Optional
from pydantic import BaseModel, Field

class UpdateCarSpaceAddress(BaseModel):
    UserName: str = Field(default=None)
    CarSpaceId: int = Field(default=None)
    OldAddress: Optional[str] = Field(default=None) 
    OldSuburb: Optional[str] = Field(default=None) 
    OldPostcode: Optional[str] = Field(default=None) 
    NewAddress: Optional[str] = Field(default=None) 
    NewSuburb: Optional[str] = Field(default=None) 
    NewPostcode: Optional[str] = Field(default=None) 
    
    class Config:
        schema = {
            "Username": "test",
            "CarSpaceId": 1,
            "OldAddress": "test",
            "OldSuburb": "test",
            "OldPostcode": "test",
            "NewAddress": "test",
            "NewSuburb": "test",
            "NewPostcode": "test",
        }


class UpdateCarSpaceDimensions(BaseModel):
    UserName: str = Field(default=None)
    CarSpaceId: int = Field(default=None)
    OldWidth: Optional[str] = Field(default=None)
    OldBreadth: Optional[str] = Field(default=None)
    OldSpacetype: Optional[str] = Field(default=None)
    OldAccessKeyRequired: bool = Field(default=None)
    OldVehicleSize: Optional[str] = Field(default=None)
    NewWidth: Optional[str] = Field(default=None)
    NewBreadth: Optional[str] = Field(default=None)
    NewSpacetype: Optional[str] = Field(default=None)
    NewAccessKeyRequired: bool = Field(default=None)
    NewVehicleSize: Optional[str] = Field(default=None)
    class Config:
        schema = {
            "Username": "test",
            "CarSpaceId": 1,
            "OldWidth": 1,
            "OldBreadth": 1,
            "OldSpaceType": "test",
            "OldAccessKeyRequired": False,
            "OldVehicleSize": "Small",
            "NewWidth": 2,
            "NewBreadth": 2,
            "NewSpaceType": "test",
            "NewAccessKeyRequired": True,
            "NewVehicleSize": "Medium"
        }


class UpdateCarSpacePrice(BaseModel):
    UserName: str = Field(default=None)
    CarSpaceId: int = Field(default=None)
    OldCurrency: Optional[str] = Field(default=None)
    OldPrice: Optional[int] = Field(default=None)
    OldFrequency: Optional[str] = Field(default=None)
    NewCurrency: Optional[str] = Field(default=None)
    NewPrice: Optional[int] = Field(default=None)
    NewFrequency: Optional[str] = Field(default=None)
    class Config:
        schema = {
            "UserName" : "test",
            "CarSpaceId" : 1,
            "OldCurrency" : "USD",
            "OldPrice" : 1,
            "OldFrequeny" : "Monthly",
            "NewCurrency" : "AUD",
            "NewPrice" : 2,
            "NewFrequency" :"Monthly"
        }


class AddImage(BaseModel):
    UserName: str = Field(default=None)
    CarSpaceId: int = Field(default=None)
    CarSpaceImage: str = Field(default=None)
