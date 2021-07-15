from everybase import settings
from relationships import models as relmods

def get_support_phone_number() -> relmods.PhoneNumber:
    """Returns system support phone number"""
    return relmods.PhoneNumber.objects.get(pk=settings.SUPPORT_PHONE_NUMBER_PK)
