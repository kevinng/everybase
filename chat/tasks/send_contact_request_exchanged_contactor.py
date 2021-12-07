from urllib.parse import urljoin
from django.urls import reverse
from celery import shared_task
from everybase import settings
from chat.constants import intents, messages
from chat.utilities.send_message import send_message
from chat.utilities.render_message import render_message
from chat.utilities.done_to_context import done_to_context
from relationships import models as relmods
from relationships.utilities.get_create_whatsapp_link import \
    get_create_whatsapp_link
from leads import models as lemods

_CONTACT_REQUEST_DOES_NOT_EXIST = -1
_CHATBOT_USER_DOES_NOT_EXIST = -2

@shared_task
def send_contact_request_exchanged_contactor(
        contact_request_id : int,
        no_external_calls : bool = False
    ):

    try:
        contact_request = lemods.ContactRequest.objects.get(
            pk=contact_request_id)
    except lemods.ContactRequest.DoesNotExist:
        return _CONTACT_REQUEST_DOES_NOT_EXIST

    try:
        chatbot = relmods.User.objects.get(pk=settings.CHATBOT_USER_PK)
    except relmods.User.DoesNotExist:
        return _CHATBOT_USER_DOES_NOT_EXIST

    contactor = contact_request.contactor
    lead = contact_request.lead

    done_to_context(
        contactor,
        intents.CONTACT_REQUEST,
        messages.CONTACT_REQUEST__EXCHANGED_CONTACTOR
    )

    params = {
        'author_first_name': lead.author.first_name,
        'author_last_name': lead.author.last_name,
        'author_country': lead.author.country.name,
        'lead_type': lead.lead_type,
        'lead_title': lead.title,
        'lead_detail_url': urljoin(
            settings.BASE_URL,
            reverse('leads:detail', args=[lead.uuid])),
        'whatsapp_url': get_create_whatsapp_link(contactor, lead.author),
        'contact_request_url': urljoin(
            settings.BASE_URL,
            reverse('leads__root:contact_request_list')
        ),
        'create_lead_url': urljoin(settings.BASE_URL, reverse('leads:create'))
    }

    return send_message(
        render_message(messages.CONTACT_REQUEST__EXCHANGED_CONTACTOR, params),
        chatbot,
        contactor,
        intents.CONTACT_REQUEST,
        messages.CONTACT_REQUEST__EXCHANGED_CONTACTOR,
        None,
        no_external_calls
    )