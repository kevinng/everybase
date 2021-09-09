import pytz, datetime
from everybase.settings import TIME_ZONE
from celery import shared_task
from relationships import models as relmods
from chat.libraries.constants import intents, messages
from chat.libraries.utility_funcs.done_to_context import done_to_context
from chat.libraries.utility_funcs.send_message import send_message
from chat.libraries.utility_funcs.render_message import render_message
from chat.libraries.utility_funcs.get_chatbot_phone_number import \
    get_chatbot_phone_number

@shared_task
def send_recommend_product_type(
        rec_id: int,
        no_external_calls: bool = False
    ):
    """Forward answer to questioner

    Parameters
    ----------
    rec_id
        ID of the recommendation we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.

    Returns
    -------
    Recommendation sent
    """
    r = relmods.Recommendation.objects.get(pk=rec_id)

    done_to_context(
        r.recommendee,
        intents.RECOMMEND,
        messages.RECOMMEND__PRODUCT_TYPE
    )

    r.recommendee.current_recommendation = r
    r.recommendee.save()

    params = {
        'product_type': r.lead.product_type.name,
        'is_buying': r.lead.is_buying
    }

    sgtz = pytz.timezone(TIME_ZONE)
    r.recommend_product_type_sent = datetime.datetime.now(tz=sgtz)
    r.save()

    return send_message(
        render_message(messages.RECOMMEND__PRODUCT_TYPE, params),
        get_chatbot_phone_number(),
        r.recommendee.phone_number,
        intents.RECOMMEND,
        messages.RECOMMEND__PRODUCT_TYPE,
        None,
        no_external_calls
    )