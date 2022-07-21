import pytz, datetime
from urllib.parse import urljoin
from common.tasks.send_email import send_email
from common.tasks.identify_amplitude_user import identify_amplitude_user

from django.urls import reverse
from django.db.models import Count, Q, F, DateTimeField
from django.db.models.functions import Trunc
from django.db.models.expressions import RawSQL
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchVectorField
from django.views.decorators.csrf import csrf_exempt

from everybase import settings

from common import models as commods
from common.tasks.send_amplitude_event import send_amplitude_event
from common.utilities.get_ip_address import get_ip_address

from leads import models, forms
from leads.utilities.get_or_set_cookie_uuid import get_or_create_cookie_uuid
from leads.utilities.set_cookie_uuid import set_cookie_uuid

from relationships.utilities.get_wechat_url import get_wechat_url
from relationships.utilities.get_whatsapp_url import get_whatsapp_url
from relationships.utilities.get_or_create_email import get_or_create_email
from relationships.utilities.get_or_create_phone_number import get_or_create_phone_number

MESSAGE_KEY__CONTACT_SENT = 'MESSAGE_KEY__CONTACT_SENT'
MESSAGE_KEY__UNAUTHORIZED_ACCESS = 'MESSAGE_KEY__UNAUTHORIZED_ACCESS'

# Helper methods

def _page_obj(params, objects, page: int, items_per_page=20):
    paginator = Paginator(objects, items_per_page)
    params['page_obj'] = paginator.get_page(page)

def _set_whatsapp_bodies(params, contact):
    params['default_whatsapp_body'] = render_to_string(
        'leads/text/default_whatsapp_message_body.txt', {
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'lead_body': contact.lead.body,
        'contact_comments': contact.comments
    }).replace('\n', '\\n') # Replace newline to newline symbols to be rendered in JS
    params['default_whatsapp_body_rows'] = params['default_whatsapp_body'].count('\\n')+1

    last_action = models.ContactAction.objects.filter(
        contact=contact,
        type='whatsapp'
    ).order_by('-created').first()
    
    if last_action is not None and last_action.body is not None and last_action.body.strip() != '':
        params['last_whatsapp_body'] = last_action.body.replace('\r\n', '\\n')
        params['last_whatsapp_body_rows'] = last_action.body.count('\r\n')+1
    else:
        params['last_whatsapp_body_rows'] = 2

def _set_wechat_bodies(params, contact):
    params['default_wechat_body'] = render_to_string(
        'leads/text/default_wechat_message_body.txt', {
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'lead_body': contact.lead.body,
        'contact_comments': contact.comments
    }).replace('\n', '\\n') # Replace newline to newline symbols to be rendered in JS
    params['default_wechat_body_rows'] = params['default_wechat_body'].count('\\n')+1

    last_action = models.ContactAction.objects.filter(
        contact=contact,
        type='wechat'
    ).order_by('-created').first()
    
    if last_action is not None and last_action.body is not None and last_action.body.strip() != '':
        params['last_wechat_body'] = last_action.body.replace('\r\n', '\\n')
        params['last_wechat_body_rows'] = last_action.body.count('\r\n')+1
    else:
        params['last_wechat_body_rows'] = 2

