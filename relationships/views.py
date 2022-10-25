from common.tasks.delete_files import delete_files
from common.tasks.send_email import send_email

import boto3, json, pytz, uuid
from PIL import Image, ImageOps
from io import BytesIO
from datetime import datetime
from ratelimit.decorators import ratelimit

from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.http import Http404, HttpResponse

from everybase import settings

from django.views.decorators.csrf import csrf_exempt
from files.utilities.get_mime_type import get_mime_type

from common import models as commods

from relationships import forms, models
from relationships.tasks.send_email_code import send_email_code
from relationships.tasks.send_whatsapp_code import send_whatsapp_code
from relationships.utilities.get_or_create_phone_number import \
    get_or_create_phone_number
from relationships.utilities.get_whatsapp_url import get_whatsapp_url
from relationships.utilities.get_or_create_email import get_or_create_email
from relationships.utilities.use_email_code import use_email_code
from relationships.utilities.use_whatsapp_code import use_whatsapp_code
from relationships.constants import email_purposes, whatsapp_purposes

from relationships.tasks.clear_files import clear_files as _clear_files
from relationships.tasks.delete_objs import delete_objs as _delete_objs
from relationships.tasks.delete_status_file import delete_status_file as \
    _delete_status_file
from relationships.tasks.delete_review_file import delete_review_file as \
    _delete_review_file

from common.tasks.send_amplitude_event import send_amplitude_event
from common.tasks.identify_amplitude_user import identify_amplitude_user

from common.utilities.get_ip_address import get_ip_address

from files import models as fimods

MESSAGE_KEY__PROFILE_UPDATE_SUCCESS = 'MESSAGE_KEY__PROFILE_UPDATE_SUCCESS'
MESSAGE_KEY__EMAIL_UPDATE_TRY_AGAIN = 'MESSAGE_KEY__EMAIL_UPDATE_TRY_AGAIN'
MESSAGE_KEY__EMAIL_UPDATE_SUCCESS = 'MESSAGE_KEY__EMAIL_UPDATE_SUCCESS'
MESSAGE_KEY__PHONE_NUMBER_UPDATE_TRY_AGAIN = \
    'MESSAGE_KEY__PHONE_NUMBER_UPDATE_TRY_AGAIN'
MESSAGE_KEY__PHONE_NUMBER_UPDATE_SUCCESS = \
    'MESSAGE_KEY__PHONE_NUMBER_UPDATE_SUCCESS'

# Helper functions

def _append_next(url, next):
    """Append next URL to input URL as a GET parameter."""
    if next is not None and next.strip() != '':
        url += f'?next={next}'
    return url

# Login/logout

def log_out(request):
    logout(request)
    return redirect('home')

# Registration

def register__enter_whatsapp(request):
    # If user is already authenticated and registered, direct user to detail.
    if request.user.is_authenticated:
        return redirect('user_detail', request.user.user.phone_number.value())
    
    if request.method == 'POST':
        form = forms.RegisterEnterWhatsAppForm(request.POST)
        if form.is_valid():
            phone_number, _ = get_or_create_phone_number(
                form.cleaned_data.get('phone_number'))

            # Find Everybase user with this phone number, but has not completed
            # registration. If such a user exists, use it. If not, create a
            # new one.

            user = models.User.objects.filter(
                phone_number=phone_number, # Has this phone number
                registered__isnull=True # Not completed registration
            ).first()

            if user is None:
                # No unregistered user with this phone number. Create a new one.
                user = models.User.objects.create(phone_number=phone_number)

            # Get list of countries matching this phone number's country code.
            countries = commods.Country.objects.filter(
                country_code=phone_number.country_code)

            if countries.count() == 1:
                # Phone number matches exactly 1 country.
                # Link this country to the user.
                user.country = countries.first()
                user.save()

                # Send WhatsApp confirmation code.
                send_whatsapp_code.delay(
                    user.id, whatsapp_purposes.VERIFY_WHATSAPP)

                # User's country is determined. Direct to confirm WhatsApp code
                # rightaway.
                target_name = 'register:confirm_whatsapp'
            else:
                # User's country is not determined (there're a few matching
                # countries). Direct user to select his country.
                target_name = 'register:select_country'

            return redirect(_append_next(
                reverse(target_name, args=(user.id,)),
                form.cleaned_data.get('next')))
    else:
        form = forms.RegisterEnterWhatsAppForm(
            initial={'next': request.GET.get('next')})

    return TemplateResponse(
        request, 'relationships/register__enter_whatsapp.html', {'form': form})

