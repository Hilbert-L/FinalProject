from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List, Union

class Search(BaseModel):
    limit: Optional[int] = Field(default=None)
    sort: bool = Field(default=False)

class SearchByPostcode(Search):
    postcode: str = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "postcode" : "2000",
                "limit" : 10,
                "sort" : False
            }
        }
    
class SearchBySuburb(Search):
    suburb: str = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "suburb" : "Kensington",
                "limit" : 10,
                "sort" : False
            }
        }
    

class SearchByAddress(Search):
    address: str = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "Address" : "123 Fake Street",
                "limit" : 10,
                "sort" : False
            }
        }
    
class AdvancedSearch(BaseModel):
    searchvalue: Optional[str] = Field(default=None)
    latitude : Optional[Union[str, float]] = Field(default=None)
    longitude : Optional[Union[str, float]] = Field(default=None)
    minprice : Optional[Union[str, int, float]] = Field(default=None)
    maxprice : Optional[Union[str, int, float]] = Field(default=None)
    spacetype: Optional[str] = Field(default=None)
    vehicletype: Optional[str] = Field(default=None)
    distancefrompin : Optional[Union[str, int, float]] = Field(default=None)
    recommendersystem : Optional[str] = Field(default=None)
    resultlimit: Optional[int] = Field(default=None)
    sortmethod: Optional[str] = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "searchvalue": "Sydney, NSW Australia",
                "latitude": -33.8688197,
                "longitude": 151.2092955,
                "minprice": 0.00,
                "maxprice": 100.00,
                "spacetype": "indoor-lot",
                "vehicletype": "suv",
                "distancefrompin": 1.0,
                "recommendersystem": "cosine",
                "resultlimit": 10,
                "sortmethod": "price-descending"
            }
        }