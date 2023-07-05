from models.Transaction import MakePayment
from fastapi import APIRouter, Depends, status, HTTPException, Header, UploadFile, File
from mongodbconnect.mongodb_connect import bank_information_collections, transaction_information_collections, users_collections
from models.BankAccounts import BankAccount
from wrappers.wrappers import check_token
from authentication.authentication import verify_user_token
import json 

BankAccountRouter = APIRouter()

@BankAccountRouter.post("/bankaccounts/create_account", tags=["User Bank Accounts"])
@check_token
async def create_account(create_account: BankAccount, token: str = Depends(verify_user_token)):
    details = {
        "username": create_account.username, 
        "bankname": create_account.bankname,
        "accountname": create_account.accountname,
        "accountbsb": create_account.accountbsb,
        "accountnumber": create_account.accountnumber
    }

    if bank_information_collections.find_one({**details}) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bank is already registered for this user")

    new_account = create_account.dict()
    num_accounts_for_user = len(bank_information_collections.find({"username": create_account.username}))
    new_account["id"] = num_accounts_for_user
    bank_information_collections.insert_one({**new_account})

    return {"Message": "Bank details added successfully"}


@BankAccountRouter.put("/bankaccounts/update_account/{username}/{id}", tags=["User Bank Accounts"])
@check_token
async def update_account(username: str, id: int, new_accounts: BankAccount, token: str = Depends(verify_user_token)):

    if bank_information_collections.find_one({"username": username, "id": id}) is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No bank account to update")

    bank_information_collections.update_one({"username": username, "id": id}, {"$set": {**new_accounts}})
    
    return {"Message": "Bank details updated successfully"}


@BankAccountRouter.get("/bankaccounts/get_bank_account/{username}", tags=["User Bank Accounts"])
@check_token
async def get_bank_accounts_for_user(username: str, token: str = Depends(verify_user_token)):
    bank_account_cursor = bank_information_collections.find({"username": username})
    bank_accounts = []
    for document in bank_account_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        bank_accounts.append(document_dict)
    return {f"bank accounts for user: {username}": bank_accounts}


@BankAccountRouter.delete("/bankaccounts/delete_account/{username}/{id}", tags=["User Bank Accounts"])
@check_token
async def delete_account(username: str, id: int, token: str = Depends(verify_user_token)):

    result = bank_information_collections.delete_many({"username": username, "id": id})

    if result is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bank account cannot be deleted")
    return {"Message": "Bank account deleted successfully"}

@BankAccountRouter.delete("/bankaccounts/delete_account", tags=["User Bank Accounts"])
@check_token
async def delete_account(create_account: BankAccount,token: str = Depends(verify_user_token)):
    details = {
        "username": create_account.username, 
        "bankname": create_account.bankname,
        "accountname": create_account.accountname,
        "accountbsb": create_account.accountbsb,
        "accountnumber": create_account.accountnumber
    }
    result = bank_information_collections.delete_many(details)

    if result is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bank is cannot be deleted")

    return {"Message": "Bank account deleted successfully"}

