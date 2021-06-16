import traceback
from django.http import HttpResponse
from http import HTTPStatus
from rest_framework.views import APIView

from everybase.settings import (TWILIO_AUTH_TOKEN,
    TWILIO_WEBHOOK_INCOMING_MESSAGES_URL, EVERYBASE_WA_NUMBER_COUNTRY_CODE,
    EVERYBASE_WA_NUMBER_NATIONAL_NUMBER)
from chat.libraries import model_utils, context_utils
from chat.handlers.get_handler import get_handler
from relationships import models as relmods

from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

def reply(message):
    """Returns TwilML response to a Twilio incoming message model row reference.
    This function ascertains the best reply for the user and replies the user.

    Parameters
    ----------
    message
        Incoming message model row reference. Message must have valid users and
        phone numbers - i.e., they must have been created if this is the first
        message sent by the user.
    """

    # Get user's context
    intent_key, message_key = context_utils.get_context(message.from_user)
    
    # Get handler for context
    handler = get_handler(message, intent_key, message_key)

    # Run handler and get message body
    body = handler.run()

    # Return TwilML response string
    response = MessagingResponse()
    response.message(body)
    return str(response)

class TwilioIncomingMessageView(APIView):
    """Webhook to receiving incoming Twilio message via a POST request."""
    def post(self, request, format=None):
        signature = request.headers.get('X-Twilio-Signature')
        validator = RequestValidator(TWILIO_AUTH_TOKEN)
        if not validator.validate(TWILIO_WEBHOOK_INCOMING_MESSAGES_URL,
            request.data, signature):
            # Authentication failed
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

        try:
            message, _, _, _, _ = model_utils.save_message(request)
            model_utils.save_message_log(request, message)
            model_utils.save_message_medias(request, message)

            return HttpResponse(
                reply(message),
                status=HTTPStatus.OK,
            )

        except:
            traceback.print_exc()
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)

def redirect_whatsapp_phone_number(request, id):
    # Note: we use temporary redirects so search engines do not associate our
    # URLs with WhatsApp phone number links
    response = HttpResponse(status=302) # Temporary redirect

    try:
        hash = relmods.PhoneNumberHash.objects.get(pk=id)
    except relmods.PhoneNumberHash.DoesNotExist:
        traceback.print_exc()
        # Direct the user to my phone number, so I'll know if the URL is bad
        response['Location'] = 'https://wa.me/' + \
            EVERYBASE_WA_NUMBER_COUNTRY_CODE + \
            EVERYBASE_WA_NUMBER_NATIONAL_NUMBER
        return response

    # Get user IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    # Log access
    ua = request.user_agent
    relmods.PhoneNumberURLAccess.objects.create(
        ip_address=ip_address,
        is_mobile=ua.is_mobile,
        is_tablet=ua.is_tablet,
        is_touch_capable=ua.is_touch_capable,
        is_pc=ua.is_pc,
        is_bot=ua.is_bot,
        browser=ua.browser,
        browser_family=ua.browser.family,
        browser_version=ua.browser.version,
        browser_version_string=ua.browser.version_string,
        os=ua.os,
        os_family=ua.os.family,
        os_version=ua.os.version,
        os_version_string=ua.os.version_string,
        device=ua.device,
        device_family=ua.device.family,
        hash=hash
    )

    response['Location'] = 'https://wa.me/' + hash.phone_number.country_code + \
        hash.phone_number.national_number
    return response