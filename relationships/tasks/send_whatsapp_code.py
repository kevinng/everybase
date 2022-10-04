import random, pytz, datetime

from everybase import settings

from chat.tasks.send_message import send_message
from chat.constants import intents, messages

from relationships import models
from relationships.constants import whatsapp_purposes
from relationships.utilities.is_whatsapp_code_rate_limited import \
    is_whatsapp_code_rate_limited

RATE_LIMITED = 'RATE_LIMITED'
NO_INTENT_AND_OR_MESSAGE = 'NO_INTENT_AND_OR_MESSAGE'

def send_whatsapp_code(
        user: models.User,
        purpose: str,
        phone_number: models.PhoneNumber=None
    ) -> bool:
    """Send WhatsApp code to user. True if successful, error flag otherwise.
    
    Parameters:
    -----------
    user
        User to generate WhatsApp code for.
    purpose
        Purpose of sending the code, see constants defined in this file.
    phone_number
        If specified, we'll use this phone number instead of user.phone_number
        to send the code via WhatsApp to. Useful in cases such as when the user
        is updating his phone number.
    """
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)

    if is_whatsapp_code_rate_limited(user):
        return RATE_LIMITED

    # Generate code
    user.whatsapp_code = random.randint(100000, 999999)
    user.whatsapp_code_generated = now
    user.save()

    # Select message
    intent = None
    message = None
    if purpose == whatsapp_purposes.LOGIN:
        intent = intents.CONFIRM_LOGIN
        message = messages.CONFIRM_LOGIN
    elif purpose == whatsapp_purposes.VERIFY_WHATSAPP:
        intent = intents.VERIFY_WHATSAPP
        message = messages.VERIFY_WHATSAPP

    p = phone_number if phone_number is not None else user.phone_number

    if intent is not None and message is not None:
        send_message.delay(user.id, intent, message, phone_number_id=p.id,
            message_params={'code': user.whatsapp_code})
        return True

    return NO_INTENT_AND_OR_MESSAGE