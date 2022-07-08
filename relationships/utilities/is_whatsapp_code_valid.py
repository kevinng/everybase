from typing import Union
import pytz, datetime
from everybase import settings
from relationships import models

INVALID = 'INVALID'
NO_CODE_GENERATED = 'NO_CODE_GENERATED'
USED = 'USED'
EXPIRED = 'EXPIRED'
def is_whatsapp_code_valid(
        code: str,
        user: models.User
    ) -> Union[bool, str]:
    """Returns True if WhatsApp code is valid, false otherwise. Return relevant code in error."""

    if code is None or code.strip() == '':
        return INVALID

    if user.whatsapp_code is None or user.whatsapp_code_generated is None:
        return NO_CODE_GENERATED
    
    if user.whatsapp_code_used is not None and user.whatsapp_code_used > user.whatsapp_code_generated:
        return USED

    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)
    difference = (now - user.whatsapp_code_generated).total_seconds()
    
    if difference > int(settings.CONFIRMATION_CODE_EXPIRY_SECONDS):
        return EXPIRED

    return user.whatsapp_code == code