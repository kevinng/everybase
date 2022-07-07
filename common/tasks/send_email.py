from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email(
    subject,
    message,
    from_email,
    recipient_list,
    html_message=None):
    """Send email. Returns True if successful. Designed to be self-contained without dependencies to other sub-systems (e.g. PostgreSQL, template renderer)."""
    if from_email is None or from_email.strip() == '':
        return False

    for email in recipient_list:
        if email is None or email.strip() == '':
            return False
    
    return send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        html_message=html_message
    ) == 1