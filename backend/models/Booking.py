from pydantic import BaseModel, Field
from datetime import datetime, date
import pytz

class BookingSchema(BaseModel):
    consumer_username: str = Field(default=None)
    provider_username: str = Field(default=None)
    carspaceid: int = Field(default=None)
    start_date: datetime = Field(default=None)
    end_date: datetime = Field(default=None)
    duration_hours: int = Field(default=None)
    total_price: int = Field(default=None)

    class Config:
        schema = {
            "sample": {
                "consumer_username": "Max",
                "provider_username": "john_doe",
                "carspaceid": 10,
                "start_date": "2023-07-08T10:00:00",
                "end_date": "2023-07-08T12:00:00",
                "duration_hours": 2,
                "total_price": 20.0,
            }
        }


class BookingCreateSchema(BaseModel):
    start_date: datetime = Field(default=None)
    end_date: datetime = Field(default=None)
    class Config:
        schema = {
            "sample": {
                "start_date": "2023-07-08T10:00:00",
                "end_date": "2023-07-08T12:00:00",               
            }
        }



class BookingUpdateSchema(BaseModel):
    start_date: datetime = Field(default=None)
    end_date: datetime = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "start_date": "2023-07-08T10:00:00",
                "end_date": "2023-07-08T12:00:00",
            }
        }

