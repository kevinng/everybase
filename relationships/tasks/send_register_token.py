from django.urls import reverse
from celery import shared_task

from everybase import settings
from relationships import models
from chat.libraries.constants import intents, messages

from chat.libraries.utility_funcs.send_message import send_message
from chat.libraries.utility_funcs.render_message import render_message
from chat.libraries.utility_funcs.done_to_context import done_to_context

import sentry_sdk

@shared_task
def send_register_token(token: str) -> str:
    try:
        token_obj = models.RegisterToken.objects.get(token=token)
        chatbot_user = models.User.objects.get(pk=settings.CHATBOT_USER_PK)
        chatbot_ph = models.PhoneNumber.objects.get(
            pk=settings.CHATBOT_PHONE_NUMBER_PK)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False

    done_to_context(
        token_obj.user,
        intents.REGISTER,
        messages.REGISTER__CONFIRM
    )

    return send_message(
        render_message(messages.REGISTER__CONFIRM, {
            'first_name': token_obj.user.first_name
        }),
        chatbot_user,
        chatbot_ph,
        token_obj.user,
        token_obj.user.phone_number,
        intents.REGISTER,
        messages.REGISTER__CONFIRM
    )