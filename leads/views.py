from statistics import mode
import traceback, boto3
from PIL import Image, ImageOps
from io import BytesIO

from django.urls import reverse
from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models.expressions import RawSQL
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchVectorField

from everybase import settings
from common import models as commods
from leads import models, forms
from relationships import models as relmods
from relationships.utilities.save_user_agent import save_user_agent
from files import models as fimods
from files.utilities.get_mime_type import get_mime_type

def get_countries():
    return commods.Country.objects.annotate(
        number_of_users=Count('users_w_this_country'))\
            .order_by('-number_of_users')

class LeadDetailView(DetailView):
    template_name = 'leads/lead_detail.html'
    model = models.Lead

def lead_detail(request, slug):
    lead = models.Lead.objects.get(slug_link=slug)
    if request.method == 'POST':
        # User posted a comment
        form = forms.LeadCommentForm(request.POST)
        if form.is_valid():
            comment = models.LeadComment.objects.create(
                lead=models.Lead.objects.get(slug_link=slug),
                commentor=request.user.user,
                body=request.POST.get('body')
            )

            comment_id = request.POST.get('comment_id')
            if comment_id is not None:
                # This is a reply to a root comment
                comment.reply_to = models.LeadComment.objects.get(pk=comment_id)
                comment.save()

            # Focus on comment created
            url = reverse('leads:lead_detail', args=(slug,)) + \
                '?focus=comment-' + str(comment.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.LeadCommentForm()

    params = {
        'lead': lead,
        'form': form
    }

    focus = request.GET.get('focus')
    if focus is not None:
        params['focus'] = focus

    return render(request, 'leads/lead_detail.html', params)

@login_required
def lead_edit(request, pk):
    lead = models.Lead.objects.get(pk=pk)

    # If requester does not own lead - redirect to lead list
    if request.user.user.id != lead.author.id:
        return HttpResponseRedirect(reverse('leads:lead_list', args=()))

    if request.method == 'POST':
        form = forms.LeadForm(request.POST)
        if form.is_valid():
            buy_country_str = form.cleaned_data.get('buy_country')
            if buy_country_str != 'any_country':
                lead.buy_country = commods.Country.objects.get(
                    programmatic_key=buy_country_str)
            else:
                lead.buy_country = None

            sell_country_str = form.cleaned_data.get('sell_country')
            if sell_country_str != 'any_country':
                lead.sell_country = commods.Country.objects.get(
                    programmatic_key=sell_country_str)
            else:
                lead.sell_country = None

            lead.lead_type = form.cleaned_data.get('lead_type')
            lead.avg_deal_size = form.cleaned_data.get('avg_deal_size')
            lead.commissions = form.cleaned_data.get('commissions')
            lead.details = form.cleaned_data.get('details')
            lead.other_comm_details = form.cleaned_data.get(
                'other_comm_details')

            lead.save()

            return HttpResponseRedirect(
                reverse('leads:lead_detail', args=(lead.slug_link,)))
    else:
        lead = models.Lead.objects.get(pk=pk)

        buy_country = 'any_country'
        if lead.buy_country != None:
            buy_country = lead.buy_country.programmatic_key

        sell_country = 'any_country'
        if lead.sell_country != None:
            sell_country = lead.sell_country.programmatic_key

        form = forms.LeadForm(initial={
            'lead_type': lead.lead_type,
            'buy_country': buy_country,
            'sell_country': sell_country,
            'avg_deal_size': lead.avg_deal_size,
            'commissions': lead.commissions,
            'details': lead.details,
            'other_comm_details': lead.other_comm_details
        })

    return render(request, 'leads/lead_edit.html', {
        'lead_pk': pk,
        'form': form,
        'countries': get_countries()
    })

@login_required
def lead_create(request):
    countries = get_countries()

    if request.method == 'POST':
        form = forms.LeadForm(request.POST, request.FILES)
        if form.is_valid():

            # Helper to get cleaned data
            get = lambda s : form.cleaned_data.get(s)

            # Helper to get country or not (i.e., any country)
            get_country = lambda c : commods.Country.objects.get(programmatic_key=c) if c != 'any_country' else None

            # Create lead
            need_agent = get('need_agent')
            commission_type = get('commission_type')
            author_type = get('author_type')
            need_logistics_agent = get('need_logistics_agent')
            lead = models.Lead.objects.create(
                author=request.user.user,
                lead_type=get('lead_type'),
                author_type=author_type,
                buy_country=get_country(get('buy_country')),
                sell_country=get_country(get('sell_country')),
                details=get('details'),
                need_agent=need_agent,
                commission_type=commission_type if need_agent else None,
                commission_type_other=get('commission_type_other') if need_agent and commission_type == 'other' else None,
                commission=get('commission') if need_agent and commission_type == 'percentage' else None,
                avg_deal_size=get('avg_deal_size') if need_agent and commission_type == 'percentage' else None,
                is_comm_negotiable=get('is_comm_negotiable') if need_agent else None,
                commission_payable_after=get('commission_payable_after') if need_agent else None,
                commission_payable_after_other=get('commission_payable_after_other') if need_agent else None,
                commission_payable_by=get('commission_payable_by') if need_agent and author_type == 'broker' else None,
                other_agent_details=get('other_agent_details') if need_agent else None,
                need_logistics_agent=need_logistics_agent,
                other_logistics_agent_details=get('other_logistics_agent_details') if need_logistics_agent else None
            )

            # We'll only reach here if form validation passes.
            #
            # A valid cache has its File model deleted field set to None.
            # Otherwise, it's invalid.
            #
            # It's not possible to have a file with a valid cache. Since cache
            # is deleted once we detect a file in the form, whether the file is
            # valid or not. If we've a file, save it.
            #
            # If file does not exist, but a valid cache exists - use the cache
            # by copying it to our desired location, and delete the cache.

            def save_img_if_exists(image_key, image_cache_use_key, image_cache_file_id_key):
                image = request.FILES.get(image_key)

                if image is not None:
                    mime_type = get_mime_type(image)

                    # Create lead file
                    file = fimods.File.objects.create(
                        uploader=request.user.user,
                        mime_type=mime_type,
                        filename=image.name,
                        lead=lead,
                        s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
                        thumbnail_s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
                    )

                    key = settings.AWS_S3_KEY_LEAD_IMAGE % (lead.id, file.id)
                    thumb_key = settings.AWS_S3_KEY_LEAD_IMAGE_THUMBNAIL % (lead.id, file.id)

                    s3 = boto3.session.Session(
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                    ).resource('s3')

                    # Upload lead image
                    lead_s3_obj = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                        Key=key,
                        Body=image,
                        ContentType=mime_type
                    )

                    # Update lead file with S3 results
                    file.s3_object_key = key
                    file.thumbnail_s3_object_key = thumb_key
                    file.s3_object_content_length = lead_s3_obj.content_length
                    file.e_tag = lead_s3_obj.e_tag
                    file.content_type = lead_s3_obj.content_type
                    file.last_modified = lead_s3_obj.last_modified
                    file.save()

                    # Resize and save thumbnail, and record sizes
                    with Image.open(image) as im:
                        # Resize preserving aspect ratio cropping from the center
                        thumbnail = ImageOps.fit(im, settings.LEAD_IMAGE_THUMBNAIL_SIZE)
                        output = BytesIO()
                        thumbnail.save(output, format='PNG')
                        output.seek(0)

                        s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                            Key=thumb_key,
                            Body=output,
                            ContentType=mime_type
                        )

                        file.width, file.height = im.size
                        file.thumbnail_width, file.thumbnail_height = thumbnail.size
                        file.save()
                else:
                    # Image does not exist

                    image_cache_use = get(image_cache_use_key)
                    image_cache_file_id = get(image_cache_file_id_key)

                    if image_cache_use == 'yes' and \
                        image_cache_file_id is not None and \
                        len(image_cache_file_id.strip()) > 0:
                        # Frontend indicates use-cache, and we have the details to do so.

                        cache_file = fimods.File.objects.get(pk=image_cache_file_id)
                        if cache_file.deleted is None:
                            # Cache is valid, use cache.
                            
                            # Create lead file model
                            lead_file = fimods.File.objects.create(
                                uploader=request.user.user,
                                mime_type=cache_file.mime_type,
                                filename=cache_file.filename,
                                lead=lead,
                                s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
                                thumbnail_s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
                                s3_object_content_type = cache_file.s3_object_content_type,
                                s3_object_content_length = cache_file.s3_object_content_length
                            )

                            lead_key = settings.AWS_S3_KEY_LEAD_IMAGE % (lead.id, lead_file.id)
                            cache_key = f'{cache_file.s3_bucket_name}/{cache_file.s3_object_key}'

                            s3 = boto3.session.Session(
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                            ).resource('s3')

                            # Copy cache to lead file S3 location
                            lead_s3_obj = s3.Object(
                                settings.AWS_STORAGE_BUCKET_NAME, lead_key)\
                                .copy_from(CopySource=cache_key)

                            thumb_key = settings.AWS_S3_KEY_LEAD_IMAGE_THUMBNAIL % (lead.id, lead_file.id)

                            # Update file model
                            lead_file.s3_object_key = lead_key
                            lead_file.thumbnail_s3_object_key = thumb_key
                            lead_file.e_tag = lead_s3_obj.get('ETag')
                            lead_file.last_modified = lead_s3_obj.get('LastModified')
                            lead_file.save()

                            # Download cache image for resize to thumbnail
                            cache = BytesIO()
                            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)\
                                .download_fileobj(cache_file.s3_object_key, cache)
                            cache.seek(0)

                            # Resize and save thumbnail, and record sizes
                            with Image.open(cache) as im:
                                # Resize preserving aspect ratio cropping from the center
                                thumbnail = ImageOps.fit(im, settings.LEAD_IMAGE_THUMBNAIL_SIZE)
                                output = BytesIO()
                                thumbnail.save(output, format='PNG')
                                output.seek(0)

                                s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                                    Key=thumb_key,
                                    Body=output,
                                    ContentType=cache_file.mime_type
                                )

                                file.width, file.height = im.size
                                file.thumbnail_width, file.thumbnail_height = thumbnail.size
                                file.save()

                            # Delete cache
                            s3.Object(settings.AWS_STORAGE_BUCKET_NAME,
                                cache_file.s3_object_key).delete()

            save_img_if_exists('image_one', 'image_one_cache_use', 'image_one_cache_file_id')
            save_img_if_exists('image_two', 'image_two_cache_use', 'image_two_cache_file_id')
            save_img_if_exists('image_three', 'image_three_cache_use', 'image_three_cache_file_id')

            save_user_agent(request, request.user.user)

            return HttpResponseRedirect(
                reverse('leads:lead_detail', args=(lead.slug_link,)))
    else:
        form = forms.LeadForm()

    return render(request, 'leads/lead_create.html', {
        'form': form,
        'countries': countries
    })

