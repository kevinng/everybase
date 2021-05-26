import traceback
from django.http import HttpResponse
from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework import status

from chat import models
from chat.libraries import model_utils, context_utils, handler_context_map
from everybase.settings import (TWILIO_AUTH_TOKEN,
    TWILIO_WEBHOOK_INCOMING_MESSAGES_URL,
    TWILIO_WEBHOOK_STATUS_UPDATE_URL)

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
    handler = handler_context_map.get_handler(message, intent_key, message_key)

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
