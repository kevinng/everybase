import pytz
from datetime import datetime

from everybase import settings
from chat import models

def expire_context(user, intent_key, message_key):
    """Set user context's 'done' timestamp to now

    Parameters
    ----------
    user : relationships.User
        User to expire context for
    intent_key : string
        Intent key for context
    message_key : string
        Message key for context

    Returns
    -------
    User-context model reference
    """
    context, _ = models.UserContext.objects.get_or_create(
        user=user,
        intent_key=intent_key,
        message_key=message_key
    )
    tz = pytz.timezone(settings.TIME_ZONE)
    context.expired = datetime.now(tz=tz)
    context.save()
    return context