def register__select_country(request, user_id):
    # If user is already authenticated and registered, direct user to detail.
    if request.user.is_authenticated:
        return redirect('user_detail', request.user.user.phone_number.value())

    # Prevent access of a non-existent user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return redirect('register:start')

    if request.method == 'POST':
        form = forms.RegisterSelectCountryForm(request.POST)
        if form.is_valid():
            # Associate country with user.
            user.country = commods.Country.objects.get(
                programmatic_key=form.cleaned_data.get('country'))
            user.save()

            return redirect(_append_next(
                reverse('register:confirm_whatsapp', args=(user.id,)),
                form.cleaned_data.get('next')))
    else:
        form = forms.RegisterSelectCountryForm(
            initial={'next': request.GET.get('next')})

    return TemplateResponse(request,
        'relationships/register__select_country.html', {
            'user': user,
            'form': form,
            'countries': commods.Country.objects.filter(
                country_code=user.phone_number.country_code)
        })

@csrf_exempt
def register__resend_whatsapp_code(request, user_id):
    # Prevent access of a non-existent user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return Http404(None) # No error message for security reasons.

    # Prevent access of a non-registering user.
    if user.registered is not None:
        return Http404(None) # No error message for security reasons.

    if request.method == 'POST':
        send_whatsapp_code(user.id, whatsapp_purposes.VERIFY_WHATSAPP)
        return HttpResponse(status=204)

def register__confirm_whatsapp(request, user_id):
    # If user is already authenticated and registered, direct user to detail.
    if request.user.is_authenticated:
        return redirect('user_detail', request.user.user.phone_number.value())

    # Prevent access of a non-existent user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return redirect('register:start')

    if request.method == 'POST':
        form = forms.RegisterConfirmWhatsAppForm(request.POST, user=user)
        if form.is_valid():
            use_whatsapp_code(user, whatsapp_purposes.VERIFY_WHATSAPP)

            return redirect(_append_next(
                reverse('register:enter_profile', args=(user.id,)),
                form.cleaned_data.get('next')
            ))
    else:
        # Send WhatsApp confirmation code and redirect user to confirm it.
        send_whatsapp_code.delay(user.id, whatsapp_purposes.VERIFY_WHATSAPP)
        form = forms.RegisterConfirmWhatsAppForm(
            user=user,
            initial={'next': request.GET.get('next')})

    return TemplateResponse(request,
        'relationships/register__confirm_whatsapp.html', {
            'form': form,
            'user': user
        })

def register__enter_profile(request, user_id):
    # If user is already authenticated and registered, direct user to detail.
    if request.user.is_authenticated:
        return redirect('user_detail', request.user.user.phone_number.value())

    # Prevent access of a non-existent user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return redirect('register:start')

    if request.method == 'POST':
        form = forms.RegisterEnterProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = get_or_create_email(form.cleaned_data.get('email'))
            user.business_name = form.cleaned_data.get('business_name')
            user.business_address = form.cleaned_data.get('business_address')
            user.business_description = \
                form.cleaned_data.get('business_description')
            user.save()

            send_email_code(user.id, email_purposes.REGISTER)

            return redirect(_append_next(
                reverse('register:confirm_email', args=(user.id,)),
                form.cleaned_data.get('next')
            ))
    else:
        form = forms.RegisterEnterProfileForm(
            initial={'next': request.GET.get('next')})

    return TemplateResponse(request,
        'relationships/register__enter_profile.html', {
            'form': form,
            'user': user
        })

@csrf_exempt
def register__resend_email_code(request, user_id):
    # Prevent access of a non-existent user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return Http404(None) # No error message for security reasons.

    # Prevent access of a non-registering user.
    if user.registered is not None:
        return Http404(None) # No error message for security reasons.

    if request.method == 'POST':
        send_email_code(user.id, email_purposes.VERIFY_EMAIL)
        return HttpResponse(status=204)

