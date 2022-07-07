from celery import shared_task
from everybase import settings
from chat.utilities.send_message import send_message as send_twilio_message
from chat.utilities.render_message import render_message
from chat.utilities.done_to_context import done_to_context
from relationships import models

_USER_DOES_NOT_EXIST = -1
_CHATBOT_USER_DOES_NOT_EXIST = -2

@shared_task
def send_message(
        user_id: int,
        done_to_context_intent: str,
        done_to_context_message: str,
        message_params: dict=None,
        phone_number: models.PhoneNumber=None,
        no_external_calls: bool=False
    ):
    """Send WhatsApp message user.

    Parameters:
    -----------
    user_id
        ID of user to send message to.
    done_to_context_intent
        Intent to 'done' the user to.
    done_to_context_message
        Message template to use.
    message_params
        Parameters to merge into the message.
    phone_number
        If specified, we'll use this phone number instead of user.phone_number. Useful in cases such as when the user is updating his phone number.
    no_external_calls
        If True, will not make any external calls. For testing purposes.
    """

    try:
        user = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return _USER_DOES_NOT_EXIST

    try:
        chatbot = models.User.objects.get(pk=settings.CHATBOT_USER_PK)
    except models.User.DoesNotExist:
        return _CHATBOT_USER_DOES_NOT_EXIST

    done_to_context(
        user,
        done_to_context_intent,
        done_to_context_message
    )

    return send_twilio_message(
        render_message(done_to_context_message, message_params),
        chatbot,
        user,
        done_to_context_intent,
        done_to_context_message,
        to_phone_number=phone_number,
        no_external_calls=no_external_calls
    )