def contact_lead(request, id):
    lead = models.Lead.objects.get(pk=id)
    kwargs = {
        'lead': lead,
        'request': request
    }
    cookie_uuid, _ = get_or_create_cookie_uuid(request)

    if request.method == 'POST':
        form = forms.ContactLeadForm(request.POST, **kwargs)
        if form.is_valid():
            email = get_or_create_email(form.cleaned_data.get('email'))
            phone_number = get_or_create_phone_number(form.cleaned_data.get('phone_number'))

            country_key = form.cleaned_data.get('country')
            country = commods.Country.objects.get(programmatic_key=country_key)

            contact = models.Contact.objects.create(
                lead=lead,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=email,
                phone_number=phone_number,

                cookie_uuid=cookie_uuid,

                via_whatsapp=form.cleaned_data.get('via_whatsapp'),
                via_wechat=form.cleaned_data.get('via_wechat'),
                via_wechat_id=form.cleaned_data.get('via_wechat_id'),

                country=country,

                comments=form.cleaned_data.get('comments'),

                to_selling_as_sales_agent=form.cleaned_data.get('to_selling_as_sales_agent'),
                to_selling_as_sourcing_goods=form.cleaned_data.get('to_selling_as_sourcing_goods'),
                to_selling_as_other=form.cleaned_data.get('to_selling_as_other'),

                to_buying_as_sourcing_agent=form.cleaned_data.get('to_buying_as_sourcing_agent'),
                to_buying_as_promoting_goods=form.cleaned_data.get('to_buying_as_promoting_goods'),
                to_buying_as_other=form.cleaned_data.get('to_buying_as_other'),

                to_sales_agent_as_seeking_cooperation=form.cleaned_data.get('to_sales_agent_as_seeking_cooperation'),
                to_sales_agent_as_sourcing_goods=form.cleaned_data.get('to_sales_agent_as_sourcing_goods'),
                to_sales_agent_as_other=form.cleaned_data.get('to_sales_agent_as_other'),

                to_sourcing_agent_as_seeking_cooperation=form.cleaned_data.get('to_sourcing_agent_as_seeking_cooperation'),
                to_sourcing_agent_as_promoting_goods=form.cleaned_data.get('to_sourcing_agent_as_promoting_goods'),
                to_sourcing_agent_as_other=form.cleaned_data.get('to_sourcing_agent_as_other'),

                to_logistics_agent_as_need_logistics=form.cleaned_data.get('to_logistics_agent_as_need_logistics'),
                to_logistics_agent_as_other=form.cleaned_data.get('to_logistics_agent_as_other'),

                to_need_logistics_as_logistics_agent=form.cleaned_data.get('to_need_logistics_as_logistics_agent'),
                to_need_logistics_as_other=form.cleaned_data.get('to_need_logistics_as_other'),
            )

            # Notify lead author by email
            if lead.author.email is not None:
                magic_login = urljoin(settings.BASE_URL, reverse('magic_login', args=(lead.author.uuid,)))
                contact_details_url = reverse('leads:contact_detail_private_notes', args=(contact.id,))
                target = f'{magic_login}?next={contact_details_url}'
                send_email.delay(
                    render_to_string('relationships/email/new_contact_subject.txt', {
                        'first_name': contact.first_name,
                        'last_name': contact.last_name
                    }),
                    render_to_string('relationships/email/new_contact.txt', {
                        'first_name': contact.first_name,
                        'last_name': contact.last_name,
                        'lead_body': lead.body,
                        'contact_details_url': target,
                    }),
                    'friend@everybase.co',
                    [lead.author.email.email]
                )

            if request.user.is_authenticated:
                user = request.user.user
                identify_amplitude_user.delay(
                    user_id=user.uuid,
                    user_properties={'num leads contacted': user.num_contacts()}
                )

            send_amplitude_event.delay(
                'qualification - contacted lead author',
                user_uuid=lead.author.uuid,
                ip=get_ip_address(request),
                event_properties={
                    'lead id': lead.id,
                    'lead type': lead.lead_type
                }
            )

            messages.info(request, MESSAGE_KEY__CONTACT_SENT)
            return HttpResponseRedirect(reverse('home'))

    elif request.method == 'GET':
        initial = {}

        # Populate form with last contact's details
        last_contact = models.Contact.objects\
            .filter(cookie_uuid=cookie_uuid)\
            .order_by('-created')\
            .first()

        if last_contact is not None:
            initial['first_name'] = last_contact.first_name
            initial['last_name'] = last_contact.last_name
            initial['email'] = last_contact.email
            initial['phone_number'] = last_contact.phone_number
            initial['via_whatsapp'] = last_contact.via_whatsapp
            initial['via_wechat'] = last_contact.via_wechat
            initial['via_wechat_id'] = last_contact.via_wechat_id
            initial['country'] = last_contact.country.programmatic_key
        elif request.user.is_authenticated:
            # Populate form with user's profile details if no last contact is found but the user is authenticated
            user = request.user.user
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
            initial['email'] = user.email.email if user.email is not None else None
            initial['phone_number'] = user.phone_number.value() if user.phone_number is not None else None
            initial['country'] = user.country.programmatic_key if user.country is not None else None

        form = forms.ContactLeadForm(initial=initial, **kwargs)

    countries = commods.Country.objects\
        .annotate(num_leads=Count('users_w_this_country'))\
        .order_by('-num_leads')

    template_name = 'leads/contact_lead.html'
    response = TemplateResponse(request, template_name, {
        'countries': countries,
        'lead': lead,
        'form': form
    })
    return set_cookie_uuid(response, cookie_uuid)

@login_required
def lead_create(request):
    kwargs = {'request': request}
    if request.method == 'POST':
        form = forms.LeadForm(request.POST, **kwargs)
        if form.is_valid():
            lead = models.Lead.objects.create(
                author=request.user.user,
                body=form.cleaned_data.get('body'),
                lead_type=form.cleaned_data.get('lead_type')
            )

            user = request.user.user
            identify_amplitude_user.delay(
                user_id=user.uuid,
                user_properties={'num leads created': user.num_leads()}
            )

            send_amplitude_event.delay(
                'discovery - created lead',
                user_uuid=lead.author.uuid,
                ip=get_ip_address(request),
                event_properties={
                    'lead id': lead.id,
                    'lead type': lead.lead_type
                }
            )

            return HttpResponseRedirect(reverse('leads:lead_created_success', args=(lead.id,)))
    elif request.method == 'GET':
        form = forms.LeadForm(**kwargs)

    return render(request, 'leads/lead_create.html', {'form': form})

@login_required
def lead_created_success(request, id):
    lead = models.Lead.objects.get(pk=id)
    return TemplateResponse(request, 'leads/lead_create_success.html', {'contact_lead_url': lead.contact_lead_url})

@login_required
def lead_detail(request, id):
    lead = models.Lead.objects.get(pk=id)

    # Disallow access if user doesn't own this lead
    if request.user.user.id != lead.author.id:
        messages.info(request, MESSAGE_KEY__UNAUTHORIZED_ACCESS)
        return HttpResponseRedirect(reverse('home'))

    params = {'lead': lead}
    _page_obj(params, lead.contacts.all().order_by('-created'), request.GET.get('page'))
    return TemplateResponse(request, 'leads/lead_detail.html', params)

@login_required
def my_leads(request):
    leads = request.user.user.leads_order_by_created_desc()
    params = {}
    _page_obj(params, leads, request.GET.get('page'))
    return TemplateResponse(request, 'leads/my_leads.html', params)

