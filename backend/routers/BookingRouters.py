from fastapi import APIRouter, Depends, status, HTTPException
from datetime import datetime, timedelta
from typing import List
from dateutil.parser import parse
import pytz

from mongodbconnect.mongodb_connect import (
    car_space_collections,
    booking_collections,
    users_collections,
    bank_information_collections,
    transaction_information_collections
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
    booking_dict["status"] = "Confirmed"

    booking_collections.insert_one(dict(booking_dict))

    # Update provider's balance
    consumer_info = bank_information_collections.find_one({"username": consumer_user["username"]})
    provider_info = bank_information_collections.find_one({"username": provider_username})
    Pnew_balance = provider_info["balance"] + total_price
    bank_information_collections.update_one(
        {"username": provider_info['username']},
        {"$set": {"balance": Pnew_balance}}
    )

    # Update consumer's balance
    Cnew_balance = consumer_info["balance"] - total_price
    # Check current balance of consumer
    if Cnew_balance < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Insufficient balance to accomplish the transaction")
    else:
        bank_information_collections.update_one(
            {"username": consumer_info['username']},
            {"$set": {"balance": Cnew_balance}}
        )

    num_transactions = transaction_information_collections.count_documents({})

    transaction_dict = dict()
    transaction_dict["TansactionID"] = num_transactions + 1
    transaction_dict["transaction_time"] = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    transaction_dict['booking_id'] = booking_dict["booking_id"]
    transaction_dict['consumer_name'] = consumer_user["username"]
    transaction_dict['provider_name'] = provider_username
    transaction_dict['total_price'] = total_price
    transaction_dict["status"] = "Confirmed"  # Add transaction status
    transaction_information_collections.insert_one(dict(transaction_dict))

    return {
        "Message": "Booking created successfully",
        "Booking": booking_dict,
    }

    

@BookingRouter.put("/booking/delete_booking/{booking_id}", tags=["Booking"])
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

    # Check the booking status
    if booking["status"] == "Canceled":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="booking not found or has been deleted")

    transaction_info = transaction_information_collections.find_one({"booking_id": booking_id})

    if transaction_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    provider_name = transaction_info['provider_name']
    consumer_name = transaction_info['consumer_name']

    consumer_info = bank_information_collections.find_one({"username": consumer_name})
    provider_info = bank_information_collections.find_one({"username": provider_name})

    amount = transaction_info["total_price"]
    # Calculate the penalty if the booking start date is less than 24 hours away
    penalty = 0
    if booking["start_date"].tzinfo is None or booking["start_date"].tzinfo.utcoffset(booking["start_date"]) is None:
        booking["start_date"] = booking["start_date"].replace(tzinfo=pytz.UTC)
    now = datetime.now().astimezone(pytz.UTC)  # now is a timezone-aware datetime object
    less_than_24h = int((booking["start_date"] - now).total_seconds()) < 24 * 60 * 60
    if less_than_24h:
        penalty = 0.05 * amount
        amount -= penalty
    # Update provider's balance
    Pnew_balance = provider_info["balance"] - amount
    # Check current balance of provider
    # Check if provider has enough balance
    if Pnew_balance < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Provider doesn't have enough balance to refund the transaction")

    bank_information_collections.update_one(
        {"username": provider_info['username']},
        {"$set": {"balance": Pnew_balance}}
    )

    # Update consumer's balance
    Cnew_balance = consumer_info["balance"] + amount
    # Check current balance of consumer

    bank_information_collections.update_one(
        {"username": consumer_info['username']},
        {"$set": {"balance": Cnew_balance}}
    )
    # Update the corresponding transaction status to 'Canceled' as well
    transaction_information_collections.update_one({"booking_id": booking_id}, {"$set": {"status": "Canceled"}})
    # Update the booking status to 'Canceled' in the database
    booking_collections.update_one({"booking_id": booking_id}, {"$set": {"status": "Canceled"}})
    return {
        "Message": "Booking cancelled successfully" +
                   (
                       " with a 5% penalty due to cancellation less than 24 hours before the start time." if less_than_24h else ""),
        "Penalty": penalty,
    }




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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not")

    # Check the booking status
    if booking["status"] == "Canceled":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking has been deleted")

    # Check if the user is authorized to update the booking
    if booking["consumer_username"] != user["username"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update this booking",
        )


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
            "status": {"$ne": "Canceled"},
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

    carspaceid = booking["carspaceid"]
    provider_username = booking["provider_username"]
    carspace = car_space_collections.find_one({"carspaceid": carspaceid, "username": provider_username})
    hour_price = carspace['price']
    total_price = hour_price * duration


    # Update the booking
    booking_collections.update_one(
        {"booking_id": booking_id},
        {"$set": {
            "start_date": booking_update.start_date,
            "end_date": booking_update.end_date,
            "duration_hours": duration,
            "total_price": total_price,
        }}
    )


    # Retrieve the updated booking
    updated_booking = booking_collections.find_one({"booking_id": booking_id},{"_id": 0})

    return {
        "Message": "Booking updated successfully",
        "Updated Booking": updated_booking,
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
    booking_cursor = booking_collections.find({"consumer_username": username},{"_id": 0})
    bookings = []
    for booking in booking_cursor:
        bookings.append(booking)

    return {"Booking History": bookings}
