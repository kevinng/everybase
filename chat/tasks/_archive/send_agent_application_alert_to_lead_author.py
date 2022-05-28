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

_APPLICATION_DOES_NOT_EXIST = -1
_CHATBOT_USER_DOES_NOT_EXIST = -2

@shared_task
def send_agent_application_alert_to_lead_author(
        application_id: int,
        no_external_calls: bool = False
    ):

    try:
        application = lemods.Application.objects.get(pk=application_id)
    except lemods.Application.DoesNotExist:
        return _APPLICATION_DOES_NOT_EXIST

    try:
        chatbot = relmods.User.objects.get(pk=settings.CHATBOT_USER_PK)
    except relmods.User.DoesNotExist:
        return _CHATBOT_USER_DOES_NOT_EXIST

    done_to_context(
        application.lead.author,
        intents.LEAD,
        messages.LEAD__RECEIVED_APPLICATION
    )

    params = {
        'first_name': application.applicant.first_name,
        'last_name': application.applicant.last_name,
        'country': application.applicant.country.name,
        'lead_headline': application.lead.headline,
        'buy_sell': 'sell' if application.lead.lead_type == 'selling' else 'buy',
        'application_detail_url': urljoin(settings.BASE_URL,
            reverse('applications:application_detail', args=(application.id,)))
    }

    return send_message(
        render_message(messages.LEAD__RECEIVED_APPLICATION, params),
        chatbot,
        application.lead.author,
        intents.LEAD,
        messages.LEAD__RECEIVED_APPLICATION,
        None,
        no_external_calls
    )