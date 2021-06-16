import importlib

def get_handler(message, intent_key, message_key):
    """Instantiate the right handler for a context (i.e., a unique
    intent/message pair) and return it

    Parameters
    ----------
    message : TwilioInboundMessage
        Incoming message to be handled
    intent_key : String
        Intent key for the user's context
    message_key : String
        Message key for the user's context
    """
    path = 'chat.handlers.%s.%s' % (intent_key, message_key)
    module = importlib.import_module(path)
    handler = module.Handler(message, intent_key, message_key)
    return handler