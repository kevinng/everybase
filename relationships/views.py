import pytz
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from everybase import settings
from common import models as commods
from leads import models as lemods
from relationships import forms, models
from relationships.utilities.save_user_agent import save_user_agent
from relationships.utilities.get_non_tracking_whatsapp_link import \
    get_non_tracking_whatsapp_link
from relationships.utilities.kill_login_tokens import kill_login_tokens
from relationships.utilities.kill_register_tokens import kill_register_tokens
from chat.tasks.send_register_message import send_register_message
from chat.tasks.send_login_message import send_login_message

from sentry_sdk import capture_message
import phonenumbers
from ratelimit.decorators import ratelimit

@login_required
def whatsapp(request, slug):
    if request.user.user.id == slug:
        # Disallow WhatsApp to self
        return HttpResponseRedirect(reverse('users:user_detail', args=(slug,)))

    contactee = models.User.objects.get(slug_link=slug)

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

def user_detail(request, slug):
    user = models.User.objects.get(slug_link=slug)
    if request.method == 'POST':
        # User posted a comment
        form = forms.UserCommentForm(request.POST)
        if form.is_valid():
            comment = models.UserComment.objects.create(
                commentee=models.User.objects.get(slug_link=slug),
                commentor=request.user.user,
                body=request.POST.get('body')
            )

            comment_id = request.POST.get('comment_id')
            if comment_id is not None:
                # This is a reply to a root comment
                comment.reply_to = models.UserComment.objects.get(pk=comment_id)
                comment.save()

            # Focus on comment created
            url = reverse('users:user_detail', args=(slug,)) + \
                '?focus=comment-' + str(comment.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.UserCommentForm()

    params = {
        'detail_user': user,
        'form': form
    }

    focus = request.GET.get('focus')
    if focus is not None:
        params['focus'] = focus

    return render(request, 'relationships/user_detail_comment_list.html', params)

@login_required
def user_edit(request, slug):
    if request.user.user.slug_link != slug:
        # Disallow user from editing another's profile
        return HttpResponseRedirect(reverse('users:user_detail', args=(slug,)))

    user = models.User.objects.get(slug_link=slug)

    if request.method == 'POST':
        form = forms.UserEditForm(request.POST)
        if form.is_valid():
            get = lambda k : form.cleaned_data.get(k)

            models.User.objects.update(
                first_name=get('first_name'),
                last_name=get('last_name'),
                goods_string=get('goods_string'),
                has_company=get('has_company'),
                company_name=get('company_name'),
                languages_string=get('languages_string'),
                is_buy_agent=get('is_buy_agent'),
                buy_agent_details=get('buy_agent_details'),
                is_sell_agent=get('is_sell_agent'),
                sell_agent_details=get('sell_agent_details'),
                is_logistics_agent=get('is_logistics_agent'),
                logistics_agent_details=get('logistics_agent_details')
            )

            return HttpResponseRedirect(
                reverse('users:user_detail', args=(slug,)))
    else:
        form = forms.UserEditForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'goods_string': user.goods_string,
            'has_company': user.has_company,
            'company_name': user.company_name,
            'languages_string': user.languages_string,
            'is_buy_agent': user.is_buy_agent,
            'buy_agent_details': user.buy_agent_details,
            'is_sell_agent': user.is_sell_agent,
            'sell_agent_details': user.sell_agent_details,
            'is_logistics_agent': user.is_logistics_agent,
            'logistics_agent_details': user.logistics_agent_details
        })

    return render(request, 'relationships/user_edit.html', {'form': form})

