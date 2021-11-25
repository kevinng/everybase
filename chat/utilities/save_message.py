from relationships import models as relmods
from chat import models
from chat.utilities import parse_twilio_phone_number
from relationships.utilities import get_or_create_phone_number

def save_message(request):
    """Saves incoming Twilio message from a HTTP request.

    Parameters
    ----------
    request
        Incoming message HTTP request

    Returns
    -------
    (message, from_ph_is_new, from_usr_is_new, to_ph_is_new, to_usr_is_new)
        message
            Message model reference.
        from_ph_is_new
            True if 'from user' phone number was created new.
        from_usr_is_new
            True if 'from user' was created new.
        to_ph_is_new
            True if 'to user' phone number was created new.
        to_usr_is_new
            True if 'to user' was created new.
    """
    # Create TwilioInboundMessage model
    message = models.TwilioInboundMessage(
        # Request Parameters
        api_version=request.data.get('ApiVersion'),
        message_sid=request.data.get('MessageSid'),
        sms_sid=request.data.get('SmsSid'),
        sms_message_sid=request.data.get('SmsMessageSid'),
        sms_status = request.data.get('SmsStatus'),
        account_sid=request.data.get('AccountSid'),
        from_str=request.data.get('From'),
        to_str=request.data.get('To'),
        body=request.data.get('Body'),
        num_media=request.data.get('NumMedia'),
        num_segments=request.data.get('NumSegments'),

        # Geographic Data-related Parameters
        from_city=request.data.get('FromCity'),
        from_state=request.data.get('FromState'),
        from_zip=request.data.get('FromZip'),
        from_country=request.data.get('FromCountry'),
        to_city=request.data.get('ToCity'),
        to_state=request.data.get('ToState'),
        to_zip=request.data.get('ToZip'),
        to_country=request.data.get('ToCountry'),

        # WhatsApp-specific Parameters
        profile_name=request.data.get('ProfileName'),
        wa_id=request.data.get('WaId'),
        forwarded=request.data.get('Forwarded'),
        frequently_forwarded=request.data.get('FrequentlyForwarded'),

        # WhatsApp Location Sharing Parameters
        latitude=request.data.get('Latitude'),
        longitude=request.data.get('Longitude'),
        address=request.data.get('Address'),
        label=request.data.get('Label')
    )

    # Commit message so we may create users associated with it
    message.save()

    # Get users and phone numbers

    _, from_raw_number = parse_twilio_phone_number(message.from_str)
    (from_phone_number, from_ph_is_new) = \
        get_or_create_phone_number(from_raw_number)

    from_usr_is_new = False
    from_user = relmods.User.objects.filter(
        phone_number=from_phone_number, # User has from phone number
        registered__isnull=False, # User is registered
        django_user__isnull=False # User has a Django user linked
    ).first()

    if from_user is None:
        from_user = relmods.User.objects.create(phone_number=from_phone_number)
        from_usr_is_new = True

    _, to_raw_number = parse_twilio_phone_number(message.to_str)
    (to_phone_number, to_ph_is_new) = \
        get_or_create_phone_number(to_raw_number)

    to_usr_is_new = False
    to_user = relmods.User.objects.filter(
        phone_number=to_phone_number, # User has to phone number
        registered__isnull=False, # User is registered
        django_user__isnull=False # User has a Django user linked
    ).first()

    if to_user is None:
        to_user = relmods.User.objects.create(phone_number=to_phone_number)
        to_usr_is_new = True

    # Update message with users and phone numbers

    message.from_user = from_user
    message.to_user = to_user

    message.from_phone_number = from_phone_number
    message.to_phone_number = to_phone_number

    message.save()

    return (message, from_ph_is_new, from_usr_is_new, to_ph_is_new,\
        to_usr_is_new)