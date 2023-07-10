from pydantic import BaseModel, Field
from datetime import datetime


class BookingSchema(BaseModel):
    booking_id: int = Field(default=None)
    carspace_id: int = Field(default=None)
    user_id: int = Field(default=None)
    start_time: datetime = Field(default=None)
    end_time: datetime = Field(default=None)
    duration_hours: int = Field(default=None)
    total_price: float = Field(default=None)
    payment_status: bool = Field(default=None)

    class Config:
        schema = {
            "sample": {
                "booking_id": 1,
                "carspace_id": 10,
                "user_id": 1,
                "start_time": "2023-07-08T10:00:00",
                "end_time": "2023-07-08T12:00:00",
                "duration_hours": 2,
                "total_price": 20.0,
                "payment_status": True
            }
        }


class BookingCreateSchema(BaseModel):
    carspace_id: int = Field(default=None)
    user_id: int = Field(default=None)
    start_time: datetime = Field(default=None)
    end_time: datetime = Field(default=None)
    duration_hours: int = Field(default=None)
    total_price: float = Field(default=None)

    class Config:
        schema = {
            "sample": {
                "carspace_id": 10,
                "user_id": 1,
                "start_time": "2023-07-08T10:00:00",
                "end_time": "2023-07-08T12:00:00",
                "duration_hours": 2,
                "total_price": 20.0
            }
        }


class BookingUpdateSchema(BaseModel):
    booking_id: int = Field(..., description="Booking ID")
    start_time: datetime = Field(None, description="Start time of the booking")
    end_time: datetime = Field(None, description="End time of the booking")
    duration_hours: int = Field(None, description="Duration of the booking in hours")
    total_price: float = Field(None, description="Total price of the booking")
    payment_status: bool = Field(None, description="Payment status of the booking")

    class Config:
        schema_extra = {
            "example": {
                "booking_id": 1,
                "start_time": "2023-07-08T10:00:00",
                "end_time": "2023-07-08T12:00:00",
                "duration_hours": 2,
                "total_price": 20.0,
                "payment_status": True
            }
        }