@login_required
def contact_detail_private_notes(request, id):
    contact = models.Contact.objects.get(pk=id)

    if request.method == 'POST':
        form = forms.ContactNoteForm(request.POST)
        if form.is_valid():
            models.ContactNote.objects.create(
                contact=contact,
                body=form.cleaned_data.get('body'),
                relevance=form.cleaned_data.get('relevance')
            )

            return HttpResponseRedirect(
                reverse('leads:contact_detail_private_notes', args=(contact.id,)))

    elif request.method == 'GET':
        form = forms.ContactNoteForm()

    params = {
        'contact': contact,
        'form': form
    }
    _page_obj(params, contact.active_notes(), request.GET.get('page'))
    _set_whatsapp_bodies(params, contact)
    _set_wechat_bodies(params, contact)
    return TemplateResponse(request, 'leads/contact_detail_private_notes.html', params)

def contact_detail_other_contacts(request, id):
    contact = models.Contact.objects.get(pk=id)
    params = {'contact': contact}
    _page_obj(params, contact.other_contacts(), request.GET.get('page'))
    _set_whatsapp_bodies(params, contact)
    _set_wechat_bodies(params, contact)
    return TemplateResponse(request, 'leads/contact_detail_other_contacts.html', params)

@login_required
def redirect_contact_whatsapp(request, id):
    if request.method == 'POST':
        contact = models.Contact.objects.get(pk=id)
        text = request.POST.get('whatsapp_body')
        text = text if type(text) == str and text.strip() != 0 else None

        models.ContactAction.objects.create(
            contact=contact,
            type='whatsapp',
            body=text
        )
        
        user = request.user.user
        identify_amplitude_user.delay(
            user_id=user.uuid,
            user_properties={'num whatsapped': user.num_whatsapped()}
        )

        send_amplitude_event.delay(
            'qualification - whatsapped',
            user_uuid=user.uuid,
            ip=get_ip_address(request),
            event_properties={'contact id': contact.lead.id}
        )

        url = get_whatsapp_url(contact.phone_number.country_code, contact.phone_number.national_number, text)
        return HttpResponseRedirect(url)

@login_required
def redirect_contact_wechat(request, id):
    if request.method == 'POST':
        contact = models.Contact.objects.get(pk=id)
        text = request.POST.get('wechat_body')
        text = text if type(text) == str and text.strip() != 0 else None

        models.ContactAction.objects.create(
            contact=contact,
            type='wechat',
            body=text
        )

        user = request.user.user
        identify_amplitude_user.delay(
            user_id=user.uuid,
            user_properties={'num wechatted': user.num_wechatted()}
        )

        send_amplitude_event.delay(
            'qualification - wechatted',
            user_uuid=user.uuid,
            ip=get_ip_address(request),
            event_properties={'contact id': contact.lead.id}
        )

        class WeixinSchemeRedirect(HttpResponsePermanentRedirect):
            allowed_schemes = ['weixin']

        url = get_wechat_url(contact.via_wechat_id)
        return WeixinSchemeRedirect(url)

