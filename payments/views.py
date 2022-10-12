from email import message
from everybase import settings
from payments import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import stripe

# create fixtures for payment models

@require_http_methods(['POST'])
def create_checkout_session(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        if pid is None:
            # Price ID does not exist, redirect to pricing page with message
            messages.add_message(request, messages.INFO, 'An error occurred with checkout. Please contact Everybase support for assistance.')
            return HttpResponseRedirect(reverse('pricing'))
        
        try:
            price = models.StripePrice.objects.get(pk=pid)
        except models.StripePrice.DoesNotExist:
            # Stripe price model row not found, redirect to pricing page with message
            messages.add_message(request, messages.INFO, 'An error occurred with checkout. Please contact Everybase support for assistance.')
            return HttpResponseRedirect(reverse('pricing'))

        # Set Stripe API key
        stripe.api_key = settings.STRIPE_SECRET_API_KEY

        user = request.user.user

        try:
            cus = models.StripeCustomer.objects.get(user=user)
        except models.StripeCustomer.DoesNotExist:
            # User doesn't have a Stripe customer, create a new one.
            res = stripe.Customer.create(
                name=f'{user.first_name} {user.last_name}',
                email=user.email.email,
                phone=f'+{user.phone_number.country_code}{user.phone_number.national_number}'
            )
            cus = models.StripeCustomer.objects.create(
                user=user,
                api_id=res.id
            )

        # Create session
        session = stripe.checkout.Session.create(
            payment_method_types=settings.STRIPE_PAYMENT_METHOD_TYPES,
            customer=cus.api_id,
            line_items=[{
                'price': price.api_id,
                'quantity': 1
            }],
            mode='payment',
            success_url=end_url,
            cancel_url=end_url
        )