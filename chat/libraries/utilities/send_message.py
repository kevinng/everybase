from everybase.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

from twilio.rest import Client

def send_message(body, from_ph, to_ph, media_url=None):
    """Send Twilio WhatsApp message

    Parameters
    ----------
    body
        Message body
    from_ph
        Model reference of phone number from which we're sending this message
        from
    to_ph
        Model reference of phone number to which we're sending this message to
    media_url
        List of media URLs we're sending with this message
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_='whatsapp:+%s%s' % (from_ph.country_code,
            from_ph.national_number),
        to='whatsapp:+%s%s' % (to_ph.country_code, to_ph.national_number),
        media_url=media_url
    )
    return message.sid
