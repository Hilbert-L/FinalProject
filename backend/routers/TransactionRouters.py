from models.Transaction import MakePayment
from fastapi import APIRouter, Depends, status, HTTPException
from mongodbconnect.mongodb_connect import bank_information_collections, transaction_information_collections, users_collections
from wrappers.wrappers import check_token
from authentication.authentication import verify_user_token
import json 

TransactionRouter = APIRouter()

@TransactionRouter.post("/transactions/make_payment", tags=["User Transactions"])
@check_token
async def make_payment(payment: MakePayment, token: str = Depends(verify_user_token)):
    payer_info = users_collections.find_one({"username": payment.payerusername})
    receiver_info = users_collections.find_one({"username": payment.receiverusername})
    
    if payer_info is None or receiver_info is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payer or receiver cannot be found")

    payer_bank_filter = {
        "username": payment.payerusername,
        "bankname": payment.payerbankname,
        "accountbsb": payment.payeraccountbsb,
        "accountnumber": payment.payeraccountnumber
    }

    receiver_bank_filter = {
        "username": payment.receiverusername,
        "bankname": payment.receiverbankname,
        "accountbsb": payment.receiveraccountbsb,
        "accountnumber": payment.receiveraccountnumber
    }

    payer_bank_info = bank_information_collections.find({**payer_bank_filter})
    receiver_bank_info = bank_information_collections.find({**receiver_bank_filter})

    if payer_bank_info is None or receiver_bank_info is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payer or receiver bank details cannot be found")

    num_transactions = bank_information_collections.count_documents({})
    
    transaction_dict = payment.dict()
    transaction_dict["id"] = num_transactions

    transaction_information_collections.insert_one(transaction_dict)

    return {"Message": "Payment added successfully"}


# TODO For Haoran we are creating separate collection for bank accounts and transaction
# not under Users 
# it may make things too complicated further down the line for data processesing 
# Please implement the following if you can
# Cancel Payment 
# Update Payment Method
# Check balance for user for each account
# Update Payment in AdminRouters.py
