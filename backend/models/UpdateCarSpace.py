from typing import Optional
from pydantic import BaseModel, Field
from pymongo import MongoClient
from fastapi import FastAPI
from base64 import b64encode

# Change this to connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['CarSpace']
app=FastAPI()

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

@app.post("/CarSpaces")
async def UpdateCareSpace(data: UpdateCarSpace):
    # Convert model to dictionary
    data = data.dict()

    data["_id"] = data.pop("CarSpaceId")

    update_values = {key: value for key, value in data.items() if value is not None and key != "_id"}

    db['spaces'].update_one({"_id": data["_id"]}, {"$set": update_values})
    return {"Car Space Information": data}

@app.post("/CarSpaces")
async def UpdateImage(data: AddImage):
    file = data.CarSpaceImage
    contents = await file.read()
    # Convert file to base64 string
    base64_str = b64encode(contents).decode("utf-8")

    data["_id"] = data.pop("CarSpaceId")
    update_values = {key: value for key, value in data.dict().items() if value is not None and key != "_id"}
    update_values["CarSpaceImage"] = base64_str
    # Update operation
    db['spaces'].update_one({"_id": data["_id"]}, {"$set": update_values})

    return {"Car Space Image": file.filename}