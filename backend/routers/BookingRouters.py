from fastapi import APIRouter, Depends, status, HTTPException
from datetime import datetime, timedelta
from typing import List
import pytz

from mongodbconnect.mongodb_connect import (
    car_space_collections,
    booking_collections,
    users_collections,
)
from models.Booking import BookingCreateSchema, BookingUpdateSchema, BookingSchema
from authentication.authentication import verify_user_token
from wrappers.wrappers import check_token

BookingRouter = APIRouter()


@BookingRouter.post("/booking/create_booking/{username}/{carspaceid}", tags=["Booking"])
@check_token
async def create_booking(
    provider_username: str,
    carspaceid: int,
    carspace_booking: BookingCreateSchema,
    token: str = Depends(verify_user_token)
):
    # Verify consumer
    consumer_user = users_collections.find_one({"username": token})
    if consumer_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    # Verify car space
    carspace = car_space_collections.find_one({"carspaceid": carspaceid, "username": provider_username})
    if carspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid carspace"
        )


    # convert start_date to UTC format
    start_date_utc = carspace_booking.start_date.replace(tzinfo=pytz.UTC)
    current_time_utc = datetime.now(pytz.UTC)
    if start_date_utc < current_time_utc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date cannot be in the past")



    # Verify start_date is ealier than the end_date
    if carspace_booking.start_date >= carspace_booking.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid booking dates. Start date should be earlier than end date."
        )


    # Verify if booking dates overlap with existing bookings
    existing_bookings = booking_collections.count_documents(
        {
            "carspaceid": carspaceid,
            "$or": [
                {
                    "start_date": {"$lte": carspace_booking.start_date},
                    "end_date": {"$gte": carspace_booking.start_date},
                },
                {
                    "start_date": {"$lte": carspace_booking.end_date},
                    "end_date": {"$gte": carspace_booking.end_date},
                },
                {
                    "start_date": {"$gte": carspace_booking.start_date},
                    "end_date": {"$lte": carspace_booking.end_date},
                },
            ],
        }
    )

    if existing_bookings > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Booking dates overlap with existing bookings"
        )

    # Calculate duration in hours
    duration= int((carspace_booking.end_date - carspace_booking.start_date).total_seconds() / 3600)
    # Create a new booking instance
    booking = BookingCreateSchema(
        start_date=carspace_booking.start_date,
        end_date=carspace_booking.end_date,
    )

    hour_price = carspace['price']
    total_price = hour_price * duration


    # Create a new booking instance
    booking_count = booking_collections.count_documents({})

    # Convert booking instance to dictionary and insert into database
    booking_dict = booking.dict()
    booking_dict["consumer_username"] = consumer_user["username"]
    booking_dict["provider_username"] = provider_username
    booking_dict["carspaceid"] = carspaceid
    booking_dict["duration_hours"] = duration
    booking_dict['total_price'] = total_price
    booking_dict["booking_id"] = booking_count + 1

    booking_collections.insert_one(dict(booking_dict))

    return {
        "Message": "Booking created successfully",
        "Booking": booking_dict,
    }

    

@BookingRouter.delete("/booking/delete_booking/{booking_id}", tags=["Booking"])
@check_token
async def delete_booking(booking_id: int, token: str = Depends(verify_user_token)):
    
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")
    
    # Verify booking
    booking = booking_collections.find_one({"booking_id": booking_id})
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="booking not found")

    
    # Check if the user is authorized to delete the booking
    if booking["consumer_username"] != user["username"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to delete this booking",
        )


    # Delete the booking from the database
    booking_collections.delete_one({"booking_id": booking_id})

    return {"Message": "Booking deleted successfully"}




@BookingRouter.put("/booking/update_booking/{booking_id}", tags=["Booking"])
@check_token
async def update_booking(
    booking_id: int,
    booking_update: BookingUpdateSchema,
    token: str = Depends(verify_user_token),
):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    # Verify booking
    booking = booking_collections.find_one({"booking_id": booking_id})
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid booking")

    # Check if the user is authorized to update the booking
    if booking["consumer_username"] != user["username"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update this booking",
        )

    '''
    # Check if payment has been made for the booking
    if booking["payment_status"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking cannot be updated as payment has been made",
        )
    '''

    # Verify start_date is ealier than the end_date
    if booking_update.start_date >= booking_update.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid booking dates. Start date should be earlier than end date."
        )

    # Verify if booking dates overlap with existing bookings
    existing_bookings = booking_collections.count_documents(
        {
            "booking_id": {"$ne": booking_id},
           "$or": [
                {
                    "start_date": {"$lte": booking_update.end_date},
                    "end_date": {"$gte": booking_update.start_date},
                },
                {
                    "start_date": {"$gte": booking_update.start_date},
                    "end_date": {"$lte": booking_update.end_date},
                },
                {
                    "start_date": {"$lte": booking_update.start_date},
                    "end_date": {"$gte": booking_update.end_date},
                },
            ],
        }
    )

    if existing_bookings > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="UpdatedBooking dates overlap with existing bookings"
        )

    # Calculate duration in hours
    duration= int((booking_update.end_date - booking_update.start_date).total_seconds() / 3600)

    # Update the booking
    booking_collections.update_one(
        {"booking_id": booking_id},
        {"$set": {
            "start_date": booking_update.start_date,
            "end_date": booking_update.end_date,
            "duration_hours": duration,
        }}
    )


    # Retrieve the updated booking
    updated_booking = booking_collections.find_one({"booking_id": booking_id})
    updated_booking_dict = dict(updated_booking)
    updated_booking_dict["_id"] = str(updated_booking_dict["_id"])

    return {
        "Message": "Booking updated successfully",
        "Updated Booking": updated_booking_dict,
    }




@BookingRouter.get("/booking/history/{username}", tags=["Booking"])
@check_token
async def get_booking_history(username: str, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    # Check if the user is authorized to view the booking history
    if username != user["username"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to view this booking history",
        )

    # Retrieve the booking history for the user
    booking_cursor = booking_collections.find({"consumer_username": username})
    bookings = []
    for booking in booking_cursor:
        booking_dict = dict(booking)
        booking_dict["_id"] = str(booking_dict["_id"])  # Convert ObjectId to string
        bookings.append(booking_dict)

    return {"Booking History": bookings}
