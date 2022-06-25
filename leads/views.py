import phonenumbers, pytz, datetime
from urllib.parse import urljoin

from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, DateTimeField
from django.db.models.functions import Trunc
from django.db.models.expressions import RawSQL
from django.template.loader import render_to_string
from django.contrib.postgres.search import (SearchVector, SearchQuery, SearchRank, SearchVectorField)
from django.template.response import TemplateResponse

from everybase import settings

from chat.tasks.send_new_application import send_new_application
from chat.tasks.send_new_message import send_new_message

from common import models as commods
from common.tasks.send_email import send_email
from common.tasks.send_amplitude_event import send_amplitude_event
from common.tasks.identify_amplitude_user import identify_amplitude_user
from common.utilities.get_ip_address import get_ip_address

from leads import models, forms

from relationships import models as relmods

# from files.utilities.get_mime_type import get_mime_type
# from PIL import Image, ImageOps
# from io import BytesIO
# import boto3

CONTACTED_SUCCESSFULLY_KEY = 'CONTACTED_SUCCESSFULLY_KEY'

@login_required
def lead_create(request):
    if request.method == 'POST':
        form = forms.LeadForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data.get('body')
            lead_type = form.cleaned_data.get('lead_type')

            lead = models.Lead.objects.create(
                author=request.user.user,
                body=body,
                lead_type=lead_type
            )

            send_amplitude_event.delay(
                'created lead',
                user_uuid=lead.author.uuid,
                ip=get_ip_address(request),
                event_properties={
                    'lead id': lead.id,
                    'lead type': lead.lead_type
                }
            )

            return HttpResponseRedirect(reverse('leads:lead_created_success', args=(lead.id,)))
    elif request.method == 'GET':
        form = forms.LeadForm()

    template_name = 'leads/metronic/lead_create.html'
    return render(request, template_name, {'form': form})

def lead_created_success(request, id):
    lead = models.Lead.objects.get(pk=id)
    template_name = 'leads/metronic/lead_create_success.html'
    return TemplateResponse(request, template_name, {'lead_capture_url': lead.lead_capture_url})

