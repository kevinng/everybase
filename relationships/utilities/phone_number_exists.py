import phonenumbers
from relationships import models

def phone_number_exists(phone_number: str, enable_whatsapp=True) -> bool:
    """Returns PhoneNumber model reference if an existing user owns this phone number, False otherwise. Returns None if error."""
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