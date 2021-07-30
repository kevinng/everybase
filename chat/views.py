import traceback, pytz, datetime
from http import HTTPStatus
from urllib.parse import urljoin

from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

from everybase import settings

from chat import models
from relationships import models as relmods
from payments import models as paymods

from common.libraries.get_ip_address import get_ip_address
from chat.libraries.utility_funcs.save_message_log import save_message_log
from chat.libraries.utility_funcs.save_message_medias import save_message_medias
from chat.libraries.utility_funcs.save_message import save_message
from chat.libraries.utility_funcs.get_context import get_context
from chat.libraries.utility_funcs.get_handler import get_handler
from chat.libraries.utility_funcs.get_non_tracking_whatsapp_link import \
    get_non_tracking_whatsapp_link
from chat.libraries.utility_funcs.save_status_callback import \
    save_status_callback
from chat.libraries.utility_funcs.save_status_callback_log import \
    save_status_callback_log
from chat.libraries.utility_funcs.get_support_phone_number import \
    get_support_phone_number

from chat.tasks.send_confirm_interests import send_confirm_interests
from chat.tasks.exchange_contacts import exchange_contacts
from chat.tasks.copy_post_request_data import copy_post_request_data

from amplitude.tasks.send_event import send_event
from amplitude.constants import events, keys

from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
import stripe, sentry_sdk

