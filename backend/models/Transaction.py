from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from pymongo import MongoClient
from fastapi import FastAPI
from base64 import b64encode


class BankAccount(BaseModel):
    username: str = Field(default=None)
    bankname: str = Field(default=None)
    accountname: str = Field(default=None)
    bankbsb: int = Field(default=None)
    bankaccountnumber: int = Field(default=None)
    class config:
        schema = {
            "sample": {
                "username": "Test123",
                "bankname": "Bank Name",
                "accountname": "Account Name",
                "bankbsb": 000000,
                "bankaccountnumber": 0000000000
            }
        }


class MakePayment(BaseModel):
    title: str = Field(default=None)
    payerusername: str = Field(default=None)
    payerbankname: str = Field(default=None)
    payerbankbsb: int = Field(default=None)
    payerbankaccountnumber: int = Field(default=None)
    receiverusername: str = Field(default=None)
    receiverbankname: str = Field(default=None)
    receiverbankbsb: int = Field(default=None)
    receiverbankaccountnumber: int = Field(default=None)
    amount: int = Field(default=None)
    class config:
        schema = {
            "sample": {
                "id": 0,
                "title": "Test Payment",
                "payerusername": "Test123",
                "payerbankname": "Bank Name",
                "payerbankbsb": 000000,
                "payerbankaccountnumber": 0000000000,
                "receiverusername": "Test123",
                "receiverbankname": "Bank Name 2",
                "receiverbankbsb": 100000,
                "receiverbankaccountnumber": 1000000000,
                "amount": 100,
            }
        }

