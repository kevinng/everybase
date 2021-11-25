from django.template.loader import render_to_string

def render_message(
        message_key : str,
        params : dict = None
    ):
    """Get message body for a message key.

    Parameters
    ----------
    message_key
        Message key as defined in messages.py for message body to get.
    params
        Parameters to be merged in message body.

    Returns
    -------
    message
        Rendered message.
    """
    return render_to_string('chat/messages/%s.txt' % message_key, params)