def register__confirm_email(request, user_id):
    # If user is already authenticated and registered, direct user to detail.
    if request.user.is_authenticated:
        return redirect('user_detail', request.user.user.phone_number.value())

    # Prevent the access of a non-existent user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return redirect('register:start')

    if request.method == 'POST':
        form = forms.RegisterConfirmEmailForm(request.POST, user=user)
        if form.is_valid():
            use_email_code(user, email_purposes.REGISTER)

            # Create/link Django user
            user.django_user, _ = \
                DjangoUser.objects.get_or_create(username=str(user.id))

            # Update user profile
            sgtz = pytz.timezone(settings.TIME_ZONE)
            user.registered = datetime.now(sgtz)

            user.save()

            # Authenticate passwordlessly
            dju = authenticate(user.django_user.username)
            if dju is not None:
                login(request, dju)

            return redirect(_append_next(
                reverse('register:enter_status', args=(user.id,)),
                form.cleaned_data.get('next')
            ))
    else:
        form = forms.RegisterConfirmEmailForm(
            user=user,
            initial={'next': request.GET.get('next')})

    return TemplateResponse(request,
        'relationships/register__confirm_email.html', {
            'form': form,
            'user': user
        })

@login_required
def register__enter_status(request, user_id):
    # Prevent the access of a non-existent user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return redirect('register:start')

    # Prevent the access of another user.
    if user.id != request.user.user.id:
        return redirect('user_detail', user.phone_number.value())

    # Prevent access to this view if status has already been set.
    if user.status_updated is not None:
        return redirect('user_detail', user.phone_number.value())

    if request.method == 'POST':
        form = forms.RegisterEnterStatusForm(request.POST)
        if form.is_valid():
            form_uuid = form.cleaned_data.get('form_uuid')

            status_files = models.StatusFile.objects\
                .filter(user=user)\
                .exclude(form_uuid=form_uuid)

            delete_objs = []
            for sf in status_files:
                file = sf.file
                delete_objs.append({'Key': file.s3_object_key})
                delete_objs.append({'Key': file.thumbnail_s3_object_key})
                sf.delete()
                file.delete()
            
            # Delete orphan files if any.
            if len(delete_objs) > 0:
                delete_files.delay(delete_objs)

            user.status = form.cleaned_data.get('status')
            sgtz = pytz.timezone(settings.TIME_ZONE)
            now = datetime.now(tz=sgtz)
            user.status_updated = now
            user.save()

            # Activate files that were submitted with this form.
            files = models.StatusFile.objects.filter(form_uuid=form_uuid)
            for file in files:
                file.activated = now
                file.save()

            next = form.cleaned_data.get('next')
            if next is not None and next.strip() != '':
                return redirect(next)
            else:
                return redirect('user_detail', user.phone_number.value())
    else:
        form = forms.RegisterEnterStatusForm(
            initial={'next': request.GET.get('next')})

    return TemplateResponse(request,
        'relationships/register__enter_status.html', {
            'form': form,
            'user': user,
            'form_uuid': uuid.uuid4()
        })

@login_required
@csrf_exempt
def upload_status_file(request, user_id):
    # Prevent access of a non-existent user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        raise Http404(None) # No message for security reasons.

    # Prevent the access of another user.
    if user.id != request.user.user.id:
        return HttpResponse(status=204)

    form_uuid = request.POST.get('form_uuid')

    _clear_files.delay(user.id, form_uuid, False)

    try:
        # Deny file creation if maximum number of images is exceeded.
        if models.StatusFile.objects\
            .filter(user=user, form_uuid=form_uuid).count() > \
                settings.MAX_STATUS_IMAGES:
            return HttpResponse(status=400)

        file_object = request.FILES.get('file')

        mime_type = get_mime_type(file_object)

        file = fimods.File.objects.create(
            uploader=user,
            mime_type=mime_type,
            filename=file_object.name,
            s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
            thumbnail_s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
        )

        key = settings.AWS_S3_KEY_STATUS_IMAGE % (user.id, file.id)
        thumb_key = settings.AWS_S3_KEY_STATUS_IMAGE_THUMBNAIL % (user.id,
            file.id)

        bucket = boto3.session.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        ).resource('s3').Bucket(settings.AWS_STORAGE_BUCKET_NAME)

        s3_obj = bucket.put_object(
            Key=key,
            Body=file_object,
            ContentType=mime_type
        )

        # Update file with S3 results
        file.s3_object_key = key
        file.thumbnail_s3_object_key = thumb_key
        file.s3_object_content_length = s3_obj.content_length
        file.e_tag = s3_obj.e_tag
        file.content_type = s3_obj.content_type
        file.last_modified = s3_obj.last_modified
        file.save()

        # Resize, save thumbnail, record sizes
        with Image.open(file_object) as im:
            # Resize preserving aspect ratio cropping from the center
            thumbnail = ImageOps.fit(im, settings.STATUS_IMAGE_THUMBNAIL_SIZE)
            output = BytesIO()
            thumbnail.save(output, format='PNG')
            output.seek(0)

            # Upload thumbnail
            bucket.put_object(
                Key=thumb_key,
                Body=output,
                ContentType=mime_type
            )

            # Update file and thumbnail sizes
            file.width, file.height = im.size
            file.thumbnail_width, file.thumbnail_height = thumbnail.size
            file.save()

        # Create new status file for this user
        models.StatusFile.objects.create(
            form_uuid=form_uuid,
            user=user,
            file=file,
            file_uuid=file.filename
        )
    except:
        return HttpResponse(status=500)
    
    return HttpResponse(status=204)

