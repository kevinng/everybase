import json, datetime, pytz
from operator import mod

from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.views.generic.list import ListView
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q

from everybase import settings
from leads import serializers, models, forms
from leads.libraries.utility_funcs.is_connected import is_connected
from leads.libraries.utility_funcs.has_contacted import has_contacted
from relationships.utilities.get_create_whatsapp_link import \
    get_create_whatsapp_link
from files import views as fiviews, models as fimods
from common import models as commods

class LeadListView(ListView):
    model = models.Lead
    paginate_by = 30

    def get_queryset(self, **kwargs):
        title = self.request.GET.get('title')
        details = self.request.GET.get('details')
        buying = self.request.GET.get('buying')
        selling = self.request.GET.get('selling')
        direct = self.request.GET.get('direct')
        broker = self.request.GET.get('broker')
        user_country = self.request.GET.get('user_country')
        lead_country = self.request.GET.get('lead_country')

        cpa__initial_deposit_received = self.request.GET.get(
            'cpa__initial_deposit_received')
        cpa__goods_shipped = self.request.GET.get('cpa__goods_shipped')
        cpa__buyer_received_goods_services = self.request.GET.get(
            'cpa__buyer_received_goods_services')
        cpa__full_payment_received = self.request.GET.get(
            'cpa__full_payment_received')
        cpa__others = self.request.GET.get('cpa__others')

        leads = models.Lead.objects.all()
        
        if title is not None:
            leads = leads.filter(title__icontains=title)

        if details is not None:
            leads = leads.filter(title__icontains=details)

        if buying is not None and selling is not None:
            pass # No need to filter
        elif buying is not None:
            leads = leads.filter(lead_type='buying')
        elif selling is not None:
            leads = leads.filter(lead_type='selling')

        if direct is not None and broker is not None:
            pass # No need to filter
        elif direct is not None:
            leads = leads.filter(author_type='direct')
        elif broker is not None:
            leads = leads.filter(author_type='broker')

        if user_country is not None and user_country.strip() != '':
            leads = leads.filter(author__country__programmatic_key=user_country)

        if lead_country is not None and lead_country.strip() != '':
            leads = leads.filter(country__programmatic_key=lead_country)

        commission_payable_after_q = Q()
        if cpa__initial_deposit_received is not None:
            commission_payable_after_q = commission_payable_after_q |\
                Q(commission_payable_after='initial_deposit_received')

        if cpa__goods_shipped is not None:
            commission_payable_after_q = commission_payable_after_q |\
                Q(commission_payable_after='goods_shipped')

        if cpa__buyer_received_goods_services is not None:
            commission_payable_after_q = commission_payable_after_q |\
                Q(commission_payable_after='buyer_received_goods_services')

        if cpa__full_payment_received is not None:
            commission_payable_after_q = commission_payable_after_q |\
                Q(commission_payable_after='full_payment_received')

        if cpa__others is not None:
            commission_payable_after_q = commission_payable_after_q |\
                Q(commission_payable_after='others')

        leads = leads.filter(commission_payable_after_q)
        
        return leads.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = commods.Country.objects.order_by('name')
        return context

def create_lead(request):
    if request.method == 'POST':
        form = forms.LeadForm(request.POST)
        if form.is_valid():
            lead = models.Lead.objects.create(
                author=request.user.user,
                title=form.cleaned_data.get('title'),
                details=form.cleaned_data.get('details'),
                lead_type=form.cleaned_data.get('lead_type'),
                author_type=form.cleaned_data.get('author_type'),
                country=commods.Country.objects.get(
                    programmatic_key=form.cleaned_data.get('country')),
                commission_pct=form.cleaned_data.get('commission_pct'),
                commission_payable_after=form.cleaned_data.\
                    get('commission_payable_after'),
                commission_payable_after_others=form.cleaned_data.\
                    get('commission_payable_after_others'),
                other_commission_details=form.cleaned_data.\
                    get('other_commission_details')
            )

            # Associate file with lead
            file_datas = json.loads(form.cleaned_data.get('files'))
            for file_data in file_datas:
                uuid, _, filename = file_data
                file = fimods.File.objects.get(uuid=uuid)
                file.lead = lead
                file.filename = filename
                file.save()
            
            messages.info(request, 'Your lead has been posted.')

            return HttpResponseRedirect(reverse('leads__root:list'))
    else:
        form = forms.LeadForm()

    countries = commods.Country.objects.order_by('name')

    return render(request, 'leads/create_lead.html', {
        'form': form,
        'countries': countries
    })

# @csrf_exempt
class WriteOnlyPresignedURLView(fiviews.WriteOnlyPresignedURLView):
    serializer_class = serializers.WriteOnlyPresignedURLSerializer

def lead_detail(request, uuid):
    try:
        lead = models.Lead.objects.get(uuid=uuid)
    except models.Lead.DoesNotExist:
        raise Http404('Lead does not exist')

    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            if is_connected(request.user.user, lead):
                # Users are already connected - direct to WhatsApp.

                # Set message as a GET parameter
                message = form.cleaned_data.get('message')
                request.GET._mutable = True
                request.GET['text'] = message

                # Direct user to WhatsApp with the message in body
                HttpResponseRedirect(
                    get_create_whatsapp_link(request.user.user, lead.author))
            elif not has_contacted(request.user.user, lead):
                # User should not be able to send a post request if he has
                # already contacted the lead owner. Users are not connected
                # and requester have not contacted this lead before.

                # Create contact request
                message = form.cleaned_data.get('message')
                contact_request = models.ContactRequest.objects.create(
                    contactor=request.user.user,
                    lead=lead,
                    message=message
                )

                # TODO: 
                # Contact lead author
                # tasks.contact_lead_author.delay(request.uuid)

                # Add message
                messages.info(request, "Message sent. We'll notify you if the \
author agrees to exchange contacts with you.")
    else:
        # Update analytics
        try:
            access = models.LeadDetailAccess.objects.get(
                lead=lead,
                accessor=request.user.user
            )
            access.access_count += 1
            access.save()
        except models.LeadDetailAccess.DoesNotExist:
            access = models.LeadDetailAccess.objects.create(
                lead=lead,
                accessor=request.user.user,
                access_count=1
            )

        if is_connected(request.user.user, lead):
            # Users are already connected, show an empty form which will allow
            # the requester to WhatsApp the lead author directly.
            contact_request = None
            form = forms.ContactForm()
        elif has_contacted(request.user.user, lead):
            # Users are not connected but requester have contacted this
            # lead before. Users are not connected but requester have contacted
            # this lead before.
        
            # Get contact request
            contact_request = models.ContactRequest.objects.get(
                contactor=request.user.user,
                lead=lead
            )

            # Show message from contact request
            form = forms.ContactForm({
                'message': contact_request.message
            })
        else:
            # User are not connected and requester have not contact lead author.
            # Show an empty form which will allow the requester to contact the
            # lead owner. Note: we do not merge this condition with is_connected
            # for clarity's sake.
            contact_request = None
            form = forms.ContactForm()

    return render(request, 'leads/lead_detail.html', {
        'lead': lead,
        'form': form,
        'contact_request': contact_request
    })

def contact_request_detail(request, uuid):
    if request.method == 'POST':
        # Allow user to approve the request

        # Whatsapp no need - because it will be a whatsapp URL
        pass
    else:
        pass

    return render(request, 'leads/contact_request_detail.html')

class ContactRequestListView(ListView):
    model = models.ContactRequest
    paginate_by = 30