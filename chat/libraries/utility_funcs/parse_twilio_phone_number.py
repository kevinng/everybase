def parse_twilio_phone_number(twilio_phone_number):
    """Twilio phone number has format - <channel>:<e164 formatted phone number>.
    Parse and return channel and phone number in parts.

    Parameters
    ----------
    twilio_phone_number
        Twilio phone number string

    Returns
    -------
    (channel, phone_number)
        channel
            Twilio channel - e.g., whatsapp
        phone_number
            Phone number
    """
    channel = twilio_phone_number.split(':')[0]
    phone_number = twilio_phone_number.split(':')[-1]
    return (channel, phone_number)