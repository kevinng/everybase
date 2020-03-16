from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import (ProductsList, ProductsListAccessLogEntry, Lead,
    ProductsInterestsList, Product)

from .tasks import send_email

def get_client_ip(request):
    """
    Helper method to get the IP address of the client from the request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Heroku uses the last item. See: https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def products(request, products_list_id):
    # Get product list
    products_list = get_object_or_404(ProductsList, pk=products_list_id)
    context = {'products_list': products_list}

    if request.method == 'GET':
        # Log access entry
        ProductsListAccessLogEntry.objects.create(
            products_list=products_list,
            ip_address=get_client_ip(request),
            referrer=request.META.get('HTTP_REFERER'),
            user_agent=request.META.get('HTTP_USER_AGENT'),
        )

    elif request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        selected_products = request.POST.get('selected_products')

        products_list = ProductsList.objects.get(pk=products_list_id)

        # Create a new lead
        lead = Lead.objects.create(
            full_name=full_name,
            email=email
        )

        # Create new products interests list
        products_interest_list = ProductsInterestsList.objects.create(
            products_list=products_list,
            lead=lead
        )

        # Get and set interested products
        for product_str in selected_products.split(';'):
            if product_str.strip() != '':
                product = get_object_or_404(Product, pk=product_str)
                products_interest_list.products.add(product)
        products_interest_list.save()

        # Send an email to Everybase and the agent
        et_path = lambda template: 'products/email/' + template
        et_context = {
            'products_interest_list': products_interest_list
        }
        send_email.delay(
            render_to_string(et_path('enquiry_subject.txt')),
            render_to_string(et_path('enquiry.html'), et_context),
            'friend@everybase.co', # From email
            [products_list.agent.email, lead.email], # Recipients list
            html_message=render_to_string(et_path('enquiry.html'), et_context)
        )

        return HttpResponseRedirect(reverse('products:thanks'))

    return render(request, 'products/products.html', context)

def thanks(request):
    return render(request, 'products/thanks.html')
