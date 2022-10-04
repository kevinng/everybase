from typing import Union
import phonenumbers, phonenumber_field
from relationships import models as relmods

def get_or_create_phone_number(
        phone_number: Union[
            str,
            phonenumbers.phonenumber.PhoneNumber,
            phonenumber_field.phonenumber.PhoneNumber
        ]
    ) -> Union[relmods.PhoneNumber, bool]:
    """Returns phone number object reference created/got, or None if error.

    Parameters
    ----------
    phone_number
        Phone number to get or create.
    """
    if type(phone_number) == str:
        if phone_number is None or phone_number.strip() == '':
            return None

        try:
            parsed = phonenumbers.parse(phone_number, None)
            country_code = parsed.country_code
            national_number = parsed.national_number
        except phonenumbers.phonenumberutil.NumberParseException:
            return None

        if not phonenumbers.is_valid_number(parsed):
            return None
    elif type(phone_number) == phonenumbers.phonenumber.PhoneNumber or \
        type(phone_number) == phonenumber_field.phonenumber.PhoneNumber:
        country_code = phone_number.country_code
        national_number = phone_number.national_number
    else:
        return None

    p, _ = relmods.PhoneNumber.objects.get_or_create(
        country_code=country_code,
        national_number=national_number
    )

    return p