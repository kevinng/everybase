from celery import shared_task
from everybase import settings
from django.urls import reverse
from urllib.parse import urljoin
from chat.constants import intents, messages
from chat.utilities.send_message import send_message
from chat.utilities.render_message import render_message
from chat.utilities.done_to_context import done_to_context
from leads import models as lemods
from relationships import models as relmods

_LEAD_DOES_NOT_EXIST = -1
_CHATBOT_USER_DOES_NOT_EXIST = -2

@shared_task
def send_lead_created_message(
        lead_id: int,
        no_external_calls: bool = False
    ):

    try:
        lead = lemods.Lead.objects.get(pk=lead_id)
    except lemods.Lead.DoesNotExist:
        return _LEAD_DOES_NOT_EXIST

    try:
        chatbot = relmods.User.objects.get(pk=settings.CHATBOT_USER_PK)
    except relmods.User.DoesNotExist:
        return _CHATBOT_USER_DOES_NOT_EXIST

    done_to_context(
        lead.author,
        intents.LEAD,
        messages.LEAD__CREATED
    )

    params = {
        'lead_headline': lead.headline,
        'lead_detail_url': urljoin(settings.BASE_URL,
            reverse('leads:lead_detail', args=(lead.slug_link,)))
    }

    return send_message(
        render_message(messages.LEAD__CREATED, params),
        chatbot,
        lead.author,
        intents.LEAD,
        messages.LEAD__CREATED,
        None,
        no_external_calls
    )