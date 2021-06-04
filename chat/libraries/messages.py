"""Message keys"""

from django.template.loader import render_to_string

NO_MESSAGE = 'NO_MESSAGE'

MENU = 'MENU'

# Minor menu options
CONFIRM_HUMAN = 'CONFIRM_HUMAN'
EXPLAIN_SERVICE = 'EXPLAIN_SERVICE'
DO_NOT_UNDERSTAND = 'DO_NOT_UNDERSTAND'
REGISTER__GET_NAME = 'REGISTER__GET_NAME'

# Find buyers / get supply
SUPPLY__GET_PRODUCT = 'SUPPLY__GET_PRODUCT'
SUPPLY__GET_AVAILABILITY = 'SUPPLY__GET_AVAILABILITY'
SUPPLY__GET_COUNTRY_STATE_READY_OTG = 'SUPPLY__GET_COUNTRY_STATE_READY_OTG'
SUPPLY__GET_COUNTRY_STATE_PRE_ORDER = 'SUPPLY__GET_COUNTRY_STATE_PRE_ORDER'
SUPPLY__CONFIRM_PACKING = 'SUPPLY__CONFIRM_PACKING'
SUPPLY__GET_PACKING = 'SUPPLY__GET_PACKING'
SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING = 'SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING'
SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING = 'SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING'
SUPPLY__GET_QUANTITY_PRE_ORDER = 'SUPPLY__GET_QUANTITY_PRE_ORDER'
SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING = 'SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING'
SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING = 'SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING'
SUPPLY__GET_PRICE_PRE_ORDER = 'SUPPLY__GET_PRICE_PRE_ORDER'
SUPPLY__GET_DEPOSIT = 'SUPPLY__GET_DEPOSIT'
SUPPLY__GET_ACCEPT_LC = 'SUPPLY__GET_ACCEPT_LC'
SUPPLY__THANK_YOU = 'SUPPLY__THANK_YOU'

# Find sellers / get demand
DEMAND__GET_PRODUCT = 'DEMAND__GET_PRODUCT'
DEMAND__GET_COUNTRY_STATE = 'DEMAND__GET_COUNTRY_STATE'
DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE = 'DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE'
DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE = 'DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE'
DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE = 'DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE'
DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE = 'DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE'
DEMAND__THANK_YOU = 'DEMAND__THANK_YOU'

# Still interested?
STILL_INTERESTED__CONFIRM = 'STILL_INTERESTED__CONFIRM'
STILL_INTERESTED__THANK_YOU = 'STILL_INTERESTED__THANK_YOU'

# Discuss
DISCUSS__CONFIRM_INTEREST = 'DISCUSS__CONFIRM_INTEREST'
DISCUSS__CONFIRM_DETAILS = 'DISCUSS__CONFIRM_DETAILS'
DISCUSS__ALREADY_CONNECTED = 'DISCUSS__ALREADY_CONNECTED'
DISCUSS__ASK = 'DISCUSS__ASK'
DISCUSS__THANK_YOU = 'DISCUSS__THANK_YOU'

# Q&A
YOUR_QUESTION = 'YOUR_QUESTION'
YOUR_ANSWER = 'YOUR_ANSWER'
ASK_QUESTION = 'ASK_QUESTION'
THANK_FOR_QUESTION = 'THANK_FOR_QUESTION'
REPLY = 'REPLY'
THANK_FOR_REPLY = 'THANK_FOR_REPLY'
STOP_DISCUSSION_REASON = 'STOP_DISCUSSION_REASON'
STOP_DISCUSSION_THANK_YOU = 'STOP_DISCUSSION_THANK_YOU'

# Pay and connect
PLEASE_PAY = 'PLEASE_PAY'
CONNECTED = 'CONNECTED'

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    (NO_MESSAGE, NO_MESSAGE),
    (MENU, MENU),
    (CONFIRM_HUMAN, CONFIRM_HUMAN),
    (EXPLAIN_SERVICE, EXPLAIN_SERVICE),
    (DO_NOT_UNDERSTAND, DO_NOT_UNDERSTAND),
    (REGISTER__GET_NAME, REGISTER__GET_NAME),
    (SUPPLY__GET_PRODUCT, SUPPLY__GET_PRODUCT),
    (SUPPLY__GET_AVAILABILITY, SUPPLY__GET_AVAILABILITY),
    (SUPPLY__GET_COUNTRY_STATE_READY_OTG, SUPPLY__GET_COUNTRY_STATE_READY_OTG),
    (SUPPLY__GET_COUNTRY_STATE_PRE_ORDER, SUPPLY__GET_COUNTRY_STATE_PRE_ORDER),
    (SUPPLY__CONFIRM_PACKING, SUPPLY__CONFIRM_PACKING),
    (SUPPLY__GET_PACKING, SUPPLY__GET_PACKING),
    (SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING, SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING),
    (SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING, SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING),
    (SUPPLY__GET_QUANTITY_PRE_ORDER, SUPPLY__GET_QUANTITY_PRE_ORDER),
    (SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING, SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING),
    (SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING, SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING),
    (SUPPLY__GET_PRICE_PRE_ORDER, SUPPLY__GET_PRICE_PRE_ORDER),
    (SUPPLY__GET_ACCEPT_LC, SUPPLY__GET_ACCEPT_LC),
    (SUPPLY__THANK_YOU, SUPPLY__THANK_YOU),
    (DEMAND__GET_PRODUCT, DEMAND__GET_PRODUCT),
    (DEMAND__GET_COUNTRY_STATE, DEMAND__GET_COUNTRY_STATE),
    (DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE, DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE),
    (DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE, DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE),
    (DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE, DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE),
    (DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE, DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE),
    (DEMAND__THANK_YOU, DEMAND__THANK_YOU),
    (STILL_INTERESTED__CONFIRM, STILL_INTERESTED__CONFIRM),
    (STILL_INTERESTED__THANK_YOU, STILL_INTERESTED__THANK_YOU),
    (DISCUSS__CONFIRM_INTEREST, DISCUSS__CONFIRM_INTEREST),
    (DISCUSS__CONFIRM_DETAILS, DISCUSS__CONFIRM_DETAILS),
    (DISCUSS__ALREADY_CONNECTED, DISCUSS__ALREADY_CONNECTED),
    (DISCUSS__ASK, DISCUSS__ASK),
    (DISCUSS__THANK_YOU, DISCUSS__THANK_YOU),
    (YOUR_QUESTION, YOUR_QUESTION),
    (YOUR_ANSWER, YOUR_ANSWER),
    (ASK_QUESTION, ASK_QUESTION),
    (THANK_FOR_QUESTION, THANK_FOR_QUESTION),
    (REPLY, REPLY),
    (THANK_FOR_REPLY, THANK_FOR_REPLY),
    (STOP_DISCUSSION_REASON, STOP_DISCUSSION_REASON),
    (STOP_DISCUSSION_THANK_YOU, STOP_DISCUSSION_THANK_YOU),
    (PLEASE_PAY, PLEASE_PAY),
    (CONNECTED, CONNECTED),
]

def get_body(message_key, params):
    """Get message body for a message key

    Parameters
    ----------
    message_key : string
        Message key as defined in messages.py for message body to get
    params : dictionary
        Parameters to be inserted in message body
    """
    return render_to_string('chat/%s.txt' % message_key, params)