class LeadListView(ListView):
    template_name = 'leads/lead_list.html'
    model = relmods.Lead
    paginate_by = 8

    def get_queryset(self, **kwargs):
#         if self.request.user.is_authenticated:
#             user = self.request.user.user
#         else:
#             user = None

#         search = self.request.GET.get('search')
#         wants_to = self.request.GET.get('wants_to')
#         buy_country_str = self.request.GET.get('buy_country')
#         sell_country_str = self.request.GET.get('sell_country')
#         sort_by = self.request.GET.get('sort_by')

#         leads = relmods.Lead.objects

#         q = models.LeadQuery()
#         q.user = user
#         q.search = search
#         q.sort_by = sort_by

# # TODO the lead query is not saved properly
#         q.save()

#         if wants_to == 'buy':
#             leads = leads.filter(lead_type='buying')
#         elif wants_to == 'sell':
#             leads = leads.filter(lead_type='selling')
#         else:
#             wants_to = 'buy_or_sell'

#         if buy_country_str != 'any_country' and buy_country_str != None and\
#             buy_country_str.strip() != '':
#             buy_country = commods.Country.objects.get(
#                 programmatic_key=buy_country_str)
#             leads = leads.filter(buy_country=buy_country)
#             q.buy_country = buy_country

#         if sell_country_str != 'any_country' and sell_country_str != None and\
#             sell_country_str.strip() != '':
#             sell_country = commods.Country.objects.get(
#                 programmatic_key=sell_country_str)
#             leads = leads.filter(sell_country=sell_country)
#             q.sell_country = sell_country