def lead_list(request):
    # Default, don't show reset button
    params = {'show_reset': False}
    cookie_uuid, _ = get_or_create_cookie_uuid(request)

    g = lambda x : request.GET.get(x)
    sourcing = g('sourcing')
    promoting = g('promoting')
    need_logistics = g('need_logistics')
    sourcing_agent = g('sourcing_agent')
    sales_agent = g('sales_agent')
    logistics_agent = g('logistics_agent')
    other = g('other')
    user_country = g('user_country')
    user_country_verified = g('user_country_verified')
    reduce_spams_and_scams = g('reduce_spams_and_scams')
    search_phrase = g('search_phrase')
    
    q = Q()

    off = lambda x : x != 'on'
    on = lambda x : x == 'on'
    if off(sourcing) and off(promoting) and off(need_logistics) and off(sourcing_agent) and\
        off(sales_agent) and off(logistics_agent) and off(other):
        # All lead types are off, turn them all on - we won't show nothing.
        sourcing = 'on'
        promoting = 'on'
        need_logistics = 'on'
        sourcing_agent = 'on'
        sales_agent = 'on'
        logistics_agent = 'on'
        other = 'on'
    if on(sourcing) and on(promoting) and on(need_logistics) and on(sourcing_agent) and\
        on(sales_agent) and on(logistics_agent) and on(other):
        # All lead types are on, we don't need to exclude anything.
        pass
    else:
        # One or more, but not all, lead types are off, filter off lead types.

        if sourcing is None or sourcing != 'on':
            q = q & ~Q(lead_type='buying')
        
        if promoting is None or promoting != 'on':
            q = q & ~Q(lead_type='selling')

        if need_logistics is None or need_logistics != 'on':
            q = q & ~Q(lead_type='need_logistics')

        if sourcing_agent is None or sourcing_agent != 'on':
            q = q & ~Q(lead_type='sourcing_agent')

        if sales_agent is None or sales_agent != 'on':
            q = q & ~Q(lead_type='sales_agent')

        if logistics_agent is None or logistics_agent != 'on':
            q = q & ~Q(lead_type='logistics_agent')

        if other is None or other != 'on':
            q = q & ~Q(lead_type='other')

        params['show_reset'] = True

    if user_country is not None and user_country != 'any_country':
        q = q & Q(author__country__programmatic_key=user_country)
        params['show_reset'] = True

    if user_country_verified == 'on':
        q = q & Q(author__phone_number__country_code=F('author__country__country_code'))

    leads = models.Lead.objects\
        .filter(deleted__isnull=True)\
        .filter(q)

    if reduce_spams_and_scams == 'on':
        # Do not judge leads with less than 10 impressions.
        # Filter leads with more than 10 impressions and more than 3 spam counts.
        # Not implemented yet - for each contact, tolerate 5 more impressions and 1 more spam count.
        spam_leads = leads.annotate(num_spam=Count('flags', filter=Q(flags__type='spam')))\
            .filter(Q(impressions__gte=10) & Q(num_spam__gte=3))
            # Following code doesn't work.
            # .annotate(num_contacts=Count('contacts'))\
            # .filter(Q(impressions__gte=10+(F('num_contacts')*5)) & Q(num_spam__gte=3+F('num_contacts')))\

        leads = leads.exclude(id__in=spam_leads)

        # Do not judge leads with less than 10 impressions.
        # Filter leads with more than 10 impressions and more than 2 scam counts.
        # Not implemented yet - for each contact, tolerate 5 more impressions and 1 more scam count.
        scam_leads = leads.annotate(num_spam=Count('flags', filter=Q(flags__type='scam')))\
            .filter(Q(impressions__gte=10) & Q(num_spam__gte=2))

        leads = leads.exclude(id__in=scam_leads)

        # Exclude leads flagged by this user
        user = request.user.user if request.user.is_authenticated else None
        flagged_lead_ids = models.LeadFlag.objects.filter(deleted__isnull=True).filter(
            Q(user=user) | Q(cookie_uuid=cookie_uuid)
        ).values_list('lead__id', flat=True)
        leads = leads.exclude(id__in=flagged_lead_ids)

        params['show_reset'] = True

    # Baseline ordering
    # Truncate to month on created, then rank within the month. I.e., entries within this month are prioritized.
    order_by = [Trunc('created', 'month', output_field=DateTimeField()).desc()]

    if search_phrase is not None and search_phrase.strip() != '':
        body_vec = SearchVector('body_vec')
        search_query = SearchQuery(search_phrase)
        leads = leads.annotate(body_vec=RawSQL('body_vec', [], output_field=SearchVectorField()))\
            .annotate(search_rank=SearchRank(body_vec, search_query))
        
        # Order by search rank within the baseline order (e.g., within the month)
        order_by.append('-search_rank')

        params['show_reset'] = True

    # Thirdly, order by num_contacts.
    order_by.append('num_contacts')
    leads = leads.annotate(num_contacts=Count('contacts'))\
        .order_by(*order_by)

    # Pass values back
    params['search_phrase'] = search_phrase
    params['reduce_spams_and_scams'] = reduce_spams_and_scams
    params['sourcing'] = sourcing
    params['promoting'] = promoting
    params['need_logistics'] = need_logistics
    params['sourcing_agent'] = sourcing_agent
    params['sales_agent'] = sales_agent
    params['logistics_agent'] = logistics_agent
    params['other'] = other
    params['user_country'] = user_country
    params['user_country_verified'] = user_country_verified

    # Save this lead query
    user = request.user.user if request.user.is_authenticated else None
    lead_query_action = models.LeadQueryAction.objects.create(
        user=user,
        cookie_uuid=cookie_uuid,
        search_phrase=search_phrase,
        reduce_spams_and_scams=reduce_spams_and_scams=='on',
        user_country=user_country,
        user_country_verified=user_country_verified=='on',
        sourcing=sourcing=='on',
        promoting=promoting=='on',
        need_logistics=need_logistics=='on',
        sourcing_agent=sourcing_agent=='on',
        sales_agent=sales_agent=='on',
        logistics_agent=logistics_agent=='on',
        other=other=='on'
    )

    _page_obj(params, leads, request.GET.get('page'), items_per_page=50)
    
    event_properties = {
        'search phrase': search_phrase,
        'reduce spams and scams': reduce_spams_and_scams=='on',
        'sourcing goods': sourcing=='on',
        'promoting goods': promoting=='on',
        'need logistics': need_logistics=='on',
        'sourcing agent': sourcing_agent=='on',
        'sales agent': sales_agent=='on',
        'logistics agent': logistics_agent=='on',
        'other': other=='on',
        'user country': user_country,
        'user country verified': user_country_verified=='on',
        'page': params['page_obj'].number
    }
    send_amplitude_event.delay(
        'discovery - searched leads',
        user_uuid=user.uuid,
        ip=get_ip_address(request),
        event_properties=event_properties
    )

    # Increment impression of all leads on this page
    for lead in params['page_obj']:
        lead.impressions += 1
        lead.save()

    params['countries'] = commods.Country.objects.annotate(
        num_leads=Count('users_w_this_country')).order_by('-num_leads')

    # Handle sign-up search notification 
    if request.method == 'POST':
        form = forms.SignUpSearchNotification(request.POST)
        if form.is_valid():
            models.SearchNotification.objects.create(
                cookie_uuid=cookie_uuid,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=get_or_create_email(form.cleaned_data.get('email')),
                phone_number=get_or_create_phone_number(form.cleaned_data.get('phone_number')),
                country=commods.Country.objects.get(programmatic_key=form.cleaned_data.get('country')),
                via_whatsapp=form.cleaned_data.get('via_whatsapp'),
                via_wechat=form.cleaned_data.get('via_wechat'),
                via_wechat_id=form.cleaned_data.get('via_wechat_id'),
                lead_query_action=lead_query_action
            )

    # Pass form to template if search phrase is entered and we can't identify the user.
    if not (search_phrase is None or search_phrase.strip() == ''):
        any_contact = models.Contact.objects.filter(cookie_uuid=cookie_uuid).first()
        any_search_notification = models.SearchNotification.objects.filter(cookie_uuid=cookie_uuid).first()
        if not request.user.is_authenticated and any_contact is None and any_search_notification is None:
            # User is not authenticated, and have not contacted any lead author, initialize empty form and pass it.
            params['susn_form'] = forms.SignUpSearchNotification()

    response = TemplateResponse(request, 'leads/home.html', params)
    return set_cookie_uuid(response, cookie_uuid)

