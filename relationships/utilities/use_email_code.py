import datetime, pytz
from everybase import settings
from relationships import models

def use_email_code(user: models.User):
    """Update email code usage timestamp for input user."""
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(sgtz)
    user.email_code_used = now