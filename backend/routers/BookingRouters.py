from fastapi import APIRouter, Depends, status, HTTPException
from datetime import datetime
from typing import List
from bson import ObjectId

from mongodbconnect.mongodb_connect import (
    car_space_collections,
    booking_collections,
    users_collections,
)
from models.Booking import BookingCreateSchema, BookingUpdateSchema, BookingSchema
from authentication.authentication import verify_user_token
from wrappers.wrappers import check_token

BookingRouter = APIRouter()


@BookingRouter.post("/booking/create_booking", tags=["Booking"])
@check_token
async def create_booking(
    create_booking: BookingCreateSchema, token: str = Depends(verify_user_token)
):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    # Verify car space
    carspace = car_space_collections.find_one(
        {"carspaceid": create_booking.carspace_id}
    )
    if carspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid carspace"
        )

    # Create a new booking instance
    booking = BookingSchema(
        booking_id=None,
        carspace_id=create_booking.carspace_id,
        user_id=user["userid"],
        start_time=create_booking.start_time,
        end_time=create_booking.end_time,
        duration_hours=create_booking.duration_hours,
        total_price=create_booking.total_price,
        payment_status=False,
    )

    # Convert booking instance to dictionary and insert into database
    booking_dict = booking.dict()
    booking_collections.insert_one(booking_dict)

    return {
        "Message": "Booking created successfully",
        "Booking": booking_dict,
    }



@BookingRouter.put("/booking/update_booking/{booking_id}", tags=["Booking"])
@check_token
async def update_booking(
    booking_id: str,
    update_booking: BookingUpdateSchema,
    token: str = Depends(verify_user_token),
):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    # Verify booking
    booking = booking_collections.find_one({"_id": ObjectId(booking_id)})
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid booking")

    # Check if the user is authorized to update the booking
    if booking["user_id"] != user["userid"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update this booking",
        )

    # Check if payment has been made for the booking
    if booking["payment_status"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking cannot be updated as payment has been made",
        )

    # Update the booking information
    updated_booking = booking.copy()
    updated_booking.update(update_booking.dict(skip_defaults=True))
    booking_collections.update_one(
        {"_id": ObjectId(booking_id)}, {"$set": updated_booking}
    )

    return {
        "Message": "Booking updated successfully",
        "Updated Booking": updated_booking,
    }




@BookingRouter.delete("/booking/cancel_booking/{booking_id}", tags=["Booking"])
@check_token
async def cancel_booking(booking_id: str, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    # Verify booking
    booking = booking_collections.find_one({"_id": ObjectId(booking_id)})
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid booking"
        )

    # Check if the user is authorized to cancel the booking
    if booking["user_id"] != user["userid"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to cancel this booking",
        )

    # Check if payment has been made for the booking
    if booking["payment_status"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking cannot be cancelled as payment has been made",
        )

    # Delete the booking from the database
    booking_collections.delete_one({"_id": ObjectId(booking_id)})

    return {"Message": "Booking cancelled successfully"}


@BookingRouter.get("/booking/history/{user_id}", tags=["Booking"])
@check_token
async def get_booking_history(
    user_id: int, token: str = Depends(verify_user_token)
):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    # Check if the user is authorized to view the booking history
    if user_id != user["userid"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to view this booking history",
        )

    # Retrieve the booking history for the user
    booking_cursor = booking_collections.find({"user_id": user_id})
    bookings = []
    for booking in booking_cursor:
        booking_dict = dict(booking)
        bookings.append(booking_dict)

    return {"Booking History": bookings}
