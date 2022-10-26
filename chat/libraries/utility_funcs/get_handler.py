import importlib
from chat.models import TwilioInboundMessage
from chat.libraries.classes.message_handler import MessageHandler

def get_handler(
        message: TwilioInboundMessage,
        intent_key: str,
        message_key: str,
        no_external_calls: bool = False,
        no_task_calls: bool = False
    ) -> MessageHandler:
    """Instantiate and return the message handler for a context (i.e., a unique
    intent/message pair). Returns None if no message handler found.

    Parameters
    ----------
    message
        Incoming message to be handled
    intent_key
        Intent key for the context
    message_key
        Message key for the context
    no_external_calls
        If True, will not make external calls. Enabled for testing purposes.
    """
    path = 'chat.handlers.%s.%s' % (intent_key, message_key)
    try:
        module = importlib.import_module(path)
    except ModuleNotFoundError:
        return None

    return module.Handler(message, intent_key, message_key, no_external_calls,
        no_task_calls)