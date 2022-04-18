from celery import shared_task
from everybase import settings
from django.urls import reverse
from chat.constants import intents, messages
from chat.utilities.send_message import send_message
from chat.utilities.render_message import render_message
from chat.utilities.done_to_context import done_to_context
from leads import models as lemods
from relationships import models as relmods

_APPLICATION_MESSAGE_DOES_NOT_EXIST = -1
_CHATBOT_USER_DOES_NOT_EXIST = -2

@shared_task
def send_agent_application_message(
        application_message_id: int,
        no_external_calls: bool = False
    ):

    try:
        am = lemods.ApplicationMessage.objects.get(pk=application_message_id)
    except lemods.ApplicationMessage.DoesNotExist:
        return _APPLICATION_MESSAGE_DOES_NOT_EXIST

    try:
        chatbot = relmods.User.objects.get(pk=settings.CHATBOT_USER_PK)
    except relmods.User.DoesNotExist:
        return _CHATBOT_USER_DOES_NOT_EXIST

    if am.author == am.application.lead.author:
        receiver = am.application.applicant
    else:
        receiver = am.application.lead.author

    done_to_context(
        receiver,
        intents.LEAD,
        messages.LEAD__MESSAGE
    )

    params = {
        'first_name': receiver.first_name,
        'last_name': receiver.last_name,
        'country': receiver.country.name,
        'lead_headline': am.application.lead.headline,
        'message_body': am.body,
        'base_url': settings.BASE_URL,
        'application_detail_url': reverse('applications:application_detail', args=(am.application.id,))
    }

    return send_message(
        render_message(messages.LEAD__MESSAGE, params),
        chatbot,
        receiver,
        intents.LEAD,
        messages.LEAD__MESSAGE,
        None,
        no_external_calls
    )