def _flag_lead(request, lead_id, type):
    """Toggle lead flag on or off."""
    lead = models.Lead.objects.get(pk=lead_id)

    user = request.user.user if request.user.is_authenticated else None
    cookie_uuid, _ = get_or_create_cookie_uuid(request)
    flag, is_created = models.LeadFlag.objects.get_or_create(
        lead=lead,
        type=type,
        user=user,
        cookie_uuid=cookie_uuid
    )

    if not is_created:
        # Flag is not created anew, check the deleted field.
        if flag.deleted is not None:
            # Flag is deleted. Restore it.
            flag.deleted = None
        else:
            # Flag is not deleted. Delete it.
            sgtz = pytz.timezone(settings.TIME_ZONE)
            flag.deleted = datetime.datetime.now(tz=sgtz)
        flag.save()

    result = 'on' if is_created else 'off'
    params = {'result': result}

    # Send updated count
    if type == 'spam':
        params['num_spam_flags'] = lead.num_spam_flags()
    elif type == 'scam':
        params['num_scam_flags'] = lead.num_scam_flags()

    response = JsonResponse(params)
    return set_cookie_uuid(response, cookie_uuid)

@require_http_methods(['POST'])
@csrf_exempt
def flag_spam(request):
    lead_id = request.POST.get('lead_id')
    return _flag_lead(request, lead_id, 'spam')

@require_http_methods(['POST'])
@csrf_exempt
def flag_scam(request):
    lead_id = request.POST.get('lead_id')
    return _flag_lead(request, lead_id, 'scam')




















































# from operator import mod
# import pytz, datetime
# from urllib.parse import urljoin
# from django.db.models import Count, Q, DateTimeField

# from django.db.models.expressions import RawSQL
# from django.http import Http404
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchVectorField

# from everybase import settings





# # from files.utilities.get_mime_type import get_mime_type
# # from PIL import Image, ImageOps
# # from io import BytesIO
# # import boto3


# @login_required
# def _lead_create(request):
#     if request.method == 'POST':
#         form = forms.LeadForm(request.POST)
#         if form.is_valid():
            
#             g = lambda x: form.cleaned_data.get(x)

#             lead_type = g('lead_type')
#             author_type = g('author_type')
#             country_key = g('country')
#             category_key = g('category')
#             commission_type = g('commission_type')
#             commission_usd_mt = g('commission_usd_mt')
#             min_commission_percentage = g('min_commission_percentage')
#             max_commission_percentage = g('max_commission_percentage')
#             headline = g('headline')
#             details = g('details')
#             questions = g('questions')

#             category = None
#             if category_key != 'other':
#                 try:
#                     category = models.LeadCategory.objects.get(programmatic_key=category_key)
#                 except models.LeadCategory.DoesNotExist:
#                     pass

#             lead = models.Lead(
#                 author=request.user.user,
#                 lead_type=lead_type,
#                 author_type=author_type,
#                 category=category,
#                 commission_type=commission_type,
#                 commission_usd_mt=commission_usd_mt,
#                 min_commission_percentage=min_commission_percentage,
#                 max_commission_percentage=max_commission_percentage,
#                 headline=headline,
#                 details=details,
#                 questions=questions
#             )

#             if country_key.strip() != 'any_country':
#                 country = commods.Country.objects.get(programmatic_key=country_key)
#                 if lead_type == 'selling':
#                     lead.buy_country = country
#                 elif lead_type == 'buying':
#                     lead.sell_country = country

#             lead.save()

#             # Email lead author
#             if lead.author.email is not None:
#                 send_email.delay(
#                     render_to_string('leads/email/lead_created_subject.txt', {}),
#                     render_to_string('leads/email/lead_created.txt', {
#                         'lead_headline': lead.headline,
#                         'lead_detail_url': \
#                             urljoin(settings.BASE_URL,
#                             reverse('leads:lead_detail', args=(lead.id,)))
#                     }),
#                     'friend@everybase.co',
#                     [lead.author.email.email]
#                 )

#             send_amplitude_event.delay(
#                 'created lead',
#                 user_uuid=lead.author.uuid,
#                 ip=get_ip_address(request),
#                 event_properties={
#                     'lead id': lead.id,
#                     'buy sell': lead.lead_type,
#                     'buy country': lead.buy_country.programmatic_key if lead.buy_country is not None else 'any_country',
#                     'sell country': lead.sell_country.programmatic_key if lead.sell_country is not None else 'any_country'
#                 }
#             )
            
#             return HttpResponseRedirect(reverse('leads:my_leads'))
#     else:
#         form = forms.LeadForm()

#     countries = commods.Country.objects.annotate(
#         num_leads=Count('leads_buy_country')).order_by('-num_leads')

#     categories = models.LeadCategory.objects\
#         .annotate(num_leads=Count('leads')).\
#         order_by('-num_leads')

#     params = {
#         'countries': countries,
#         'categories': categories,
#         'form': form
#     }

#     return render(request, 'leads/superio/lead_create.html', params)

# def _lead_list(request):
#     leads = models.Lead.objects\
#         .filter(deleted__isnull=True)\
#         .order_by('-created')

#     # Logging query
#     query = models.LeadQuery(
#         user=request.user.user if request.user.is_authenticated else None
#     )

#     params = {}

#     # Filter by buy/sell

