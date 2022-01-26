"""Message keys"""

NO_MESSAGE = 'NO_MESSAGE' # No message has been sent to the user
DO_NOT_UNDERSTAND_OPTION = 'DO_NOT_UNDERSTAND_OPTION'
DO_NOT_UNDERSTAND_NUMBER = 'DO_NOT_UNDERSTAND_NUMBER'
DO_NOT_UNDERSTAND_EMAIL = 'DO_NOT_UNDERSTAND_EMAIL'
CONTACT_REQUEST__CONFIRM = 'CONTACT_REQUEST__CONFIRM'
CONTACT_REQUEST__CONTEXT_EXPIRED = 'CONTACT_REQUEST__CONTEXT_EXPIRED'
CONTACT_REQUEST__EXCHANGED_AUTHOR = 'CONTACT_REQUEST__EXCHANGED_AUTHOR'
CONTACT_REQUEST__EXCHANGED_CONTACTOR = 'CONTACT_REQUEST__EXCHANGED_CONTACTOR'
CONTACT_REQUEST__REASON_THANK_YOU = 'CONTACT_REQUEST__REASON_THANK_YOU'
CONTACT_REQUEST__REASON = 'CONTACT_REQUEST__REASON'
GENERIC = 'GENERIC'
LOGIN__CONFIRM = 'LOGIN__CONFIRM'
LOGIN__CONFIRMED = 'LOGIN__CONFIRMED'
LOGIN__AGAIN = 'LOGIN__AGAIN'
LOGIN__DO_NOT_UNDERSTAND = 'LOGIN__DO_NOT_UNDERSTAND'
REGISTER__LINK = 'REGISTER__LINK'
REGISTER__AGAIN = 'REGISTER__AGAIN'
REGISTER__CONFIRMED = 'REGISTER__CONFIRMED'
REGISTER__DO_NOT_UNDERSTAND = 'REGISTER__DO_NOT_UNDERSTAND'

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    (NO_MESSAGE, NO_MESSAGE),
    (DO_NOT_UNDERSTAND_OPTION, DO_NOT_UNDERSTAND_OPTION),
    (DO_NOT_UNDERSTAND_NUMBER, DO_NOT_UNDERSTAND_NUMBER),
    (DO_NOT_UNDERSTAND_EMAIL, DO_NOT_UNDERSTAND_EMAIL),
    (CONTACT_REQUEST__CONFIRM, CONTACT_REQUEST__CONFIRM),
    (CONTACT_REQUEST__CONTEXT_EXPIRED, CONTACT_REQUEST__CONTEXT_EXPIRED),
    (CONTACT_REQUEST__EXCHANGED_AUTHOR, CONTACT_REQUEST__EXCHANGED_AUTHOR),
    (CONTACT_REQUEST__EXCHANGED_CONTACTOR, CONTACT_REQUEST__EXCHANGED_CONTACTOR),
    (CONTACT_REQUEST__REASON_THANK_YOU, CONTACT_REQUEST__REASON_THANK_YOU),
    (CONTACT_REQUEST__REASON, CONTACT_REQUEST__REASON),
    (GENERIC, GENERIC),
    (LOGIN__CONFIRM, LOGIN__CONFIRM),
    (LOGIN__CONFIRMED, LOGIN__CONFIRMED),
    (LOGIN__AGAIN, LOGIN__AGAIN),
    (LOGIN__DO_NOT_UNDERSTAND, LOGIN__DO_NOT_UNDERSTAND),
    (REGISTER__LINK, REGISTER__LINK),
    (REGISTER__AGAIN, REGISTER__AGAIN),
    (REGISTER__CONFIRMED, REGISTER__CONFIRMED),
    (REGISTER__DO_NOT_UNDERSTAND, REGISTER__DO_NOT_UNDERSTAND),
]