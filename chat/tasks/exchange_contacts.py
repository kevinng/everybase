from typing import Tuple
import pytz, datetime
from everybase.settings import TIME_ZONE

from chat import models
from relationships import models as relmods

from chat.libraries.constants import intents, messages
from chat.libraries.utility_funcs.get_create_whatsapp_link import \
    get_create_whatsapp_link
from chat.libraries.utility_funcs.get_chatbot import get_chatbot
from chat.libraries.utility_funcs.render_message import render_message
from chat.libraries.utility_funcs.send_message import send_message
from chat.libraries.utility_funcs.done_to_context import done_to_context

def exchange_contacts(
        match: relmods.Match,
        no_external_calls: bool = False
    ) -> Tuple[models.TwilioOutboundMessage, models.TwilioOutboundMessage]:
    """Exchange buyer and seller contacts to each other

    Parameters
    ----------
    match
        Match we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.

    Returns
    -------
    Tuple of outbound messages sent:

    (buyer_msg, seller_msg)
    """

    chatbot_ph = get_chatbot().phone_number
    buyer = match.demand.user
    seller = match.supply.user

    # Send buyer
    buyer_msg = send_message(
        render_message(
            messages.CONNECTED,
            {
                'buying': True,
                'contact': seller,
                'whatsapp_url': get_create_whatsapp_link(
                    buyer,
                    seller
                )
            }
        ),
        chatbot_ph,
        buyer.phone_number,
        intents.QNA,
        messages.CONNECTED,
        None,
        no_external_calls
    )

    # Switch buyer's context
    done_to_context(buyer, intents.QNA, messages.CONNECTED)

    # Update sent-buyer timestamp
    sgtz = pytz.timezone(TIME_ZONE)
    match.sent_contact_to_buyer = datetime.datetime.now(tz=sgtz)

    # Send seller
    seller_msg = send_message(
        render_message(
            messages.CONNECTED,
            {
                'buying': False,
                'contact': buyer,
                'whatsapp_url': get_create_whatsapp_link(
                    seller,
                    buyer
                )
            }
        ),
        chatbot_ph,
        seller.phone_number,
        intents.QNA,
        messages.CONNECTED,
        None,
        no_external_calls
    )

    # Update sent_seller timestamp
    match.sent_contact_to_seller = datetime.datetime.now(tz=sgtz)

    # Switch buyer's context
    done_to_context(seller, intents.QNA, messages.CONNECTED)

    return (buyer_msg, seller_msg)