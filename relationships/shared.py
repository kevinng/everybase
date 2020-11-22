# Shared functions

from .models import Email, InvalidEmail
from django.core.exceptions import ValidationError

def create_get_email(email_str, import_job=None):
    """Attempt to get an existing email and return its primary key id, or create
    a new email if the input email does not exist.

    Args:
        email_str: Email address to get, or create if it does not exist.
        import_job: Import job model reference to associate the creation of this email with.

    """
    try:
        return Email.objects.get(email=email_str)
    except Email.DoesNotExist:
        pass

    try:
        e = Email(email=email_str, import_job=import_job)
        e.full_clean() # Raise validation error if inputs invalid
        e.save()
        return e
    except ValidationError:
        return None

def create_get_invalid_email(email_str, import_job=None):
    """Attempt to get an existing invalid email and return its primary key id,
    or create a new invalid email if the input email does not exist.

    Args:
        email_str: Invalid email address to get, or create if it does not exist.
        import_job: Import job model reference to associate the creation of this invalid email with.

    """
    try:
        return InvalidEmail.objects.get(email=email_str)
    except InvalidEmail.DoesNotExist:
        pass
    
    try:
        e = InvalidEmail(email=email_str, import_job=import_job)
        e.full_clean() # Raise validation error if inputs invalid
        e.save()
        return e
    except ValidationError:
        return None

def record_email(email_str, import_job=None):
    """Record email as either an email or an invalid-email.

    Args:
        email_str: Email to record.
        import_job: Import job model reference to associate this email with.

    Returns:
        (<email model reference>, <invalid-email model reference or None>)
    """
    if email_str is None or email_str == '':
        return (None, None)

    email = create_get_email(email_str, import_job)

    invalid_email = None
    if email is None:
        invalid_email = create_get_invalid_email(email_str, import_job)

    return (email, invalid_email)