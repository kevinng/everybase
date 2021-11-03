import sentry_sdk
from celery import shared_task

from everybase import settings
from relationships import models
from chat.libraries.constants import intents, messages
from chat.libraries.utility_funcs.send_message import send_message
from chat.libraries.utility_funcs.render_message import render_message

@shared_task
def send_register_token(token_id: int) -> str:
    try:
        register_token = models.RegisterToken.objects.get(pk=token_id)
        chatbot_user = models.User.objects.get(pk=settings.CHATBOT_USER_PK)
        chatbot_ph = models.PhoneNumber.objects.get(
            pk=settings.CHATBOT_PHONE_NUMBER_PK)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False

    return send_message(
        render_message(messages.REGISTER__CONFIRM, {}),
        chatbot_user,
        chatbot_ph,
        register_token.user,
        register_token.user.phone_number,
        intents.REGISTER,
        messages.REGISTER__CONFIRM
    )