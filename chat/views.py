import traceback
from django.http import HttpResponse
from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework import status

from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from . import models
from .libraries import chat
from everybase.settings import (TWILIO_AUTH_TOKEN,
    TWILIO_WEBHOOK_INCOMING_MESSAGES_URL,
    TWILIO_WEBHOOK_STATUS_UPDATE_URL)

class TwilioIncomingMessageView(APIView):
    """Webhook to receiving incoming Twilio message via a POST request.

    Last updated: 17 May 2021, 7:27 PM
    """
    def post(self, request, format=None):
        signature = request.headers.get('X-Twilio-Signature')
        validator = RequestValidator(TWILIO_AUTH_TOKEN)
        if not validator.validate(TWILIO_WEBHOOK_INCOMING_MESSAGES_URL,
            request.data, signature):
            # Authentication failed
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

        try:
            (message, ph_is_new, usr_is_new, _, _) = \
                chat.save_message(request)
            chat.save_message_log(request, message)
            chat.save_message_medias(request, message)

            return HttpResponse(
                chat.reply(message, ph_is_new, usr_is_new),
                status=HTTPStatus.OK,
            )

        except:
            traceback.print_exc()
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)
