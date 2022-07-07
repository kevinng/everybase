import pytz, datetime
from everybase import settings
from relationships import models

INVALID = 'INVALID'
NO_CODE_GENERATED = 'NO_CODE_GENERATED'
USED = 'USED'
RATE_LIMITED = 'RATE_LIMITED'
EXPIRED = 'EXPIRED'
def is_email_code_valid(code: str, user: models.User) -> bool:
    """Returns True if email code is valid, false otherwise. Return relevant code in error."""

    if code is None or code.strip() == '':
        return INVALID

    if user.email_login_code is None or user.email_login_code_generated is None:
        return NO_CODE_GENERATED
    
    if user.last_email_login is not None and user.last_email_login > user.email_login_code_generated:
        return USED

    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)
    difference = (now - user.email_login_code_generated).total_seconds()
    
    if difference > int(settings.CONFIRMATION_CODE_RESEND_INTERVAL_SECONDS):
        return RATE_LIMITED
    
    if difference > int(settings.CONFIRMATION_CODE_EXPIRY_SECONDS):
        return EXPIRED

    return user.email_login_code == code