#         vector = SearchVector('search_i_need_agents_veccol')
#         query = SearchQuery(search)
#         leads = leads.annotate(
#             search_i_need_agents_veccol=RawSQL(
#                 'search_i_need_agents_veccol', [],
#                 output_field=SearchVectorField()))\
#             .annotate(rank=SearchRank(vector, query))\
#             .order_by('-rank')
        
# # TODO: the sort_by keys here are wrong
#         if sort_by == 'timestamp':
#             leads = leads.order_by('-created')
#         elif sort_by == 'comm_percent_hi_lo':
#             leads = leads.order_by('-commissions')
#         elif sort_by == 'comm_percent_lo_hi':
#             leads = leads.order_by('commissions')
#         elif sort_by == 'comm_dollar_hi_lo':
#             leads = leads.order_by('-avg_deal_comm')
#         elif sort_by == 'comm_dollar_lo_hi':
#             leads = leads.order_by('avg_deal_comm')
#         elif sort_by == 'relevance':
#             leads = leads.order_by('-rank')
#         else:
#             leads = leads.order_by('-created')

#         save_user_agent(self.request, user)

        return models.Lead.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = get_countries()

        # Render search and country back into the template
        context['search_value'] = self.request.GET.get('search')
        context['wants_to_value'] = self.request.GET.get('wants_to')
        context['buy_country_value'] = self.request.GET.get('buy_country')
        context['sell_country_value'] = self.request.GET.get('sell_country')
        context['sort_by_value'] = self.request.GET.get('sort_by')

        return context

