from celery import shared_task
from everybase import settings
from relationships import models as relmods
from chat.utilities.done_to_context import done_to_context
from chat.utilities.send_message import send_message
from chat.utilities.render_message import render_message
from chat.constants import intents, messages

_USER_DOES_NOT_EXIST = -1
_CHATBOT_USER_DOES_NOT_EXIST = -2

@shared_task
def send_whatsapp_verification_code(
        user_id: int,
        no_external_calls: bool = False
    ):

    try:
        user = relmods.User.objects.get(pk=user_id)
    except relmods.User.DoesNotExist:
        return _USER_DOES_NOT_EXIST

    try:
        chatbot = relmods.User.objects.get(pk=settings.CHATBOT_USER_PK)
    except relmods.User.DoesNotExist:
        return _CHATBOT_USER_DOES_NOT_EXIST

    done_to_context(
        user,
        intents.VERIFY_WHATSAPP,
        messages.VERIFY_WHATSAPP
    )

    return send_message(
        render_message(messages.VERIFY_WHATSAPP, {'code': user.whatsapp_login_code}),
        chatbot,
        user,
        intents.VERIFY_WHATSAPP,
        messages.VERIFY_WHATSAPP,
        None,
        no_external_calls
    )