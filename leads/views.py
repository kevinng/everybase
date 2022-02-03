from datetime import datetime
import json, requests, pytz, traceback

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, \
    SearchRank, SearchVectorField
from django.db.models import Q, Count
from django.db.models.expressions import RawSQL
from django.template.response import TemplateResponse

from everybase import settings
from common import models as commods
from files import views as fiviews, models as fimods
from leads import serializers, models, forms
from leads.utilities.is_connected import is_connected
from leads.utilities.has_contacted import has_contacted
from relationships.utilities.get_create_whatsapp_link import \
    get_create_whatsapp_link
from chat.tasks.send_contact_request_confirm import send_contact_request_confirm
from chat.tasks.send_contact_request_exchanged_author import \
    send_contact_request_exchanged_author
from chat.tasks.send_contact_request_exchanged_contactor import \
    send_contact_request_exchanged_contactor
from relationships import models as relmods
from relationships.utilities.save_user_agent import save_user_agent

# def i_need_agent_detail(request, pk):
#     template_name = 'leads/i_need_agent_detail.html'
#     context = {}
#     print(pk)
#     return TemplateResponse(request, template_name, context)

# def i_need_agent_edit(request, pk):
#     template_name = 'leads/lead_edit.html'
#     context = {}
#     print(pk)
#     return TemplateResponse(request, template_name, context)

def i_need_agent_author_list(request, user_pk):
    pass

class LeadEdit(UpdateView):
    template_name = 'leads/lead_edit.html'
    model = models.Lead
    fields = ['lead_type', 'buy_country', 'sell_country', 'avg_deal_size',
        'avg_comm_pct', 'details', 'other_commission_details']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = commods.Country.objects.annotate(
            number_of_users=Count('users_w_this_country'))\
            .order_by('-number_of_users')

        return context

    def get_success_url(self):
        return reverse('leads:lead_detail', args=(self.object.id,))

class LeadDetail(DetailView):
    template_name = 'leads/lead_detail.html'
    model = models.Lead

@login_required
def lead_create(request):
    countries = commods.Country.objects.annotate(
        number_of_users=Count('users_w_this_country'))\
            .order_by('-number_of_users')

    if request.method == 'POST':
        form = forms.INeedAgentForm(request.POST)
        if form.is_valid():
            buy_country_str = form.cleaned_data.get('buy_country')
            buy_country = None
            if buy_country_str != 'any_country':
                buy_country = commods.Country.objects.get(
                    programmatic_key=buy_country_str)

            sell_country_str = form.cleaned_data.get('sell_country')
            sell_country = None
            if sell_country_str != 'any_country':
                sell_country = commods.Country.objects.get(
                    programmatic_key=sell_country_str)

            lead = models.Lead.objects.create(
                author=request.user.user,
                lead_type=form.cleaned_data.get('lead_type'),
                buy_country=buy_country,
                sell_country=sell_country,
                avg_deal_size=form.cleaned_data.get('avg_deal_size'),
                avg_comm_pct=form.cleaned_data.get('avg_comm_pct'),
                details=form.cleaned_data.get('details'),
                other_commission_details=form.cleaned_data.get(
                    'other_comm_details')
            )

            if request.user.is_authenticated:
                user = request.user.user
            else:
                user = None

            save_user_agent(request, user)

            return HttpResponseRedirect(
                reverse('leads__root:i_need_agent_detail', args=(lead.id,)))
    else:
        form = forms.INeedAgentForm()

    return render(request, 'leads/lead_create.html', {
        'form': form,
        'countries': countries
    })