class UserLeadListView(ListView):
    template_name = 'relationships/user_detail_lead_list.html'
    context_object_name = 'leads'
    model = lemods.Lead
    paginate_by = 8

    def get_queryset(self, **kwargs):
        return lemods.Lead.objects.filter(
            author=models.User.objects.get(slug_link=self.kwargs['slug'])
        ).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = models.User.objects.get(slug_link=self.kwargs['slug'])
        context['detail_user'] = user
        return context

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

            has_company = form.cleaned_data.get('has_company')
            if has_company is None:
                has_company = False

            is_buy_agent = form.cleaned_data.get('is_buy_agent')
            if is_buy_agent is None:
                is_buy_agent = False

            is_sell_agent = form.cleaned_data.get('is_sell_agent')
            if is_sell_agent is None:
                is_sell_agent = False

            is_logistics_agent = form.cleaned_data.get('is_logistics_agent')
            if is_logistics_agent is None:
                is_logistics_agent = False

            # Create an Everybase user
            user = models.User.objects.create(
                phone_number=phone_number,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                goods_string=form.cleaned_data.get('goods_string'),
                languages_string=form.cleaned_data.get('languages_string'),
                has_company=has_company,
                company_name=form.cleaned_data.get('company_name'),
                email=email,
                country=country,
                is_buy_agent=is_buy_agent,
                buy_agent_details=form.cleaned_data.get('buy_agent_details'),
                is_sell_agent=is_sell_agent,
                sell_agent_details=form.cleaned_data.get('sell_agent_details'),
                is_logistics_agent=is_logistics_agent,
                logistics_agent_details=form.cleaned_data.get('logistics_agent_details'),
            )

            # Kill all tokens
            kill_register_tokens(user)

            # Create new token
            models.RegisterToken.objects.create(user=user)

            # Send message
            send_register_message.delay(user.id)

            # Append next URL
            next_url = form.cleaned_data.get('next')
            confirm_register = reverse('confirm_register',
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

@ratelimit(key='user_or_ip', rate='10/h', block=True, method=['POST'])
def confirm_register(request, user_uuid):
    user = models.User.objects.get(uuid=user_uuid)

    if request.method == 'POST':
        # User request to resend message

        # Kill all tokens
        kill_register_tokens(user)

        # Create new token
        models.RegisterToken.objects.create(user=user)
        
        # Send message
        send_register_message.delay(user.id)

        # If the user requested to resend the message, read next URL and
        # redirect to self. Because we're not using a Django form, we need to
        # manually read the next parameter from the HTML form, and render it
        # back into the URL as a GET parameter. Django will then call this URL
        # again and render the parameter back into the form.

        confirm_register = reverse('confirm_register',
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
        params['next'] = reverse('home')

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

        kill_register_tokens(user)

        # TODO Amplitude
    else:
        capture_message('User not able to log in after registration. Django\
user ID: %d, user ID: %d' % (django_user.id, django_user.user.id),
        level='error')

    return JsonResponse({'r': True})

def log_in(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Parse phone number
            ph_str = form.cleaned_data.get('whatsapp_phone_number')
            parsed_ph = phonenumbers.parse(str(ph_str), None)
            ph_cc = parsed_ph.country_code
            ph_nn = parsed_ph.national_number

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
            kill_login_tokens(user)

            # Create login token
            models.LoginToken.objects.create(user=user)

            # Send message
            send_login_message.delay(user.id)

            confirm_login_url = reverse('confirm_login',
                kwargs={'user_uuid': user.uuid})

            if next_url is not None:
                confirm_login_url += f'?next={next_url}'

            save_user_agent(request, user)
            
            return HttpResponseRedirect(confirm_login_url)
    else:
        form = forms.LoginForm()

    params = {'form': form}

    # Read 'next' URL from GET parameters to form input. We'll add it to the
    # redirect URL when the user submits this form.
    next = request.GET.get('next')
    if next is not None:
        params['next'] = next

    return render(request, 'relationships/login.html', params)

@ratelimit(key='user_or_ip', rate='10/h', block=True, method=['POST'])
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

                # Kill all tokens
                kill_login_tokens(user)

                # Create login token
                models.LoginToken.objects.create(user=user)

                # Create token and send message
                send_login_message.delay(user.id)

                return HttpResponseRedirect(
                    reverse('confirm_login', kwargs={'user_uuid': user.uuid}))
                
            except (models.User.DoesNotExist, models.PhoneNumber.DoesNotExist):
                # Not possible - unless user hacked the form
                return HttpResponseRedirect(reverse('login', kwargs={}))

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
        params['next'] = reverse('home')

    return render(request, 'relationships/confirm_login.html', params)

def is_logged_in(request, user_uuid):
    """This view is called in the background of the confirm_login page to
    ascertain if the user has confirmed his login by replying 'yes' to the
    chatbot.
    """
    user = models.User.objects.get(uuid=user_uuid)

    # Get latest token for this user.
    # Note: do not filter conditions here because the latest token for the
    #   matching conditions may not be the latest-of-all token for this user.
    token = models.LoginToken.objects.filter(user=user.id)\
        .order_by('-created').first()
    
    if token is not None:
        expiry_datetime = token.created + timedelta(
            seconds=settings.LOGIN_TOKEN_EXPIRY_SECS)
        sgtz = pytz.timezone(settings.TIME_ZONE)
        if datetime.now(tz=sgtz) < expiry_datetime and \
            user.django_user is not None and token.activated is not None and \
            token.is_not_latest is None:
            # Checks passed
            #   Token is not expired
            #   User is registered (i.e., user.django_user is not None)
            #   Token has been activated via chatbot (activated is not None)
            #   Token is latest (is_not_latest is None)

            django_user = user.django_user

            # Authenticate user
            in_user = authenticate(django_user.username)

            if in_user is not None:
                # Authentication successful, log the user in with password
                login(request, in_user, backend=\
                    'relationships.auth.backends.DirectBackend')

                # TODO Amplitude
                save_user_agent(request, user)

                return JsonResponse({'l': True})

    return JsonResponse({'l': False})

def log_out(request):
    logout(request)
    next_url = request.GET.get('next')
    if next_url is not None:
        return HttpResponseRedirect(next_url)

    return HttpResponseRedirect(reverse('home'))

@login_required
@csrf_exempt
def toggle_save_user(request, slug):
    if request.user.user.slug_link == slug:
        # Disallow saving of self
        return HttpResponseRedirect(reverse('users:user_detail', args=(slug,)))

    def toggle():
        try:
            saved_user = models.SavedUser.objects.get(
                savee=models.User.objects.get(slug_link=slug),
                saver=request.user.user
            )

            # Toggle save-unsave
            saved_user.active = not saved_user.active
            saved_user.save()
        except models.SavedUser.DoesNotExist:
            saved_user = models.SavedUser.objects.create(
                savee=models.User.objects.get(slug_link=slug),
                saver=request.user.user,
                active=True
            )
        
        return {'s': saved_user.active}

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
    # parameter exists. Other redirect user to default user details page.
    next_url = request.GET.get('next')
    if next_url is not None and len(next_url.strip()) > 0:
        return HttpResponseRedirect(next_url)
    else:
        return HttpResponseRedirect(
            reverse('users:user_detail', args=(slug,)))

def user_list(request):
    pass

# class AgentListView(ListView):
#     template_name = 'leads/agent_list.html'
#     context_object_name = 'agents'
#     model = relmods.User
#     paginate_by = 8

#     def get_queryset(self, **kwargs):
#         # search = self.request.GET.get('search')
#         # country = self.request.GET.get('country')

#         # users = relmods.User.objects
#         # if country is not None and country != 'any_country':
#         #     users = users.filter(country__programmatic_key=country)

#         # # Save query
#         # try:
#         #     if self.request.user.is_authenticated:
#         #         user = self.request.user.user
#         #     else:
#         #         user = None

#         #     if country == 'any_country' or country is None:
#         #         country_model = None
#         #     else:
#         #         country_model = commods.Country.objects.get(
#         #             programmatic_key=country)
                
#         #     if user is not None and search is not None and country is not None:
#         #         models.AgentQuery.objects.create(
#         #             user=user,
#         #             search=search,
#         #             country=country_model
#         #         )
#         # except:
#         #     traceback.print_exc()

#         # vector = SearchVector('search_agents_veccol')
#         # query = SearchQuery(search)
#         # users = users.annotate(
#         #     search_agents_veccol=RawSQL('search_agents_veccol', [],
#         #         output_field=SearchVectorField()))\
#         #     .annotate(rank=SearchRank(vector, query))\
#         #     .order_by('-rank')
            
#         # return users

#         return relmods.User.objects.all()
        
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['countries'] = get_countries()

#         # Render search and country back into the template
#         context['search_value'] = self.request.GET.get('search')
#         context['country_value'] = self.request.GET.get('country')

#         return context