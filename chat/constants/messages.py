"""Message keys"""

NO_MESSAGE = 'NO_MESSAGE' # No message has been sent to the user
DO_NOT_UNDERSTAND_OPTION = 'DO_NOT_UNDERSTAND_OPTION'
DO_NOT_UNDERSTAND_NUMBER = 'DO_NOT_UNDERSTAND_NUMBER'
DO_NOT_UNDERSTAND_EMAIL = 'DO_NOT_UNDERSTAND_EMAIL'
LOGIN__AGAIN = 'LOGIN__AGAIN'
LOGIN__CONFIRM = 'LOGIN__CONFIRM'
LOGIN__CONFIRMED = 'LOGIN__CONFIRMED'
LOGIN__DO_NOT_UNDERSTAND = 'LOGIN__DO_NOT_UNDERSTAND'
REGISTER__AGAIN = 'REGISTER__AGAIN'
REGISTER__CONFIRM = 'REGISTER__CONFIRM'
REGISTER__CONFIRMED = 'REGISTER__CONFIRMED'
REGISTER__DO_NOT_UNDERSTAND = 'REGISTER__DO_NOT_UNDERSTAND'
LEAD__CREATED = 'LEAD__CREATED'

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    (NO_MESSAGE, NO_MESSAGE),
    (DO_NOT_UNDERSTAND_OPTION, DO_NOT_UNDERSTAND_OPTION),
    (DO_NOT_UNDERSTAND_NUMBER, DO_NOT_UNDERSTAND_NUMBER),
    (DO_NOT_UNDERSTAND_EMAIL, DO_NOT_UNDERSTAND_EMAIL),
    (LOGIN__AGAIN, LOGIN__AGAIN),
    (LOGIN__CONFIRM, LOGIN__CONFIRM),
    (LOGIN__CONFIRMED, LOGIN__CONFIRMED),
    (LOGIN__DO_NOT_UNDERSTAND, LOGIN__DO_NOT_UNDERSTAND),
    (REGISTER__AGAIN, REGISTER__AGAIN),
    (REGISTER__CONFIRM, REGISTER__CONFIRM),
    (REGISTER__CONFIRMED, REGISTER__CONFIRMED),
    (REGISTER__DO_NOT_UNDERSTAND, REGISTER__DO_NOT_UNDERSTAND),
    (LEAD__CREATED, LEAD__CREATED)
]