class AgentListView(ListView):
    template_name = 'leads/agent_list.html'
    context_object_name = 'agents'
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
        context['countries'] = get_countries()

        # Render search and country back into the template
        context['search_value'] = self.request.GET.get('search')
        context['country_value'] = self.request.GET.get('country')

        return context

@login_required
@csrf_exempt
def toggle_save_lead(request, slug):
    # Disallow saving of leads owned by the owner
    try:
        lead = models.Lead.objects.get(slug_link=slug)
        if lead.author.id == request.user.user.id:
            HttpResponseRedirect(reverse('leads:lead_detail', args=(slug,)))
    except models.Lead.DoesNotExist:
        HttpResponseRedirect(reverse('leads:lead_detail', args=(slug,)))

    def toggle():
        try:
            saved_lead = models.SavedLead.objects.get(
                saver=request.user.user,
                lead=lead
            )

            # Toggle save-unsave
            saved_lead.active = not saved_lead.active
            saved_lead.save()
        except models.SavedLead.DoesNotExist:
            saved_lead = models.SavedLead.objects.create(
                saver=request.user.user,
                lead=lead,
                active=True
            )
        
        return {'s': saved_lead.active}

    if request.method == 'POST':
        # AJAX call, toggle save-unsave, return JSON.
        return JsonResponse(toggle())

    # Unauthenticated call. User will be given the URL to click only if the
    # user is authenticated. Otherwise, a click on the 'save' button will
    # result in an AJAX post to this URL.
    #
    # Toggle save-unsave, redirect user to next URL.
    toggle()

    # Read 'next' URL from GET parameters. Redirect user there if the
    # parameter exists. Other redirect user to default lead details page.
    next_url = request.GET.get('next')
    if next_url is not None and len(next_url.strip()) > 0:
        return HttpResponseRedirect(next_url)
    else:
        return HttpResponseRedirect(
            reverse('leads:lead_detail', args=(slug,)))





