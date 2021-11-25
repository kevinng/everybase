import pytz
from datetime import datetime

from everybase import settings
from chat import models

def start_context(user, intent_key, message_key):
    """Start context for user. Note: does not done/pause/expire other contexts.

    Parameters
    ----------
    user : relationships.User
        User to start context for
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

    # Start this context
    context.started = datetime.now(tz=tz)
    context.done = None
    context.paused = None
    context.expired = None

    context.save()
    return context