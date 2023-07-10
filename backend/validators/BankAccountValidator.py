import re
class BankAccountValidator:
    @classmethod
    def validate_card_number(cls, bankcardnumber: str):
        # Bank Card Number should be in the format XXXX-XXXX-XXXX-XXXX
        return re.match('^\d{4}-\d{4}-\d{4}-\d{4}$', bankcardnumber) is not None

    @classmethod
    def validate_bsb(cls, bsb):
        # BSB should be in the format XXX-XXX
        return re.match('^\d{3}-\d{3}$', bsb) is not None
    
    @classmethod
    def validate_account_number(cls, num):
        # Australian bank accounts have the following formats:
        # Cannot start with 0, 00 or 000
        # Contains 6 to 10 digits
        return re.match('^(?!000)(?!00)(?!0)[0-9]{6,10}$', num) is not None
    
    @classmethod
    def validate_expiry_date(cls, date):
        # Expiry date should be in the format MM/YY
        return re.match('^(0[1-9]|1[0-2])/(0[0-9]|[1-9][0-9])$', date) is not None
    
    @classmethod
    def validate_ccv(cls, ccv):
        # CCV should be a 3 digits string
        return re.match('^\d{3}$', ccv) is not None
    