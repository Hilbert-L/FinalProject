from models.Transaction import BankAccount, MakePayment
from fastapi import APIRouter, Depends, status, HTTPException, Header, UploadFile, File
from mongodbconnect.mongodb_connect import bank_information_collections, transaction_information_collections, users_collections
from models.UserAuthentication import UserRegistrationSchema, UserSchema, LoginSchema
from models.UpdateUserInfo import UpdatePassword, UpdatePersonalDetails
from models.UpdateCarSpace import UpdateCarSpace
from wrappers.wrappers import check_token
from authentication.authentication import verify_user_token
import os
from typing import Optional
import json 


TransactionRouter = APIRouter()

@TransactionRouter.post("/transactions/create_account")
@check_token
async def create_account(create_account: BankAccount,token: str = Depends(verify_user_token)):
    details = {
        "username": create_account.username, 
        "bankname": create_account.bankname,
        "accountname": create_account.accountname,
        "bankbsb": create_account.bankbsb,
        "bankaccountnumber": create_account.bankaccountnumber
    }
    contains_bank_details = bank_information_collections.find(details)

    if contains_bank_details is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bank is already registered for this user")

    bank_information_collections.insert_one(details)

    return {"Message": "Bank details added successfully"}


@TransactionRouter.get("/transactions/{username}")
@check_token
async def get_bank_accounts_for_user(username: str,token: str = Depends(verify_user_token)):
    bank_account_cursor = bank_information_collections.find({"username": username})
    bank_accounts = []
    for document in bank_account_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        bank_accounts.append(document_dict)
    return {f"bank accounts for user: {username}": bank_accounts}


@TransactionRouter.delete("/transactions/delete_account")
@check_token
async def delete_account(create_account: BankAccount,token: str = Depends(verify_user_token)):
    details = {
        "username": create_account.username, 
        "bankname": create_account.bankname,
        "accountname": create_account.accountname,
        "bankbsb": create_account.bankbsb,
        "bankaccountnumber": create_account.bankaccountnumber
    }
    result = bank_information_collections.delete_many(details)

    if result is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bank is cannot be deleted")

    bank_information_collections.insert_one(details)

    return {"Message": "Bank account deleted successfully"}



@TransactionRouter.post("/transactions/make_payment")
@check_token
async def make_payment(payment: MakePayment, token: str = Depends(verify_user_token)):
    payer_info = users_collections.find_one({"username": payment.payerusername})
    receiver_info = users_collections.find_one({"username": payment.receiverusername})
    
    if payer_info is None or receiver_info is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payer or receiver cannot be found")

    payer_bank_filter = {
        "username": payment.payerusername,
        "bankname": payment.payerbankname,
        "bankbsb": payment.payerbankbsb,
        "bankaccountnumber": payment.payerbankaccountnumber
    }

    receiver_bank_filter = {
        "username": payment.receiverusername,
        "bankname": payment.receiverbankname,
        "bankbsb": payment.receiverbankbsb,
        "bankaccountnumber": payment.receiverbankaccountnumber
    }

    payer_bank_info = bank_information_collections.find(payer_bank_filter)
    receiver_bank_info = bank_information_collections.find(receiver_bank_filter)

    if payer_bank_info is None or receiver_bank_info is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payer or receiver bank details cannot be found")

    num_transactions = bank_information_collections.count_documents({})
    
    transaction_dict = payment.dict()
    transaction_dict["id"] = num_transactions

    transaction_information_collections.insert_one(transaction_dict)

    return {"Message": "Payment added successfully"}


@TransactionRouter.post("/transactions/cancel_payment")
@check_token
async def cancel_payment(payment: MakePayment, token: str = Depends(verify_user_token)):
    pass


@TransactionRouter.post("/transactions/make_payment")
@check_token
async def update_payment(payment: MakePayment, token: str = Depends(verify_user_token)):
    pass


# Contains routers for the following
# Check balance for user for each account
# Make payment for user
# Cancel payment for user


# For users table will need to return bank information and transactions
# Maybe just add a few more routers

