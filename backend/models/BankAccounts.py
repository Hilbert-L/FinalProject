from pydantic import BaseModel, Field, validator
from typing import Optional
from validators.BankAccountValidator import BankAccountValidator

class BankAccount(BaseModel):
    username: str = Field(default=None)
    bankname: str = Field(default=None)
    accountname: str = Field(default=None)
    accountbsb: Optional[str] = Field(default=None)
    accountnumber: Optional[str] = Field(default=None)
    cardtitle: Optional[str] = Field(default=None)
    cardnumber: str = Field(default=None)
    cardexpirydate: str = Field(default=None)
    cardccv: str = Field(default=None)

    @validator('cardnumber')
    def validate_bank_card_number(cls, cardnumber):
        # Bank Card Number should be in the format XXXX-XXXX-XXXX-XXXX
        if cardnumber and not BankAccountValidator.validate_card_number(cardnumber):
            raise ValueError('Invalid Card number format. It should be XXXX-XXXX-XXXX-XXXX')
        return cardnumber

    @validator('accountbsb')
    def validate_bsb(cls, accountbsb):
        # BSB should be in the format XXX-XXX
        if accountbsb and not BankAccountValidator.validate_bsb(accountbsb):
            raise ValueError('Invalid BSB format. It should be XXX-XXX.')
        return accountbsb

    @validator('accountnumber')
    def validate_account_number(cls, accountnumber):
        # Australian bank accounts have the following formats:
        # Cannot start with 0, 00 or 000
        # Contains 6 to 10 digits
        if accountnumber and not BankAccountValidator.validate_account_number(accountnumber):
            raise ValueError('Invalid account number format. It should be be a 6-10 digit string with no leading zeros.')
        return accountnumber

    @validator('cardexpirydate')
    def validate_expiry_date(cls, cardexpirydate):
        # Expiry date should be in the format MM/YY
        if cardexpirydate and not BankAccountValidator.validate_expiry_date(cardexpirydate):
            raise ValueError('Invalid expiry date format. It should be MM/YY.')
        return cardexpirydate

    @validator('cardccv')
    def validate_ccv(cls, cardccv):
        # CCV should be a 3 digits string
        if cardccv and not BankAccountValidator.validate_ccv(cardccv):
            raise ValueError('Invalid CCV. It should be a 3 digits string.')
        return cardccv

    class config:
        schema = {
            "sample": {
                "username": "Test123",
                "bankname": "Bank Name",
                "accountname": "Account Name",
                "accountbsb": "123-456",
                "accountnumber": "12345678",
                "cardtitle": "Mr XXX XXX",
                "cardnumber": "1234-1234-1234-1234",
                "cardexpirydate": "01/23",
                "cardccv": "123",
            }
        }
