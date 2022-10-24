from relationships import models as relmods
from chat.libraries.utility_funcs.get_context import get_context
from chat.libraries.utility_funcs.done_context import done_context
from chat.libraries.utility_funcs.start_context import start_context

def done_to_context(
        user: relmods.User,
        intent_key: str,
        message_key: str
    ):
    """Switch user's current context to the specified context

    Parameters
    ----------
    user
        User for whom we're changing the context for
    intent_key
        Intent key for next context
    message_key
        Message key for next context
    """
    # Get current context
    now_intent_key, now_message_key = get_context(user)

    # Done current context
    done_context(user, now_intent_key, now_message_key)

    # Start next context
    start_context(user, intent_key, message_key)