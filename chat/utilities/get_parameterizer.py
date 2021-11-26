import importlib, typing
from chat.parameterizers.library import MessageParameterizer

if typing.TYPE_CHECKING:
    from chat.handlers.library import MessageHandler

def get_parameterizer(
        message_handler : 'MessageHandler',
        intent_key : str,
        message_key : str
    ) -> MessageParameterizer:
    """Instantiate and return the parameterizer for a context (i.e., a unique
    intent/message pair). Returns None if no parameterizer found.

    Parameters
    ----------
    message_handler
        Message handler the parameterizer is used in.
    intent_key
        Intent key for the context.
    message_key
        Message key for the context.

    Returns
    -------
    parameterizer
        Parameterizer found. None if no parameterizer found.
    """
    path = 'chat.parameterizers.%s.%s' % (intent_key, message_key)
    try:
        module = importlib.import_module(path)
    except ModuleNotFoundError:
        return None

    return module.Parameterizer(message_handler)