@login_required
@csrf_exempt
def delete_status_file(request, user_id):
    # Prevent access of a non-existent user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        raise Http404(None) # No message for security reasons.

    # Prevent the access of another user.
    if user.id != request.user.user.id:
        return HttpResponse(status=204)

    params = json.loads(request.body)
    file_uuid = params.get('file_uuid')
    form_uuid = params.get('form_uuid')

    _delete_status_file.delay(user_id, file_uuid, form_uuid)

    return HttpResponse(status=204)

@login_required
@csrf_exempt
def clear_files(request, user_id):
    # Prevent access of a non-existent user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        raise Http404(None) # No message for security reasons.

    # Prevent the access of another user.
    if user.id != request.user.user.id:
        return HttpResponse(status=204)

    status_files_to_delete = models.StatusFile.objects\
        .filter(user=user, activated__isnull=True)

    objs = []

    for sf in status_files_to_delete:
        file = sf.file
        objs.append({'Key': file.s3_object_key})
        objs.append({'Key': file.thumbnail_s3_object_key})
        sf.delete()
        file.delete()

    review_files_to_delete = models.ReviewFile.objects\
        .filter(reviewer=user, activated__isnull=True)

    for rf in review_files_to_delete:
        file = rf.file
        objs.append({'Key': file.s3_object_key})
        objs.append({'Key': file.thumbnail_s3_object_key})
        rf.delete()
        file.delete()

    _delete_objs.delay(objs)

    return HttpResponse(status=204)

def _get_phone_user(phone_number):
    p, _ = get_or_create_phone_number(f'+{phone_number}')
    if p is None:
        raise Http404(None) # Don't give too much information.

    try:
        user = models.User.objects.filter(phone_number=p).first()
    except models.User.DoesNotExist:
        user = None

    return (p, user)

def _user_detail__status_update(request, phone_number, user, route, template,
    more_params={}):
    """Shared status update code for all user detail views with status update
    form.
    """
    if request.method == 'POST':
        # Prevent the access of another user.
        if user.id != request.user.user.id:
            return redirect(route, user.phone_number.value())

        form = forms.UserDetailUpdateStatusForm(request.POST)
        if form.is_valid():
            form_uuid = form.cleaned_data.get('form_uuid')

            sgtz = pytz.timezone(settings.TIME_ZONE)
            now = datetime.now(tz=sgtz)

            # Activate files that were submitted with this form.
            files = models.StatusFile.objects.filter(form_uuid=form_uuid)
            for file in files:
                file.activated = now
                file.save()

            status_files_to_delete = models.StatusFile.objects\
                .filter(user=user)\
                .exclude(form_uuid=form_uuid)

            objs = []

            for sf in status_files_to_delete:
                file = sf.file
                objs.append({'Key': file.s3_object_key})
                objs.append({'Key': file.thumbnail_s3_object_key})
                sf.delete()
                file.delete()

            _delete_objs.delay(objs)

            user.status = form.cleaned_data.get('status')
            user.status_updated = now
            user.save()

            return redirect(route, user.phone_number.value())
        else:
            is_show_update_form = True
    else:
        form = forms.UserDetailUpdateStatusForm()
        is_show_update_form = False

    absolute_url = request.build_absolute_uri(
        reverse(route, args=(phone_number.value(),)))

    params = {
        'absolute_url': absolute_url,
        'phone_number': phone_number,
        'user': user,
        'form': form,
        'is_show_update_form': is_show_update_form,
        'form_uuid': uuid.uuid4()
    }

    # Merge params with more params.
    params = {**params, **more_params}

    return TemplateResponse(request, template, params)

