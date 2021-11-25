from relationships import models as relmods
from chat.utilities import get_context, expire_context, start_context

def expire_to_context(
        user : relmods.User,
        intent_key : str,
        message_key : str
    ):
    """Expire user's current context and switch to the specified context.

    Parameters
    ----------
    user
        User for whom we're changing the context for.
    intent_key
        Intent key for next context.
    message_key
        Message key for next context.
    """
    # Get current context
    now_intent_key, now_message_key = get_context(user)

    # Expire current context
    expire_context(user, now_intent_key, now_message_key)

    # Start next context
    start_context(user, intent_key, message_key)