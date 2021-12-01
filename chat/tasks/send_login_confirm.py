from celery import shared_task
from everybase import settings
from chat.constants import intents, messages
from chat.utilities.send_message import send_message
from chat.utilities.render_message import render_message
from chat.utilities.done_to_context import done_to_context
from relationships import models as relmods

_USER_DOES_NOT_EXIST = -1
_CHATBOT_USER_DOES_NOT_EXIST = -2

@shared_task
def send_login_confirm(
        user_id : int,
        no_external_calls : bool = False
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
        intents.LOGIN,
        messages.LOGIN__CONFIRM
    )

    params = {
        'first_name': user.first_name,
        'last_name': user.last_name
    }

    return send_message(
        render_message(messages.LOGIN__CONFIRM, params),
        chatbot,
        user,
        intents.LOGIN,
        messages.LOGIN__CONFIRM,
        None,
        no_external_calls
    )