# No login required, not rate limited.
# Internal links will use user_detail_with_id, which require authentication
# and is rate limited. User detail page open graph sets phone number link
# as canonical, so they'll be index.
def user_detail(request, phone_number):
    phone_number, user = _get_phone_user(phone_number)

    send_amplitude_event.delay(
        'review - viewed user detail',
        user_uuid=user.uuid,
        ip=get_ip_address(request),
        event_properties={
            'viewee country code': user.phone_number.country_code
        }
    )

    return _user_detail__status_update(request, phone_number, user,
        'user_detail', 'relationships/user_detail.html')

@login_required
@ratelimit(key='user_or_ip', rate='240/d', block=True)
def user_reviews(request, phone_number):
    phone_number, user = _get_phone_user(phone_number)

    reviews = models.Review.objects\
        .filter(phone_number=phone_number)\
        .order_by('-created')
    reviews_per_page = 20
    paginator = Paginator(reviews, reviews_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    more_params = {'page_obj': page_obj}

    return _user_detail__status_update(request, phone_number, user,
        'user_reviews', 'relationships/user_reviews.html', more_params)

@login_required
def user_whatsapp(request, phone_number):
    # We use phone number instead of user ID because an account may not be
    # claimed. There's no need to rate limit this view because the phone
    # number is in the URL, so a scraper should have no problem getting to it.
    # Login is required so humans have to login before contacting (most won't
    # hack the URL for the phone number just to bypass sign-up).

    p, _ = get_or_create_phone_number(f'+{phone_number}')
    if p is None:
        raise Http404(None) # Don't give too much information.

    try:
        contactee = models.User.objects.filter(phone_number=p).first()
    except models.User.DoesNotExist:
        contactee = None

    contactor = request.user.user

    action, _ = models.ContactAction.objects.get_or_create(
        contactor=contactor,
        phone_number=p
    )
    action.action_count += 1
    action.save()
    
    # Temporary redirect so destination is not indexed.
    response = HttpResponse(status=302)

    response['Location'] = get_whatsapp_url(p.country_code, p.national_number)

    text = render_to_string(
        'relationships/texts/user_whatsapp.txt', {
            'url': reverse('user_detail', args=(phone_number,)),
            'contactor': contactor,
            'contactee': contactee,
            'phone_number': p
    }).replace('\n', '%0A').replace(' ', '%20')

    response['Location'] += f'?text={text}'

    return response

# Named 'log_in' and not 'login' to prevent clash with Django login
@ratelimit(key='ip', rate='60/h', block=True, method=['POST'])
def log_in(request):
    if request.user.is_authenticated:
        return redirect('user_detail', request.user.user.phone_number.value())
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            send_whatsapp_code.delay(user.id, whatsapp_purposes.LOGIN)
            url = reverse('login:confirm', args=(user.id,))
            return redirect(_append_next(
                url, form.cleaned_data.get('next')))
    else:
        form = forms.LoginForm(
            initial={'next': request.GET.get('next')})

    return TemplateResponse(request, 'relationships/login.html',{
        'form': form,
        'next': request.GET.get('next')
    })

def confirm_whatsapp_login(request, user_id):
    if request.user.is_authenticated:
        return redirect('user_detail', user.phone_number.value)
    
    try:
        user = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return redirect('login') # Unlikely error
    
    if request.method == 'POST':
        form = forms.ConfirmWhatsAppLoginForm(request.POST, user=user)
        if form.is_valid():
            user = form.user
            use_whatsapp_code(user, whatsapp_purposes.LOGIN)
            dju = authenticate(user.django_user.username) # Passwordless
            if dju is not None:
                login(request, dju)
                models.LoginAction.objects.create(user=user, type='whatsapp')
                next = form.cleaned_data.get('next')
                if next is not None and next.strip() != '':
                    return redirect(next)
                else:
                    return redirect('user_detail', user.phone_number.value())
    elif request.method == 'GET':
        form = forms.ConfirmWhatsAppLoginForm(
            user=user,
            initial={
            'next': request.GET.get('next')
        })
    
    return TemplateResponse(request,
        'relationships/login__confirm.html', {
            'form': form,
            'user': user
        })

# Don't name profile settings function 'settings', it conflicts with
# everybase.settings.
@login_required
def users__settings(request):
    user = request.user.user

    if request.method == 'POST':
        form = forms.SettingsForm(request.POST, user=user)
        if form.is_valid():
            send_amplitude_event.delay(
                'account - updated settings',
                user_uuid=user.uuid,
                ip=get_ip_address(request)
            )

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            country_str = form.cleaned_data.get('country')
            try:
                country = commods.Country.objects.get(
                    programmatic_key=country_str)
            except commods.Country.DoesNotExist:
                country = None
            business_name = form.cleaned_data.get('business_name')
            business_address = form.cleaned_data.get('business_address')
            business_description = form.cleaned_data.get('business_description')

            # Override existing data without checking.
            user.first_name = first_name
            user.last_name = last_name
            user.country = country
            user.business_name = business_name
            user.business_address = business_address
            user.business_description = business_description
            user.save()

            email_str = form.cleaned_data.get('email')
            email = get_or_create_email(email_str)
            if user.email != email:
                # Email changed, send WhatsApp code.
                user.pending_email = email
                user.save()
                send_email_code.delay(
                    user.id,
                    email_purposes.UPDATE_EMAIL,
                    user.pending_email.email
                )
                return redirect('users:confirm_email')
    else:
        form = forms.SettingsForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'country': user.country.programmatic_key,
            'business_name': user.business_name,
            'business_address': user.business_address,
            'business_description': user.business_description,
            'email': user.email,
        }, user=user)

    return TemplateResponse(request, 'relationships/settings.html', {
        'form': form,
        'countries': commods.Country.objects.filter(
            country_code=user.phone_number.country_code)
    })

