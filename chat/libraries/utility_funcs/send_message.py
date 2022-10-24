from typing import List
from everybase.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

from chat import models
from relationships import models as relmods

from twilio.rest import Client

def send_message(
        body: str,
        from_ph: relmods.PhoneNumber,
        to_ph: relmods.PhoneNumber,
        intent_key: str = None,
        message_key: str = None,
        media_url: List[str] = None,
        no_external_calls: bool = False
    ) -> models.TwilioOutboundMessage:
    """Send Twilio WhatsApp message

    Parameters
    ----------
    body
        Message body
    from_ph
        Phone number we're sending this message from
    to_ph
        Phone number we're sending this message to
    intent_key
        Intent key of message's context
    message_key
        Message key of message's context
    media_url
        List of media URLs we're sending with this message
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.
    """
    # Send message
    message = None
    if no_external_calls == False:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=body,
            from_='whatsapp:+%s%s' % (from_ph.country_code,
                from_ph.national_number),
            to='whatsapp:+%s%s' % (to_ph.country_code, to_ph.national_number),
            media_url=media_url
        )

    # Log and return
    return models.TwilioOutboundMessage.objects.create(
        intent_key=intent_key,
        message_key=message_key,

        date_created=message.date_created if message is not None else None,
        date_sent=message.date_sent if message is not None else None,
        direction=message.direction if message is not None else None,
        account_sid=message.account_sid if message is not None else None,
        message_sid=message.sid if message is not None else None,
        from_str=message.from_ if message is not None else None,
        to_str=message.to if message is not None else None,
        body=message.body if message is not None else body, # Use body
        uri=message.uri if message is not None else None,
        error_message=message.error_message if message is not None else None,
        error_code=message.error_code if message is not None else None,
        api_version=message.api_version if message is not None else None,

        from_user=from_ph.user,
        to_user=to_ph.user,

        from_phone_number=from_ph,
        to_phone_number=to_ph
    )