import traceback
from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
import sentry_sdk

from everybase.settings import (TWILIO_AUTH_TOKEN,
    TWILIO_WEBHOOK_INCOMING_MESSAGES_URL, STRIPE_PAYMENT_METHOD_TYPES,
    CHATBOT_PHONE_NUMBER_PK, STRIPE_PUBLISHABLE_API_KEY)

from common.libraries.get_ip_address import get_ip_address

from chat import models
from relationships import models as relmods
from payments import models as paymods

from chat.libraries.utility_funcs.save_message_log import save_message_log
from chat.libraries.utility_funcs.save_message_medias import save_message_medias
from chat.libraries.utility_funcs.save_message import save_message
from chat.libraries.utility_funcs.get_context import get_context
from chat.libraries.utility_funcs.get_handler import get_handler
from chat.libraries.utility_funcs.get_non_tracking_whatsapp_link import \
    get_non_tracking_whatsapp_link

from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

import stripe

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
    intent_key, message_key = get_context(message.from_user)
    
    # Get handler for context
    handler = get_handler(message, intent_key, message_key)

    # Run handler and get message body
    body = handler.run()

    # Capture error - if any
    if body is None:
        sentry_sdk.capture_message('Handler %s %s for message %d failed' %
            (intent_key, message_key, message.id), 'fatal')

    # Log
    models.TwilioOutboundMessage.objects.create(
        intent_key=intent_key,
        message_key=message_key,
        body=body,
        to_user=message.from_user,
        to_phone_number=message.from_phone_number,
        twilml_response_to=message
    )

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
            message, _, _, _, _ = save_message(request)
            save_message_log(request, message)
            save_message_medias(request, message)

            return HttpResponse(
                reply(message),
                status=HTTPStatus.OK,
            )

        except:
            traceback.print_exc()
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)

def redirect_whatsapp_phone_number(request, id):
    """Redirects user from our short tracking URL to WhatsApp"""
    # Log access
    ua = request.user_agent
    access = relmods.PhoneNumberLinkAccess.objects.create(
        ip_address=get_ip_address(request),
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
        device_family=ua.device.family
    )

    try:
        hash = relmods.PhoneNumberHash.objects.get(
            pk=id,
            expired__isnull=False
        )
        access.hash = hash
        access.save()
    except relmods.PhoneNumberHash.DoesNotExist as err:
        sentry_sdk.capture_exception(err)

        # Update log status
        access.outcome = relmods.PHONE_NUMBER_ACCESS_FAILED
        access.save()

        return render(request, 'chat/pages/error.html', {})

    # Note: we use temporary redirects so search engines do not associate our
    # URLs with WhatsApp phone number links
    response = HttpResponse(status=302) # Temporary redirect
    response['Location'] = get_non_tracking_whatsapp_link(
        hash.phone_number.country_code,
        hash.phone_number.national_number)
    
    # Update log status
    access.outcome = relmods.PHONE_NUMBER_ACCESS_SUCCESSFUL
    access.save()

    return response

def redirect_checkout_page(request, id):
    """Redirect user to the Stripe checkout page"""
    # Log access
    ua = request.user_agent
    access = paymods.PaymentLinkAccess.objects.create(
        ip_address=get_ip_address(request),
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
        device_family=ua.device.family
    )

    try:
        hash = paymods.PaymentHash.objects.get(pk=id)
        access.hash = hash
        access.save()

        if hash.expired is not None:
            return render(request, 'chat/pages/expired.html', {})
    except paymods.PaymentHash.DoesNotExist as err:
        sentry_sdk.capture_exception(err)

        # Update log status
        access.outcome = paymods.PAYMENT_LINK_ACCESS_FAILED
        access.save()

        return render(request, 'chat/pages/error.html', {})

    # Chatbot phone number - for success/cancel URL
    chatbot_ph = relmods.PhoneNumber.objects.get(pk=CHATBOT_PHONE_NUMBER_PK)
    end_url = get_non_tracking_whatsapp_link(
        chatbot_ph.country_code,
        chatbot_ph.national_number)

    # Create session
    session = stripe.checkout.Session.create(
        payment_method_types=STRIPE_PAYMENT_METHOD_TYPES,
        line_items=[{
            'price_data': {
                'currency': hash.currency.programmatic_key,
                'product_data': { 'name': hash.product_name },
                'unit_amount': hash.unit_amount
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=end_url,
        cancel_url=end_url,
    )

    # Update log status
    access.outcome = paymods.PAYMENT_LINK_ACCESS_SUCCESSFUL
    access.save()

    context = {
        'session_id': session.id,
        'stripe_publishable_api_key': STRIPE_PUBLISHABLE_API_KEY
    }

    return render(request, 'chat/pages/checkout.html', context)

class StripeFulfilmentCallbackView(APIView):
    """Webhook to receive Stripe fuilfilment callback."""
    # TODO