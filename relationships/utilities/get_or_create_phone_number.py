from typing import Union
import phonenumbers
from relationships import models as relmods

def get_or_create_phone_number(
        raw_number: str
    ) -> Union[relmods.PhoneNumber, bool]:
    """Returns phone number object reference created/got, or False if error.

    Parameters
    ----------
    raw_number
        Raw phone number to get or create.
    """
    try:
        parsed_number = phonenumbers.parse(raw_number, None)
    except Exception:
        return None

    phone_number, _ = relmods.PhoneNumber.objects.get_or_create(
        country_code=parsed_number.country_code,
        national_number=parsed_number.national_number
    )

    return phone_number