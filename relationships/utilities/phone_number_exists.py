from typing import Union
import phonenumbers, phonenumber_field
from relationships import models

def phone_number_exists(
        phone_number: Union[phonenumbers.phonenumber.PhoneNumber, str],
        enable_whatsapp=True
    ) -> Union[bool, models.User]:
    """Returns PhoneNumber model reference if an existing user owns this phone number, False otherwise. Returns None if error.
    
    Parameters:
    -----------
    phone_number
        Phone number to check.
    enable_whatsapp
        User.enable_whatsapp setting. Default True - i.e., only include users who have enabled WhatsApp.
    """
    if type(phone_number) == str:
        if phone_number is None or phone_number.strip() == '':
            return False

        try:
            parsed = phonenumbers.parse(phone_number, None)
            country_code = parsed.country_code
            national_number = parsed.national_number
        except phonenumbers.phonenumberutil.NumberParseException:
            return False

        if not phonenumbers.is_valid_number(parsed):
            return False
    elif type(phone_number) == phonenumbers.phonenumber.PhoneNumber or \
        type(phone_number) == phonenumber_field.phonenumber.PhoneNumber:
        country_code = phone_number.country_code
        national_number = phone_number.national_number
    else:
        return False

    try:
        p = models.PhoneNumber.objects.get(
            country_code=country_code,
            national_number=national_number
        )

        u = models.User.objects.filter(
            phone_number=p.id, # User has phone number
            registered__isnull=False, # User is registered
            django_user__isnull=False, # User has a Django user linked
            deleted__isnull=True, # User is not deleted
            enable_whatsapp=enable_whatsapp # User has enabled WhatsApp
        ).first()
        
        if u is not None:
            # Phone number belongs to an existing user
            return u
    except models.PhoneNumber.DoesNotExist:
        return False
    
    return False