@login_required
def users__settings__confirm_email(request):
    user = request.user.user

    if request.method == 'POST':
        form = forms.SettingsConfirmEmailForm(request.POST, user=user)
        if form.is_valid():
            use_email_code(user, email_purposes.UPDATE_EMAIL)
            user.email = user.pending_email
            user.save()
            return redirect('users:settings')
            
    return TemplateResponse(request,
        'relationships/settings__confirm_email.html')

@login_required
@csrf_exempt
def users__settings__resend_email_code(request, user_id):
    # Prevent access of a non-existent user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return Http404(None) # No error message for security reasons.

    if request.user.user.id != user_id:
        return Http404(None) # No error message for security reasons.

    if request.method == 'POST':
        send_email_code(user.id, email_purposes.UPDATE_EMAIL)
        return HttpResponse(status=204)

@login_required
def review_create(request, phone_number):
    p, _ = get_or_create_phone_number(f'+{phone_number}')
    if p is None:
        raise Http404(None) # Don't give too much information.

    reviewee = models.User.objects.filter(phone_number=p).first()
    
    reviewer = request.user.user

    # Don't allow reviewee to review himself.
    if reviewee is not None and reviewee.id == reviewer.id:
        return redirect('user_detail', phone_number)

    if request.method == 'POST':
        if models.Review.objects.filter(
            reviewer=reviewer,
            phone_number=phone_number
        ).count() > 1:
            return redirect('review_detail', reviewee.phone_number.value,
                reviewer.phone_number.value)

        form = forms.ReviewCreateForm(request.POST)

        if form.is_valid():
            review = form.cleaned_data.get('review')
            rating = form.cleaned_data.get('rating')
            form_uuid = form.cleaned_data.get('form_uuid')

            send_amplitude_event.delay(
                'review - created review',
                user_uuid=reviewer.uuid,
                ip=get_ip_address(request),
                event_properties={
                    'reviewee country code': reviewee.phone_number.country_code,
                    'reviewer country code': reviewer.phone_number.country_code,
                    'review type': rating
                }
            )
            
            # Activate files that were submitted with this form.
            sgtz = pytz.timezone(settings.TIME_ZONE)
            now = datetime.now(tz=sgtz)
            files = models.ReviewFile.objects.filter(form_uuid=form_uuid)
            for file in files:
                file.activated = now
                file.save()

            objs = []

            review_files = models.ReviewFile.objects\
                .filter(reviewer=reviewer, activated__isnull=True)

            for rf in review_files:
                file = rf.file
                objs.append({'Key': file.s3_object_key})
                objs.append({'Key': file.thumbnail_s3_object_key})
                rf.delete()
                file.delete()
    
            _delete_objs.delay(objs)

            models.Review.objects.create(
                reviewer=reviewer,
                phone_number=p,
                body=review,
                rating=rating
            )

            if reviewee is not None:
                # Email reviewee if phone number has been claimed.
                subject = render_to_string(
                    'relationships/email/review_received_subject.txt')

                url = request.build_absolute_uri(
                    reverse('review_detail', args=(p.value(),
                        reviewer.phone_number.value())))

                body = render_to_string(
                    'relationships/email/review_received.txt', {
                        'rating': 'good' if rating == 'good' else 'bad',
                        'url': url
                })

                send_email.delay(subject, body,
                    'friend@everybase.co', [reviewee.email.email])

            return redirect('user_reviews', phone_number)
    else:
        form = forms.ReviewCreateForm()

    return TemplateResponse(request, 'relationships/review_create.html', {
        'reviewee': reviewee,
        'reviewer': reviewer,
        'phone_number': p,
        'form': form,
        'form_uuid': uuid.uuid4()
    })

