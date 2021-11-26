import typing
from django.template.loader import render_to_string

def get_target_message_body(
        intent_key : str,
        message_key : str,
        params_func : typing.Callable = None,
        variation_key : str = None
    ):
    """
    Render and return the target message body the chatbot should reply with in
    a test environment.
    
    Likely, the rendered message is used to assert against a manually written
    text in an automated test to ascertain that the chatbot is behaving
    correctly.

    A target message body is a Django template saved at the path
    chat/templates/chat/messages/test/{intent_key}/{message_key}.txt, where
    intent_key is the intent key for the context, and message_key is the message
    key for the target message body. Since the template outputs text, the file
    ends with a .txt extension to indicate so. E.g.,
    
    chat/templates/chat/messages/test/LOGIN/LOGIN__CONFIRM.txt

    A target message body may not always have parameters - so the template may
    not have any parameters to be merged in. E.g., messages presenting a menu
    to the user usually do not have any parameters to be merged in.

    However, if the target message body do have parameters - they may be
    specified as a dictionary returned by the params_func parameter of this
    function. If params_func is not None, it will be run and merged into target
    message body.

    A target message may have variations, such as when we test the reply of the
    chatbot with different inputs. It's common for the chatbot to have different
    responses to different inputs from the user.

    We identify a unique variation for a message with a variation key. A
    variation key is unique under a message key. I.e., a message-variation key
    pair is unique.

    If a message has variations, we save each variation of the message at
    chat/templates/chat/messages/test/{intent_key}/{message_key}/{variation_key}.txt.
    
    E.g., intent key is LEAD, message key is LEAD__DETAILS - which has two
    variations: BUYER and SELLER, for say, buyer and seller respectively.

    For the buyer's variation of the LEAD_DETAILS message:
    chat/templates/chat/messages/test/LEAD/LEAD_DETAILS/BUYER.txt

    For the seller's variation of the LEAD_DETAILS message:
    chat/templates/chat/messages/test/LEAD/LEAD_DETAILS/SELLER.txt

    Parameters
    ----------
    intent_key
        Intent of the user AFTER the chatbot has replied. This intent will be
        used to render the target message.
    message_key
        Message the chatbot repliED with. This message will be used to render
        the target message.
    target_body_params_func
        If specified, run this function to compute the message parameters for
        the target message.
    target_body_variation_key
        If specified, use this key to select variation of the target message.
    """
    target_path = f'chat/messages/test/{intent_key}/{message_key}'
    if variation_key is None:
        target_path += '.txt'
    else:
        target_path += f'/{variation_key}.txt'

    if params_func is None:
        params = {}
    else:
        params = params_func()
    
    return render_to_string(target_path, params)