# Deprecated
# class _LeadListView(ListView):
#     model = models.Lead
#     paginate_by = 54

#     def get_queryset(self, **kwargs):
#         title = self.request.GET.get('title')
#         details = self.request.GET.get('details')
#         buying = self.request.GET.get('buying')
#         selling = self.request.GET.get('selling')
#         direct = self.request.GET.get('direct')
#         broker = self.request.GET.get('broker')
#         user_country = self.request.GET.get('user_country')
#         lead_country = self.request.GET.get('lead_country')

#         cpa__initial_deposit_received = self.request.GET.get(
#             'cpa__initial_deposit_received')
#         cpa__goods_shipped = self.request.GET.get('cpa__goods_shipped')
#         cpa__buyer_received_goods_services = self.request.GET.get(
#             'cpa__buyer_received_goods_services')
#         cpa__full_payment_received = self.request.GET.get(
#             'cpa__full_payment_received')
#         cpa__others = self.request.GET.get('cpa__others')

#         leads = models.Lead.objects.all()

#         ffp = models.FilterFormPost()

#         if title is not None:
#             leads = leads.filter(title__icontains=title)
#             ffp.title = title

#         if details is not None:
#             leads = leads.filter(title__icontains=details)
#             ffp.details = details

#         if buying is not None and selling is not None:
#             pass # No need to filter
#         elif buying is not None:
#             leads = leads.filter(lead_type='buying')
#             ffp.is_buying = True
#         elif selling is not None:
#             leads = leads.filter(lead_type='selling')
#             ffp.is_selling = True

#         if direct is not None and broker is not None:
#             pass # No need to filter
#         elif direct is not None:
#             leads = leads.filter(author_type='direct')
#             ffp.is_direct = True
#         elif broker is not None:
#             leads = leads.filter(author_type='broker')
#             ffp.is_agent = True

#         if user_country is not None and user_country.strip() != '':
#             leads = leads.filter(author__country__programmatic_key=user_country)
#             ffp.user_country = user_country

#         if lead_country is not None and lead_country.strip() != '':
#             leads = leads.filter(country__programmatic_key=lead_country)
#             ffp.lead_country = lead_country

#         commission_payable_after_q = Q()
#         if cpa__initial_deposit_received is not None:
#             commission_payable_after_q = commission_payable_after_q |\
#                 Q(commission_payable_after='initial_deposit_received')
#             ffp.is_initial_deposit = True

#         if cpa__goods_shipped is not None:
#             commission_payable_after_q = commission_payable_after_q |\
#                 Q(commission_payable_after='goods_shipped')
#             ffp.is_goods_shipped = True

#         if cpa__buyer_received_goods_services is not None:
#             commission_payable_after_q = commission_payable_after_q |\
#                 Q(commission_payable_after='buyer_received_goods_services')
#             ffp.is_goods_received = True

#         if cpa__full_payment_received is not None:
#             commission_payable_after_q = commission_payable_after_q |\
#                 Q(commission_payable_after='full_payment_received')
#             ffp.is_payment_received = True

#         if cpa__others is not None:
#             commission_payable_after_q = commission_payable_after_q |\
#                 Q(commission_payable_after='others')
#             ffp.is_others = True

#         leads = leads.filter(commission_payable_after_q)

#         if self.request.user.is_authenticated:
#             try:
#                 ffp.user = self.request.user.user
#             except relmods.User.DoesNotExist:
#                 # Prevents error when I'm logging in as admin
#                 pass
        
#         ffp.save()
        
