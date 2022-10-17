import datetime, pytz
from everybase import settings
from relationships import models

def use_email_code(
        user: models.User,
        purpose: str
    ):
    """Update email code usage timestamp for input user if it matches the
    input purpose."""
    if user.email_code_purpose == purpose:
        sgtz = pytz.timezone(settings.TIME_ZONE)
        now = datetime.datetime.now(sgtz)
        user.email_code_used = now
        user.save()