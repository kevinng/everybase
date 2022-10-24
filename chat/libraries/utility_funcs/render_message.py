from django.template.loader import render_to_string

def render_message(message_key, params):
    """Get message body for a message key

    Parameters
    ----------
    message_key : string
        Message key as defined in messages.py for message body to get
    params : dictionary
        Parameters to be inserted in message body
    """
    return render_to_string('chat/messages/%s.txt' % message_key, params)