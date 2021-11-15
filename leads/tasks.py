from celery import Celery

from leads import models

from chat.libraries.constants import intents, messages
from chat.libraries.utility_funcs.render_message import render_message
from chat.libraries.utility_funcs.send_message import send_message
from chat.libraries.utility_funcs.get_chatbot_phone_number import \
    get_chatbot_phone_number

app = Celery()

@app.task
def contact_lead_author(contact_request_id):
    r = models.ContactRequest.objects.get(pk=contact_request_id)

    chatbot_ph = get_chatbot_phone_number()

    m = send_message(
        render_message(
            messages.CONTACT_REQUEST__CONFIRM, {
                'lead_title': r.lead.title,
                'message': r.message,
                'contactor_name':
                    f'{r.contactor.first_name} \{r.contactor.last_name}',
                'contactor_country': r.contactor.country.name,

                

            }
        ),
        chatbot_ph,
        buyer.phone_number,
        intents.CONTACT_REQUEST,
        messages.CONTACT_REQUEST__CONFIRM,
        None,
        no_external_calls
    )