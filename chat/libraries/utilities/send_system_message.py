from everybase.settings import (MESSAGE_SENDER_PHONE_NUMBER_PK,
    MESSAGE_RECEIVER_PHONE_NUMBER_PK)
from relationships import models as relmods
from chat.libraries.utilities.send_message import send_message

def send_system_message(body):
    """Send message to system user"""
    from_ph = relmods.PhoneNumber.objects.get(pk=MESSAGE_SENDER_PHONE_NUMBER_PK)
    to_ph = relmods.PhoneNumber.objects.get(pk=MESSAGE_RECEIVER_PHONE_NUMBER_PK)
    send_message(body, from_ph, to_ph)