@login_required
def lead_detail(request, id):
    lead = models.Lead.objects.get(pk=id)
    params = {'lead': lead}

    # Paginate

    contacts_per_page = 20
    paginator = Paginator(lead.contacts.all().order_by('-created'), contacts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    params['page_obj'] = page_obj

    template_name = 'leads/metronic/lead_detail.html'
    return TemplateResponse(request, template_name, params)

@login_required
def my_leads(request):
    leads = request.user.user.leads_order_by_created_desc()

    params = {}

    # Paginate

    leads_per_page = 20
    paginator = Paginator(leads, leads_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    params['page_obj'] = page_obj

    template_name = 'leads/metronic/my_leads.html'
    return TemplateResponse(request, template_name, params)

def lead_capture(request, id):
    lead = models.Lead.objects.get(pk=id)

    if request.method == 'POST':
        form = forms.LeadCaptureForm(request.POST)
        if form.is_valid():
            # Email
            email, _ = relmods.Email.objects.get_or_create(
                email=form.cleaned_data.get('email'))

            # Phone number
            parsed_ph = phonenumbers.parse(
                str(form.cleaned_data.get('phone_number')), None)
            ph_cc = parsed_ph.country_code
            ph_nn = parsed_ph.national_number
            phone_number, _ = relmods.PhoneNumber.objects.get_or_create(
                country_code=ph_cc,
                national_number=ph_nn
            )

            # Country
            country_key = form.cleaned_data.get('country')
            country = commods.Country.objects.get(programmatic_key=country_key)

            models.Contact.objects.create(
                lead=lead,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=email,
                phone_number=phone_number,
                is_whatsapp=form.cleaned_data.get('is_whatsapp'),
                is_wechat=form.cleaned_data.get('is_wechat'),
                wechat_id=form.cleaned_data.get('wechat_id'),
                is_other=form.cleaned_data.get('is_other'),
                country=country,
                comments=form.cleaned_data.get('comments'),
                is_buyer=form.cleaned_data.get('is_buyer'),
                is_sell_comm=form.cleaned_data.get('is_sell_comm'),
                is_seller=form.cleaned_data.get('is_seller'),
                is_buy_comm=form.cleaned_data.get('is_buy_comm')
            )

            messages.info(request, CONTACTED_SUCCESSFULLY_KEY)
            return HttpResponseRedirect(reverse('home'))
    elif request.method == 'GET':
        form = forms.LeadCaptureForm()

    countries = commods.Country.objects.annotate(
        num_leads=Count('users_w_this_country')).order_by('-num_leads')

    template_name = 'leads/metronic/lead_capture.html'
    return TemplateResponse(request, template_name, {
        'countries': countries,
        'lead': lead,
        'form': form
    })















@login_required
def _lead_create(request):
    if request.method == 'POST':
        form = forms.LeadForm(request.POST)
        if form.is_valid():
            
            g = lambda x: form.cleaned_data.get(x)

            lead_type = g('lead_type')
            author_type = g('author_type')
            country_key = g('country')
            category_key = g('category')
            commission_type = g('commission_type')
            commission_usd_mt = g('commission_usd_mt')
            min_commission_percentage = g('min_commission_percentage')
            max_commission_percentage = g('max_commission_percentage')
            headline = g('headline')
            details = g('details')
            questions = g('questions')

            category = None
            if category_key != 'other':
                try:
                    category = models.LeadCategory.objects.get(programmatic_key=category_key)
                except models.LeadCategory.DoesNotExist:
                    pass

            lead = models.Lead(
                author=request.user.user,
                lead_type=lead_type,
                author_type=author_type,
                category=category,
                commission_type=commission_type,
                commission_usd_mt=commission_usd_mt,
                min_commission_percentage=min_commission_percentage,
                max_commission_percentage=max_commission_percentage,
                headline=headline,
                details=details,
                questions=questions
            )

            if country_key.strip() != 'any_country':
                country = commods.Country.objects.get(programmatic_key=country_key)
                if lead_type == 'selling':
                    lead.buy_country = country
                elif lead_type == 'buying':
                    lead.sell_country = country

            lead.save()

            # Email lead author
            if lead.author.email is not None:
                send_email.delay(
                    render_to_string('leads/email/lead_created_subject.txt', {}),
                    render_to_string('leads/email/lead_created.txt', {
                        'lead_headline': lead.headline,
                        'lead_detail_url': \
                            urljoin(settings.BASE_URL,
                            reverse('leads:lead_detail', args=(lead.id,)))
                    }),
                    'friend@everybase.co',
                    [lead.author.email.email]
                )

            send_amplitude_event.delay(
                'created lead',
                user_uuid=lead.author.uuid,
                ip=get_ip_address(request),
                event_properties={
                    'lead id': lead.id,
                    'buy sell': lead.lead_type,
                    'buy country': lead.buy_country.programmatic_key if lead.buy_country is not None else 'any_country',
                    'sell country': lead.sell_country.programmatic_key if lead.sell_country is not None else 'any_country'
                }
            )
            
            return HttpResponseRedirect(reverse('leads:my_leads'))
    else:
        form = forms.LeadForm()

    countries = commods.Country.objects.annotate(
        num_leads=Count('leads_buy_country')).order_by('-num_leads')

    categories = models.LeadCategory.objects\
        .annotate(num_leads=Count('leads')).\
        order_by('-num_leads')

    params = {
        'countries': countries,
        'categories': categories,
        'form': form
    }

    return render(request, 'leads/superio/lead_create.html', params)




def contact_detail(request, id):
    template_name = 'leads/metronic/contact_detail.html'
    return TemplateResponse(request, template_name, {})

def lead_list(request):
    template_name = 'leads/metronic/home.html'
    return TemplateResponse(request, template_name, {})

def _lead_list(request):
    leads = models.Lead.objects\
        .filter(deleted__isnull=True)\
        .order_by('-created')

    # Logging query
    query = models.LeadQuery(
        user=request.user.user if request.user.is_authenticated else None
    )

    params = {}

    # Filter by buy/sell

    buy_sell = request.GET.get('buy_sell')
    query.buy_sell = buy_sell # Log
    if buy_sell is not None and buy_sell.strip() != '' and buy_sell != 'buy_or_sell':
        if buy_sell == 'buy_only':
            leads = leads.filter(lead_type='buying')
        elif buy_sell == 'sell_only':
            leads = leads.filter(lead_type='selling')
        
        # Pass value back to view
        params['buy_sell'] = buy_sell

    # Filter by category

    category = request.GET.get('category')
    query.category = category # Log
    if category is not None and category.strip() != '' and category != 'any_category':
        c = models.LeadCategory.objects.get(programmatic_key=category)
        leads = leads.filter(category=c)

        # Pass value back to view
        params['category'] = category

    # Filter by country

    country = request.GET.get('country')
    query.country = country # Log
    if country is not None and country.strip() != '' and country != 'any_country':
        c = commods.Country.objects.get(programmatic_key=country)

        if buy_sell == 'buy_or_sell':
            leads = leads.filter(Q(buy_country=c) | Q(sell_country=c))
        elif buy_sell == 'buy_only':
            leads = leads.filter(Q(sell_country=c))
        elif buy_sell == 'sell_only':
            leads = leads.filter(Q(buy_country=c))

        # Pass value back to view
        params['country'] = country

    # Maximum commission percentage for view filter

    # max_comm_lead = models.Lead.objects.all()\
    #     .filter(max_commission_percentage__isnull=False)\
    #     .order_by('-max_commission_percentage')\
    #     .first()
        
    # params['max_commission_percentage'] = 0 if max_comm_lead is None else max_comm_lead.max_commission_percentage

    # Filter by commissions
    
    # min_commission_percentage_filter = request.GET.get('min_commission_percentage_filter')
    # query.min_commission_percentage = float(min_commission_percentage_filter) if min_commission_percentage_filter is not None else None # Log
    # if min_commission_percentage_filter is not None and min_commission_percentage_filter.strip() != '':
    #     # Note: we're only filtering on maximum commission percentage with the slider's
    #     # minimum and maximum values.
    #     leads = leads.filter(max_commission_percentage__gte=min_commission_percentage_filter)\
    #         .filter(max_commission_percentage__isnull=False)\
    #         .filter(min_commission_percentage__isnull=False)

    #     # Pass value back to view
    #     params['min_commission_percentage_filter'] = min_commission_percentage_filter
    # else:
    #     # Pass value back to view
    #     params['min_commission_percentage_filter'] = 0
    
    # max_commission_percentage_filter = request.GET.get('max_commission_percentage_filter')
    # query.max_commission_percentage = float(max_commission_percentage_filter) if max_commission_percentage_filter is not None else None # Log
    # if max_commission_percentage_filter is not None and max_commission_percentage_filter.strip() != '':
    #     leads = leads.filter(max_commission_percentage__lte=max_commission_percentage_filter)\
    #         .filter(max_commission_percentage__isnull=False)\
    #         .filter(min_commission_percentage__isnull=False)

    #     # Pass value back to view
    #     params['max_commission_percentage_filter'] = max_commission_percentage_filter
    # else:
    #     # Pass value back to view
    #     params['max_commission_percentage_filter'] = params['max_commission_percentage']

    # Baseline ordering

    order_by = [Trunc('created', 'week', output_field=DateTimeField()).desc()]

    # Search

    search_phrase = request.GET.get('search_phrase')
    query.search_phrase = search_phrase # Log
    if search_phrase is not None and search_phrase.strip() != '':
        headline_details_vec = SearchVector('headline_details_vec')
        search_query = SearchQuery(search_phrase)
        leads = leads.annotate(
            headline_details_vec=RawSQL('headline_details_vec', [],
            output_field=SearchVectorField()))\
            .annotate(search_rank=SearchRank(headline_details_vec, search_query))

        order_by.append('-search_rank')

        # Pass value back to view
        params['search_phrase'] = search_phrase

    # Order leads
    
    leads = leads.order_by(*order_by)

    #  Set filter countries - only use countries used by leads

    params['countries'] = commods.Country.objects.\
            annotate(num_buy_leads=Count('leads_buy_country')).\
            annotate(num_sell_leads=Count('leads_sell_country')).\
            filter(Q(num_buy_leads__gt=0) | Q(num_sell_leads__gt=0)).\
            order_by('-num_buy_leads')

    # Set filter categories - only use categories used by leads

    params['categories'] = models.LeadCategory.objects\
        .annotate(num_leads=Count('leads')).\
        filter(num_leads__gt=0).\
        order_by('-num_leads')

    # Paginate

    leads_per_page = 20
    paginator = Paginator(leads, leads_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    params['page_obj'] = page_obj

    # Save log if it's not empty
    if (query.search_phrase is not None and query.search_phrase.strip() != '') or\
        (query.buy_sell is not None and query.buy_sell.strip() != 'buy_or_sell') or\
        (query.country is not None and query.country.strip() != 'any_country') or\
        (query.category is not None and query.category.strip() != 'any_category'):
        query.save()

    return render(request, 'leads/superio/lead_list.html', params)



def _lead_detail(request, slug):
    try:
        lead = models.Lead.objects.get(slug_link=slug)
    except models.Lead.DoesNotExist:
        raise Http404('Lead not found')

    # Disallow access to deleted lead
    if lead.deleted:
        raise Http404('Lead not found')
    
    if request.method == 'POST':
        # User applied to be an agent
        form = forms.ApplicationForm(request.POST)
        if request.user.user != lead.author and form.is_valid():

            # Default false if checkbox is not checked
            # has_experience = False if not form.cleaned_data.get('has_experience') else True
            # has_buyers = False if not form.cleaned_data.get('has_buyers') else True

            # answers = form.cleaned_data.get('answers')

            applicant_comments = form.cleaned_data.get('applicant_comments')

            application = models.Application.objects.create(
                lead=lead,
                applicant=request.user.user,
                # has_experience=has_experience,
                # has_buyers=has_buyers,
                applicant_comments=applicant_comments,
                questions=lead.questions,
                # answers=answers
            )

            # Application detail link with 'magic login'
            app_det_link = urljoin(settings.BASE_URL, reverse('magic_login', args=(application.lead.author.uuid,))) +\
                '?next=' + reverse('applications:application_detail', args=(application.id,))

            if application.lead.author.email is not None:
                # Email lead author
                send_email.delay(
                    render_to_string('leads/email/new_application_subject.txt', {
                        'lead_headline': application.lead.headline
                    }),
                    render_to_string('leads/email/new_application.txt', {
                        'lead_author_first_name': application.lead.author.first_name,
                        'lead_author_last_name': application.lead.author.last_name,
                        'lead_headline': application.lead.headline,
                        'application_detail_url': app_det_link
                    }),
                    'friend@everybase.co',
                    [application.lead.author.email.email]
                )

            if application.lead.author.phone_number is not None:
                # WhatsApp lead author
                send_new_application.delay(
                    application.lead.author.id,
                    application.lead.author.first_name,
                    application.lead.author.last_name,
                    application.lead.headline,
                    app_det_link
                )

            event_props = {
                'application id': application.id,
                'lead_type': application.lead.lead_type
            }

            if application.lead.buy_country is not None:
                event_props['buy_country'] = application.lead.buy_country.programmatic_key

            if application.lead.sell_country is not None:
                event_props['sell_country'] = application.lead.sell_country.programmatic_key
            
            send_amplitude_event.delay(
                'applied as an agent',
                user_uuid=lead.author.uuid,
                ip=get_ip_address(request),
                event_properties=event_props
            )
    else:
        form = forms.ApplicationForm()

    # Record user access if authenticated
    if request.user.is_authenticated:
        v, _ = models.LeadDetailView.objects.get_or_create(
            lead=lead,
            viewer=request.user.user
        )

        v.count += 1
        v.save()
    
    params = {
        'form': form,
        'lead': lead
    }

    return render(request, 'leads/superio/lead_detail.html', params)







@login_required
def lead_edit(request, slug):
    lead = models.Lead.objects.get(slug_link=slug)
    if request.method == 'POST':
        form = forms.LeadForm(request.POST)
        if form.is_valid():
            g = lambda x: form.cleaned_data.get(x)

            lead_type = g('lead_type')
            author_type = g('author_type')
            country_key = g('country')
            category_key = g('category')
            commission_type = g('commission_type')
            commission_usd_mt = g('commission_usd_mt')
            min_commission_percentage = g('min_commission_percentage')
            max_commission_percentage = g('max_commission_percentage')
            headline = g('headline')
            details = g('details')
            questions = g('questions')

            category = None
            if category_key != 'other':
                try:
                    category = models.LeadCategory.objects.get(programmatic_key=category_key)
                except models.LeadCategory.DoesNotExist:
                    pass

            lead.author = request.user.user
            lead.lead_type = lead_type
            lead.author_type = author_type
            lead.category = category
            lead.commission_type = commission_type
            lead.commission_usd_mt = commission_usd_mt
            lead.min_commission_percentage = min_commission_percentage
            lead.max_commission_percentage = max_commission_percentage
            lead.headline = headline
            lead.details = details
            lead.questions = questions

            country = commods.Country.objects.get(programmatic_key=country_key)
            if lead_type == 'selling':
                lead.buy_country = country
            elif lead_type == 'buying':
                lead.sell_country = country

            lead.save()
            
            return HttpResponseRedirect(reverse('leads:my_leads'))
    else:
        initial = {
            'author': lead.author,
            'lead_type': lead.lead_type,
            'author_type': lead.author_type,
            'commission_type': lead.commission_type,
            'commission_usd_mt': lead.commission_usd_mt,
            'min_commission_percentage': lead.min_commission_percentage,
            'max_commission_percentage': lead.max_commission_percentage,
            'headline': lead.headline,
            'details': lead.details,
            'questions': lead.questions
        }

        if lead.category is not None:
            initial['category'] = lead.category.programmatic_key

        if lead.lead_type == 'selling':
            initial['country'] = lead.buy_country.programmatic_key
        elif lead.lead_type == 'buying':
            initial['country'] = lead.sell_country.programmatic_key

        form = forms.LeadForm(initial=initial)

    countries = commods.Country.objects.annotate(
        num_leads=Count('leads_buy_country')).order_by('-num_leads')

    categories = models.LeadCategory.objects\
        .annotate(num_leads=Count('leads')).\
        filter(num_leads__gt=0).\
        order_by('-num_leads')

    params = {
        'slug_link': lead.slug_link,
        'categories': categories,
        'countries': countries,
        'form': form
    }

    return render(request, 'leads/superio/lead_edit.html', params)



@login_required
def _my_leads(request):
    leads = models.Lead.objects.all()\
        .filter(
            deleted__isnull=True,
            author=request.user.user
        )\
        .order_by('-created')

    # Paginate

    # products_per_page = 36
    # paginator = Paginator(products, products_per_page)

    # page_number = request.GET.get('page')

    # Set context parameters
    params = {}
    
    # page_obj = paginator.get_page(page_number)
    # params['page_obj'] = page_obj
    params['page_obj'] = leads

    return render(request, 'leads/superio/my_leads.html', params)

@login_required
def lead_delete(request, slug):
    if request.method == 'POST':
        lead = models.Lead.objects.get(slug_link=slug)
        
        # Set delete flag.
        # Model associations are protected, so deleting is a massive operation.
        sgtz = pytz.timezone(settings.TIME_ZONE)
        lead.deleted = datetime.datetime.now(tz=sgtz)
        lead.save()

        return HttpResponseRedirect(reverse('leads:my_leads'))

@login_required
def application_list(request):
    # Get first of all applications associated with this user
    first = request.user.user.applications().first()
    if first:
        return HttpResponseRedirect(
            reverse('applications:application_detail', args=(first.id,)))
    
    form = forms.ApplicationMessageForm()

    return render(request, 'leads/superio/inbox.html', {'form': form})

@login_required
def application_detail(request, pk):
    # Application of focus
    application = models.Application.objects.get(pk=pk)

    if application.deleted is not None:
        # Application is deleted, stop
        return HttpResponseRedirect(reverse('applications:inbox'))
    
    author_replied = models.ApplicationMessage.objects.filter(
        application=application,
        author=application.lead.author
    ).count() > 0
    if application.applicant == request.user.user and not author_replied:
        # Accessing user is an applicant and the author has not replied, stop
        return HttpResponseRedirect(reverse('applications:inbox'))

    if request.method == 'POST':
        # User posted a message
        form = forms.ApplicationMessageForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data.get('body')
            models.ApplicationMessage.objects.create(
                application=application,
                author=request.user.user,
                body=body
            )
            
            sgtz = pytz.timezone(settings.TIME_ZONE)
            now = datetime.datetime.now(tz=sgtz)
            application.last_messaged = now
            application.save()

            if application.applicant.id == request.user.user.id:
                counter_party = application.lead.author
                counter_party_is_agent = False
            else:
                counter_party = application.applicant
                counter_party_is_agent = True

            # Application detail link with 'magic login'
            app_det_link = urljoin(settings.BASE_URL, reverse('magic_login', args=(counter_party.uuid,))) +\
                '?next=' + reverse('applications:application_detail', args=(application.id,))

            # Email counter party
            if counter_party.email is not None:
                send_email.delay(
                    render_to_string('leads/email/new_message_subject.txt', {
                        'lead_headline': application.lead.headline
                    }),
                    render_to_string('leads/email/new_message.txt', {
                        'counter_party_first_name': counter_party.first_name,
                        'counter_party_last_name': counter_party.last_name,
                        'lead_headline': application.lead.headline,
                        'application_detail_url': app_det_link
                    }),
                    'friend@everybase.co',
                    [counter_party.email.email]
                )

            # WhatsApp counter party
            if counter_party.phone_number is not None:
                send_new_message.delay(
                    counter_party.id,
                    counter_party.first_name,
                    counter_party.last_name,
                    application.lead.headline,
                    app_det_link
                )

            num_messages_sent = models.ApplicationMessage.objects.filter(
                author=request.user.user
            ).count()

            identify_amplitude_user.delay(
                user_id=request.user.user.uuid,
                user_properties={
                    'num messages sent': num_messages_sent
                }
            )
            send_amplitude_event.delay(
                'agent application - messaged counterparty',
                user_uuid=request.user.user.uuid,
                ip=get_ip_address(request),
                event_properties={
                    'application id': application.id,
                    'counter party is agent': 'true' if counter_party_is_agent else 'false'
                }
            )
    elif request.method == 'GET':
        form = forms.ApplicationMessageForm()

    # All applications associated with the user - to populate the list
    applications = request.user.user.applications()

    params = {
        'form': form,
        'application': application,
        'applications': applications
    }

    return render(request, 'leads/superio/inbox.html', params)

@login_required
def application_delete(request, pk):
    if request.method == 'POST':
        application = models.Application.objects.get(pk=pk)
        if application.applicant == request.user.user:
            deleted_by = 'agent'
        else:
            deleted_by = 'author'

        sgtz = pytz.timezone(settings.TIME_ZONE)
        application.deleted = datetime.datetime.now(tz=sgtz)
        application.deleted_by = deleted_by
        application.save()

        send_amplitude_event.delay(
            'agent application - deleted conversation',
            user_uuid=request.user.user.uuid,
            ip=get_ip_address(request),
            event_properties={
                'application id': application.id,
                'deleted by': deleted_by
            }
        )

    return HttpResponseRedirect(reverse('applications:inbox'))









































# @login_required
# def lead_edit(request, slug):
#     if not _is_profile_complete(request):
#         return HttpResponseRedirect(reverse('users:profile'))

#     if request.method == 'POST':
#         form = forms.LeadForm(request.POST, request.FILES)
#         if form.is_valid():
#             lead = models.Lead.objects.get(slug_link=slug)
#             lead.headline = form.cleaned_data.get('headline')
#             lead.details = form.cleaned_data.get('details')
#             lead.questions = form.cleaned_data.get('questions')

#             # TODO CONTINUE FROM HERE

#             cover_photo = request.FILES.get('cover_photo')
#             mime_type = get_mime_type(cover_photo)

#             # Create lead file
#             file = fimods.File.objects.create(
#                 uploader=request.user.user,
#                 mime_type=mime_type,
#                 filename=cover_photo.name,
#                 lead=lead,
#                 s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
#                 thumbnail_s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
#             )

#             key = settings.AWS_S3_KEY_LEAD_IMAGE % (lead.id, file.id)
#             thumb_key = settings.AWS_S3_KEY_LEAD_IMAGE_THUMBNAIL % (lead.id, file.id)

#             s3 = boto3.session.Session(
#                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
#             ).resource('s3')

#             # Upload lead image
#             lead_s3_obj = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
#                 Key=key,
#                 Body=cover_photo,
#                 ContentType=mime_type
#             )

#             # Update file with S3 results
#             file.s3_object_key = key
#             file.thumbnail_s3_object_key = thumb_key
#             file.s3_object_content_length = lead_s3_obj.content_length
#             file.e_tag = lead_s3_obj.e_tag
#             file.content_type = lead_s3_obj.content_type
#             file.last_modified = lead_s3_obj.last_modified
#             file.save()

#             # Resize, save thumbnail, record sizes
#             with Image.open(cover_photo) as im:
#                 # Resize preserving aspect ratio cropping from the center
#                 thumbnail = ImageOps.fit(im, settings.LEAD_IMAGE_THUMBNAIL_SIZE)
#                 output = BytesIO()
#                 thumbnail.save(output, format='PNG')
#                 output.seek(0)

#                 # Upload thumbnail
#                 s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
#                     Key=thumb_key,
#                     Body=output,
#                     ContentType=mime_type
#                 )

#                 # Update file and thumbnail sizes
#                 file.width, file.height = im.size
#                 file.thumbnail_width, file.thumbnail_height = thumbnail.size
#                 file.save()
            
#             return HttpResponseRedirect(reverse('leads:my_leads'))
#     elif request.method == 'GET':
#         pass

#     # Return rendered

# from django.template.loader import render_to_string
# import requests, json
# from urllib.parse import urljoin
# from django.db.models import DateTimeField
# from django.db.models.functions import Trunc
# from django.db.models.expressions import RawSQL
# from django.contrib.postgres.search import (SearchVector, SearchQuery, SearchRank, SearchVectorField)
# from django.views.generic.list import ListView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from payments import models as paymods
# from common.tasks.send_amplitude_event import send_amplitude_event
# from files.utilities.delete_file import delete_file
# from django.contrib import messages
# from chat.tasks.send_lead_created_message import send_lead_created_message
# from chat.tasks.send_agent_application_alert_to_agent import send_agent_application_alert_to_agent
# from chat.tasks.send_agent_application_alert_to_lead_author import send_agent_application_alert_to_lead_author
# from chat.tasks.send_agent_application_message import send_agent_application_message

# _recaptcha_failed_msg = "We suspect you're a bot. Please wait a short while before posting."

# def get_countries():
#     return commods.Country.objects.annotate(
#         number_of_users=Count('users_w_this_country'))\
#             .order_by('-number_of_users')

# def save_thumbnail(image, s3, thumb_key, mime_type, file):
#     # Resize and save thumbnail, and record sizes
#     with Image.open(image) as im:
#         # Resize preserving aspect ratio cropping from the center
#         thumbnail = ImageOps.fit(im, settings.LEAD_IMAGE_THUMBNAIL_SIZE)
#         output = BytesIO()
#         thumbnail.save(output, format='PNG')
#         output.seek(0)

#         s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
#             Key=thumb_key,
#             Body=output,
#             ContentType=mime_type
#         )

#         file.width, file.height = im.size
#         file.thumbnail_width, file.thumbnail_height = thumbnail.size
#         file.save()

# def save_img_if_exists(
#         image_key,
#         image_cache_use_key,
#         image_cache_file_id_key,
#         request,
#         lead,
#         form
#     ):

#     # We'll only reach here if form validation passes.
#     #
#     # A valid cache has its File model deleted field set to None.
#     # Otherwise, it's invalid.
#     #
#     # It's not possible to have a file with a valid cache. Since cache
#     # is deleted once we detect a file in the form, whether the file is
#     # valid or not. If we've a file, save it.
#     #
#     # If file does not exist, but a valid cache exists - use the cache
#     # by copying it to our desired location, and delete the cache.
#     #
#     # Though we're dealing with 'cache' images - i.e., cached images that's a
#     # result of failed form validation - 'cache' images can also refer to
#     # actual lead images. We set actual lead images as cache when we're editing
#     # a post.

#     # Helper to get cleaned data
#     get = lambda s : form.cleaned_data.get(s)

#     image = request.FILES.get(image_key)

#     image_cache_use = get(image_cache_use_key)

#     if image_cache_use is not None and image_cache_use == 'no':
#         # Doesn't matter if this image is a cache image (that's set as a
#         # result of failed form validation) or an actual lead image (that's
#         # set as a result of an edit operation), delete this image if the
#         # frontend indicates that we no longer need this image.
#         image_cache_file_id = get(image_cache_file_id_key)
#         delete_file(image_cache_file_id)

#     if image is not None:
#         mime_type = get_mime_type(image)

#         # Create lead file
#         file = fimods.File.objects.create(
#             uploader=request.user.user,
#             mime_type=mime_type,
#             filename=image.name,
#             lead=lead,
#             s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
#             thumbnail_s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
#         )

#         key = settings.AWS_S3_KEY_LEAD_IMAGE % (lead.id, file.id)
#         thumb_key = settings.AWS_S3_KEY_LEAD_IMAGE_THUMBNAIL % (lead.id, file.id)

#         s3 = boto3.session.Session(
#             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
#         ).resource('s3')

#         # Upload lead image
#         lead_s3_obj = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
#             Key=key,
#             Body=image,
#             ContentType=mime_type
#         )

#         # Update lead file with S3 results
#         file.s3_object_key = key
#         file.thumbnail_s3_object_key = thumb_key
#         file.s3_object_content_length = lead_s3_obj.content_length
#         file.e_tag = lead_s3_obj.e_tag
#         file.content_type = lead_s3_obj.content_type
#         file.last_modified = lead_s3_obj.last_modified
#         file.save()

#         save_thumbnail(image, s3, thumb_key, mime_type, file)
#     else:
#         # Image does not exist

#         image_cache_file_id = get(image_cache_file_id_key)

#         if image_cache_file_id is not None and \
#             len(image_cache_file_id.strip()) > 0 and \
#             image_cache_use == 'yes':
#             # Frontend indicates use-cache, and we have the details to do so.

#             cache_file = fimods.File.objects.get(pk=image_cache_file_id)

#             # If this file is NOT a cache, i.e. - its ID and URL were set in an
#             # edit operation, we do not need to copy it from a cache location
#             # to an actual lead image location. We create a test key here to
#             # ascertain if the cache file is located in an actual lead image
#             # location. If equal, the image is not a 'cache' that's created as a
#             # result of form validation failure (though we name it as such).
#             # Instead, the ID and URL were set in an edit operation.
#             test_key = settings.AWS_S3_KEY_LEAD_IMAGE % (lead.id, cache_file.id)
#             if cache_file.deleted is None and \
#                 cache_file.s3_object_key != test_key:
#                 # Cache is valid and not an actual lead image, copy cache
#                 # to actual lead image location.
                
#                 # Create lead file model
#                 lead_file = fimods.File.objects.create(
#                     uploader=request.user.user,
#                     mime_type=cache_file.mime_type,
#                     filename=cache_file.filename,
#                     lead=lead,
#                     s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
#                     thumbnail_s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
#                     s3_object_content_type = cache_file.s3_object_content_type,
#                     s3_object_content_length = cache_file.s3_object_content_length
#                 )

#                 lead_key = settings.AWS_S3_KEY_LEAD_IMAGE % (lead.id, lead_file.id)
#                 cache_key = f'{cache_file.s3_bucket_name}/{cache_file.s3_object_key}'

#                 s3 = boto3.session.Session(
#                     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
#                 ).resource('s3')

#                 # Copy cache to lead file S3 location
#                 lead_s3_obj = s3.Object(
#                     settings.AWS_STORAGE_BUCKET_NAME, lead_key)\
#                     .copy_from(CopySource=cache_key)

#                 thumb_key = settings.AWS_S3_KEY_LEAD_IMAGE_THUMBNAIL % (lead.id, lead_file.id)

#                 # Update file model
#                 lead_file.s3_object_key = lead_key
#                 lead_file.thumbnail_s3_object_key = thumb_key
#                 lead_file.e_tag = lead_s3_obj.get('ETag')
#                 lead_file.last_modified = lead_s3_obj.get('LastModified')
#                 lead_file.save()

#                 # Download cache image for resize to thumbnail
#                 cache = BytesIO()
#                 s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)\
#                     .download_fileobj(cache_file.s3_object_key, cache)
#                 cache.seek(0)

#                 save_thumbnail(cache, s3, thumb_key, cache_file.mime_type, lead_file)

#                 # Delete cache
#                 delete_file(cache_file.id)

# def lead_detail(request, slug):
#     lead = models.Lead.objects.get(slug_link=slug)

#     # Track who've seen this lead
#     if request.user.is_authenticated:
#         v, _ = models.LeadDetailView.objects.get_or_create(
#             lead=lead,
#             viewer=request.user.user
#         )

#         v.count += 1
#         v.save()

#     # An application may have 2 or 3 required questions
#     has_3_questions = lead.question_3 is not None and len(lead.question_3) > 0

#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             # User is not authenticated. Direct user to login with next URL as this detail page.
#             url = reverse('login') + '?next=' + \
#                 reverse('leads:lead_detail', args=(slug,))
#             return HttpResponseRedirect(url)

#         # User is applying to this lead

#         can_apply_lead = models.Application.objects.filter(
#             lead=lead,
#             applicant=request.user.user
#         ).count() == 0 and lead.author != request.user.user

#         if not can_apply_lead:
#             # User is not eligible to apply to this lead
#             return HttpResponseRedirect(reverse('leads:lead_detail', args=(slug,)))

#         if has_3_questions:
#             form = forms.ApplicationFormQ3(request.POST)
#         else:
#             form = forms.ApplicationFormNoQ3(request.POST)

#         recaptcha_response = request.POST.get('g-recaptcha-response')
#         recaptcha_call = requests.post('https://www.google.com/recaptcha/api/siteverify', params={
#             'secret': settings.RECAPTCHA_SECRET_KEY,
#             'response': recaptcha_response
#         })
#         recaptcha_results = json.loads(recaptcha_call.text)
#         if recaptcha_results.get('success') is not True or\
#             recaptcha_results.get('score') is None:
#             form.add_error(None, _recaptcha_failed_msg)
#         elif recaptcha_results.get('success') is True and\
#             recaptcha_results.get('score') is not None and\
#             float(recaptcha_results.get('score')) < float(settings.RECAPTCHA_THRESHOLD):
#             form.add_error(None, _recaptcha_failed_msg)
#         elif form.is_valid():
#             a = models.Application.objects.create(
#                 lead=lead,
#                 applicant=request.user.user,
#                 question_1=lead.question_1,
#                 answer_1=form.cleaned_data.get('answer_1'),
#                 question_2=lead.question_2,
#                 answer_2=form.cleaned_data.get('answer_2'),
#                 question_3=lead.question_3,
#                 answer_3=form.cleaned_data.get('answer_3'),
#                 applicant_comments=form.cleaned_data.get('applicant_comments')
#             )

#             # Send message to both parties
#             send_agent_application_alert_to_lead_author.delay(a.id)
#             send_agent_application_alert_to_agent.delay(a.id)

#             # Amplitude call
#             send_amplitude_event.delay(
#                 'agent application - applied as an agent',
#                 user_uuid=request.user.user.uuid,
#                 event_properties={
#                     'application_id': a.lead.id,
#                     'buy_sell': lead.lead_type,
#                     'buy_country': '' if lead.buy_country is None else lead.buy_country.programmatic_key,
#                     'sell_country': '' if lead.sell_country is None else lead.sell_country.programmatic_key
#                 }
#             )

#             return HttpResponseRedirect(
#                 reverse('applications:application_detail', args=(a.id,)))
#     else:
#         if has_3_questions:
#             form = forms.ApplicationFormQ3()
#         else:
#             form = forms.ApplicationFormNoQ3()

#     params = {
#         'lead': lead,
#         'form': form
#     }

#     return render(request, 'leads/lead_detail.html', params)

# @login_required
# def lead_edit(request, slug):
#     lead = models.Lead.objects.get(slug_link=slug)

#     # If requester does not own lead - redirect to lead detail
#     if request.user.user.id != lead.author.id:
#         return HttpResponseRedirect(reverse('leads:lead_detail', args=(slug)))

#     if request.method == 'POST':
#         form = forms.LeadForm(request.POST, request.FILES)
#         if form.is_valid():

#             # Helper to get cleaned data
#             get = lambda s : form.cleaned_data.get(s)

#             # Helper to get country or not (i.e., any country)
#             get_country = lambda c : commods.Country.objects.get(programmatic_key=c) if c != 'any_country' else None

#             # Update lead
#             lead.lead_type = get('lead_type')
#             lead.currency = paymods.Currency.objects.get(programmatic_key=get('currency'))
#             lead.author_type = get('author_type')
#             lead.buy_country = get_country(get('buy_country'))
#             lead.sell_country = get_country(get('sell_country'))
#             lead.headline = get('headline')
#             lead.details = get('details')
#             lead.agent_job = get('agent_job')
#             lead.commission_type = get('commission_type')
#             lead.commission_percentage = get('commission_percentage')
#             lead.commission_earnings = get('commission_earnings')
#             lead.commission_quantity_unit_string = get('commission_quantity_unit_string')
#             lead.commission_type_other = get('commission_type_other')
#             lead.commission_payable_by = get('commission_payable_by')
#             lead.commission_payable_after = get('commission_payable_after')
#             lead.commission_payable_after_other = get('commission_payable_after_other')
#             lead.other_comm_details = get('other_comm_details')
#             lead.is_comm_negotiable = get('is_comm_negotiable')
#             lead.question_1 = get('question_1')
#             lead.question_2 = get('question_2')
#             lead.question_3 = get('question_3')
#             lead.save()

#             save_img_if_exists('image_one', 'image_one_cache_use', 'image_one_cache_file_id', request, lead, form)
#             save_img_if_exists('image_two', 'image_two_cache_use', 'image_two_cache_file_id', request, lead, form)
#             save_img_if_exists('image_three', 'image_three_cache_use', 'image_three_cache_file_id', request, lead, form)

#             return HttpResponseRedirect(reverse('leads:lead_detail', args=(lead.slug_link,)))
#     else:
#         initial = {
#             'lead_type': lead.lead_type,
#             'currency': lead.currency,
#             'author_type': lead.author_type,
#             'buy_country': lead.buy_country.programmatic_key,
#             'sell_country': lead.sell_country.programmatic_key,
#             'headline': lead.headline,
#             'details': lead.details,
#             'agent_job': lead.agent_job,
#             'commission_type': lead.commission_type,
#             'commission_percentage': lead.commission_percentage,
#             'commission_earnings': lead.commission_earnings,
#             'commission_quantity_unit_string': lead.commission_quantity_unit_string,
#             'commission_type_other': lead.commission_type_other,
#             'commission_payable_by': lead.commission_payable_by,
#             'commission_payable_after': lead.commission_payable_after,
#             'commission_payable_after_other': lead.commission_payable_after_other,
#             'other_comm_details': lead.other_comm_details,
#             'is_comm_negotiable': lead.is_comm_negotiable,
#             'question_1': lead.question_1,
#             'question_2': lead.question_2,
#             'question_3': lead.question_3
#         }

#         names = [
#             ('image_one_cache_file_id', 'image_one_cache_url'),
#             ('image_two_cache_file_id', 'image_two_cache_url'),
#             ('image_three_cache_file_id', 'image_three_cache_url')
#         ]
#         for i, f in enumerate(lead.display_images()):
#             # File ID
#             initial[names[i][0]] = f.id

#             # File URL
#             initial[names[i][1]] = urljoin(settings.MEDIA_URL, f.s3_object_key)

#         form = forms.LeadForm(initial=initial)

#     return render(request, 'leads/lead_edit.html', {
#         'form': form,
#         'slug_link': lead.slug_link,
#         'countries': get_countries()
#     })

# @login_required
# def lead_create(request):
#     if request.method == 'POST':
#         form = forms.LeadForm(request.POST, request.FILES)
#         if form.is_valid():

#             # Helper to get cleaned data
#             get = lambda s : form.cleaned_data.get(s)

#             # Helper to get country or not (i.e., any country)
#             get_country = lambda c : commods.Country.objects.get(programmatic_key=c) if c != 'any_country' else None

#             # Create lead
#             lead = models.Lead.objects.create(
#                 author=request.user.user,
#                 lead_type=get('lead_type'),
#                 currency=paymods.Currency.objects.get(programmatic_key=get('currency')),
#                 author_type=get('author_type'),
#                 buy_country=get_country(get('buy_country')),
#                 sell_country=get_country(get('sell_country')),
#                 headline=get('headline'),
#                 details=get('details'),
#                 agent_job=get('agent_job'),
#                 commission_type=get('commission_type'),
#                 commission_percentage=get('commission_percentage'),
#                 commission_earnings=get('commission_earnings'),
#                 commission_quantity_unit_string=get('commission_quantity_unit_string'),
#                 commission_type_other=get('commission_type_other'),
#                 other_comm_details=get('other_comm_details'),
#                 commission_payable_by=get('commission_payable_by'),
#                 commission_payable_after=get('commission_payable_after'),
#                 commission_payable_after_other=get('commission_payable_after_other'),
#                 is_comm_negotiable=get('is_comm_negotiable'),
#                 question_1=get('question_1'),
#                 question_2=get('question_2'),
#                 question_3=get('question_3')
#             )

#             save_img_if_exists('image_one', 'image_one_cache_use', 'image_one_cache_file_id', request, lead, form)
#             save_img_if_exists('image_two', 'image_two_cache_use', 'image_two_cache_file_id', request, lead, form)
#             save_img_if_exists('image_three', 'image_three_cache_use', 'image_three_cache_file_id', request, lead, form)

#             # Send message to user
#             send_lead_created_message.delay(lead.id)

#             # Amplitude call
#             send_amplitude_event.delay(
#                 'discovery - created lead',
#                 user_uuid=request.user.user.uuid,
#                 event_properties={
#                     'lead_id': lead.id,
#                     'buy_sell': lead.lead_type,
#                     'buy_country': '' if lead.buy_country is None else lead.buy_country.programmatic_key,
#                     'sell_country': '' if lead.sell_country is None else lead.sell_country.programmatic_key
#                 }
#             )

#             return HttpResponseRedirect(
#                 reverse('leads:lead_detail', args=(lead.slug_link,)))
#     else:
#         form = forms.LeadForm()

#     return render(request, 'leads/lead_create.html', {
#         'form': form,
#         'countries': get_countries()
#     })

# def lead_list(request):
#     if request.method == 'GET':
#         user = request.user.user if request.user.is_authenticated else None

#         get = lambda s : request.GET.get(s)

#         search = get('search') # labelled 'search'
#         buy_sell = get('buy_sell')
#         buy_country = get('buy_country')
#         sell_country = get('sell_country')

#         leads = models.Lead.objects.all()

#         is_not_empty = lambda s : s is not None and s.strip() != ''
#         match = lambda t, v: is_not_empty(t) and t == v

#         # Buy sell
#         if match(buy_sell, 'buy'):
#             leads = leads.filter(lead_type='buying')
#         elif buy_sell == 'sell':
#             leads = leads.filter(lead_type='selling')

#         if is_not_empty(buy_country) and buy_country.strip() != 'any_country':
#             # Buy country is selected
#             c = commods.Country.objects.get(programmatic_key=buy_country)
#             leads = leads.filter(buy_country=c)

#         if is_not_empty(sell_country) and sell_country.strip() != 'any_country':
#             # Sell country is selected
#             c = commods.Country.objects.get(programmatic_key=sell_country)
#             leads = leads.filter(sell_country=c)

#         order_by = [Trunc('created', 'month', output_field=DateTimeField()).desc()]

#         if is_not_empty(search):
#             # Goods services details is filled
#             headline_details_vec = SearchVector('headline_details_vec')
#             search_query = SearchQuery(search)
#             leads = leads.annotate(
#                 headline_details_vec=RawSQL('headline_details_vec', [],
#                     output_field=SearchVectorField()))\
#                 .annotate(goods_services_rank=SearchRank(headline_details_vec, search_query))
            
#             order_by.append('-goods_services_rank')

#         # Log unique search
#         l, _ = models.LeadQueryLog.objects.get_or_create(
#             user=user,
#             search=search,
#             buy_sell=buy_sell,
#             buy_country=buy_country,
#             sell_country=sell_country
#         )

#         l.count += 1
#         l.save()

#         # Order leads
#         leads = leads.order_by(*order_by)

#         # Set context parameters
#         params = {}

#         params['countries'] = get_countries()
#         params['search'] = get('search')
#         params['buy_sell'] = get('buy_sell')
#         params['buy_country'] = get('buy_country')
#         params['sell_country'] = get('sell_country')

#         # Paginate

#         leads_per_page = 12
#         paginator = Paginator(leads, leads_per_page)

#         page_number = request.GET.get('page')
        
#         page_obj = paginator.get_page(page_number)
#         params['page_obj'] = page_obj

#         return render(request, 'leads/lead_list.html', params)

# class LeadApplicationListView(LoginRequiredMixin, ListView):
#     template_name = 'leads/lead_detail_application_list.html'
#     context_object_name = 'applications'
#     model = models.Application
#     paginate_by = 8

#     def get_queryset(self, **kwargs):
#         return models.Application.objects.filter(
#             lead=models.Lead.objects.get(slug_link=self.kwargs['slug'])
#         ).order_by('-created')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['lead'] = models.Lead.objects.get(slug_link=self.kwargs['slug'])
#         return context

# @login_required
# def application_detail(request, pk):
#     application = models.Application.objects.get(pk=pk)

#     if application.applicant.id != request.user.user.id and \
#         application.lead.author.id != request.user.user.id:
#         # Only allow the author or applicant to access to this page
#         return HttpResponseRedirect(
#             reverse('leads:lead_detail',
#             args=(application.lead.slug_link,)))

#     if request.method == 'POST':
#         form = forms.ApplicationDetailForm(request.POST)
#         recaptcha_response = request.POST.get('g-recaptcha-response')
#         recaptcha_call = requests.post('https://www.google.com/recaptcha/api/siteverify', params={
#             'secret': settings.RECAPTCHA_SECRET_KEY,
#             'response': recaptcha_response
#         })
#         recaptcha_results = json.loads(recaptcha_call.text)
#         if recaptcha_results.get('success') is not True or\
#             recaptcha_results.get('score') is None:
#             form.add_error(None, _recaptcha_failed_msg)
#         elif recaptcha_results.get('success') is True and\
#             recaptcha_results.get('score') is not None and\
#             float(recaptcha_results.get('score')) < float(settings.RECAPTCHA_THRESHOLD):
#             form.add_error(None, _recaptcha_failed_msg)
#         elif form.is_valid():
#             purpose = form.cleaned_data.get('purpose')
#             if purpose == 'reject':
#                 application.response = 'rejected'
#                 application.save()
#             elif purpose == 'start_work':
#                 application.response = 'started_work'
#                 application.save()
#             elif purpose == 'stop_work':
#                 application.response = 'stopped_work'
#                 application.save()
#             elif purpose == 'message':
#                 am = models.ApplicationMessage.objects.create(
#                     application=application,
#                     author=request.user.user,
#                     body=form.cleaned_data.get('body')
#                 )

#                 send_agent_application_message.delay(am.id)

#                 # Amplitude call
#                 send_amplitude_event.delay(
#                     'agent application - messaged counterparty',
#                     user_uuid=request.user.user.uuid,
#                     event_properties={
#                         'application_id': application.lead.id,
#                         'buy_sell': application.lead.lead_type,
#                         'buy_country': '' if application.lead.buy_country is None else application.lead.buy_country.programmatic_key,
#                         'sell_country': '' if application.lead.sell_country is None else application.lead.sell_country.programmatic_key
#                     }
#                 )

#             return HttpResponseRedirect(
#                 reverse('applications:application_detail',
#                     args=(application.id,)))
#     else:
#         form = forms.ApplicationDetailForm()

#     params = {
#         'application': application,
#         'form': form
#     }

#     return render(request, 'leads/application_detail.html', params)

# @login_required
# def application_for_my_leads_list(request):
#     if request.method == 'GET':
#         status = request.GET.get('status')

#         if status == 'started_work':
#             applications = models.Application.objects.filter(
#                 lead__author=request.user.user,
#                 response='started_work'
#             ).order_by('-created')
#         elif status == 'stopped_work':
#             applications = models.Application.objects.filter(
#                 lead__author=request.user.user,
#                 response='stopped_work'
#             ).order_by('-created')
#         elif status == 'rejected':
#             applications = models.Application.objects.filter(
#                 lead__author=request.user.user,
#                 response='rejected'
#             ).order_by('-created')
#         else:
#             applications = models.Application.objects.filter(
#                 lead__author=request.user.user
#             ).order_by('-created')

#         # Status counts

#         all_statuses_count = models.Application.objects.filter(
#             lead__author=request.user.user
#         ).count()

#         new_count = models.Application.objects\
#             .filter(lead__author=request.user.user)\
#             .exclude(response='started_work')\
#             .exclude(response='stopped_work')\
#             .exclude(response='rejected')\
#             .count()

#         started_work_count = models.Application.objects\
#             .filter(lead__author=request.user.user)\
#             .filter(response='started_work')\
#             .count()

#         stopped_work_count = models.Application.objects\
#             .filter(lead__author=request.user.user)\
#             .filter(response='stopped_work')\
#             .count()

#         rejected_count = models.Application.objects\
#             .filter(lead__author=request.user.user)\
#             .filter(response='rejected')\
#             .count()

#         params = {
#             'status': status,
#             'all_statuses_count': all_statuses_count,
#             'new_count': new_count,
#             'started_work_count': started_work_count,
#             'stopped_work_count': stopped_work_count,
#             'rejected_count': rejected_count
#         }

#         # Paginate

#         applications_per_page = 12
#         paginator = Paginator(applications, applications_per_page)

#         page_number = request.GET.get('page')
        
#         page_obj = paginator.get_page(page_number)
#         params['page_obj'] = page_obj

#         return render(request, 'leads/application_for_my_leads_list.html', params)

# @login_required
# def application_from_me_as_an_agent_list(request):
#     if request.method == 'GET':
#         status = request.GET.get('status')

#         if status == 'started_work':
#             applications = models.Application.objects.filter(
#                 applicant=request.user.user,
#                 response='started_work'
#             ).order_by('-created')
#         elif status == 'stopped_work':
#             applications = models.Application.objects.filter(
#                 applicant=request.user.user,
#                 response='stopped_work'
#             ).order_by('-created')
#         elif status == 'rejected':
#             applications = models.Application.objects.filter(
#                 applicant=request.user.user,
#                 response='rejected'
#             ).order_by('-created')
#         else:
#             applications = models.Application.objects.filter(
#                 applicant=request.user.user
#             ).order_by('-created')

#         # Status counts

#         all_statuses_count = models.Application.objects.filter(
#             applicant=request.user.user
#         ).count()

#         new_count = models.Application.objects\
#             .filter(applicant=request.user.user)\
#             .exclude(response='started_work')\
#             .exclude(response='stopped_work')\
#             .exclude(response='rejected')\
#             .count()

#         started_work_count = models.Application.objects\
#             .filter(applicant=request.user.user)\
#             .filter(response='started_work')\
#             .count()

#         stopped_work_count = models.Application.objects\
#             .filter(applicant=request.user.user)\
#             .filter(response='stopped_work')\
#             .count()

#         rejected_count = models.Application.objects\
#             .filter(applicant=request.user.user)\
#             .filter(response='rejected')\
#             .count()

#         params = {
#             'status': status,
#             'all_statuses_count': all_statuses_count,
#             'new_count': new_count,
#             'started_work_count': started_work_count,
#             'stopped_work_count': stopped_work_count,
#             'rejected_count': rejected_count
#         }

#         # Paginate

#         applications_per_page = 12
#         paginator = Paginator(applications, applications_per_page)

#         page_number = request.GET.get('page')
        
#         page_obj = paginator.get_page(page_number)
#         params['page_obj'] = page_obj

#     return render(request, 'leads/application_from_me_as_an_agent_list.html', params)

# @login_required
# @csrf_exempt
# def toggle_save_lead(request, slug):
#     try:
#         lead = models.Lead.objects.get(slug_link=slug)
#     except models.Lead.DoesNotExist:
#         return HttpResponseRedirect(reverse('leads:lead_detail', args=(slug,)))

#     # Disallow saving of leads owned by the owner
#     if lead.author.id == request.user.user.id:
#         return HttpResponseRedirect(reverse('leads:lead_detail', args=(slug,)))

#     def toggle():
#         try:
#             saved_lead = models.SavedLead.objects.get(
#                 saver=request.user.user,
#                 lead=lead
#             )

#             # Toggle save-unsave
#             saved_lead.active = not saved_lead.active
#             saved_lead.save()
#         except models.SavedLead.DoesNotExist:
#             saved_lead = models.SavedLead.objects.create(
#                 saver=request.user.user,
#                 lead=lead,
#                 active=True
#             )
        
#         return {'s': saved_lead.active}

#     if request.method == 'POST':
#         # AJAX call, toggle save-unsave, return JSON.
#         return JsonResponse(toggle())

#     # Unauthenticated call. User will be given the URL to click only if the
#     # user is authenticated. Otherwise, a click on the 'save' button will
#     # result in an AJAX post to this URL.
#     #
#     # Toggle save-unsave, redirect user to next URL.
#     toggle()

#     # Read 'next' URL from GET parameters. Redirect user there if the
#     # parameter exists. Other redirect user to default lead details page.
#     next_url = request.GET.get('next')
#     if next_url is not None and len(next_url.strip()) > 0:
#         return HttpResponseRedirect(next_url)
#     else:
#         return HttpResponseRedirect(
#             reverse('leads:lead_detail', args=(slug,)))