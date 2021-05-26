from datetime import datetime
from pytz import timezone
import pytz
from everybase import settings
from chat import models
from chat.libraries import intents, messages

def get_context(user):
    """Get user context - i.e., intent and message key

    Parameters
    ----------
    user : relationships.User
        User whom we're getting the context for
    """
    intent_key = intents.NO_INTENT
    message_key = messages.NO_MESSAGE

    active = models.UserContext.objects.filter(
        # Do not deal with stopped contexts
        done__isnull=True,
        paused__isnull=True,
        expired__isnull=True
    ).exclude(
        # Do not store nor deal with context 'no intent'/'no message'
        intent_key=intents.NO_INTENT,
        message_key=messages.NO_MESSAGE
    ).filter(user=user).first() # User has at most 1 active context at a time

    if active:
        intent_key = active.intent_key
        message_key = active.message_key

    return (intent_key, message_key)

def start_context(user, intent_key, message_key):
    """Start context for user.
    
    Other active contexts have to be paused/doned/expired first.

    Parameters
    ----------
    user : relationships.User
        User to start context for
    intent_key : string
        Intent key as defined in intents.py
    message_key : string
        Message key as defined in messages.py
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

def done_context(user, intent_key, message_key):
    """Set user context's 'done' timestamp to now

    Parameters
    ----------
    user : relationships.User
        User to done context for
    intent_key : string
        Intent key as defined in intents.py
    message_key : string
        Message key as defined in messages.py
    """
    context, _ = models.UserContext.objects.get_or_create(
        user=user,
        intent_key=intent_key,
        message_key=message_key
    )
    tz = pytz.timezone(settings.TIME_ZONE)
    context.done = datetime.now(tz=tz)
    context.save()

def pause_context(user, intent_key, message_key):
    """Set user context's 'done' timestamp to now

    Parameters
    ----------
    user : relationships.User
        User to done context for
    intent_key : string
        Intent key as defined in intents.py
    message_key : string
        Message key as defined in messages.py
    """
    context, _ = models.UserContext.objects.get_or_create(
        user=user,
        intent_key=intent_key,
        message_key=message_key
    )
    tz = pytz.timezone(settings.TIME_ZONE)
    context.paused = datetime.now(tz=tz)
    context.save()

def expire_context(user, intent_key, message_key):
    """Set user context's 'done' timestamp to now

    Parameters
    ----------
    user : relationships.User
        User to done context for
    intent_key : string
        Intent key as defined in intents.py
    message_key : string
        Message key as defined in messages.py
    """
    context, _ = models.UserContext.objects.get_or_create(
        user=user,
        intent_key=intent_key,
        message_key=message_key
    )
    tz = pytz.timezone(settings.TIME_ZONE)
    context.expired = datetime.now(tz=tz)
    context.save()