from models.Transaction import MakePayment, CancelPayment
from fastapi import APIRouter, Depends, status, HTTPException
from mongodbconnect.mongodb_connect import bank_information_collections, transaction_information_collections, users_collections
from wrappers.wrappers import check_token
from authentication.authentication import verify_user_token
from datetime import datetime
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
    receiver_bank_info = bank_information_collections.find_one({**receiver_bank_filter})

    if payer_bank_info is None or receiver_bank_info is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payer or receiver bank details cannot be found")

    # Update receiver's balance
    new_balance = receiver_bank_info["balance"] + payment.amount
    bank_information_collections.update_one(
        {"username": payment.receiverusername},
        {"$set": {"balance": new_balance}}
    )

    num_transactions = transaction_information_collections.count_documents({})
    
    transaction_dict = payment.dict()
    transaction_dict["id"] = num_transactions + 1
    transaction_dict["transaction_time"] = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    transaction_information_collections.insert_one(transaction_dict)

    return {"Message": "Payment added successfully"}

@TransactionRouter.get("/transactions/get_paymanet_detail/{transaction_id}", tags=["User Transactions"])
@check_token
async def get_payment_detail(transaction_id: int, token: str = Depends(verify_user_token)):
    transaction_info = transaction_information_collections.find_one({"id": transaction_id})

    if transaction_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    PaymentDetail = {
        "Transaction ID": transaction_info["id"],
        "Title": transaction_info["title"],
        "Created At": transaction_info["transaction_time"],
        "Receiver": transaction_info["receiverusername"],
        "Amount": transaction_info["amount"]
    }

    return PaymentDetail

@TransactionRouter.delete("/transactions/cancel_payment/{transaction_id}", tags=["User Transactions"])
@check_token
async def cancel_payment(transaction_id: int, token: str = Depends(verify_user_token)):
    transaction_info = transaction_information_collections.find_one({"id": transaction_id})

    if transaction_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    payer_bank_filter = {
        "username": transaction_info["payerusername"],
        "bankname": transaction_info["payerbankname"],
        "accountbsb": transaction_info["payeraccountbsb"],
        "accountnumber": transaction_info["payeraccountnumber"]
    }
    print(payer_bank_filter)
    receiver_bank_filter = {
        "username": transaction_info["receiverusername"],
        "bankname": transaction_info["receiverbankname"],
        "accountbsb": transaction_info["receiveraccountbsb"],
        "accountnumber": transaction_info["receiveraccountnumber"]
    }


    payer_bank_info = bank_information_collections.find_one({**payer_bank_filter})
    print(payer_bank_info)
    receiver_bank_info = bank_information_collections.find_one({**receiver_bank_filter})
    print(receiver_bank_info)

    if payer_bank_info is None or receiver_bank_info is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Payer or receiver bank details cannot be found")

    payer_balance = payer_bank_info.get("balance", 0)
    receiver_balance = receiver_bank_info.get("balance", 0)

    # Update balances
    amount = transaction_info["amount"]
    updated_payer_balance = payer_balance + amount
    updated_receiver_balance = receiver_balance - amount

    # Update payer bank account balance
    bank_information_collections.update_one(
        {**payer_bank_filter},
        {"$set": {"balance": updated_payer_balance}}
    )

    # Update receiver bank account balance
    bank_information_collections.update_one(
        {**receiver_bank_filter},
        {"$set": {"balance": updated_receiver_balance}}
    )

    transaction_information_collections.delete_one({"id": transaction_id})

    return {"Message": "Payment cancelled successfully"}

# TODO For Haoran we are creating separate collection for bank accounts and transaction
# not under Users 
# it may make things too complicated further down the line for data processesing 
# Please implement the following if you can
# Cancel Payment 
# Update Payment Method
# Check balance for user for each account
# Update Payment in AdminRouters.py

