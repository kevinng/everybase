import pytz
from datetime import datetime

from everybase import settings
from chat import models
from relationships import models as relmods

def expire_context(
        user : relmods.User,
        intent_key : str,
        message_key : str
    ):
    """Set user context's 'expired' timestamp to now.

    Parameters
    ----------
    user
        User to expire context for.
    intent_key
        Intent key for context to expire.
    message_key
        Message key for context to expire.

    Returns
    -------
    context
        User's context model reference.
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