@login_required
@csrf_exempt
def upload_review_file(request, reviewer_id, phone_number_id):
    # Prevent review by a non-existent user.
    try:
        reviewer = models.User.objects.get(id=reviewer_id)
    except models.User.DoesNotExist:
        raise Http404(None) # No message for security reasons.

    # Prevent review of a non-existent phone number.
    try:
        phone_number = models.PhoneNumber.objects.get(id=phone_number_id)
    except models.User.DoesNotExist:
        raise Http404(None) # No message for security reasons.

    # Prevent the access of another user.
    if reviewer.id != request.user.user.id:
        return HttpResponse(status=204)

    form_uuid = request.POST.get('form_uuid')

    # Delete unused files that were uploaded in abandoned forms.
    _clear_files.delay(reviewer.id, form_uuid, False)

    try:
        # Deny file creation if maximum number of images is exceeded.
        if models.ReviewFile.objects\
            .filter(reviewer=reviewer, form_uuid=form_uuid).count() > \
                settings.MAX_REVIEW_IMAGES:
            return HttpResponse(status=400)

        file_object = request.FILES.get('file')

        mime_type = get_mime_type(file_object)

        file = fimods.File.objects.create(
            uploader=reviewer,
            mime_type=mime_type,
            filename=file_object.name,
            s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
            thumbnail_s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
        )

        key = settings.AWS_S3_KEY_REVIEW_IMAGE % \
            (phone_number.id, reviewer.id, file.id)
        thumb_key = settings.AWS_S3_KEY_REVIEW_IMAGE_THUMBNAIL % \
            (phone_number.id, reviewer.id, file.id)

        bucket = boto3.session.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        ).resource('s3').Bucket(settings.AWS_STORAGE_BUCKET_NAME)

        s3_obj = bucket.put_object(
            Key=key,
            Body=file_object,
            ContentType=mime_type
        )

        # Update file with S3 results
        file.s3_object_key = key
        file.thumbnail_s3_object_key = thumb_key
        file.s3_object_content_length = s3_obj.content_length
        file.e_tag = s3_obj.e_tag
        file.content_type = s3_obj.content_type
        file.last_modified = s3_obj.last_modified
        file.save()

        # Resize, save thumbnail, record sizes
        with Image.open(file_object) as im:
            # Resize preserving aspect ratio cropping from the center
            thumbnail = ImageOps.fit(im, settings.REVIEW_IMAGE_THUMBNAIL_SIZE)
            output = BytesIO()
            thumbnail.save(output, format='PNG')
            output.seek(0)

            # Upload thumbnail
            bucket.put_object(
                Key=thumb_key,
                Body=output,
                ContentType=mime_type
            )

            # Update file and thumbnail sizes
            file.width, file.height = im.size
            file.thumbnail_width, file.thumbnail_height = thumbnail.size
            file.save()

        # Create new review file for this user
        models.ReviewFile.objects.create(
            form_uuid=form_uuid,
            phone_number=phone_number,
            reviewer=reviewer,
            file=file,
            file_uuid=file.filename
        )
    except:
        return HttpResponse(status=500)
    
    return HttpResponse(status=204)

