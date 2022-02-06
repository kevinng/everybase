import pytz, datetime
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.response import TemplateResponse
from django.views.generic.list import ListView
from django.template.loader import render_to_string

from everybase import settings
from common import models as commods
from leads import models as lemods
from relationships import forms, models
from relationships.utilities.save_user_agent import save_user_agent
from relationships.utilities.get_non_tracking_whatsapp_link import \
    get_non_tracking_whatsapp_link
from chat.tasks.send_register_message import send_register_message
from chat.tasks.send_login_message import send_login_message

from sentry_sdk import capture_message
import phonenumbers

@login_required
def whatsapp(request, pk):
    if request.user.user.id == pk:
        return HttpResponseRedirect(reverse('users:user_comments', args=(pk,)))

    contactee = models.User.objects.get(pk=pk)

    if request.method == 'POST':
        form = forms.WhatsAppBodyForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data.get('body')
            contactor = request.user.user

            lemods.WhatsAppMessageBody.objects.create(
                contactor=contactor,
                contactee=contactee,
                body=body
            )
            
            response = HttpResponse(status=302) # Temporary redirect
            response['Location'] = get_non_tracking_whatsapp_link(
                contactee.phone_number.country_code,
                contactee.phone_number.national_number
            )
            response['Location'] += '?text=' + render_to_string(
                'chat/bodies/whatsapp_author.txt', {
                    'contactee': contactee,
                    'contactor': contactor,
                    'body': body
            }).replace('\n', '%0A').replace(' ', '%20')

            return response
    else:
        form = forms.WhatsAppBodyForm()

    params = {
        'contactee': contactee,
        'form': form
    }

    last_msg_body = lemods.WhatsAppMessageBody.objects.\
        filter(contactor=request.user.user).\
        order_by('-created').\
        first()

    if last_msg_body is not None:
        params['last_msg_body'] = last_msg_body.body

    return render(request, 'relationships/message.html', params)

def user_comments(request, pk):
    user = models.User.objects.get(pk=pk)
    template = 'relationships/user_detail_comment_list.html'

    if request.method == 'POST':
        # Disallow commenting on self
        if not request.user.is_authenticated or user.id == request.user.user.id:
            return render(request, template, {'detail_user': user})

        form = forms.CommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data.get('body')
            is_public = form.cleaned_data.get('is_public')
            if is_public is None:
                is_public = False

            commentor = request.user.user

            models.Comment.objects.create(
                commentee=user,
                commentor=commentor,
                body=body,
                is_public=is_public
            )

            return HttpResponseRedirect(
                reverse('users:user_comments', args=(pk,)))
    else:
        form = forms.CommentForm()

    return render(request, template, {'detail_user': user, 'form': form})

@login_required
def user_edit(request, pk):
    user = models.User.objects.get(pk=pk)

    if request.method == 'POST':
        form = forms.UserEditForm(request.POST)
        if form.is_valid():
            # Get or create a new email for this user
            email, _ = models.Email.objects.get_or_create(
                email=form.cleaned_data.get('email')
            )

            is_not_agent = form.cleaned_data.get('is_not_agent')
            if is_not_agent is None:
                is_not_agent = False

            models.User.objects.update(
                first_name = form.cleaned_data.get('first_name'),
                last_name = form.cleaned_data.get('last_name'),
                email=email,
                goods_string=form.cleaned_data.get('goods_string'),
                languages_string=form.cleaned_data.get('languages_string'),
                is_agent=not is_not_agent
            )

            return HttpResponseRedirect(
                reverse('users:user_comments', args=(pk,)))
    else:
        form = forms.UserEditForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email.email,
            'goods_string': user.goods_string,
            'languages_string': user.languages_string,
            'is_not_agent': not user.is_agent
        })

    return TemplateResponse(request, 'relationships/user_edit.html', {
        'whatsapp_phone_number': str(user.phone_number.country_code) + \
            str(user.phone_number.national_number),
        'form': form
    })

class UserLeadListView(ListView):
    template_name = 'relationships/user_detail_lead_list.html'
    context_object_name = 'leads'
    model = lemods.Lead
    paginate_by = 8

    def get_queryset(self, **kwargs):
        return lemods.Lead.objects.filter(
            author=models.User.objects.get(pk=self.kwargs['pk'])
        ).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = models.User.objects.get(pk=self.kwargs['pk'])
        context['detail_user'] = user
        return context

def kill_live_register_tokens(user):
    live_tokens = models.RegisterToken.objects.filter(
        user=user,
        activated__isnull=True, # Not activated
        killed__isnull=True # Not killed
    )
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(tz=sgtz)
    for t in live_tokens:
        t.killed = now
        t.save()

