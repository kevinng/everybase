import phonenumbers
from twilio.twiml.messaging_response import MessagingResponse
from relationships import models as relmods
from django.template.loader import render_to_string

def create_phone_number_if_not_exists(twilio_from_str):
    """Create phone number if it does not exists. Returns reference to phone
    number.

    Last updated: 15 May 2021, 10:37 PM

    Parameters
    ----------
    twilio_from_str
        From string from a Twilio's incoming message
    """
    raw_number = twilio_from_str.split(':')[-1]
    parsed_number = phonenumbers.parse(raw_number, None)

    try:
        # Find phone number
        number = relmods.PhoneNumber.objects.get(
            country_code=parsed_number.country_code,
            national_number=parsed_number.national_number
        )
    except relmods.PhoneNumber.DoesNotExist:
        # Create phone number if it doesn't exist
        number = relmods.PhoneNumber(
            country_code=parsed_number.country_code,
            national_number=parsed_number.national_number
        )
        number.save()

    return number

def get_user_with_phone_number(phone_number):
    """Returns tuple of reference to user with phone_number and boolean to
    indicate if the user was created new. Create user if he does not exist.

    Parameters
    ----------
    phone_number
        Reference to phone number for user we're looking for.

    Returns
    -------
    (user, created)
        user - reference to user; created - boolean, True if user did not exist
        before and was created new.
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

def get_twilml_response_string(twilio_from_str):
    """Returns TwilML response string to user.

    Last updated: 15 May 2021, 4:58 PM

    Parameters
    ----------
    twilio_from_str
        From string from a Twilio's incoming message
    """
    response = MessagingResponse()

    # Menu by default
    body = render_to_string('chat/menu.txt', {'name': 'to be filled'})

    phone_number = create_phone_number_if_not_exists(twilio_from_str)

    (user, created) = get_user_with_phone_number(phone_number)
    if created:
        # User does not exist - ask for his name
        body = render_to_string('chat/whats_your_name.txt', {})
        # TODO: set context CONTINUE FROM HERE
        # USER to be used to set context
    
    response.message(body)
    
    print(str(response))

    return str(response)
    