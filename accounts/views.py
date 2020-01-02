from django.http import HttpResponse, HttpResponseRedirect

from django.template import loader
from django.template.loader import render_to_string

from django.shortcuts import render
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
)
from django.contrib.auth.models import User

from .forms import LoginForm, ResetPasswordForm, SetPasswordForm
from .models import PasswordResetCode
from .tasks import send_email

_default_login_redirection_url = '/documents'

def is_documents_url(url):
    """Check if the supplied URL is a valid document link, plus return the
    cleaned-up link if it is so.

    Returns:
    (Boolean, String): Respectively - is this URL a valid document link?
        And, the cleaned-up document link.
    """
    url_tokens = list(filter(lambda i: i != '', url.split('/')))
    if url_tokens[0] == 'documents' and \
        len(url_tokens) == 2:
        return (True, '/documents/' + url_tokens[1])

    return (False, None)

def login(request):

    if request.method == 'POST':
        # Log into system
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Success, direct to next or default URL
                auth_login(request, user)
                next = form.cleaned_data['next']
                if next == '':
                    # No next URL, direct to default
                    return HttpResponseRedirect(_default_login_redirection_url)
                return HttpResponseRedirect(next)
            else:
                # Failure, direct to login page with message
                messages.error(request, 'LOGIN_FAILED')
                return HttpResponseRedirect(reverse('login'))
    else:
        next = request.GET.get('next', None)
        if next != None and next != '':
            (is_doc_url, cleaned_url) = is_documents_url(next)
            if is_doc_url:
                # Next link is a document link, clean it up
                messages.info(request, 'IS_DOCUMENT_LINK')
                next = cleaned_url
        form = LoginForm(initial={'next': next})

    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    messages.info(request, 'LOGGED_OUT')
    return HttpResponseRedirect(reverse('login'))

def send_sample_email(request):
    et_path = lambda template: 'accounts/email/' + template
    send_email.delay(
        'warehouse@thomson-chemicals Sent You Documents',
        'hello world',
        'kevin@everybase.co', # Need to change this to no-reply@everybase.co when the domain is verified
        ['kevin@everybase.co'],
        html_message=render_to_string(et_path('send_document.html'), {})
    )
    return render(request, 'accounts/email/send_document.html', {})

def reset_password(request):
    if request.method == 'POST':
        # Reset password
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            user_qs = User.objects.filter(username=email)
            user = user_qs.first()
            if user is not None:
                # User exists

                # Get latest code for this user
                code = PasswordResetCode.objects \
                    .filter(user__in=user_qs) \
                    .order_by('-created') \
                    .first()

                if code is not None and (code.is_old_enough() or not code.is_valid()) \
                    or code is None:
                    # Code is not valid or old enough, or code don't exist

                    if code is not None:
                        # Expire old code
                        code.used = True
                        code.save()

                    # Issue new code
                    new_code = PasswordResetCode(user=user)
                    new_code.save()

                    # Email template base URL maker
                    et_path = lambda template: 'accounts/email/' + template

                    # Prepare context
                    full_reset_url = 'https://everybase.co' + \
                        reverse('set_password', args={new_code.id})
                    et_context = {
                        'reset_url': full_reset_url,
                        'email': user.email
                    }

                    # Set next URL, if it exists
                    next = form.cleaned_data.get('next', None)
                    if next is not None and next != '':
                        et_context['next'] = next

                    send_email.delay(
                        render_to_string(et_path('password_reset_subject.txt')),
                        render_to_string(et_path('password_reset.txt'), et_context),
                        'kevin@everybase.co', # Need to change this to no-reply@everybase.co when the domain is verified
                        [user.email],
                        html_message=render_to_string(et_path('password_reset.html'), et_context)
                    )
                
            return render(request, 'accounts/password_reset_link_sent.html')
    else:
        next = request.GET.get('next', None)
        form = ResetPasswordForm(initial={'next': next})

    return render(request, 'accounts/reset_password.html', {'form': form})

def set_password(request, code=None):
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        # Set password
        code = request.POST['code']
        code_obj = PasswordResetCode.objects.filter(id=code).first()
        if code_obj is not None and code_obj.is_valid():
            # Code is valid
            if form.is_valid():
                # Update password
                password = form.cleaned_data['password'] # Validated by form
                code_obj.user.set_password(password)
                code_obj.user.save()

                # Invalid code
                code_obj.used = True
                code_obj.save()
                
                # Log the user in
                user = authenticate(request,
                    username=code_obj.user.email,
                    password=password)
                
                if user is not None:
                    # Success, direct to next or default login URL
                    auth_login(request, user)
                    next = form.cleaned_data.get('next', None)
                    if next is not None and next != '':
                        # Have next URL, direct to destination
                        return HttpResponseRedirect(next)
                    
                    return HttpResponseRedirect(_default_login_redirection_url)
                    
                
                # Login failed - direct user to login page
                return HttpResponseRedirect(reverse('login'))
        else:
            # Code is invalid
            messages.error(request, 'CODE_INVALID')
            return HttpResponseRedirect(reverse('reset_password'))
    else:
        # Visit from email
        code_obj = PasswordResetCode.objects.filter(id=code).first()
        initial = {}
        if code_obj is not None and code_obj.is_valid():
            # Code is valid
            initial['code'] = code_obj.id

            # Set the next URL, if it exists
            next = request.GET.get('next', None)
            if next != None and next != '':
                initial['next'] = next
        else:
            # Code does not exist or is expired
            messages.error(request, 'CODE_INVALID')
            return HttpResponseRedirect(reverse('reset_password'))
        
        form = SetPasswordForm(initial=initial)

    return render(request, 'accounts/set_password.html', {'form': form})

def r(request, file_to_render):
    template = loader.get_template('accounts/%s' % file_to_render)
    return HttpResponse(template.render({}, request))