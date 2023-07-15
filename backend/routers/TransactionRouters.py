from models.Transaction import  CancelPayment
from fastapi import APIRouter, Depends, status, HTTPException
from mongodbconnect.mongodb_connect import bank_information_collections, transaction_information_collections, users_collections, booking_collections
from wrappers.wrappers import check_token
from authentication.authentication import verify_user_token
from datetime import datetime
import json 

TransactionRouter = APIRouter()

@TransactionRouter.post("/transactions/make_payment", tags=["User Transactions"])
@check_token
async def make_payment(booking_id: int, token: str = Depends(verify_user_token)):
    # Verify consumer
    consumer_user = users_collections.find_one({"username": token})
    if consumer_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    bookingInfo = booking_collections.find_one({"booking_id": booking_id})
    if bookingInfo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not booking found")

    consumer_name = bookingInfo['consumer_username']
    provider_name = bookingInfo['provider_username']
    total_price = bookingInfo['total_price']

    consumer_info = bank_information_collections.find_one({"username": consumer_name})
    provider_info = bank_information_collections.find_one({"username": provider_name})

    # Update provider's balance
    Pnew_balance = provider_info["balance"] + total_price
    bank_information_collections.update_one(
        {"username": provider_info['username']},
        {"$set": {"balance": Pnew_balance}}
    )

    # Update consumer's balance
    Cnew_balance = consumer_info["balance"] - total_price
    # Check current balance of consumer
    if Cnew_balance < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance to accomplish the transaction")
    else:
        bank_information_collections.update_one(
            {"username": consumer_info['username']},
            {"$set": {"balance": Cnew_balance}}
        )

    num_transactions = transaction_information_collections.count_documents({})

    transaction_dict = dict()
    transaction_dict["TansactionID"] = num_transactions + 1
    transaction_dict["transaction_time"] = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    transaction_dict['booking_id'] = booking_id
    transaction_dict['consumer_name'] = consumer_name
    transaction_dict['provider_name'] = provider_name
    transaction_dict['total_price'] = total_price
    transaction_dict["status"] = "Confirmed"  # Add transaction status
    transaction_information_collections.insert_one(dict(transaction_dict))

    return {"Message": "Payment added successfully",
            "Transaction": transaction_dict
            }

@TransactionRouter.get("/transactions/get_paymanet_detail/{transaction_id}", tags=["User Transactions"])
@check_token
async def get_payment_detail(transaction_id: int, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    transaction_info = transaction_information_collections.find_one({"TansactionID": transaction_id})

    if transaction_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    PaymentDetail = {
        "Transaction ID": transaction_info["TansactionID"],
        "Status": transaction_info["status"],
        "Created At": transaction_info["transaction_time"],
        "Receiver": transaction_info["provider_name"],
        "Amount": transaction_info["total_price"]
    }

    return PaymentDetail

@TransactionRouter.get("/transactions/payment_history", tags=["User Transactions"])
@check_token
async def get_all_transactions(username: str, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    # Check if the user is authorized to view the booking history
    if username != user["username"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to view this transaction history",
        )

    # Get all transactions
    trans_cursor = transaction_information_collections.find({"consumer_name": username})
    transactions = []
    for i in trans_cursor:
        trans_dict = dict(i)
        trans_dict["_id"] = str(trans_dict["_id"])  # Convert ObjectId to string
        transactions.append(trans_dict)

    return {"Message": "Transactions fetched successfully",
            "Transactions": transactions
            }

@TransactionRouter.delete("/transactions/cancel_payment/{transaction_id}", tags=["User Transactions"])
@check_token
async def cancel_payment(transaction_id: int, token: str = Depends(verify_user_token)):
    # Verify consumer
    consumer_user = users_collections.find_one({"username": token})
    if consumer_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    transaction_info = transaction_information_collections.find_one({"TansactionID": transaction_id})

    if transaction_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    provider_name = transaction_info['provider_name']
    consumer_name = transaction_info['consumer_name']

    consumer_info = bank_information_collections.find_one({"username": consumer_name})
    provider_info = bank_information_collections.find_one({"username": provider_name})

    amount = transaction_info["total_price"]
    # Update provider's balance
    Pnew_balance = provider_info["balance"] - amount
    # Check current balance of provider
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

    # Update transaction status to "Cancelled"
    transaction_information_collections.delete_one({"TansactionID": transaction_id})

    return {"Message": "Payment cancelled successfully"}
