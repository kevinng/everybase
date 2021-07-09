import importlib, typing
from chat.libraries.classes.message_parameterizer import MessageParameterizer

if typing.TYPE_CHECKING:
    from chat.libraries.classes.message_handler import MessageHandler

def get_parameterizer(
        message_handler: 'MessageHandler',
        intent_key: str,
        message_key: str
    ) -> MessageParameterizer:
    """Instantiate and return the parameterizer for a context (i.e., a unique
    intent/message pair). Returns None if no parameterizer found.

    Parameters
    ----------
    message_handler
        Message handler the parameterizer is used in
    intent_key
        Intent key for the context
    message_key
        Message key for the context
    """
    path = 'chat.parameterizers.%s.%s' % (intent_key, message_key)
    try:
        module = importlib.import_module(path)
    except ModuleNotFoundError:
        return None

    return module.Parameterizer(message_handler)