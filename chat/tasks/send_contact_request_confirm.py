from urllib.parse import urljoin
from django.urls import reverse
from celery import shared_task
from everybase import settings
from chat.constants import intents, messages
from chat.utilities.send_message import send_message
from chat.utilities.render_message import render_message
from chat.utilities.done_to_context import done_to_context
from relationships import models as relmods
from leads import models as lemods

_CONTACT_REQUEST_DOES_NOT_EXIST = -1
_CHATBOT_USER_DOES_NOT_EXIST = -2

@shared_task
def send_contact_request_confirm(
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
        contact_request.lead.author,
        intents.CONTACT_REQUEST,
        messages.CONTACT_REQUEST__CONFIRM
    )

    params = {
        'first_name': contact_request.lead.author.first_name,
        'last_name': contact_request.lead.author.last_name,
        'message': contact_request.message,
        'contactor_first_name': contactor.first_name,
        'contactor_last_name': contactor.last_name,
        'contactor_country': contactor.country.name,
        'lead_type': lead.lead_type,
        'lead_title': lead.title,
        'lead_detail_url': urljoin(
            settings.BASE_URL,
            reverse('leads:detail', args=[lead.uuid])),
        'contact_request_detail_url': urljoin(
            settings.BASE_URL,
            reverse('leads__root:contact_request_detail',
            args=[contact_request.uuid]))
    }

    return send_message(
        render_message(messages.CONTACT_REQUEST__CONFIRM, params),
        chatbot,
        contact_request.lead.author,
        intents.CONTACT_REQUEST,
        messages.CONTACT_REQUEST__CONFIRM,
        None,
        no_external_calls
    )