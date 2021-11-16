from celery import Celery

from leads import models

from django.urls import reverse

from chat.libraries.constants import intents, messages
from chat.libraries.utility_funcs.render_message import render_message
from chat.libraries.utility_funcs.send_message import send_message
from chat.libraries.utility_funcs.get_chatbot_phone_number import \
    get_chatbot_phone_number
from chat.libraries.utility_funcs.done_to_context import done_to_context

app = Celery()

@app.task
def contact_lead_author(contact_request_uuid, no_external_calls=False):
    r = models.ContactRequest.objects.get(uuid=contact_request_uuid)
    chatbot_ph = get_chatbot_phone_number()

    m = send_message(
        render_message(
            messages.CONTACT_REQUEST__CONFIRM, {
                'lead_title': r.lead.title,
                'message': r.message,
                'first_name': r.contactor.first_name,
                'last_name': r.contactor.last_name,
                'country': r.contactor.country.name,
                'contact_detail_url': reverse('leads_root:message_detail',
                    {'uuid': contact_request_uuid})
            }
        ),
        chatbot_ph,
        r.author.phone_number,
        intents.CONTACT_REQUEST,
        messages.CONTACT_REQUEST__CONFIRM,
        None,
        no_external_calls
    )

    done_to_context(
        r.author,
        intents.CONTACT_REQUEST,
        messages.CONTACT_REQUEST__CONFIRM
    )

    return m