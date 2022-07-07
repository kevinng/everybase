import phonenumbers
from relationships import models as relmods

def get_or_create_phone_number(
        raw_number: str
    ) -> relmods.PhoneNumber:
    """Returns phone number object reference created/got.

    Parameters
    ----------
    raw_number
        Raw phone number to get or create.
    """
    parsed_number = phonenumbers.parse(raw_number, None)
    return relmods.PhoneNumber.objects.get_or_create(
        country_code=parsed_number.country_code,
        national_number=parsed_number.national_number
    )