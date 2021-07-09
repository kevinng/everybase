import pytz
from datetime import datetime

from everybase import settings
from chat import models

def done_context(user, intent_key, message_key):
    """Set user context's 'done' timestamp to now

    Parameters
    ----------
    user : relationships.User
        User to done context for
    intent_key : String
        Intent key for context
    message_key : String
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
    context.done = datetime.now(tz=tz)
    context.save()
    return context