def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            # Part of the form check includes checking if the phone number and
            # email belongs to a registered user. If so, is_valid() will return
            # False.

            # Parse phone number
            ph_str = form.cleaned_data.get('whatsapp_phone_number')
            parsed_ph = phonenumbers.parse(str(ph_str), None)
            ph_cc = parsed_ph.country_code
            ph_nn = parsed_ph.national_number

            # Get or create new phone number for this user
            whatsapp = models.PhoneNumberType.objects.get(
                programmatic_key='whatsapp'
            )
            phone_number, _ = \
                models.PhoneNumber.objects.get_or_create(
                country_code=ph_cc,
                national_number=ph_nn
            )
            phone_number.types.add(whatsapp)
            phone_number.save()

            # Get or create a new email for this user
            email, _ = models.Email.objects.get_or_create(
                email=form.cleaned_data.get('email')
            )

            # Get country from user's WhatsApp phone number country code
            try:
                country = commods.Country.objects.get(country_code=ph_cc)
            except commods.Country.DoesNotExist:
                country = None

            # Get or create an Everybase user
            user, _ = models.User.objects.get_or_create(
                phone_number=phone_number)
            
            is_not_agent = form.cleaned_data.get('is_not_agent')
            if is_not_agent is None:
                is_not_agent = False

            # Override or set user details
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.languages_string = form.cleaned_data.get('languages')
            user.is_agent = not is_not_agent
            user.phone_number = phone_number
            user.email = email
            user.country = country
            user.save()

            # Kill all tokens
            kill_live_register_tokens(user)

            # Send register message
            send_register_message.delay(user.id)

            # Append next URL
            next_url = form.cleaned_data.get('next')
            confirm_register = reverse('relationships:confirm_register',
                kwargs={'user_uuid': user.uuid})

            if next_url is not None:
                confirm_register += f'?next={next_url}'

            # TODO Amplitude
            save_user_agent(request, user)

            return HttpResponseRedirect(confirm_register)
    else:
        form = forms.RegisterForm()

    params = {'form': form}

    # Read 'next' URL from GET parameters to form input. We'll add it to the
    # redirect URL when the user submits this form.
    next = request.GET.get('next')
    if next is not None:
        params['next'] = next

    return render(request, 'relationships/register.html', params)

def confirm_register(request, user_uuid):
    user = models.User.objects.get(uuid=user_uuid)

    if request.method == 'POST':
        # Resend message

        # Kill all tokens
        kill_live_register_tokens(user)
        
        # Create token and send message
        send_register_message.delay(user.id)

        # If the user requested to resend the message, read next URL and
        # redirect to self. Because we're not using a Django form, we need to
        # manually read the next parameter from the HTML form, and render it
        # back into the URL as a GET parameter. Django will then call this URL
        # again and render the parameter back into the form.

        confirm_register = reverse('relationships:confirm_register',
            kwargs={'user_uuid': user.uuid})

        next_url = request.POST.get('next')

        if next_url is not None:
            confirm_register += f'?next={next_url}'
        
        return HttpResponseRedirect(confirm_register)
    
    params = {
        'user_uuid': user_uuid,
        'country_code': user.phone_number.country_code,
        'national_number': user.phone_number.national_number
    }

    next_url = request.GET.get('next')
    if next_url is not None and len(next_url.strip()) > 0:
        params['next'] = next_url
    else:
        # TODO redirect to home
        params['next'] = reverse('leads__root:agents')

    return render(request,
        'relationships/confirm_register.html', params)

def is_registered(request, user_uuid):
    """This view is called in the background of the confirm_register page to
    ascertain if the user has confirmed his registration by replying 'yes' to
    the chatbot.
    """
    try:
        # If the user has confirmed registration - i.e., replied 'yes' to the
        # chatbot when sent a verification message, his Everybase User model
        # will have an associated Django user model. Here, we check for the
        # associated Django user model.

        django_user = User.objects.get(username=user_uuid)
    except User.DoesNotExist:
        # User has not confirmed registration - i.e., no associated Django user
        return JsonResponse({'r': False})

    # Authenticate user
    in_user = authenticate(django_user.username)
    if in_user is not None:
        # Authentication successful, log user in
        login(request, in_user)

        user = models.User.objects.get(uuid=user_uuid)

        kill_live_register_tokens(user)

        # TODO Amplitude
    else:
        capture_message('User not able to log in after registration. Django\
user ID: %d, user ID: %d' % (django_user.id, django_user.user.id),
        level='error')

    return JsonResponse({'r': True})

def kill_live_login_tokens(user):
    live_tokens = models.LoginToken.objects.filter(
        user=user,
        activated__isnull=True, # Not activated
        killed__isnull=True # Not killed
    )
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(tz=sgtz)
    for t in live_tokens:
        t.killed = now
        t.save()

