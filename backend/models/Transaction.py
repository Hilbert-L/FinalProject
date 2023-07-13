from pydantic import BaseModel, Field, EmailStr, constr, validator
from typing import Optional, List
from pymongo import MongoClient
from fastapi import FastAPI
from base64 import b64encode
from validators.BankAccountValidator import BankAccountValidator

class Payment(BaseModel):
    title: str = Field(default=None)
    payerusername: str = Field(default=None)
    payerbankname: str = Field(default=None)
    payeraccountbsb: str = Field(default=None)
    payeraccountnumber: str = Field(default=None)
    receiverusername: str = Field(default=None)
    receiverbankname: str = Field(default=None)
    receiveraccountbsb: str = Field(default=None)
    receiveraccountnumber: str = Field(default=None)
    amount: int = Field(default=None)

    class config:
        schema = {
            "sample": {
                "title": "Test Payment",
                "payerusername": "Test123",
                "payerbankname": "Bank Name",
                "payeraccountbsb": "123-456",
                "payeraccountnumber": "12345678",
                "receiverusername": "Test123",
                "receiverbankname": "Bank Name 2",
                "receiveraccountbsb": "123-456",
                "receiveraccountnumber": "12345678",
                "amount": 100,
            }
        }

class CancelPayment(BaseModel):
    title: str = Field(default=None)
    receiverusername: str = Field(default=None)
    receiverbankname: str = Field(default=None)
    receiveraccountbsb: str = Field(default=None)
    receiveraccountnumber: str = Field(default=None)

    @validator('receiveraccountbsb')
    def validate_receiver_bsb(cls, receiveraccountbsb):
        # BSB should be in the format XXX-XXX
        if receiveraccountbsb and not BankAccountValidator.validate_bsb(receiveraccountbsb):
            raise ValueError('Invalid receiver BSB format. It should be XXX-XXX.')
        return receiveraccountbsb

    @validator('receiveraccountnumber')
    def validate_receiver_account_number(cls, receiveraccountnumber):
        # Australian bank accounts have the following formats:
        # Cannot start with 0, 00 or 000
        # Contains 6 to 10 digits
        if receiveraccountnumber and not BankAccountValidator.validate_account_number(receiveraccountnumber):
            raise ValueError('Invalid receiver account number format. It should be be a 6-10 digit string with no leading zeros.')
        return receiveraccountnumber

    class config:
        schema = {
            "sample": {
                "title": "Test Payment",
                "receiverusername": "Test123",
                "receiverbankname": "Bank Name 2",
                "receiveraccountbsb": "123-456",
                "receiveraccountnumber": "12345678",
            }
        }

class UpdatePaymentMethod(BaseModel):
    username: str = Field(default=None)
    bankname: str = Field(default=None)
    accountname: str = Field(default=None)
    accountbsb: str = Field(default=None)
    accountnumber: str = Field(default=None)
