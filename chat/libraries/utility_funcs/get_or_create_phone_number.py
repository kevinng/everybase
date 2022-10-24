import phonenumbers
from relationships import models as relmods

def get_or_create_phone_number(raw_number):
    """
    Parameters
    ----------
    raw_number
        Raw phone number to get/create

    Returns
    ----------
    (phone_number, created)
        phone_number
            Phone number model reference
        created
            True if a new phone number was created
    """
    parsed_number = phonenumbers.parse(raw_number, None)
    return relmods.PhoneNumber.objects.get_or_create(
        country_code=parsed_number.country_code,
        national_number=parsed_number.national_number
    )