@login_required
@csrf_exempt
def delete_review_file(request):
    params = json.loads(request.body)
    file_uuid = params.get('file_uuid')
    form_uuid = params.get('form_uuid')
    _delete_review_file.delay(request.user.user.id, file_uuid, form_uuid)
    return HttpResponse(status=204)

@login_required
def review_detail(request, reviewee_phone_number, reviewer_phone_number):
    reviewee_ph, _ = get_or_create_phone_number(f'+{reviewee_phone_number}')
    if reviewee_ph is None:
        raise Http404(None) # Don't give too much information.

    reviewer_ph, _ = get_or_create_phone_number(f'+{reviewer_phone_number}')
    if reviewer_ph is None:
        raise Http404(None) # Don't give too much information.

    reviewee = models.User.objects.filter(phone_number=reviewee_ph).first()

    reviewer = models.User.objects.filter(phone_number=reviewer_ph).first()
    if reviewer is None:
        raise Http404(None) # Don't give too much information.

    review = models.Review.objects.filter(
        reviewer=reviewer,
        phone_number=reviewee_ph
    ).first()
    if review is None:
        raise Http404(None) # Don't give too much information.

    if request.method == 'POST':
        # Prevent users other than the reviewee and reviewer from responding
        # to this review.
        
        user = request.user.user

        if (reviewee is not None and reviewee.id == user.id) or\
            reviewer.id == user.id:
            form = forms.ReviewCommentCreateForm(request.POST)
            if form.is_valid():
                body = form.cleaned_data.get('body')
                models.ReviewComment.objects.create(
                    author=request.user.user,
                    review=review,
                    body=body
                )

        send_amplitude_event.delay(
            'review - responded review',
            user_uuid=reviewer.uuid,
            ip=get_ip_address(request),
            event_properties={
                'responder country code': request.user.user.phone_number\
                    .country_code,
                'reviewee country code': reviewee.phone_number.country_code,
                'reviewer country code': reviewer.phone_number.country_code
            }
        )

        if request.user.user.id == reviewee.id:
            receiver = reviewer
        else:
            receiver = reviewee

        subject = render_to_string(
            'relationships/email/response_received_subject.txt')

        url = request.build_absolute_uri(
            reverse('review_detail', args=(
                reviewee_phone_number,
                reviewer_phone_number)))

        body = render_to_string(
            'relationships/email/response_received.txt', {
                'rating': 'good' if review.rating == 'good' else 'bad',
                'url': url
        })

        send_email.delay(subject, body, 'friend@everybase.co', [
            receiver.email.email])

        return redirect('review_detail', reviewee_phone_number,
            reviewer_phone_number)
    else:
        form = forms.ReviewCommentCreateForm()

    absolute_url = request.build_absolute_uri(
        reverse('review_detail', args=(
            reviewee_phone_number,
            reviewer_phone_number)))

    responses = models.ReviewComment.objects\
        .filter(review=review).order_by('-created')
    responses_per_page = 20
    paginator = Paginator(responses, responses_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    send_amplitude_event.delay(
        'review - viewed review',
        user_uuid=reviewer.uuid,
        ip=get_ip_address(request),
        event_properties={
            'viewer country code': request.user.user.phone_number.country_code,
            'reviewee country code': reviewee.phone_number.country_code,
            'reviewer country code': reviewer.phone_number.country_code
        }
    )

    template_name = 'relationships/review_detail.html'
    return TemplateResponse(request, template_name, {
        'reviewee_phone_number': reviewee_ph,
        'reviewer_phone_number': reviewer_ph,
        'reviewee': reviewee,
        'reviewer': reviewer,
        'review': review,
        'absolute_url': absolute_url,
        'responses': responses,
        'form': form,
        'page_obj': page_obj
    })

def lookup(request):
    if request.method == 'POST':
        form = forms.LookUpForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            p = f'{phone_number.country_code}{phone_number.national_number}'

            send_amplitude_event.delay(
                'review - viewed user detail',
                ip=get_ip_address(request),
                event_properties={
                    'phone number country code': phone_number.country_code
                }
            )

            return redirect('user_detail', p)
    else:
        form = forms.LookUpForm()

    template_name = 'relationships/lookup.html'
    return TemplateResponse(request, template_name, {'form': form})