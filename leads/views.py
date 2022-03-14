from urllib.parse import urljoin
import boto3
from PIL import Image, ImageOps
from io import BytesIO

from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models.expressions import RawSQL
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchVectorField

from everybase import settings
from common import models as commods
from files.utilities.delete_file import delete_file
from leads import models, forms
from relationships import models as relmods
from relationships.utilities.save_user_agent import save_user_agent
from files import models as fimods
from files.utilities.get_mime_type import get_mime_type

def get_countries():
    return commods.Country.objects.annotate(
        number_of_users=Count('users_w_this_country'))\
            .order_by('-number_of_users')

def save_thumbnail(image, s3, thumb_key, mime_type, file):
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

def save_img_if_exists(
        image_key,
        image_cache_use_key,
        image_cache_file_id_key,
        request,
        lead,
        form
    ):

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
    #
    # Though we're dealing with 'cache' images - i.e., cached images that's a
    # result of failed form validation - 'cache' images can also refer to
    # actual lead images. We set actual lead images as cache when we're editing
    # a post.

    # Helper to get cleaned data
    get = lambda s : form.cleaned_data.get(s)

    image = request.FILES.get(image_key)

    image_cache_use = get(image_cache_use_key)

    if image_cache_use is not None and image_cache_use == 'no':
        # Doesn't matter if this image is a cache image (that's set as a
        # result of failed form validation) or an actual lead image (that's
        # set as a result of an edit operation), delete this image if the
        # frontend indicates that we no longer need this image.
        image_cache_file_id = get(image_cache_file_id_key)
        delete_file(image_cache_file_id)

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

        save_thumbnail(image, s3, thumb_key, mime_type, file)
    else:
        # Image does not exist

        image_cache_file_id = get(image_cache_file_id_key)

        if image_cache_file_id is not None and \
            len(image_cache_file_id.strip()) > 0 and \
            image_cache_use == 'yes':
            # Frontend indicates use-cache, and we have the details to do so.

            cache_file = fimods.File.objects.get(pk=image_cache_file_id)

            # If this file is NOT a cache, i.e. - its ID and URL were set in an
            # edit operation, we do not need to copy it from a cache location
            # to an actual lead image location. We create a test key here to
            # ascertain if the cache file is located in an actual lead image
            # location. If equal, the image is not a 'cache' that's created as a
            # result of form validation failure (though we name it as such).
            # Instead, the ID and URL were set in an edit operation.
            test_key = settings.AWS_S3_KEY_LEAD_IMAGE % (lead.id, cache_file.id)
            if cache_file.deleted is None and \
                cache_file.s3_object_key != test_key:
                # Cache is valid and not an actual lead image, copy cache
                # to actual lead image location.
                
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

                save_thumbnail(cache, s3, thumb_key, cache_file.mime_type, lead_file)

                # Delete cache
                delete_file(cache_file.id)

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
def lead_edit(request, slug):
    lead = models.Lead.objects.get(slug_link=slug)

    # If requester does not own lead - redirect to lead detail
    if request.user.user.id != lead.author.id:
        return HttpResponseRedirect(reverse('leads:lead_detail', args=(slug)))

    if request.method == 'POST':
        form = forms.LeadForm(request.POST, request.FILES)
        if form.is_valid():

            # Helper to get cleaned data
            get = lambda s : form.cleaned_data.get(s)

            # Helper to get country or not (i.e., any country)
            get_country = lambda c : commods.Country.objects.get(programmatic_key=c) if c != 'any_country' else None

            # Update lead
            need_agent = get('need_agent')
            commission_type = get('commission_type')
            author_type = get('author_type')
            need_logistics_agent = get('need_logistics_agent')
            lead.lead_type = get('lead_type')
            lead.author_type = author_type
            lead.buy_country = get_country(get('buy_country'))
            lead.sell_country = get_country(get('sell_country'))
            lead.details = get('details')
            lead.need_agent = need_agent
            lead.commission_type = commission_type if need_agent else None
            lead.commission_type_other = get('commission_type_other') if need_agent and commission_type == 'other' else None
            lead.commission = get('commission') if need_agent and commission_type == 'percentage' else None
            lead.avg_deal_size = get('avg_deal_size') if need_agent and commission_type == 'percentage' else None
            lead.is_comm_negotiable = get('is_comm_negotiable') if need_agent else None
            lead.commission_payable_after = get('commission_payable_after') if need_agent else None
            lead.commission_payable_after_other = get('commission_payable_after_other') if need_agent else None
            lead.commission_payable_by = get('commission_payable_by') if need_agent and author_type == 'broker' else None
            lead.other_agent_details = get('other_agent_details') if need_agent else None
            lead.need_logistics_agent = need_logistics_agent
            lead.logistics_agent_details=get('logistics_agent_details') if need_logistics_agent else None
            lead.save()

            save_img_if_exists('image_one', 'image_one_cache_use', 'image_one_cache_file_id', request, lead, form)
            save_img_if_exists('image_two', 'image_two_cache_use', 'image_two_cache_file_id', request, lead, form)
            save_img_if_exists('image_three', 'image_three_cache_use', 'image_three_cache_file_id', request, lead, form)

            return HttpResponseRedirect(reverse('leads:lead_detail', args=(slug,)))
    else:
        initial = {
            'lead_type': lead.lead_type,
            'author_type': lead.author_type,
            'buy_country': lead.buy_country.programmatic_key,
            'sell_country': lead.sell_country.programmatic_key,
            'details': lead.details,
            'need_agent': lead.need_agent,
            'commission_type': lead.commission_type,
            'commission_type_other': lead.commission_type_other,
            'commission': lead.commission,
            'avg_deal_size': lead.avg_deal_size,
            'is_comm_negotiable': lead.is_comm_negotiable,
            'commission_payable_after': lead.commission_payable_after,
            'commission_payable_after_other': lead.commission_payable_after_other,
            'commission_payable_by': lead.commission_payable_by,
            'other_agent_details': lead.other_agent_details,
            'need_logistics_agent': lead.need_logistics_agent,
            'logistics_agent_details': lead.logistics_agent_details
        }

        names = [
            ('image_one_cache_file_id', 'image_one_cache_url'),
            ('image_two_cache_file_id', 'image_two_cache_url'),
            ('image_three_cache_file_id', 'image_three_cache_url')
        ]
        for i, f in enumerate(lead.display_images()):
            # File ID
            initial[names[i][0]] = f.id

            # File URL
            initial[names[i][1]] = urljoin(settings.MEDIA_URL, f.s3_object_key)

        form = forms.LeadForm(initial=initial)

    return render(request, 'leads/lead_edit.html', {
        'form': form,
        'slug_link': lead.slug_link,
        'countries': get_countries()
    })

