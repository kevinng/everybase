from sys import api_version
from everybase.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

from chat import models
from twilio.rest import Client

def send_message(body, from_ph, to_ph, intent_key=None, message_key=None,
    media_url=None):
    """Send Twilio WhatsApp message

    Parameters
    ----------
    body: String
        Message body
    from_ph: relationships.PhoneNumber
        Model reference of phone number from which we're sending this message
        from
    to_ph: relationships.PhoneNumber
        Model reference of phone number to which we're sending this message to
    intent_key: String, optional
        Intent key of this message's context
    message_key: String, optional
        Message key of this message's context
    media_url: String, optional
        List of media URLs we're sending with this message
    """
    # Send message
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_='whatsapp:+%s%s' % (from_ph.country_code,
            from_ph.national_number),
        to='whatsapp:+%s%s' % (to_ph.country_code, to_ph.national_number),
        media_url=media_url
    )

    # Log
    models.TwilioOutboundMessage.objects.create(
        intent_key=intent_key,
        message_key=message_key,

        date_created=message.date_created,
        date_sent=message.date_sent,
        direction=message.direction,
        account_sid=message.account_sid,
        message_sid=message.sid,
        from_str=message.from_,
        to_str=message.to,
        body=message.body,
        uri=message.uri,
        error_message=message.error_message,
        error_code=message.error_code,
        api_version=message.api_version,

        from_user=from_ph.user,
        to_user=to_ph.user,

        from_phone_number=from_ph,
        to_phone_number=to_ph
    )

    return message.sid
