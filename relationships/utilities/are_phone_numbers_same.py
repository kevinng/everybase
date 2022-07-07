from phonenumbers.phonenumber import PhoneNumber
from phonenumber_field.formfields import PhoneNumberField 
from relationships import models
from typing import Union

def are_phone_numbers_same(
        p1: Union[PhoneNumber, PhoneNumberField, models.PhoneNumber],
        p2: Union[PhoneNumber, PhoneNumberField, models.PhoneNumber]
    ) -> bool:
    """Returns True if two PhoneNumberField or PhoneNumber object references have the same phone number."""
    return str(p1.country_code) == str(p2.country_code) and str(p1.national_number) == str(p2.national_number)