#     buy_sell = request.GET.get('buy_sell')
#     query.buy_sell = buy_sell # Log
#     if buy_sell is not None and buy_sell.strip() != '' and buy_sell != 'buy_or_sell':
#         if buy_sell == 'buy_only':
#             leads = leads.filter(lead_type='buying')
#         elif buy_sell == 'sell_only':
#             leads = leads.filter(lead_type='selling')
        
#         # Pass value back to view
#         params['buy_sell'] = buy_sell

#     # Filter by category

#     category = request.GET.get('category')
#     query.category = category # Log
#     if category is not None and category.strip() != '' and category != 'any_category':
#         c = models.LeadCategory.objects.get(programmatic_key=category)
#         leads = leads.filter(category=c)

#         # Pass value back to view
#         params['category'] = category

#     # Filter by country

#     country = request.GET.get('country')
#     query.country = country # Log
#     if country is not None and country.strip() != '' and country != 'any_country':
#         c = commods.Country.objects.get(programmatic_key=country)

#         if buy_sell == 'buy_or_sell':
#             leads = leads.filter(Q(buy_country=c) | Q(sell_country=c))
#         elif buy_sell == 'buy_only':
#             leads = leads.filter(Q(sell_country=c))
#         elif buy_sell == 'sell_only':
#             leads = leads.filter(Q(buy_country=c))

#         # Pass value back to view
#         params['country'] = country

#     # Maximum commission percentage for view filter

#     # max_comm_lead = models.Lead.objects.all()\
#     #     .filter(max_commission_percentage__isnull=False)\
#     #     .order_by('-max_commission_percentage')\
#     #     .first()
        
#     # params['max_commission_percentage'] = 0 if max_comm_lead is None else max_comm_lead.max_commission_percentage

#     # Filter by commissions
    
#     # min_commission_percentage_filter = request.GET.get('min_commission_percentage_filter')
#     # query.min_commission_percentage = float(min_commission_percentage_filter) if min_commission_percentage_filter is not None else None # Log
#     # if min_commission_percentage_filter is not None and min_commission_percentage_filter.strip() != '':
#     #     # Note: we're only filtering on maximum commission percentage with the slider's
#     #     # minimum and maximum values.
#     #     leads = leads.filter(max_commission_percentage__gte=min_commission_percentage_filter)\
#     #         .filter(max_commission_percentage__isnull=False)\
#     #         .filter(min_commission_percentage__isnull=False)

#     #     # Pass value back to view
#     #     params['min_commission_percentage_filter'] = min_commission_percentage_filter
#     # else:
#     #     # Pass value back to view
#     #     params['min_commission_percentage_filter'] = 0
    
#     # max_commission_percentage_filter = request.GET.get('max_commission_percentage_filter')
#     # query.max_commission_percentage = float(max_commission_percentage_filter) if max_commission_percentage_filter is not None else None # Log
#     # if max_commission_percentage_filter is not None and max_commission_percentage_filter.strip() != '':
#     #     leads = leads.filter(max_commission_percentage__lte=max_commission_percentage_filter)\
#     #         .filter(max_commission_percentage__isnull=False)\
#     #         .filter(min_commission_percentage__isnull=False)

#     #     # Pass value back to view
#     #     params['max_commission_percentage_filter'] = max_commission_percentage_filter
#     # else:
#     #     # Pass value back to view
#     #     params['max_commission_percentage_filter'] = params['max_commission_percentage']

#     # Baseline ordering



#     # Search

#     search_phrase = request.GET.get('search_phrase')
#     query.search_phrase = search_phrase # Log
#     if search_phrase is not None and search_phrase.strip() != '':
#         headline_details_vec = SearchVector('headline_details_vec')
#         search_query = SearchQuery(search_phrase)
#         leads = leads.annotate(
#             headline_details_vec=RawSQL('headline_details_vec', [],
#             output_field=SearchVectorField()))\
#             .annotate(search_rank=SearchRank(headline_details_vec, search_query))

#         order_by.append('-search_rank')

#         # Pass value back to view
#         params['search_phrase'] = search_phrase

#     # Order leads
    
#     leads = leads.order_by(*order_by)

#     #  Set filter countries - only use countries used by leads

#     params['countries'] = commods.Country.objects.\
#             annotate(num_buy_leads=Count('leads_buy_country')).\
#             annotate(num_sell_leads=Count('leads_sell_country')).\
#             filter(Q(num_buy_leads__gt=0) | Q(num_sell_leads__gt=0)).\
#             order_by('-num_buy_leads')

#     # Set filter categories - only use categories used by leads

#     params['categories'] = models.LeadCategory.objects\
#         .annotate(num_leads=Count('leads')).\
#         filter(num_leads__gt=0).\
#         order_by('-num_leads')

#     # Paginate

#     leads_per_page = 20
#     paginator = Paginator(leads, leads_per_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     params['page_obj'] = page_obj

#     # Save log if it's not empty
#     if (query.search_phrase is not None and query.search_phrase.strip() != '') or\
#         (query.buy_sell is not None and query.buy_sell.strip() != 'buy_or_sell') or\
#         (query.country is not None and query.country.strip() != 'any_country') or\
#         (query.category is not None and query.category.strip() != 'any_category'):
#         query.save()

#     return render(request, 'leads/superio/lead_list.html', params)

# def _lead_detail(request, slug):
#     try:
#         lead = models.Lead.objects.get(slug_link=slug)
#     except models.Lead.DoesNotExist:
#         raise Http404('Lead not found')

#     # Disallow access to deleted lead
#     if lead.deleted:
#         raise Http404('Lead not found')
    
#     if request.method == 'POST':
#         # User applied to be an agent
#         form = forms.ApplicationForm(request.POST)
#         if request.user.user != lead.author and form.is_valid():

