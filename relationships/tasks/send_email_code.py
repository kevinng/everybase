import random, pytz, datetime
from statistics import mode
from celery import shared_task
from django.template.loader import render_to_string
from everybase import settings
from common.tasks.send_email import send_email
from relationships import models
from relationships.constants import email_purposes
from relationships.utilities.is_email_code_rate_limited import \
    is_email_code_rate_limited

RATE_LIMITED = 'RATE_LIMITED'
NO_SUBJECT_AND_OR_BODY = 'NO_SUBJECT_AND_OR_BODY'

@shared_task
def send_email_code(
        user_id: int,
        purpose: int,
        email: str = None
    ) -> str:
    """Send email code to user. True if successful, False otherwise.
    
    Parameters:
    -----------
    user_id
        ID of user to generate email code for.
    purpose
        Purpose of sending the code, see constants defined in this file.
    email
        If specified, we'll send to this email instead of user.email. Useful in
        cases such as when the user is updating his email.
    """
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)

    user = models.User.objects.get(pk=user_id)

    if is_email_code_rate_limited(user):
        return RATE_LIMITED

    # Generate code
    user.email_code = random.randint(100000, 999999)
    user.email_code_generated = now
    user.save()

    # Select subject and body
    subject = None
    body = None
    if purpose == email_purposes.LOGIN:
        subject = render_to_string(
            'relationships/email/confirm_login_subject.txt', {})
        body = render_to_string(
            'relationships/email/confirm_login.txt',
            {'code': user.email_code})
    elif purpose == email_purposes.VERIFY_EMAIL:
        subject = render_to_string(
            'relationships/email/verify_email_subject.txt', {})
        body = render_to_string(
            'relationships/email/verify_email.txt',
            {'code': user.email_code})

    if subject is not None and body is not None:
        to = email if email is not None else user.email.email
        send_email.delay(subject, body, 'friend@everybase.co', [to])
        return True
    
    return NO_SUBJECT_AND_OR_BODY