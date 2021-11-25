from celery import Celery
from django.urls import reverse

from everybase import settings

from chat.constants import intents, messages
from chat.utilities import render_message, send_message, done_to_context

from leads import models
from relationships import models as relmods

app = Celery()

@app.task
def contact_lead_author(contact_request_uuid, no_external_calls=False):
    r = models.ContactRequest.objects.get(uuid=contact_request_uuid)
    chatbot_ph = relmods.PhoneNumber.objects.get(
        pk=settings.CHATBOT_PHONE_NUMBER_PK)

# TODO: we need to update the message tempalte
    m = send_message(
        render_message(
            messages.CONTACT_REQUEST__CONFIRM, {
                'lead_title': r.lead.title,
                'message': r.message,
                'first_name': r.contactor.first_name,
                'last_name': r.contactor.last_name,
                'country': r.contactor.country.name,
                'contact_detail_url': reverse('leads_root:contact_request_detail',
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