#             # Default false if checkbox is not checked
#             # has_experience = False if not form.cleaned_data.get('has_experience') else True
#             # has_buyers = False if not form.cleaned_data.get('has_buyers') else True

#             # answers = form.cleaned_data.get('answers')

#             applicant_comments = form.cleaned_data.get('applicant_comments')

#             application = models.Application.objects.create(
#                 lead=lead,
#                 applicant=request.user.user,
#                 # has_experience=has_experience,
#                 # has_buyers=has_buyers,
#                 applicant_comments=applicant_comments,
#                 questions=lead.questions,
#                 # answers=answers
#             )

#             # Application detail link with 'magic login'
#             app_det_link = urljoin(settings.BASE_URL, reverse('magic_login', args=(application.lead.author.uuid,))) +\
#                 '?next=' + reverse('applications:application_detail', args=(application.id,))

#             if application.lead.author.email is not None:
#                 # Email lead author
#                 send_email.delay(
#                     render_to_string('leads/email/new_application_subject.txt', {
#                         'lead_headline': application.lead.headline
#                     }),
#                     render_to_string('leads/email/new_application.txt', {
#                         'lead_author_first_name': application.lead.author.first_name,
#                         'lead_author_last_name': application.lead.author.last_name,
#                         'lead_headline': application.lead.headline,
#                         'application_detail_url': app_det_link
#                     }),
#                     'friend@everybase.co',
#                     [application.lead.author.email.email]
#                 )

#             if application.lead.author.phone_number is not None:
#                 # WhatsApp lead author
#                 send_new_application.delay(
#                     application.lead.author.id,
#                     application.lead.author.first_name,
#                     application.lead.author.last_name,
#                     application.lead.headline,
#                     app_det_link
#                 )

#             event_props = {
#                 'application id': application.id,
#                 'lead_type': application.lead.lead_type
#             }

#             if application.lead.buy_country is not None:
#                 event_props['buy_country'] = application.lead.buy_country.programmatic_key

#             if application.lead.sell_country is not None:
#                 event_props['sell_country'] = application.lead.sell_country.programmatic_key
            
#             send_amplitude_event.delay(
#                 'applied as an agent',
#                 user_uuid=lead.author.uuid,
#                 ip=get_ip_address(request),
#                 event_properties=event_props
#             )
#     else:
#         form = forms.ApplicationForm()

#     # Record user access if authenticated
#     if request.user.is_authenticated:
#         v, _ = models.LeadDetailView.objects.get_or_create(
#             lead=lead,
#             viewer=request.user.user
#         )

#         v.count += 1
#         v.save()
    
#     params = {
#         'form': form,
#         'lead': lead
#     }

#     return render(request, 'leads/superio/lead_detail.html', params)

# @login_required
# def lead_edit(request, slug):
#     lead = models.Lead.objects.get(slug_link=slug)
#     if request.method == 'POST':
#         form = forms.LeadForm(request.POST)
#         if form.is_valid():
#             g = lambda x: form.cleaned_data.get(x)

#             lead_type = g('lead_type')
#             author_type = g('author_type')
#             country_key = g('country')
#             category_key = g('category')
#             commission_type = g('commission_type')
#             commission_usd_mt = g('commission_usd_mt')
#             min_commission_percentage = g('min_commission_percentage')
#             max_commission_percentage = g('max_commission_percentage')
#             headline = g('headline')
#             details = g('details')
#             questions = g('questions')

#             category = None
#             if category_key != 'other':
#                 try:
#                     category = models.LeadCategory.objects.get(programmatic_key=category_key)
#                 except models.LeadCategory.DoesNotExist:
#                     pass

#             lead.author = request.user.user
#             lead.lead_type = lead_type
#             lead.author_type = author_type
#             lead.category = category
#             lead.commission_type = commission_type
#             lead.commission_usd_mt = commission_usd_mt
#             lead.min_commission_percentage = min_commission_percentage
#             lead.max_commission_percentage = max_commission_percentage
#             lead.headline = headline
#             lead.details = details
#             lead.questions = questions

#             country = commods.Country.objects.get(programmatic_key=country_key)
#             if lead_type == 'selling':
#                 lead.buy_country = country
#             elif lead_type == 'buying':
#                 lead.sell_country = country

#             lead.save()
            
#             return HttpResponseRedirect(reverse('leads:my_leads'))
#     else:
#         initial = {
#             'author': lead.author,
#             'lead_type': lead.lead_type,
#             'author_type': lead.author_type,
#             'commission_type': lead.commission_type,
#             'commission_usd_mt': lead.commission_usd_mt,
#             'min_commission_percentage': lead.min_commission_percentage,
#             'max_commission_percentage': lead.max_commission_percentage,
#             'headline': lead.headline,
#             'details': lead.details,
#             'questions': lead.questions
#         }

#         if lead.category is not None:
#             initial['category'] = lead.category.programmatic_key

#         if lead.lead_type == 'selling':
#             initial['country'] = lead.buy_country.programmatic_key
#         elif lead.lead_type == 'buying':
#             initial['country'] = lead.sell_country.programmatic_key

#         form = forms.LeadForm(initial=initial)

#     countries = commods.Country.objects.annotate(
#         num_leads=Count('leads_buy_country')).order_by('-num_leads')

#     categories = models.LeadCategory.objects\
#         .annotate(num_leads=Count('leads')).\
#         filter(num_leads__gt=0).\
#         order_by('-num_leads')

#     params = {
#         'slug_link': lead.slug_link,
#         'categories': categories,
#         'countries': countries,
#         'form': form
#     }

