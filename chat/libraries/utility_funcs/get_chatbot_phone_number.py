from everybase import settings
from relationships import models as relmods

def get_chatbot_phone_number() -> relmods.User:
    """Returns system chatbot phone number"""
    return relmods.PhoneNumber.objects.get(pk=settings.CHATBOT_PHONE_NUMBER_PK)
