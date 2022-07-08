import pytz, datetime
from everybase import settings

def is_whatsapp_code_rate_limited(user):
    """Returns True if user is rate limited for requesting a phone number code. False otherwise."""
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)

    if user.whatsapp_code_generated is not None:
        difference = (now - user.whatsapp_code_generated).total_seconds()
        if difference < settings.CONFIRMATION_CODE_RESEND_INTERVAL_SECONDS:
            return True
    
    return False