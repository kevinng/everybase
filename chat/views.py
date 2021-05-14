from . import models
from django.http import HttpResponse
from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework import status
import traceback

class TwilioIncomingMessageView(APIView):
    """Webhook to receiving incoming Twilio message via a POST request.

    Last updated: 14 May 2021, 1:59 PM
    """
    def post(self, request, format=None):
        # TODO: Authenticate incoming request.

        try:
            num_media = request.data.get('NumMedia')

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

            # Read media content-type and URL if num_media is > 0
            if num_media.isnumeric():
                for i in range(int(num_media)):
                    # Create TwilioInboundMessageMedia model
                    media = models.TwilioInboundMessageMedia(
                        media_type = request.data[f'MediaContentType{i}'],
                        media_url = request.data[f'MediaUrl{i}'],
                        message=message
                    )
                    media.save()

            return HttpResponse(status=HTTPStatus.OK)

        except:
            traceback.print_exc()
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)