class LeadListView(ListView):
    template_name = 'leads/lead_list.html'
    model = relmods.Lead
    paginate_by = 8

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search')
        wants_to = self.request.GET.get('wants_to')
        buy_country = self.request.GET.get('buy_country')
        sell_country = self.request.GET.get('sell_country')
        sort_by = self.request.GET.get('sort_by')

        leads = relmods.Lead.objects

        if wants_to == 'buy':
            leads = leads.filter(lead_type='buying')
        elif wants_to == 'sell':
            leads = leads.filter(lead_type='selling')

        if buy_country != 'any_country':
            leads = leads.filter(buy_country=buy_country)

        if sell_country != 'any_country':
            leads = leads.filter(sell_country=sell_country)

        vector = SearchVector('search_i_need_agents_veccol')
        query = SearchQuery(search)
        leads = leads.annotate(
            search_i_need_agents_veccol=RawSQL(
                'search_i_need_agents_veccol', [],
                output_field=SearchVectorField()))\
            .annotate(rank=SearchRank(vector, query))\
            .order_by('-rank')
        
        if sort_by == 'comm_percent_hi_lo':
            leads = leads.order_by('-avg_comm_pct')
        elif sort_by == 'comm_percent_lo_hi':
            leads = leads.order_by('avg_comm_pct')
        elif sort_by == 'comm_dollar_hi_lo':
            leads = leads.order_by('-avg_deal_comm')
        elif sort_by == 'comm_dollar_lo_hi':
            leads = leads.order_by('avg_deal_comm')
        else:
            leads = leads.order_by('-rank')

        # Save query
        if self.request.user.is_authenticated:
            user = self.request.user.user
        else:
            user = None

        q = models.INeedAgentQuery()
        q.user=user
        q.search=search
        if wants_to is None or wants_to.strip() == '':
            wants_to = 'buy_or_sell'
        q.wants_to=wants_to
        if buy_country != 'any_country' and buy_country != None and \
            buy_country.strip() != '':
            q.buy_country=commods.Country.objects.get(
                programmatic_key=buy_country)
        if sell_country != 'any_country' and sell_country != None and \
            sell_country.strip() != '':
            q.sell_country=commods.Country.objects.get(
                programmatic_key=sell_country)
        q.sort_by=sort_by
        q.save()

        save_user_agent(self.request, user)

        return leads

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = commods.Country.objects.annotate(
            number_of_users=Count('users_w_this_country'))\
            .order_by('-number_of_users')

        # Render search and country back into the template
        context['search_value'] = self.request.GET.get('search')
        context['wants_to_value'] = self.request.GET.get('wants_to')
        context['buy_country_value'] = self.request.GET.get('buy_country')
        context['sell_country_value'] = self.request.GET.get('sell_country')
        context['sort_by_value'] = self.request.GET.get('sort_by')

        return context

class AgentListView(ListView):
    template_name = 'leads/agent_list.html'
    model = relmods.User
    paginate_by = 8

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search')
        country = self.request.GET.get('country')

        users = relmods.User.objects
        if country is not None and country != 'any_country':
            users = users.filter(country__programmatic_key=country)

        # Save query
        try:
            if self.request.user.is_authenticated:
                user = self.request.user.user
            else:
                user = None

            if country == 'any_country' or country is None:
                country_model = None
            else:
                country_model = commods.Country.objects.get(
                    programmatic_key=country)
                
            if user is not None and search is not None and country is not None:
                models.AgentQuery.objects.create(
                    user=user,
                    search=search,
                    country=country_model
                )
        except:
            traceback.print_exc()

        vector = SearchVector('search_agents_veccol')
        query = SearchQuery(search)
        users = users.annotate(
            search_agents_veccol=RawSQL('search_agents_veccol', [],
                output_field=SearchVectorField()))\
            .annotate(rank=SearchRank(vector, query))\
            .order_by('-rank')
            
        return users
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = commods.Country.objects.annotate(
            number_of_users=Count('users_w_this_country'))\
            .order_by('-number_of_users')

        # Render search and country back into the template
        context['search_value'] = self.request.GET.get('search')
        context['country_value'] = self.request.GET.get('country')

        return context

class LeadListView(ListView):
    model = models.Lead
    paginate_by = 54

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

        ffp = models.FilterFormPost()

        if title is not None:
            leads = leads.filter(title__icontains=title)
            ffp.title = title

        if details is not None:
            leads = leads.filter(title__icontains=details)
            ffp.details = details

        if buying is not None and selling is not None:
            pass # No need to filter
        elif buying is not None:
            leads = leads.filter(lead_type='buying')
            ffp.is_buying = True
        elif selling is not None:
            leads = leads.filter(lead_type='selling')
            ffp.is_selling = True

        if direct is not None and broker is not None:
            pass # No need to filter
        elif direct is not None:
            leads = leads.filter(author_type='direct')
            ffp.is_direct = True
        elif broker is not None:
            leads = leads.filter(author_type='broker')
            ffp.is_agent = True

        if user_country is not None and user_country.strip() != '':
            leads = leads.filter(author__country__programmatic_key=user_country)
            ffp.user_country = user_country

        if lead_country is not None and lead_country.strip() != '':
            leads = leads.filter(country__programmatic_key=lead_country)
            ffp.lead_country = lead_country

        commission_payable_after_q = Q()
        if cpa__initial_deposit_received is not None:
            commission_payable_after_q = commission_payable_after_q |\
                Q(commission_payable_after='initial_deposit_received')
            ffp.is_initial_deposit = True

        if cpa__goods_shipped is not None:
            commission_payable_after_q = commission_payable_after_q |\
                Q(commission_payable_after='goods_shipped')
            ffp.is_goods_shipped = True

        if cpa__buyer_received_goods_services is not None:
            commission_payable_after_q = commission_payable_after_q |\
                Q(commission_payable_after='buyer_received_goods_services')
            ffp.is_goods_received = True

        if cpa__full_payment_received is not None:
            commission_payable_after_q = commission_payable_after_q |\
                Q(commission_payable_after='full_payment_received')
            ffp.is_payment_received = True

        if cpa__others is not None:
            commission_payable_after_q = commission_payable_after_q |\
                Q(commission_payable_after='others')
            ffp.is_others = True

        leads = leads.filter(commission_payable_after_q)

        if self.request.user.is_authenticated:
            try:
                ffp.user = self.request.user.user
            except relmods.User.DoesNotExist:
                # Prevents error when I'm logging in as admin
                pass
        
        ffp.save()
        
        return leads.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = commods.Country.objects.order_by('name')
        context['amplitude_api_key'] = settings.AMPLITUDE_API_KEY
        if self.request.user.is_authenticated:
            try:
                eb_user = self.request.user.user
                context['amplitude_user_id'] = eb_user.uuid
                context['country_code'] = eb_user.phone_number.country_code
                context['register_date_time'] = eb_user.registered.isoformat()
                sgtz = pytz.timezone(settings.TIME_ZONE)
                context['last_seen_date_time'] = datetime.now(tz=sgtz).isoformat()
                context['num_whatsapp_lead_author'] = \
                    eb_user.num_whatsapp_lead_author()
                context['num_leads_created'] = eb_user.num_leads_created()
            except relmods.User.DoesNotExist:
                # Prevents error when I'm logging in as admin
                pass

        return context