def log_in(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Parse phone number
            ph_str = form.cleaned_data.get('whatsapp_phone_number')
            parsed_ph = phonenumbers.parse(str(ph_str), None)
            ph_cc = parsed_ph.country_code
            ph_nn = parsed_ph.national_number

            try:
                phone_number = models.PhoneNumber.objects.get(
                    country_code=ph_cc,
                    national_number=ph_nn
                )

                user = models.User.objects.filter(
                    phone_number=phone_number.id, # User has phone number
                    registered__isnull=False, # User is registered
                    django_user__isnull=False # User has a Django user linked
                ).first()

                next_url = form.cleaned_data.get('next')

                # Kill all tokens
                kill_live_login_tokens(user)

                # Create token and send message
                send_login_message.delay(user.id)

                confirm_login_url = reverse('relationships:confirm_login',
                    kwargs={'user_uuid': user.uuid})

                if next_url is not None:
                    confirm_login_url += f'?next={next_url}'

                save_user_agent(request, user)
                
                return HttpResponseRedirect(confirm_login_url)
            except (models.User.DoesNotExist, models.PhoneNumber.DoesNotExist):
                messages.info(request, "Account don't exist.")
    else:
        form = forms.LoginForm()

    params = {'form': form}

    # Read 'next' URL from GET parameters to form input. We'll add it to the
    # redirect URL when the user submits this form.
    next = request.GET.get('next')
    if next is not None:
        params['next'] = next

    return render(request, 'relationships/login.html', params)

def confirm_login(request, user_uuid):
    if request.method == 'POST':
        # Resend login message

        # Note: we use the same LoginForm class as the log_in view.
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Parse phone number
            ph_str = form.cleaned_data.get('whatsapp_phone_number')
            parsed_ph = phonenumbers.parse(str(ph_str), None)
            ph_cc = parsed_ph.country_code
            ph_nn = parsed_ph.national_number

            try:
                phone_number = models.PhoneNumber.objects.get(
                    country_code=ph_cc,
                    national_number=ph_nn
                )

                user = models.User.objects.filter(
                    phone_number=phone_number.id, # User has phone number
                    registered__isnull=False, # User is registered
                    django_user__isnull=False # User has a Django user linked
                ).first()

                # Kill all live tokens
                kill_live_login_tokens(user)

                # Create token and send message
                send_login_message.delay(user.id)

                return HttpResponseRedirect(
                    reverse('relationships:confirm_login',
                        kwargs={'user_uuid': user.uuid}))
                
            except (models.User.DoesNotExist, models.PhoneNumber.DoesNotExist):
                # Not possible - unless user hacked the form
                return HttpResponseRedirect(reverse('relationships:login',
                    kwargs={}))

    user = models.User.objects.get(uuid=user_uuid)
    params = {
        'user_uuid': user_uuid,
        'country_code': user.phone_number.country_code,
        'national_number': user.phone_number.national_number,
    }

    # Read 'next' URL from GET parameters to be rendered as a form input. We'll
    # add it to the redirect URL when the user submits this form.
    next_url = request.GET.get('next')
    if next_url is not None and len(next_url.strip()) > 0:
        params['next'] = next_url
    else:
        params['next'] = reverse('leads__root:agents')

    return render(request, 'relationships/confirm_login.html', params)

def is_logged_in(request, user_uuid):
    """This view is called in the background of the confirm_login page to
    ascertain if the user has confirmed his login by replying 'yes' to the
    chatbot.
    """
    user = models.User.objects.get(uuid=user_uuid)

    token = models.LoginToken.objects.filter(
        user=user.id,
        activated__isnull=False # Activated
    ).order_by('-created').first()
    
    if token is not None:
        expiry_datetime = token.created + timedelta(
            seconds=settings.LOGIN_TOKEN_EXPIRY_SECS)
        sgtz = pytz.timezone(settings.TIME_ZONE)
        if datetime.now(tz=sgtz) < expiry_datetime and \
            user.django_user is not None:
            # Registered user has activated this unexpired token

            django_user = user.django_user

            # Authenticate user
            in_user = authenticate(django_user.username)
            if in_user is not None:

                # Authentication successful, log the user in
                login(request, in_user, backend=\
                    'relationships.auth.backends.DirectBackend')
                
                # Activate this token
                sgtz = pytz.timezone(settings.TIME_ZONE)
                now = datetime.now(tz=sgtz)
                token.activated = now
                token.save()

                # Kill other live tokens
                kill_live_login_tokens(user)

                # TODO Amplitude
                save_user_agent(request, user)

                return JsonResponse({'l': True})

    return JsonResponse({'l': False})

def log_out(request):
    logout(request)
    # TODO redirect to home
    return HttpResponseRedirect(reverse('leads__root:agents'))