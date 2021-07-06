from everybase import settings
from relationships import models as relmods

def get_chatbot() -> relmods.PhoneNumber:
    """Returns system chatbot user"""
    return relmods.User.objects.get(pk=settings.CHATBOT_PHONE_NUMBER_PK)
