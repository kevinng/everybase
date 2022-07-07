import random, pytz, datetime
from everybase import settings
from chat.tasks.send_message import send_message
from chat.constants import intents, messages
from relationships import models
from relationships.constants import whatsapp_purposes

def send_whatsapp_code(
        user: models.User,
        purpose: str,
        phone_number: models.PhoneNumber=None
    ) -> bool:
    """Send WhatsApp code to user. True if successful, False otherwise.
    
    Parameters:
    -----------
    user
        User to generate WhatsApp code for.
    purpose
        Purpose of sending the code, see constants defined in this file.
    phone_number
        If specified, we'll use this phone number instead of user.phone_number to send the code via WhatsApp to. Useful in cases such as when the user is updating his phone number.
    """
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)
    user.whatsapp_code = random.randint(100000, 999999)
    user.whatsapp_code_generated = now
    user.save()

    intent = None
    message = None

    if purpose == whatsapp_purposes.LOGIN:
        intent = intents.CONFIRM_LOGIN
        message = messages.CONFIRM_LOGIN
    elif purpose == whatsapp_purposes.UPDATE_PHONE_NUMBER:
        intent = intents.CONFIRM_PHONE_NUMBER_UPDATE
        message = intents.CONFIRM_PHONE_NUMBER_UPDATE

    if intent is not None and message is not None:
        send_message.delay(user.id, intent, message, {'code': user.whatsapp_code}, phone_number=phone_number)
        return True

    return False