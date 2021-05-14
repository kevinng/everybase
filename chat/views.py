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
            num_media = request.data['NumMedia']

            # Create TwilioInboundMessage model
            message = models.TwilioOutboundMessage(
                # Request Parameters
                api_version=request.data['ApiVersion'],
                message_sid=request.data['MessageSid'],
                sms_sid=request.data['SmsSid'],
                sms_message_sid=request.data['SmsMessageSid'],
                sms_status = request.data['SmsStatus'],
                account_sid=request.data['AccountSid'],
                from_str=request.data['From'],
                to_str=request.data['To'],
                body=request.data['Body'],
                num_media=num_media,
                num_segments=request.data['NumSegments'],

                # Geographic Data-related Parameters
                from_city=request.data['FromCity'],
                from_state=request.data['FromState'],
                from_zip=request.data['FromZip'],
                from_country=request.data['FromCountry'],
                to_city=request.data['ToCity'],
                to_state=request.data['ToState'],
                to_zip=request.data['ToZip'],
                to_country=request.data['ToCountry'],

                # WhatsApp-specific Parameters
                profile_name=request.data['ProfileName'],
                wa_id=request.data['WaId'],
                forwarded=request.data['Forwarded'],
                frequently_forwarded=request.data['FrequentlyForwarded'],

                # WhatsApp Location Sharing Parameters
                latitude=request.data['Latitude'],
                longitude=request.data['Longitude'],
                address=request.data['Address'],
                label=request.data['Label']
            )
            message.save()

            # Read media content-type and URL if num_media is > 0
            if num_media.is_numeric():
                for i in range(int(num_media)):
                    # Create TwilioInboundMessageMedia model
                    models.TwilioInboundMessageMedia(
                        media_type = request.data[f'MediaContentType{i}'],
                        media_url = request.data[f'MediaUrl{i}'],
                        message=message
                    ).save()

            return HttpResponse(status=HTTPStatus.OK)

        except:
            traceback.print_exc()
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)