#         return leads.order_by('-created')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['countries'] = commods.Country.objects.order_by('name')
#         context['amplitude_api_key'] = settings.AMPLITUDE_API_KEY
#         if self.request.user.is_authenticated:
#             try:
#                 eb_user = self.request.user.user
#                 context['amplitude_user_id'] = eb_user.uuid
#                 context['country_code'] = eb_user.phone_number.country_code
#                 context['register_date_time'] = eb_user.registered.isoformat()
#                 sgtz = pytz.timezone(settings.TIME_ZONE)
#                 context['last_seen_date_time'] = datetime.now(tz=sgtz).isoformat()
#                 context['num_whatsapp_lead_author'] = \
#                     eb_user.num_whatsapp_lead_author()
#                 context['num_leads_created'] = eb_user.num_leads_created()
#             except relmods.User.DoesNotExist:
#                 # Prevents error when I'm logging in as admin
#                 pass

#         return context

# Deprecated
# @login_required
# def create_lead(request):
#     if request.method == 'POST':
#         form = forms.OldLeadForm(request.POST)
#         if form.is_valid():
#             # reCaptcha check
#             # Note: blocking
#             client_response = request.POST.get('g-recaptcha-response')
#             server_response = requests.post(
#                 settings.RECAPTCHA_VERIFICATION_URL, {
#                     'secret': settings.RECAPTCHA_SECRET,
#                     'response': client_response
#             })

#             sr = json.loads(server_response.text)
#             if sr.get('success') == True:
#                 # Disable recaptcha
#                 #  and sr.get('score') > \
#                 # float(settings.RECAPTCHA_THRESHOLD):
#                 lead = models.Lead.objects.create(
#                     author=request.user.user,
#                     title=form.cleaned_data.get('title'),
#                     details=form.cleaned_data.get('details'),
#                     lead_type=form.cleaned_data.get('lead_type'),
#                     author_type=form.cleaned_data.get('author_type'),
#                     country=commods.Country.objects.get(
#                         programmatic_key=form.cleaned_data.get('country')),
#                     commission_pct=form.cleaned_data.get('commission_pct'),
#                     commission_payable_after=form.cleaned_data.\
#                         get('commission_payable_after'),
#                     commission_payable_after_others=form.cleaned_data.\
#                         get('commission_payable_after_others'),
#                     other_comm_details=form.cleaned_data.\
#                         get('other_comm_details')
#                 )

#                 # Associate file with lead
#                 files = form.cleaned_data.get('files')
#                 if files.lower().strip() != '':
#                     file_datas = json.loads(files)
#                     for file_data in file_datas:
#                         uuid, _, filename = file_data
#                         file = fimods.File.objects.get(uuid=uuid)
#                         file.lead = lead
#                         file.filename = filename
#                         file.save()
                
#                 messages.info(request, 'Your lead has been posted.')

#                 return HttpResponseRedirect(reverse('leads__root:list'))
#             else:
#                 messages.info(request, 'Are you a robot? Please slow down. [' + str(sr.get('score')) + ']')
#     else:
#         form = forms.OldLeadForm()

#     countries = commods.Country.objects.order_by('name')

#     eb_user = request.user.user
#     sgtz = pytz.timezone(settings.TIME_ZONE)

#     return render(request, 'leads/create_lead.html', {
#         'form': form,
#         'countries': countries,
#         'amplitude_api_key': settings.AMPLITUDE_API_KEY,
#         'amplitude_user_id': eb_user.uuid,
#         'country_code': eb_user.phone_number.country_code,
#         'register_date_time': eb_user.registered.isoformat(),
#         'last_seen_date_time': datetime.now(tz=sgtz).isoformat(),
#         'num_whatsapp_lead_author': eb_user.num_whatsapp_lead_author(),
#         'num_leads_created': eb_user.num_leads_created()
#     })

# Deprecated
# @csrf_exempt
# class WriteOnlyPresignedURLView(fiviews.WriteOnlyPresignedURLView):
#     serializer_class = serializers.WriteOnlyPresignedURLSerializer

