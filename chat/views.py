import traceback
from http import HTTPStatus
from urllib.parse import urljoin

from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

from everybase import settings
from chat import models
from chat.utilities import (save_message_log, save_message_medias, save_message,
    get_context, get_handler, save_status_callback, save_status_callback_log)
from chat.tasks.copy_post_request_data import copy_post_request_data
from relationships import models as relmods
from relationships.utilities import get_non_tracking_whatsapp_link

from amplitude.tasks.send_event import send_event
from amplitude.constants import event

from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
import sentry_sdk

def reply(message, no_external_calls=False, no_task_calls=False, request=None):
    """Returns TwilML response to a Twilio incoming message model row reference.
    This function ascertains the best reply for the user and replies the user.

    Parameters
    ----------
    message
        Incoming message model row reference. Message must have valid users and
        phone numbers - i.e., they must have been created if this is the first
        message sent by the user.
    no_external_calls
        If True, will not make external calls.
    no_task_calls
        If True, will not make background task calls.
    request
        HttpRequest that initiated this function call.
    """

    # Get user's context
    intent_key, message_key = get_context(message.from_user)
    
    # Get handler for context
    handler = get_handler(message, intent_key, message_key, no_external_calls,
        no_task_calls, request)

    # Run handler and get message body
    body = handler.run()

    # Capture error - if any
    if body is None:
        sentry_sdk.capture_message('Handler %s %s for message %d failed' %
            (intent_key, message_key, message.id), 'fatal')

    # Log
    msg = models.TwilioOutboundMessage.objects.create(
        intent_key=intent_key,
        message_key=message_key,
        body=body,
        to_user=message.from_user,
        to_phone_number=message.from_phone_number,
        twilml_response_to=message
    )

    # Return TwilML response string
    status_callback_url = urljoin(settings.BASE_URL,
        reverse('chat:status_update_message', kwargs={ 'msg_id': msg.id }))
    response = MessagingResponse()
    response.message(
        body=body,
        action=status_callback_url,
        status_callback=status_callback_url,
        method='POST'
    )
    return str(response)

class TwilioIncomingMessageView(APIView):
    """Webhook to receiving incoming Twilio message via a POST request."""
    def post(self, request):
        # Copy post to Missive
        copy_post_request_data.delay(
            settings.MISSIVE_TWILIO_WA_CALLBACK_URL,
            request.data
        )

        signature = request.headers.get('X-Twilio-Signature')
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
        if not validator.validate(settings.TWILIO_WEBHOOK_INCOMING_MESSAGES_URL,
            request.data, signature):
            # Authentication failed
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

        try:
            message, _, _, _, _ = save_message(request)
            save_message_log(request, message)
            save_message_medias(request, message)

            return HttpResponse(
                reply(message, request=request),
                status=HTTPStatus.OK,
            )

        except:
            traceback.print_exc()
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)

class TwilioIncomingStatusView(APIView):
    """Webhook to receiving incoming Twilio status via a POST request."""
    def post(self, request, msg_id=None):
        # Copy post to Missive
        copy_post_request_data.delay(
            settings.MISSIVE_TWILIO_WA_CALLBACK_URL,
            request.data
        )

        signature = request.headers.get('X-Twilio-Signature')
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

        if msg_id is None:
            # Validate for the general URL - this status update is for a message
            # we sent our explicitly, so we have its Twilio message SID at the
            # time of sending.
            this_url = settings.TWILIO_WEBHOOK_STATUS_UPDATE_URL
        else:
            # Validate for the message-specific URL - this status update is for
            # a reply which uses TwilML. Because we use TwilML, we do not have
            # the Twilio message SID at the point of reply, so we must link it
            # to our message ID.
            this_url = urljoin(settings.BASE_URL,
                reverse('chat:status_update_message',
                kwargs={ 'msg_id': msg_id }
            ))

        if not validator.validate(this_url, request.data, signature):
            # Authentication failed
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

        try:
            callback = save_status_callback(request, msg_id)
            save_status_callback_log(request, callback)

            return HttpResponse(status=HTTPStatus.OK)
        except:
            traceback.print_exc()
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)

def redirect_whatsapp_phone_number(request, id):
    """Redirects user from our short tracking URL to WhatsApp"""

    try:
        hash = relmods.PhoneNumberHash.objects.get(pk=id)
    except relmods.PhoneNumberHash.DoesNotExist as err:
        sentry_sdk.capture_exception(err)
        # TODO: move this file back in, and use rendered paths
        return render(request, 'chat/pages/error.html', {})
    
    # TODO: we need to update this call
    # Make Amplitude call
    # send_event.delay(
    #     user_id=hash.user.id,
    #     event_type=events.CLICKED_WHATSAPP_LINK,
    #     user_properties={
    #         keys.COUNTRY_CODE: hash.user.phone_number.country_code
    #     },
    #     # app_version=settings.APP_VERSION
    # )

    # Note: we use temporary redirects so search engines do not associate our
    # URLs with WhatsApp phone number links
    response = HttpResponse(status=302) # Temporary redirect
    response['Location'] = get_non_tracking_whatsapp_link(
        hash.phone_number.country_code,
        hash.phone_number.national_number,
        request.GET.get('text')
    )

    return response