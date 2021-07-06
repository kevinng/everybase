from celery import shared_task

from chat.libraries.utilities.render_message import render_message

# ===== Start: New Supply/Demand =====

@shared_task
def capture_supply(last_message):
    """Capture supply entered by the user

    Parameters
    ----------
    last_message
        Last TwilioInboundMessage from the user in the supply-capture sequence

    Returns
    -------
    True if successful. False otherwise.
    """
    pass

@shared_task
def capture_demand(last_message):
    """Capture demand entered by the user

    Parameters
    ----------
    last_message
        Last TwilioInboundMessage from the user in the demand-capture sequence

    Returns
    -------
    True if successful. False otherwise.
    """
    pass

# ===== End: New Supply/Demand =====

# ===== Start: Confirm-Interest =====

@shared_task
def send_confirm_interest(match, no_external_calls=False):
    """Send confirm-interest to both seller and buyer of a match

    Parameters
    ----------
    match
        Match we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.

    Returns
    -------
    True if successful. False otherwise.
    """
    pass

@shared_task
def re_capture_supply(match):
    """Re-capture supply for a match - following a user's indication that the
    previous one was not correct.

    Parameters
    ----------
    match
        Match we're working on

    Returns
    -------
    True if successful. False otherwise.
    """
    pass

@shared_task
def re_capture_demand(match):
    """Re-capture demand for a match - following a user's indication that the
    previous one was not correct.

    Parameters
    ----------
    match
        Match we're working on

    Returns
    -------
    True if successful. False otherwise.
    """
    pass

# ===== End: Confirm-Interest =====

# ===== Start: Q&A =====

@shared_task
def auto_clean_question(qna_pair, no_external_calls=False):
    """Auto-clean question

    Parameters
    ----------
    qna_pair
        Q&A pair which we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.

    Returns
    -------
    True if successful. False otherwise.
    """
    pass

@shared_task
def forward_question(qna_pair, no_external_calls=False):
    """Forward question to answerer

    Parameters
    ----------
    qna_pair
        Q&A pair which we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.

    Returns
    -------
    True if successful. False otherwise.
    """
    pass

@shared_task
def auto_clean_answer(qna_pair, no_external_calls=False):
    """Auto-clean answer

    Parameters
    ----------
    qna_pair
        Q&A pair which we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.

    Returns
    -------
    True if successful. False otherwise.
    """
    pass

@shared_task
def forward_answer(qna_pair, no_external_calls=False):
    """Forward answer to asker

    Parameters
    ----------
    qna_pair
        Q&A pair which we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.

    Returns
    -------
    True if successful. False otherwise.
    """
    pass

# ===== End: Q&A =====

# ===== Start: Connected =====

def send_connections(match, no_external_calls=False):
    """Send buyer and seller contacts to each other

    Parameters
    ----------
    match
        Match we're working on
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.

    Returns
    -------
    True if successful. False otherwise.
    """
    pass