def reply(message, no_external_calls=False, no_task_calls=False):
    """Returns TwilML response to a Twilio incoming message model row reference.
    This function ascertains the best reply for the user and replies the user.

    Parameters
    ----------
    message
        Incoming message model row reference. Message must have valid users and
        phone numbers - i.e., they must have been created if this is the first
        message sent by the user.
    no_external_calls
        If True, will not make external calls. Enabled for testing purposes.
    """

    # Get user's context
    intent_key, message_key = get_context(message.from_user)
    
    # Get handler for context
    handler = get_handler(message, intent_key, message_key, no_external_calls,
        no_task_calls)

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
                reply(message),
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
    # Log access
    ua = request.user_agent
    access = relmods.PhoneNumberLinkAccess(
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
        hash = relmods.PhoneNumberHash.objects.get(pk=id)
        access.hash = hash
        access.save()
    except relmods.PhoneNumberHash.DoesNotExist as err:
        sentry_sdk.capture_exception(err)

        # Update log status
        access.outcome = relmods.PHONE_NUMBER_ACCESS_FAILED
        access.save()

        return render(request, 'chat/pages/error.html', {})

    # Make Amplitude call
    send_event.delay(
        user_id=hash.user.id,
        event_type=events.CLICKED_WHATSAPP_LINK,
        user_properties={
            keys.COUNTRY_CODE: hash.user.phone_number.country_code
        },
        app_version=settings.APP_VERSION
    )

    # Note: we use temporary redirects so search engines do not associate our
    # URLs with WhatsApp phone number links
    response = HttpResponse(status=302) # Temporary redirect
    response['Location'] = get_non_tracking_whatsapp_link(
        hash.phone_number.country_code,
        hash.phone_number.national_number
    )
    
    # Update log status
    access.outcome = relmods.PHONE_NUMBER_ACCESS_SUCCESSFUL
    access.save()

    return response

def redirect_checkout_page(request, id):
    """Redirect user to the Stripe checkout page"""
    # Log access
    ua = request.user_agent
    access = paymods.PaymentLinkAccess(
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

        sph = get_support_phone_number()
        params = { 'whatsapp_url': get_non_tracking_whatsapp_link(
            sph.country_code, sph.national_number) }

        # Make Amplitude call
        send_event.delay(
            user_id=hash.user.id,
            event_type=events.CLICKED_PAYMENT_LINK,
            user_properties={
                keys.COUNTRY_CODE: hash.user.phone_number.country_code
            },
            app_version=settings.APP_VERSION
        )

        if hash.expired is not None:
            return render(request, 'chat/pages/expired.html', params)
        elif hash.price is None:
            return render(request, 'chat/pages/error.html', params)
        elif hash.succeeded is not None:
            return render(request, 'chat/pages/paid.html', params)

    except paymods.PaymentHash.DoesNotExist as err:
        sentry_sdk.capture_exception(err)

        # Update log status
        access.outcome = paymods.PAYMENT_LINK_ACCESS_FAILED
        access.save()

        return render(request, 'chat/pages/error.html', {})

    # Chatbot phone number - for success/cancel URL
    chatbot_ph = relmods.PhoneNumber.objects.get(
        pk=settings.CHATBOT_PHONE_NUMBER_PK)
    end_url = get_non_tracking_whatsapp_link(
        chatbot_ph.country_code,
        chatbot_ph.national_number)

    # Create session
    session = stripe.checkout.Session.create(
        payment_method_types=settings.STRIPE_PAYMENT_METHOD_TYPES,
        line_items=[{
            'price': hash.price.programmatic_key,
            'quantity': 1
        }],
        mode='payment',
        success_url=end_url,
        cancel_url=end_url,
        api_key = settings.STRIPE_SECRET_API_KEY
    )

    # Update hash
    sgtz = pytz.timezone(settings.TIME_ZONE)
    hash.started = datetime.datetime.now(tz=sgtz)
    hash.session_id = session.id
    hash.save()

    # Update log status
    access.outcome = paymods.PAYMENT_LINK_ACCESS_SUCCESSFUL
    access.save()

    context = {
        'session_id': session.id,
        'stripe_publishable_api_key': settings.STRIPE_PUBLISHABLE_API_KEY
    }

    return render(request, 'chat/pages/checkout.html', context)

class StripeFulfilmentCallbackView(APIView):
    """Webhook to receive Stripe fuilfilment callback."""
    def post(self, request):

        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            s = event['data']['object']
            cd = s.get('customer_details')
            session = paymods.StripeCallbackCheckoutSession.objects.create(
                session_id=s.get('id'),
                amount_total=s.get('amount_total'),
                currency=s.get('currency'),
                customer=s.get('customer'),
                customer_details_email=cd.get('email') if cd is not None else None,
                mode=s.get('mode'),
                payment_intent=s.get('payment_intent'),
                payment_status=s.get('payment_status'),
                success_url=s.get('success_url'),
                cancel_url=s.get('cancel_url')
            )

            try:
                hash = paymods.PaymentHash.objects.get(
                    session_id=session.session_id)
            except Exception as e:
                sentry_sdk.capture_exception(e)

            sgtz = pytz.timezone(settings.TIME_ZONE)
            now = datetime.datetime.now(tz=sgtz)

            if session.payment_status == \
                paymods.StripeCallbackCheckoutSession_Paid:
                hash.succeeded = now
                match = hash.match

                # Make Amplitude call
                send_event.delay(
                    user_id=hash.user.id,
                    event_type=events.PAID,
                    user_properties={
                        keys.COUNTRY_CODE: hash.user.phone_number.country_code
                    },
                    app_version=settings.APP_VERSION,
                    product_id=hash.price.id,
                    revenue=hash.price.value
                )

                # Fulfill order
                exchange_contacts.delay(match.id)

                # Update match
                if hash.user.id == match.supply.user.id:
                    # Seller paid
                    match.seller_bought_contact = now
                    match.seller_payment_hash = hash
                else:
                    # Buyer paid
                    match.buyer_bought_contact = now
                    match.buyer_payment_hash = hash

                match.save()
            elif session.payment_status == \
                paymods.StripeCallbackCheckoutSession_Unpaid:
                hash.failed = now

            hash.save()

        # Passed signature verification
        return HttpResponse(status=200)

class SendConfirmInterestsView(APIView):
    """API to send confirm interest messages"""
    def post(self, request):
        match_id = request.data.get('match_id')
        
        if match_id is None:
            return HttpResponse('match_id is None',
                status=HTTPStatus.BAD_REQUEST)

        send_confirm_interests.delay(
            match_id=match_id,
            buyer_only=request.data.get('buyer_only'),
            seller_only=request.data.get('seller_only'),
            no_external_calls=request.data.get('no_external_calls')
        )

        return HttpResponse('Done', status=HTTPStatus.OK)