# Deprecated
# def lead_detail(request, uuid):
#     try:
#         lead = models.Lead.objects.get(uuid=uuid)
#     except models.Lead.DoesNotExist:
#         raise Http404('Lead does not exist')

#     contact_request = None

#     if request.method == 'POST':
#         form = forms.ContactForm(request.POST)
#         if form.is_valid():
#             if is_connected(request.user.user, lead):
#                 # Users are already connected - direct to WhatsApp.

#                 # Set message as a GET parameter
#                 message = form.cleaned_data.get('message')
#                 request.GET._mutable = True
#                 request.GET['text'] = message

#                 # Direct user to WhatsApp with the message in body
#                 HttpResponseRedirect(
#                     get_create_whatsapp_link(request.user.user, lead.author))
#             elif not has_contacted(request.user.user, lead):
#                 # User should not be able to send a post request if he has
#                 # already contacted the lead owner. Users are not connected
#                 # and requester have not contacted this lead before.

#                 # Create contact request
#                 message = form.cleaned_data.get('message')
#                 contact_request = models.ContactRequest.objects.create(
#                     contactor=request.user.user,
#                     lead=lead,
#                     message=message
#                 )

#                 # Ask lead author to confirm contact request
#                 send_contact_request_confirm(contact_request.id)

#                 # Add message
#                 messages.info(request, "Message sent. We'll notify you if the \
# author agrees to exchange contacts with you.")
#     else:
#         if request.user.is_authenticated:
#             # Update analytics for authenticated user
#             try:
#                 access = models.LeadDetailAccess.objects.get(
#                     lead=lead,
#                     accessor=request.user.user
#                 )
#                 access.access_count += 1
#                 access.save()
#             except models.LeadDetailAccess.DoesNotExist:
#                 access = models.LeadDetailAccess.objects.create(
#                     lead=lead,
#                     accessor=request.user.user,
#                     access_count=1
#                 )

#             if is_connected(request.user.user, lead):
#                 # Users are already connected, show an empty form which will allow
#                 # the requester to WhatsApp the lead author directly.
#                 form = forms.ContactForm()
#             elif has_contacted(request.user.user, lead):
#                 # Users are not connected but requester have contacted this
#                 # lead before. Users are not connected but requester have contacted
#                 # this lead before.
            
#                 # Get contact request
#                 contact_request = models.ContactRequest.objects.get(
#                     contactor=request.user.user,
#                     lead=lead
#                 )

#                 # Show message from contact request
#                 form = forms.ContactForm({
#                     'message': contact_request.message
#                 })
#             else:
#                 form = forms.ContactForm()
#         else:
#             # User are not connected and requester have not contact lead author.
#             # Show an empty form which will allow the requester to contact the
#             # lead owner. Note: we do not merge this condition with is_connected
#             # for clarity's sake.
#             form = forms.ContactForm()

#     return render(request, 'leads/lead_detail.html', {
#         'lead': lead,
#         'form': form,
#         'contact_request': contact_request
#     })

# Deprecated
# def contact_request_detail(request, uuid):
#     contact_request = models.ContactRequest.objects.get(uuid=uuid)
#     if request.method == 'POST':
#         # Exchange contact with the contactor (requester is the lead owner).
        
#         contact_request.response = 'accept'
#         contact_request.save()

#         # Send message to both parties.
#         send_contact_request_exchanged_author.delay(contact_request.id)
#         send_contact_request_exchanged_contactor.delay(contact_request.id)

#     return render(request, 'leads/contactrequest_detail.html', {
#         'contact_request': contact_request,
#         'whatsapp_link': get_create_whatsapp_link(
#             contact_request.lead.author,
#             contact_request.contactor)
#     })

# Deprecated
# class ContactRequestListView(LoginRequiredMixin, ListView):
#     model = models.ContactRequest
#     paginate_by = 30

#     def get_queryset(self):
#         return models.ContactRequest.objects.filter(
#             lead__author=self.request.user.user)