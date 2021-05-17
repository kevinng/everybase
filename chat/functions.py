from datetime import datetime
from pytz import timezone

from django.template.loader import render_to_string

from . import models
from everybase import settings
from relationships import models as relmods

from twilio.twiml.messaging_response import MessagingResponse
import phonenumbers

def get_phone_number(raw_number):
    """Last updated: 17 May 2021, 11:10 PM

    Parameters
    ----------
    (phone_number, is_new)
        phone_number - reference to phone number model row
        is_new - True if new phone number was created
    """
    parsed_number = phonenumbers.parse(raw_number, None)

    try:
        # Find phone number
        number = relmods.PhoneNumber.objects.get(
            country_code=parsed_number.country_code,
            national_number=parsed_number.national_number
        )
        return (number, False)
    except relmods.PhoneNumber.DoesNotExist:
        # Create phone number if it doesn't exist
        number = relmods.PhoneNumber(
            country_code=parsed_number.country_code,
            national_number=parsed_number.national_number
        )
        number.save()
        return (number, True)

def get_user(phone_number):
    """Last updated: 17 May 2021, 2:19 PM

    Parameters
    ----------
    phone_number
        Reference to user's phone number model row

    Returns
    -------
    (user, is_new)
        user - reference to user model row
        is_new - boolean: True if new user was created
    """
    try:
        user = relmods.User.objects.get(
            phone_number=phone_number
        )
        return (user, False)
    except relmods.User.DoesNotExist:
        user = relmods.User(
            phone_number=phone_number
        )
        user.save()
        return (user, True)

def start_context(user, context):
    """Start context for user - i.e., set context started time to now and
    stopped time to null.

    Parameters
    ----------
    user
        Reference to user we're starting the context for
    context
        Context key reference
    """
    try:
        chat_context = models.UserChatContext.objects.get(
            user=user,
            context=context
        )
        # Start this context
        chat_context.started = datetime.now(tz=timezone(settings.TIME_ZONE))
        chat_context.stopped = None
    except models.UserChatContext.DoesNotExist:
        # Create new context if it does not exist
        chat_context = models.UserChatContext(
            started=datetime.now(tz=timezone(settings.TIME_ZONE)),
            user=user,
            context=context
        )

    chat_context.save()

def get_phone_number_string(twilio_phone_number):
    """Last updated: 17 May 2021, 3:32 PM

    Parameters
    ----------
    twilio_phone_number
        Twilio phone number string

    Returns
    -------
    Phone number portion of a Twilio phone number in the format -
    <channel>:<e164 formatted phone number>
    """
    return twilio_phone_number.split(':')[-1]

def get_active_chat_contexts(user):
    """Last updated: 17 May 2021, 3:33 PM

    Parameters
    ----------
    user
        User whose active contexts we're returning
    
    Returns
    -------
    All active contexts of user
    """
    ret = []
    contexts = models.UserChatContext.objects.filter(
        user=user,
        stopped__isnull=True
    )
    for c in contexts:
        ret.append(c.context)
    return ret

def save_message(request):
    """Saves Twilio incoming message as a new model row from a HTTP request.
    
    Last updated: 17 May 2021, 3:07 PM

    Parameters
    ----------
    request
        Incoming message HTTP request

    Returns
    -------
    (message, is_from_new, is_to_new)
        message - Message model reference
        is_from_new - True if 'from user' was created new
        is_to_new - True if 'to user' was created new
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

    from_raw_number = get_phone_number_string(message.from_str)
    (from_phone_number, from_ph_is_new) = get_phone_number(from_raw_number)
    (from_user, from_usr_is_new) = get_user(from_phone_number)

    to_raw_number = get_phone_number_string(message.from_str)
    (to_phone_number, to_ph_is_new) = get_phone_number(to_raw_number)
    (to_user, to_usr_is_new) = get_user(to_phone_number)

    # Update message with users and phone numbers

    message.from_user = from_user
    message.to_user = to_user

    message.from_phone_number = from_phone_number
    message.to_phone_number = to_phone_number

    message.save()

    return (message, from_ph_is_new, from_usr_is_new, to_ph_is_new,\
        to_usr_is_new)

def save_message_medias(request, message):
    """Save media associated with message.

    Parameters
    ----------
    request
        HTTP request with full Twilio incoming message and medias
    message
        Reference to message model row for which we're saving medias for
    """
    if message.num_media.isnumeric():
        for i in range(int(message.num_media)):
            # Create TwilioInboundMessageMedia model
            media = models.TwilioInboundMessageMedia(
                content_type = request.data[f'MediaContentType{i}'],
                url = request.data[f'MediaUrl{i}'],
                message=message
            )
            media.save()

def save_message_log(request, message):
    """Saves Twilio incoming message as a new log model row from a HTTP request.
    
    Last updated: 17 May 2021, 5:38 PM

    Parameters
    ----------
    request
        Incoming message HTTP request
    message
        Message to log
    """
    try:
        log_payload = 'request.stream\n'
        log_payload += str(request.stream) + '\n\n'
        log_payload += 'request.content_type\n'
        log_payload += str(request.content_type) + '\n\n'
        log_payload += 'request.method\n'
        log_payload += str(request.method) + '\n\n'
        log_payload += 'request.query_params\n'
        log_payload += str(request.query_params) + '\n\n'
        log_payload += 'request.headers\n'
        log_payload += str(request.headers) + '\n\n'
        log_payload += 'request.data\n'
        log_payload += str(dict(request.data))
        log_message = models.TwilioInboundMessageLogEntry(
            payload=log_payload,
            message=message
        )
        log_message.save()
        return True
    except:
        return False

def reply(message, ph_is_new, usr_is_new):
    """Returns TwilML response to a Twilio incoming message model row reference.

    Last updated: 17 May 2021, 10:39 PM

    Parameters
    ----------
    message
        Incoming message model row reference
    """
    contexts = get_active_chat_contexts(message.from_user)

    if ph_is_new or usr_is_new:
        # User is new - register
        start_context(message.from_user, models.CHAT_CONTEXT__USER_REGISTRATION)
        body = render_to_string('chat/whats_your_name.txt', {})

    elif models.CHAT_CONTEXT__USER_REGISTRATION in contexts:
        # Save user's name
        message.from_user.name = message.body.strip()
        message.from_user.save()
        # Reply with menu (and set context)
        start_context(message.from_user, models.CHAT_CONTEXT__MENU)
        body = render_to_string('chat/menu.txt',
            {'name': message.from_user.name})
        # Stop user registration

    # Return TwilML response string
    response = MessagingResponse()
    response.message(body)
    return str(response)