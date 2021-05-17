import phonenumbers
from datetime import datetime
from twilio.twiml.messaging_response import MessagingResponse
from relationships import models as relmods
from . import models
from django.template.loader import render_to_string

def get_phone_number(raw_number):
    """
    Returns tuple with phone number model row reference and boolean to indicate
    if the phone number was created new. Create phone number if it does not
    already exist.

    Last updated: 17 May 2021, 11:10 PM

    Parameters
    ----------
    (phone_number, is_new)
        phone_number - reference to phone number model row; is_new - boolean:
        True if phone number did not exist before and was created new.
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
    """Returns tuple with user owning phone_number and boolean to indicate if
    the user was created new. Create user if he does not already exist.

    Last updated: 17 May 2021, 2:19 PM

    Parameters
    ----------
    phone_number
        Reference to user's phone number model row

    Returns
    -------
    (user, is_new)
        user - reference to user model row; is_new - boolean: True if user
        did not exist before and was created new.
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
    """Start context for user. Set started time of the UserChatContext model to
    now and stopped time to null.

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
        chat_context.started = datetime.now()
        chat_context.stopped = None
    except models.UserChatContext.DoesNotExist:
        # Create new context if it does not exist
        chat_context = models.UserChatContext(
            started=datetime.now(),
            user=user,
            context=context
        )

    chat_context.save()

def get_phone_number_string(twilio_phone_number):
    """Twilio's phone number follows this address scheme:

    <channel>:<e164 formatted phone number>

    Returns the phone number portion of a Twilio phone number.

    Parameters
    ----------
    twilio_phone_number
        Twilio phone number string
    """
    return twilio_phone_number.split(':')[-1]

def get_active_chat_contexts(user):
    """Returns all active contexts of user.

    Parameters
    ----------
    user
        User whose active contexts we're returning
    """
    return models.UserChatContext.objects.filter(
        user=user,
        stopped__isnull=True
    )

def reply(message):
    """Returns TwilML response to a Twilio incoming message model row reference.

    Last updated: 17 May 2021, 10:39 PM

    Parameters
    ----------
    message
        Incoming message model row reference
    """
    # Menu by default
    # 

    raw_number = get_phone_number_string(message.from_str)
    (phone_number, ph_is_new) = get_phone_number(raw_number)
    (user, usr_is_new) = get_user(phone_number)

    contexts = get_active_chat_contexts(user)

    if ph_is_new or usr_is_new:
        # User is new - register
        start_context(user, models.CHAT_CONTEXT__USER_REGISTRATION)
        body = render_to_string('chat/whats_your_name.txt', {})
    elif contexts.filter(context=models.CHAT_CONTEXT__USER_REGISTRATION)\
        .exists():
        # Save user's name
        user.name = message.body.strip()
        user.save()
        # Reply with menu
        start_context(user, models.CHAT_CONTEXT__MENU)
        body = render_to_string('chat/menu.txt', {'name': user.name})

    # Return TwilML response string
    response = MessagingResponse()
    response.message(body)
    return str(response)