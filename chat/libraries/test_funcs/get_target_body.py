from django.template.loader import render_to_string
from chat.libraries.utility_funcs.get_twilml_body import get_twilml_body

def get_target_body(
        intent_key: str,
        message_key: str,
        target_body_intent_key: str = None,
        target_body_message_key: str = None,
        target_body_params_func: str = None,
        target_body_variation_key: str = None
    ):
    """Receive inbound message, reply, assert - after-reply context and
    target response text.

    Target response text is how the message should look like. We store
    these texts at chat.templates.test.

    If a template has no variations, it is stored in a file with its
    message key and the .txt extension. E.g., MENU.txt.

    If a template has variations, it is stored in a folder with its message
    key, with each variation of the template stored in the folder with
    its variation key and the .txt extension. E.g., YOUR_QUESTION/OTG.txt.

    Parameters
    ----------
    body
        Message body
    intent_key
        Intent key for after-reply context. User's context after-reply will
        be asserted against this key. Further, the after-reply message
        target response text will be determined with this key.
    message_key
        Message key for after-reply context. User's context after-reply will
        be asserted against this key. Further, the after-reply message
        target response text will be determined with this key.
    target_body_intent_key
        If specified, this intent key will be used intead of intent_key to
        render the after-reply target response text.
    target_body_message_key
        If specified, this message key will be used instead of message_key
        to render the after-reply target response text.
    target_body_params_func
        If specified, we will run this function to compute the parameters
        for the after-reply target response text.
    target_body_variation_key
        If specified, we will use this key to pick-up specific variation
        of the after-reply target response text.
    """
    if target_body_intent_key is None:
        render_intent_key = intent_key
    else:
        render_intent_key = target_body_intent_key
    
    if target_body_message_key is None:
        render_message_key = message_key
    else:
        render_message_key = target_body_message_key

    target_path = 'chat/messages/test/%s/%s' % \
        (render_intent_key, render_message_key)
    if target_body_variation_key is None:
        target_path += '.txt'
    else:
        target_path += '/%s.txt' % target_body_variation_key

    if target_body_params_func is None:
        target_params = {}
    else:
        target_params = target_body_params_func()
    
    return render_to_string(target_path, target_params)