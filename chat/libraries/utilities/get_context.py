from chat import models
from chat.libraries import intents, messages

def get_context(user):
    """Get user context - i.e., intent and message key

    Parameters
    ----------
    user : relationships.User
        User whom we're getting the context for

    Returns
    -------
    (intent_key, message_key) : Tuple
        intent_key
            Context intent key
        message_key
            Context intent key
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