import datetime, pytz
from everybase import settings
from relationships import models

def use_whatsapp_code(
        user: models.User,
        purpose: str
    ):
    """Update whatsapp code usage timestamp for input user if it matches the
    input purpose."""
    if user.whatsapp_code_purpose == purpose:
        sgtz = pytz.timezone(settings.TIME_ZONE)
        now = datetime.datetime.now(sgtz)
        user.whatsapp_code_used = now
        user.save()