import traceback
from django.http import HttpResponse
from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework import status

from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from . import models
from . import logics
from everybase.settings import (TWILIO_AUTH_TOKEN,
    TWILIO_WEBHOOK_INCOMING_MESSAGES_URL,
    TWILIO_WEBHOOK_STATUS_UPDATE_URL)

class TwilioIncomingMessageView(APIView):
    """Webhook to receiving incoming Twilio message via a POST request.

    Last updated: 15 May 2021, 12:50 PM
    """
    def post(self, request, format=None):
        signature = request.headers.get('X-Twilio-Signature')
        validator = RequestValidator(TWILIO_AUTH_TOKEN)
        if not validator.validate(TWILIO_WEBHOOK_INCOMING_MESSAGES_URL,
            request.data, signature):
            # Authentication failed
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

        try:
            num_media = request.data.get('NumMedia')
            from_str = request.data.get('From')

            # Create TwilioInboundMessage model
            message = models.TwilioInboundMessage(
                # Request Parameters
                api_version=request.data.get('ApiVersion'),
                message_sid=request.data.get('MessageSid'),
                sms_sid=request.data.get('SmsSid'),
                sms_message_sid=request.data.get('SmsMessageSid'),
                sms_status = request.data.get('SmsStatus'),
                account_sid=request.data.get('AccountSid'),
                from_str=from_str,
                to_str=request.data.get('To'),
                body=request.data.get('Body'),
                num_media=num_media,
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
            message.save()

            # Save message payload for audit and debugging
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

            # Read media content-type and URL if num_media is > 0
            if num_media.isnumeric():
                for i in range(int(num_media)):
                    # Create TwilioInboundMessageMedia model
                    media = models.TwilioInboundMessageMedia(
                        content_type = request.data[f'MediaContentType{i}'],
                        url = request.data[f'MediaUrl{i}'],
                        message=message
                    )
                    media.save()

            # print('hello')
            # print(logics.get_user(from_str))
            # print('world')

            # Formulate reply as a TwilML response
            # response = MessagingResponse()
            # msg = response.message('hello world')

            return HttpResponse(
                logics.get_twilml_response_string(from_str),
                status=HTTPStatus.OK,
            )

        except:
            traceback.print_exc()
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)
