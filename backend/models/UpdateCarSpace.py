from typing import Optional
from pydantic import BaseModel, Field


class UpdateCarSpace(BaseModel):
    address: Optional[str] = Field(default=None) 
    suburb: Optional[str] = Field(default=None) 
    postcode: Optional[str] = Field(default=None)
    longitude:str = Field(default=None)
    latitude:str = Field(default=None)
    width: Optional[str] = Field(default=None)
    breadth: Optional[str] = Field(default=None)
    spacetype: Optional[str] = Field(default=None)
    accesskeyrequired: Optional[bool] = Field(default=None)
    vehiclesize: Optional[str] = Field(default=None)
    currency: Optional[str] = Field(default=None)
    price: int = Field(default=None)
    frequency: Optional[str] = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "address": "test2",
                "suburb": "test2",
                "postcode": "test2",
                "longitude": "string",
                "latitude": "string",
                "width": "101",
                "breadth": "101",
                "spacetype": "test2",
                "accesskeyrequired": False,
                "vehiclesize": "Medium2",
                "currency" : "AUD2",
                "price" : 101,
                "frequency" :"Weekly",
            }
        }