@login_required
def create_lead(request):
    if request.method == 'POST':
        form = forms.LeadForm(request.POST)
        if form.is_valid():
            # reCaptcha check
            # Note: blocking
            client_response = request.POST.get('g-recaptcha-response')
            server_response = requests.post(
                settings.RECAPTCHA_VERIFICATION_URL, {
                    'secret': settings.RECAPTCHA_SECRET,
                    'response': client_response
            })

            sr = json.loads(server_response.text)
            if sr.get('success') == True:
                # Disable recaptcha
                #  and sr.get('score') > \
                # float(settings.RECAPTCHA_THRESHOLD):
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
                files = form.cleaned_data.get('files')
                if files.lower().strip() != '':
                    file_datas = json.loads(files)
                    for file_data in file_datas:
                        uuid, _, filename = file_data
                        file = fimods.File.objects.get(uuid=uuid)
                        file.lead = lead
                        file.filename = filename
                        file.save()
                
                messages.info(request, 'Your lead has been posted.')

                return HttpResponseRedirect(reverse('leads__root:list'))
            else:
                messages.info(request, 'Are you a robot? Please slow down. [' + str(sr.get('score')) + ']')
    else:
        form = forms.LeadForm()

    countries = commods.Country.objects.order_by('name')

    eb_user = request.user.user
    sgtz = pytz.timezone(settings.TIME_ZONE)

    return render(request, 'leads/create_lead.html', {
        'form': form,
        'countries': countries,
        'amplitude_api_key': settings.AMPLITUDE_API_KEY,
        'amplitude_user_id': eb_user.uuid,
        'country_code': eb_user.phone_number.country_code,
        'register_date_time': eb_user.registered.isoformat(),
        'last_seen_date_time': datetime.now(tz=sgtz).isoformat(),
        'num_whatsapp_lead_author': eb_user.num_whatsapp_lead_author(),
        'num_leads_created': eb_user.num_leads_created()
    })

# @csrf_exempt
class WriteOnlyPresignedURLView(fiviews.WriteOnlyPresignedURLView):
    serializer_class = serializers.WriteOnlyPresignedURLSerializer

def lead_detail(request, uuid):
    try:
        lead = models.Lead.objects.get(uuid=uuid)
    except models.Lead.DoesNotExist:
        raise Http404('Lead does not exist')

    contact_request = None

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

                # Ask lead author to confirm contact request
                send_contact_request_confirm(contact_request.id)

                # Add message
                messages.info(request, "Message sent. We'll notify you if the \
author agrees to exchange contacts with you.")
    else:
        if request.user.is_authenticated:
            # Update analytics for authenticated user
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
                form = forms.ContactForm()
        else:
            # User are not connected and requester have not contact lead author.
            # Show an empty form which will allow the requester to contact the
            # lead owner. Note: we do not merge this condition with is_connected
            # for clarity's sake.
            form = forms.ContactForm()

    return render(request, 'leads/lead_detail.html', {
        'lead': lead,
        'form': form,
        'contact_request': contact_request
    })

def contact_request_detail(request, uuid):
    contact_request = models.ContactRequest.objects.get(uuid=uuid)
    if request.method == 'POST':
        # Exchange contact with the contactor (requester is the lead owner).
        
        contact_request.response = 'accept'
        contact_request.save()

        # Send message to both parties.
        send_contact_request_exchanged_author.delay(contact_request.id)
        send_contact_request_exchanged_contactor.delay(contact_request.id)

    return render(request, 'leads/contactrequest_detail.html', {
        'contact_request': contact_request,
        'whatsapp_link': get_create_whatsapp_link(
            contact_request.lead.author,
            contact_request.contactor)
    })

class ContactRequestListView(LoginRequiredMixin, ListView):
    model = models.ContactRequest
    paginate_by = 30

    def get_queryset(self):
        return models.ContactRequest.objects.filter(
            lead__author=self.request.user.user)