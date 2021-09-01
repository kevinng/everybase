"""Data Keys"""

NO_DATA = 'NO_DATA'
STRAY_INPUT = 'STRAY_INPUT'
INVALID_CHOICE = 'INVALID_CHOICE'

##### Active 1 Sep 2021 #####

MENU = 'MENU'
MENU__FIND_BUYERS = 'MENU__FIND_BUYERS'
MENU__FIND_SELLERS = 'MENU__FIND_SELLERS'
MENU__TALK_TO_AN_EVERYBASE_AGENT = 'MENU__TALK_TO_AN_EVERYBASE_AGENT'
MENU__REGISTER_ME = 'MENU__REGISTER_ME'

LOCATION = 'LOCATION'

##### Deprecated 1 Sep 2021 #####

# AVAILABILITY = 'AVAILABILITY'
# AVAILABILITY__READY_OTG = 'AVAILABILITY__READY_OTG'
# AVAILABILITY__PRE_ORDER = 'AVAILABILITY__PRE_ORDER'

# QUESTION = 'QUESTION'
# ANSWER = 'ANSWER'

# CONFIRM_DETAILS = 'CONFIRM_DETAILS'
# CONFIRM_DETAILS__YES = 'CONFIRM_DETAILS__YES'
# CONFIRM_DETAILS__NO = 'CONFIRM_DETAILS__NO'

# CONFIRM_INTEREST = 'CONFIRM_INTEREST'
# CONFIRM_INTEREST__YES = 'CONFIRM_INTEREST__YES'
# CONFIRM_INTEREST__NO = 'CONFIRM_INTEREST__NO'

# STILL_INTERESTED = 'STILL_INTERESTED'
# STILL_INTERESTED__YES = 'STILL_INTERESTED__YES'
# STILL_INTERESTED__NO = 'STILL_INTERESTED__NO'

# CONFIRM_PACKING = 'CONFIRM_PACKING'
# CONFIRM_PACKING__YES = 'CONFIRM_PACKING__YES'
# CONFIRM_PACKING__NO = 'CONFIRM_PACKING__NO'

# ACCEPT_LC = 'ACCEPT_LC'
# ACCEPT_LC__YES = 'ACCEPT_LC__YES'
# ACCEPT_LC__NO = 'ACCEPT_LC__NO'

# PRODUCT = 'PRODUCT'
# COUNTRY_STATE = 'COUNTRY_STATE'
# DEPOSIT = 'DEPOSIT'
# PACKING = 'PACKING'
# PRICE = 'PRICE'
# QUANTITY = 'QUANTITY'
# STOP_DISCUSSION__REASON = 'STOP_DISCUSSION__REASON'

# MENU__LEARN_MORE = 'MENU__LEARN_MORE'

# QNA = 'QNA'
# QNA__ASK_QUESTION = 'QNA__ASK_QUESTION'
# QNA__ANSWER_QUESTION = 'QNA__ANSWER_QUESTION'
# QNA__BUY_CONTACT = 'QNA__BUY_CONTACT'
# QNA__STOP_DISCUSSION = 'QNA__STOP_DISCUSSION'
# QNA__LEARN_MORE = 'QNA__LEARN_MORE'

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    # Active
    (NO_DATA, NO_DATA),
    (STRAY_INPUT, STRAY_INPUT),
    (INVALID_CHOICE, INVALID_CHOICE),
    (MENU__FIND_BUYERS, MENU__FIND_BUYERS),
    (MENU__FIND_SELLERS, MENU__FIND_SELLERS),
    (MENU__TALK_TO_AN_EVERYBASE_AGENT, MENU__TALK_TO_AN_EVERYBASE_AGENT),
    (MENU__REGISTER_ME, MENU__REGISTER_ME),
    (LOCATION, LOCATION)

    # Deprecated
    # (AVAILABILITY, AVAILABILITY),
    # (AVAILABILITY__READY_OTG, AVAILABILITY__READY_OTG),
    # (AVAILABILITY__PRE_ORDER, AVAILABILITY__PRE_ORDER),
    # (QUESTION, QUESTION),
    # (ANSWER, ANSWER),
    # (CONFIRM_DETAILS, CONFIRM_DETAILS),
    # (CONFIRM_DETAILS__YES, CONFIRM_DETAILS__YES),
    # (CONFIRM_DETAILS__NO, CONFIRM_DETAILS__NO),
    # (CONFIRM_INTEREST, CONFIRM_INTEREST),
    # (CONFIRM_INTEREST__YES, CONFIRM_INTEREST__YES),
    # (CONFIRM_INTEREST__NO, CONFIRM_INTEREST__NO),
    # (STILL_INTERESTED, STILL_INTERESTED),
    # (STILL_INTERESTED__YES, STILL_INTERESTED__YES),
    # (STILL_INTERESTED__NO, STILL_INTERESTED__NO),
    # (CONFIRM_PACKING, CONFIRM_PACKING),
    # (CONFIRM_PACKING__YES, CONFIRM_PACKING__YES),
    # (CONFIRM_PACKING__NO, CONFIRM_PACKING__NO),
    # (ACCEPT_LC, ACCEPT_LC),
    # (ACCEPT_LC__YES, ACCEPT_LC__YES),
    # (ACCEPT_LC__NO, ACCEPT_LC__NO),
    # (PRODUCT, PRODUCT),
    # (COUNTRY_STATE, COUNTRY_STATE),
    # (DEPOSIT, DEPOSIT),
    # (PACKING, PACKING),
    # (PRICE, PRICE),
    # (QUANTITY, QUANTITY),
    # (STOP_DISCUSSION__REASON, STOP_DISCUSSION__REASON),
    # (MENU__LEARN_MORE, MENU__LEARN_MORE),
    # (QNA, QNA),
    # (QNA__ASK_QUESTION, QNA__ASK_QUESTION),
    # (QNA__ANSWER_QUESTION, QNA__ANSWER_QUESTION),
    # (QNA__BUY_CONTACT, QNA__BUY_CONTACT),
    # (QNA__STOP_DISCUSSION, QNA__STOP_DISCUSSION),
    # (QNA__LEARN_MORE, QNA__LEARN_MORE),
]