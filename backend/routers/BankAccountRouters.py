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
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    # Check if the user exists
    user_info = users_collections.find_one({"username": create_account.username})
    if user_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not exist")

    # Check if the user already has a bank account
    existing_account = bank_information_collections.find_one({"username": create_account.username})
    if existing_account is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already has a bank account")

    new_account = create_account.dict()
    new_account["balance"] = 0
    bank_information_collections.insert_one({**new_account})

    return {"Message": "Bank details added successfully"}


@BankAccountRouter.put("/bankaccounts/update_account/{username}/{id}", tags=["User Bank Accounts"])
@check_token
async def update_account(username: str, id: int, new_accounts: BankAccount, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    if bank_information_collections.find_one({"username": username, "id": id}) is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No bank account to update")

    bank_information_collections.update_one({"username": username, "id": id}, {"$set": {**new_accounts}})
    
    return {"Message": "Bank details updated successfully"}


@BankAccountRouter.get("/bankaccounts/get_bank_account/{username}", tags=["User Bank Accounts"])
@check_token
async def get_bank_accounts_for_user(username: str, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")
    bank_account_cursor = bank_information_collections.find({"username": username})
    bank_accounts = []
    for document in bank_account_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        bank_accounts.append(document_dict)
    return {f"bank accounts for user: {username}": bank_accounts}


@BankAccountRouter.delete("/bankaccounts/delete_account", tags=["User Bank Accounts"])
@check_token
async def delete_account(username: str, confirm: bool = False, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    # Check if the bank account exists
    bank_account = bank_information_collections.find_one({"username": username})
    if bank_account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank account not found")

    # If confirm is False, return a warning message
    if not confirm:
        warning_message = "Warning: Deleting your bank account will result in loss of all your deposits. Please confirm this action."
        return {"Message": warning_message}

    # If confirm is True, delete the bank account
    result = bank_information_collections.delete_one({"username": username})

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bank account cannot be deleted")

    return {"Message": "Bank account deleted successfully"}



@BankAccountRouter.get("/bankaccounts/balance/{username}", tags=["User Bank Accounts"])
@check_token
async def get_balance(username: str, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")
    bank_account = bank_information_collections.find_one({"username": username})

    if bank_account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank account not found")

    return {"Balance": bank_account["balance"]}

@BankAccountRouter.put("/bankaccounts/deposit/{username}", tags=["User Bank Accounts"])
@check_token
async def deposit_money(username: str,deposit:int, token: str = Depends(verify_user_token)):
    # Verify user
    user = users_collections.find_one({"username": token})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

    # Check if the user exists
    user_info = users_collections.find_one({"username": username})
    if user_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not exist")

    # Check if the bank account exists
    bank_account = bank_information_collections.find_one({"username": username})
    if bank_account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank account not found")

        # Update the balance
    new_balance = bank_account["balance"] + deposit
    bank_information_collections.update_one({"username": username}, {"$set": {"balance": new_balance}})

    return {"Message": "Deposit successful", "New Balance": new_balance}