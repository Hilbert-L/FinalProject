from typing import Optional

from pydantic import BaseModel, Field


class UpdateCarSpace(BaseModel):
    CarSpaceId: str = Field(default=None)# CarSpaceID may not be modified by providers
    NewAddress: Optional[str] = Field(default=None) 
    NewSuburb: Optional[str] = Field(default=None) 
    NewPostcode: Optional[str] = Field(default=None) 
    NewWidth: Optional[str] = Field(default=None)
    NewBreadth: Optional[str] = Field(default=None)
    NewSpacetype: Optional[str] = Field(default=None)
    NewAccessKeyRequired: bool = Field(default=None)
    NewVehicleSize: Optional[str] = Field(default=None)
    NewCurrency: Optional[str] = Field(default=None)
    NewPrice: Optional[str] = Field(default=None)
    NewFrequency: Optional[str] = Field(default=None)

    class Config:
        schema = {
            "sample" : {
                "carspaceid": "11",
                "newaddress": "test2",
                "newsuburb": "test2",
                "newpostcode": "test2",
                "newwidth": "101",
                "newbreadth": "101",
                "newspacetype": "test2",
                "newaccesskeyrequired": "False",
                "newvehiclesize": "Medium2",
                "newcurrency" : "AUD2",
                "newprice" : "101",
                "newfrequency" :"Weekly"
            }
        }


class AddImage(BaseModel):
    UserName: str = Field(default=None)
    CarSpaceId: str = Field(default=None)
    CarSpaceImage: str = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "username": "test",
                "carspaceid": "10",
                "carspaceimage": "test"
            }
        }