#     return render(request, 'leads/superio/lead_edit.html', params)

# @login_required
# def _my_leads(request):
#     leads = models.Lead.objects.all()\
#         .filter(
#             deleted__isnull=True,
#             author=request.user.user
#         )\
#         .order_by('-created')

#     # Paginate

#     # products_per_page = 36
#     # paginator = Paginator(products, products_per_page)

#     # page_number = request.GET.get('page')

#     # Set context parameters
#     params = {}
    
#     # page_obj = paginator.get_page(page_number)
#     # params['page_obj'] = page_obj
#     params['page_obj'] = leads

#     return render(request, 'leads/superio/my_leads.html', params)

# @login_required
# def lead_delete(request, slug):
#     if request.method == 'POST':
#         lead = models.Lead.objects.get(slug_link=slug)
        
#         # Set delete flag.
#         # Model associations are protected, so deleting is a massive operation.
#         sgtz = pytz.timezone(settings.TIME_ZONE)
#         lead.deleted = datetime.datetime.now(tz=sgtz)
#         lead.save()

#         return HttpResponseRedirect(reverse('leads:my_leads'))

# @login_required
# def application_list(request):
#     # Get first of all applications associated with this user
#     first = request.user.user.applications().first()
#     if first:
#         return HttpResponseRedirect(
#             reverse('applications:application_detail', args=(first.id,)))
    
#     form = forms.ApplicationMessageForm()

#     return render(request, 'leads/superio/inbox.html', {'form': form})

# @login_required
# def application_detail(request, pk):
#     # Application of focus
#     application = models.Application.objects.get(pk=pk)

#     if application.deleted is not None:
#         # Application is deleted, stop
#         return HttpResponseRedirect(reverse('applications:inbox'))
    
#     author_replied = models.ApplicationMessage.objects.filter(
#         application=application,
#         author=application.lead.author
#     ).count() > 0
#     if application.applicant == request.user.user and not author_replied:
#         # Accessing user is an applicant and the author has not replied, stop
#         return HttpResponseRedirect(reverse('applications:inbox'))

#     if request.method == 'POST':
#         # User posted a message
#         form = forms.ApplicationMessageForm(request.POST)
#         if form.is_valid():
#             body = form.cleaned_data.get('body')
#             models.ApplicationMessage.objects.create(
#                 application=application,
#                 author=request.user.user,
#                 body=body
#             )
            
#             sgtz = pytz.timezone(settings.TIME_ZONE)
#             now = datetime.datetime.now(tz=sgtz)
#             application.last_messaged = now
#             application.save()

#             if application.applicant.id == request.user.user.id:
#                 counter_party = application.lead.author
#                 counter_party_is_agent = False
#             else:
#                 counter_party = application.applicant
#                 counter_party_is_agent = True

#             # Application detail link with 'magic login'
#             app_det_link = urljoin(settings.BASE_URL, reverse('magic_login', args=(counter_party.uuid,))) +\
#                 '?next=' + reverse('applications:application_detail', args=(application.id,))

#             # Email counter party
#             if counter_party.email is not None:
#                 send_email.delay(
#                     render_to_string('leads/email/new_message_subject.txt', {
#                         'lead_headline': application.lead.headline
#                     }),
#                     render_to_string('leads/email/new_message.txt', {
#                         'counter_party_first_name': counter_party.first_name,
#                         'counter_party_last_name': counter_party.last_name,
#                         'lead_headline': application.lead.headline,
#                         'application_detail_url': app_det_link
#                     }),
#                     'friend@everybase.co',
#                     [counter_party.email.email]
#                 )

#             # WhatsApp counter party
#             if counter_party.phone_number is not None:
#                 send_new_message.delay(
#                     counter_party.id,
#                     counter_party.first_name,
#                     counter_party.last_name,
#                     application.lead.headline,
#                     app_det_link
#                 )

#             num_messages_sent = models.ApplicationMessage.objects.filter(
#                 author=request.user.user
#             ).count()

#             identify_amplitude_user.delay(
#                 user_id=request.user.user.uuid,
#                 user_properties={
#                     'num messages sent': num_messages_sent
#                 }
#             )
#             send_amplitude_event.delay(
#                 'agent application - messaged counterparty',
#                 user_uuid=request.user.user.uuid,
#                 ip=get_ip_address(request),
#                 event_properties={
#                     'application id': application.id,
#                     'counter party is agent': 'true' if counter_party_is_agent else 'false'
#                 }
#             )
#     elif request.method == 'GET':
#         form = forms.ApplicationMessageForm()

#     # All applications associated with the user - to populate the list
#     applications = request.user.user.applications()

#     params = {
#         'form': form,
#         'application': application,
#         'applications': applications
#     }

#     return render(request, 'leads/superio/inbox.html', params)

# @login_required
# def application_delete(request, pk):
#     if request.method == 'POST':
#         application = models.Application.objects.get(pk=pk)
#         if application.applicant == request.user.user:
#             deleted_by = 'agent'
#         else:
#             deleted_by = 'author'

#         sgtz = pytz.timezone(settings.TIME_ZONE)
#         application.deleted = datetime.datetime.now(tz=sgtz)
#         application.deleted_by = deleted_by
#         application.save()

#         send_amplitude_event.delay(
#             'agent application - deleted conversation',
#             user_uuid=request.user.user.uuid,
#             ip=get_ip_address(request),
#             event_properties={
#                 'application id': application.id,
#                 'deleted by': deleted_by
#             }
#         )

#     return HttpResponseRedirect(reverse('applications:inbox'))


































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