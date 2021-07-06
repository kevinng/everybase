from everybase.settings import TIME_ZONE
import pytz, datetime
from celery import shared_task
from chat.libraries.constants import intents, messages
from chat.libraries.utilities.send_message import send_message
from chat.libraries.utilities.done_to_context import done_to_context
from chat.libraries.utilities.get_chatbot import get_chatbot
from chat.libraries.utilities.render_message import render_message

@shared_task
def send_confirm_interests(
        match,
        buyer_only: bool = False,
        seller_only: bool = False,
        no_external_calls: bool = False
    ):
    """Send confirm-interest to both seller and buyer of a match.

    Each user's context will be set accordingly.

    Parameters
    ----------
    match
        Match we're working on
    buyer_only
        If True, will send buyer only.
    seller_only
        If True, will send seller only.
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.
    """
    sgtz = pytz.timezone(TIME_ZONE)

    # Buyer
    if seller_only == False:
        buyer = match.demand.user

        # Switch buyer's context
        done_to_context(
            buyer,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST
        )

        # Send and log
        match.sent_buyer_confirm_interest = datetime.datetime.now(tz=sgtz)
        match.sent_buyer_confirm_interest_message = send_message(
            render_message(messages.DISCUSS__CONFIRM_INTEREST, {
                'name': buyer.name,
                'buying': True,
                'supply': match.supply
            }),
            get_chatbot().phone_number,
            buyer.phone_number,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST, None,
            no_external_calls
        )

    # Seller
    if buyer_only == False:
        seller = match.supply.user

        # Switch seller's context
        done_to_context(
            seller,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST
        )

        # Send and log
        match.sent_seller_confirm_interest = datetime.datetime.now(tz=sgtz)
        match.sent_seller_confirm_interest_message = send_message(
            render_message(messages.DISCUSS__CONFIRM_INTEREST, {
                'name': seller.name,
                'buying': False,
                'demand': match.demand
            }),
            get_chatbot().phone_number,
            seller.phone_number,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST, None,
            no_external_calls
        )