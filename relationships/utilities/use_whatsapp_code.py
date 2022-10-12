import datetime, pytz
from everybase import settings
from relationships import models

def use_whatsapp_code(user: models.User):
    """Update whatsapp code usage timestamp for input user."""
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(sgtz)
    user.whatsapp_code_used = now
    user.save()