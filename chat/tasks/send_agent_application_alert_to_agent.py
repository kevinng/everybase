from celery import shared_task
from everybase import settings
from django.urls import reverse
from chat.constants import intents, messages
from chat.utilities.send_message import send_message
from chat.utilities.render_message import render_message
from chat.utilities.done_to_context import done_to_context
from leads import models as lemods
from relationships import models as relmods

_APPLICATION_DOES_NOT_EXIST = -1
_CHATBOT_USER_DOES_NOT_EXIST = -2

@shared_task
def send_agent_application_alert_to_agent(
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
        application.applicant,
        intents.LEAD,
        messages.LEAD__APPLIED_AS_AGENT
    )

    params = {
        'lead_headline': application.lead.headline,
        'buyer_seller': 'seller' if application.lead.lead_type == 'selling' else 'buyer',
        'base_url': settings.BASE_URL,
        'application_detail_url': reverse('applications:application_detail', args=(application.id,))
    }

    return send_message(
        render_message(messages.LEAD__APPLIED_AS_AGENT, params),
        chatbot,
        application.applicant,
        intents.LEAD,
        messages.LEAD__APPLIED_AS_AGENT,
        None,
        no_external_calls
    )