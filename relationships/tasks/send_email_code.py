import random, pytz, datetime
from django.template.loader import render_to_string
from everybase import settings
from common.tasks.send_email import send_email
from relationships.constants import email_purposes

RATE_LIMITED = 'RATE_LIMITED'
SUBJECT_AND_OR_BODY_NONE = 'SUBJECT_AND_OR_BODY_NONE'

def send_email_code(
        user, # No type hint, because model reference creates circular import
        purpose: int,
        email: str=None
    ) -> bool:
    """Send email code to user. True if successful, False otherwise.
    
    Parameters:
    -----------
    user
        User to generate email code for.
    purpose
        Purpose of sending the code, see constants defined in this file.
    email
        If specified, we'll send to this email instead of user.email. Useful in cases such as when the user is updating his email.
    """
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)

    # Rate limit
    if user.email_code_generated is not None:
        difference = (now - user.email_code_generated).total_seconds()
        if difference < settings.CONFIRMATION_CODE_RESEND_INTERVAL_SECONDS:
            return RATE_LIMITED

    # Generate code
    user.email_code = random.randint(100000, 999999)
    user.email_code_generated = now
    user.save()

    # Select subject and body
    subject = None
    body = None
    if purpose == email_purposes.LOGIN:
        subject = render_to_string('relationships/email/confirm_login_subject.txt', {})
        body = render_to_string('relationships/email/confirm_login.txt', {'code': user.email_code})
    elif purpose == email_purposes.UPDATE_EMAIL:
        subject = render_to_string('relationships/email/confirm_email_update_subject.txt', {})
        body = render_to_string('relationships/email/confirm_email_update.txt', {'code': user.email_code})

    if subject is not None and body is not None:
        to = email if email is not None else user.email.email
        send_email.delay(subject, body, 'friend@everybase.co', [to])
        return True
    
    return SUBJECT_AND_OR_BODY_NONE