from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email(
    subject,
    message,
    from_email,
    recipient_list,
    html_message=None):
    """Send specified email. Designed to be self-contained without dependencies
    to other sub-systems (e.g. PostgreSQL, template renderer)

    Returns:
    Boolean: True if successful
    """
    
    success = send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        html_message=html_message
    ) == 1

    print('Email sent: %s' + str(success))

    return success