from models.Transaction import  CancelPayment
from fastapi import APIRouter, Depends, status, HTTPException
from mongodbconnect.mongodb_connect import bank_information_collections, transaction_information_collections, users_collections, booking_collections
from wrappers.wrappers import check_token
from authentication.authentication import verify_user_token
from datetime import datetime
import json 

TransactionRouter = APIRouter()

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