@login_required
def lead_create(request):
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
                logistics_agent_details=get('logistics_agent_details') if need_logistics_agent else None
            )

            save_img_if_exists('image_one', 'image_one_cache_use', 'image_one_cache_file_id', request, lead, form)
            save_img_if_exists('image_two', 'image_two_cache_use', 'image_two_cache_file_id', request, lead, form)
            save_img_if_exists('image_three', 'image_three_cache_use', 'image_three_cache_file_id', request, lead, form)

            save_user_agent(request, request.user.user)

            return HttpResponseRedirect(
                reverse('leads:lead_detail', args=(lead.slug_link,)))
    else:
        form = forms.LeadForm()

    return render(request, 'leads/lead_create.html', {
        'form': form,
        'countries': get_countries()
    })

def lead_list(request):
    if request.method == 'GET':
        user = request.user.user if request.user.is_authenticated else None

        get = lambda s : request.GET.get(s)

        commented_only = get('commented_only')

        saved_only = get('saved_only')
        buy_sell = get('buy_sell')
        direct_middleman = get('direct_middleman')
        buy_country = get('buy_country')
        sell_country = get('sell_country')
        goods_services = get('goods_services')
        need_agent = get('need_agent')
        commission_type = get('commission_type')
        commission_type_other = get('commission_type_other')
        min_commission = get('min_commission')
        max_commission = get('max_commission')
        min_avg_deal = get('min_avg_deal')
        max_avg_deal = get('max_avg_deal')
        comm_negotiable = get('comm_negotiable')
        commission_payable_after = get('commission_payable_after')
        commission_payable_after_other = get('commission_payable_after_other')
        other_agent_details = get('other_agent_details')
        need_logistics_agent = get('need_logistics_agent')
        logistics_agent_details = get('logistics_agent_details')

        leads = models.Lead.objects.all()

        is_not_empty = lambda s : s is not None and s.strip() != ''
        match = lambda t, v: is_not_empty(t) and t == v

        if user is not None:
            # Allow commented-only and saved-only if the user is authenticated

            if match(commented_only, 'on'):
                # Commented only is checked
                commented_leads = models.LeadComment.objects.filter(
                    commentor=user,
                    deleted__isnull=True
                ).values('lead')

                leads = leads.filter(id__in=commented_leads)
            
            if match(saved_only, 'on'):
                # Saved only is checked
                saved_leads = models.SavedLead.objects.filter(
                    saver=user,
                    deleted__isnull=True,
                    active=True
                ).values('lead')

                leads = leads.filter(id__in=saved_leads)

        # Buy sell
        if match(buy_sell, 'buy'):
            leads = leads.filter(lead_type='buying')
        elif buy_sell == 'sell':
            leads = leads.filter(lead_type='selling')

        # Direct middleman
        if match(direct_middleman, 'direct'):
            leads = leads.filter(author_type='direct')
        elif direct_middleman == 'middleman':
            leads = leads.filter(author_type='broker')

        if is_not_empty(buy_country) and buy_country.strip() != 'any_country':
            # Buy country is selected
            c = commods.Country.objects.get(programmatic_key=buy_country)
            leads = leads.filter(buy_country=c)

        if is_not_empty(sell_country) and sell_country.strip() != 'any_country':
            # Sell country is selected
            c = commods.Country.objects.get(programmatic_key=sell_country)
            leads = leads.filter(sell_country=c)

        order_by = []

        if is_not_empty(goods_services):
            # Goods services details is filled
            details_vec = SearchVector('details_vec')
            goods_services_qry = SearchQuery(goods_services)
            leads = leads.annotate(
                details_vec=RawSQL('details_vec', [],
                    output_field=SearchVectorField()))\
                .annotate(goods_services_rank=SearchRank(details_vec, goods_services_qry))
            
            order_by.append('-goods_services_rank')

        if match(need_agent, 'on'):
            # Need agent is checked
            leads = leads.filter(need_agent=True)

        # Commission type
        if match(commission_type, 'percentage'):
            leads = leads.filter(commission_type='percentage')
        elif commission_type == 'other':
            leads = leads.filter(commission_type='other')

        if is_not_empty(commission_type_other):
            # Commission type other details is filled
            commission_type_other_vec = SearchVector('commission_type_other_vec')
            commission_type_other_qry = SearchQuery(commission_type_other)
            leads = leads.annotate(
                commission_type_other_vec=RawSQL('commission_type_other_vec', [],
                    output_field=SearchVectorField()))\
                .annotate(commission_type_other_rank=SearchRank(
                    commission_type_other_vec,
                    commission_type_other_qry
                ))
            
            order_by.append('-commission_type_other_rank')

        if is_not_empty(min_commission):
            # Minimum commission is filled
            try:
                leads = leads.filter(commission__gte=float(min_commission))
            except Exception:
                pass
        
        if is_not_empty(max_commission):
            # Maximum commission is filled
            try:
                leads = leads.filter(commission__lte=float(max_commission))
            except Exception:
                pass

        if is_not_empty(min_avg_deal):
            # Minimum average deal is filled
            try:
                leads = leads.filter(avg_deal_size__gte=float(min_avg_deal))
            except Exception:
                pass
        
        if is_not_empty(max_avg_deal):
            # Maximum average deal is filled
            try:
                leads = leads.filter(avg_deal_size__lte=float(max_avg_deal))
            except Exception:
                pass
        
        # Is commission negotiable
        if match(comm_negotiable, 'not_negotiable'):
            leads = leads.filter(is_comm_negotiable=False)
        if comm_negotiable == 'negotiable':
            leads = leads.filter(is_comm_negotiable=True)

        # Commission payable after
        if match(commission_payable_after, 'initial_deposit_received'):
            leads = leads.filter(commission_payable_after='initial_deposit_received')
        elif commission_payable_after == 'goods_shipped':
            leads = leads.filter(commission_payable_after='goods_shipped')
        elif commission_payable_after == 'buyer_received_goods_services':
            leads = leads.filter(commission_payable_after='buyer_received_goods_services')
        elif commission_payable_after == 'full_payment_received':
            leads = leads.filter(commission_payable_after='full_payment_received')
        elif commission_payable_after == 'other':
            leads = leads.filter(commission_payable_after='other')
            if is_not_empty(commission_payable_after_other):
                # Commission payable after other details is filled
                commission_payable_after_other_vec = SearchVector('commission_payable_after_other_vec')
                commission_payable_after_other_qry = SearchQuery(commission_payable_after_other)
                leads = leads.annotate(
                    commission_payable_after_other_vec=RawSQL('commission_payable_after_other_vec', [],
                        output_field=SearchVectorField()))\
                    .annotate(commission_payable_after_other_rank=SearchRank(
                        commission_payable_after_other_vec,
                        commission_payable_after_other_qry
                    ))
                
                order_by.append('-commission_payable_after_other_rank')

        if is_not_empty(other_agent_details):
            # Other agent details is filled
            other_agent_details_vec = SearchVector('other_agent_details_vec')
            other_agent_details_qry = SearchQuery(other_agent_details)
            leads = leads.annotate(
                other_agent_details_vec=RawSQL('other_agent_details_vec', [],
                    output_field=SearchVectorField()))\
                .annotate(other_agent_details_rank=SearchRank(
                    other_agent_details_vec,
                    other_agent_details_qry
                ))
            
            order_by.append('-other_agent_details_rank')
        
        if match(need_logistics_agent, 'on'):
            # Need logistics agent is checked
            leads = leads.filter(need_logistics_agent=True)

            if is_not_empty(logistics_agent_details):
                # Logistics agent details is filled
                other_logistics_agent_details_vec = SearchVector('other_logistics_agent_details_vec')
                other_logistics_agent_details_qry = SearchQuery(logistics_agent_details)
                leads = leads.annotate(
                    other_logistics_agent_details_vec=RawSQL('other_logistics_agent_details_vec', [],
                        output_field=SearchVectorField()))\
                    .annotate(other_logistics_agent_details_rank=SearchRank(
                        other_logistics_agent_details_vec,
                        other_logistics_agent_details_qry
                    ))
                
                order_by.append('-other_logistics_agent_details_rank')

        order_by.append('-created')

        # Save lead query if it's not the default (empty) form post
        if is_not_empty(commented_only) or is_not_empty(saved_only) or\
            not match(buy_sell, 'all') or not match(direct_middleman, 'all') or\
            not match(buy_country, 'any_country') or not match(sell_country, 'any_country') or\
            is_not_empty(goods_services) or is_not_empty(need_agent) or\
            not match(commission_type, 'all') or is_not_empty(commission_type_other) or\
            is_not_empty(min_commission) or is_not_empty(max_commission) or\
            is_not_empty(min_avg_deal) or is_not_empty(max_avg_deal) or\
            not match(comm_negotiable, 'all') or not match(commission_payable_after, 'all') or\
            is_not_empty(commission_payable_after_other) or is_not_empty(other_agent_details) or\
            is_not_empty(need_logistics_agent) or is_not_empty(logistics_agent_details):
            models.LeadQuery.objects.create(
                user=user,
                commented_only=commented_only,
                saved_only=saved_only,
                buy_sell=buy_sell,
                direct_middleman=direct_middleman,
                buy_country=buy_country,
                sell_country=sell_country,
                goods_services=goods_services,
                need_agent=need_agent,
                commission_type=commission_type,
                commission_type_other=commission_type_other,
                min_commission=min_commission,
                max_commission=max_commission,
                min_avg_deal=min_avg_deal,
                max_avg_deal=max_avg_deal,
                comm_negotiable=comm_negotiable,
                commission_payable_after=commission_payable_after,
                commission_payable_after_other=commission_payable_after_other,
                other_agent_details=other_agent_details,
                need_logistics_agent=need_logistics_agent,
                logistics_agent_details=logistics_agent_details
            )

        # Order leads
        leads = leads.order_by(*order_by)

        # Set context parameters
        params = {}

        params['countries'] = get_countries()
        params['commented_only'] = get('commented_only')
        params['saved_only'] = get('saved_only')
        params['buy_sell'] = get('buy_sell')
        params['direct_middleman'] = get('direct_middleman')
        params['buy_country'] = get('buy_country')
        params['sell_country'] = get('sell_country')
        params['goods_services'] = get('goods_services')

        need_agent = get('need_agent')
        params['need_agent'] = get('need_agent')

        if match(need_agent, 'on'):
            commission_type = get('commission_type')
            params['commission_type'] = commission_type

            if commission_type == 'others' or commission_type == 'all':
                params['commission_type_other'] = get('commission_type_other')
            
            if commission_type == 'percentage' or commission_type == 'all':
                params['min_commission'] = get('min_commission')
                params['max_commission'] = get('max_commission')
                params['min_avg_deal'] = get('min_avg_deal')
                params['max_avg_deal'] = get('max_avg_deal')
            
            params['comm_negotiable'] = get('comm_negotiable')
            params['commission_payable_after'] = get('commission_payable_after')
            params['commission_payable_after_other'] = get('commission_payable_after_other')
            params['other_agent_details'] = get('other_agent_details')
        
        need_logistics_agent = get('need_logistics_agent')
        params['need_logistics_agent'] = need_logistics_agent

        if match(need_logistics_agent, 'on'):
            params['logistics_agent_details'] = get('logistics_agent_details')

        # Paginate

        leads_per_page = 8
        paginator = Paginator(leads, leads_per_page)

        page_number = request.GET.get('page')
        
        page_obj = paginator.get_page(page_number)
        params['page_obj'] = page_obj

        return render(request, 'leads/lead_list.html', params)

@login_required
@csrf_exempt
def toggle_save_lead(request, slug):
    try:
        lead = models.Lead.objects.get(slug_link=slug)
    except models.Lead.DoesNotExist:
        return HttpResponseRedirect(reverse('leads:lead_detail', args=(slug,)))

    # Disallow saving of leads owned by the owner
    if lead.author.id == request.user.user.id:
        return HttpResponseRedirect(reverse('leads:lead_detail', args=(slug,)))

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