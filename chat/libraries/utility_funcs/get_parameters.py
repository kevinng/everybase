import typing
from chat.libraries.utility_funcs.get_parameterizer import get_parameterizer

if typing.TYPE_CHECKING:
    from chat.libraries.classes.message_handler import MessageHandler

def get_parameters(
        message_handler: 'MessageHandler',
        intent_key: str,
        message_key: str,
        params_func: typing.Callable = None
    ) -> typing.Dict[str, str]:
    """Returns parameters for a context's message. If params_func is
    specified, run it to get parameters for the message. Otherwise, look
    up the parameterizer for the context and run it to get the parameters.
    If parameterizer is not found - return an empty dictionary.

    Parameters
    ----------
    intent_key
        Intent key for the message's context
    messge_key
        Message key for the message's context
    params_func
        Optional parameters function that returns parameters for the message
    """
    if params_func is not None:
        # Parameters function is specified, run it to get parameters for the
        # message.
        params = params_func()
    else:
        p = get_parameterizer(
            message_handler,
            intent_key,
            message_key
        )
        params = p.run() if p is not None else {}

    return params