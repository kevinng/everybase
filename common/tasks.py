from celery import shared_task

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
    
    return django.core.mail.send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        html_message=html_message
    ) == 1