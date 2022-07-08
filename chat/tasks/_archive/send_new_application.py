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
def send_new_application(
        user_id: int,
        lead_author_first_name: str,
        lead_author_last_name: str,
        lead_headline: str,
        application_detail_url: str,
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
        intents.NEW_APPLICATION,
        messages.NEW_APPLICATION
    )

    return send_message(
        render_message(messages.NEW_APPLICATION, {
            'lead_author_first_name': lead_author_first_name,
            'lead_author_last_name': lead_author_last_name,
            'lead_headline': lead_headline,
            'application_detail_url': application_detail_url
        }),
        chatbot,
        user,
        intents.NEW_APPLICATION,
        messages.NEW_APPLICATION,
        None,
        no_external_calls
    )