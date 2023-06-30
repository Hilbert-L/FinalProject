from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List

class Search(BaseModel):
    limit: str = Field(default=None)
    sort: bool = Field(default=False)

class SearchByPostcode(Search):
    postcode: str = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "postcode" : "2000",
                "limit" : "10",
                "sort" : False
            }
        }
    
class SearchBySuburb(Search):
    suburb: str = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "suburb" : "Kensington",
                "limit" : "10",
                "sort" : False
            }
        }
    

class SearchByAddress(Search):
    address: str = Field(default=None)
    class Config:
        schema = {
            "sample" : {
                "Address" : "123 Fake Street",
                "limit" : "10",
                "sort" : False
            }
        }
    