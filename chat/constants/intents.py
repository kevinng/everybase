"""Intent keys"""

from chat.constants.messages import NEW_MESSAGE


NO_INTENT = 'NO_INTENT' # User has no intent
REGISTER = 'REGISTER'
LOGIN = 'LOGIN'
LEAD = 'LEAD'
WELCOME = 'WELCOME'
CONFIRM_LOGIN = 'CONFIRM_LOGIN'
NEW_APPLICATION = 'NEW_APPLICATION'
NEW_MESSAGE = 'NEW_MESSAGE'

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    (NO_INTENT, NO_INTENT),
    (REGISTER, REGISTER),
    (LOGIN, LOGIN),
    (LEAD, LEAD),
    (WELCOME, WELCOME),
    (CONFIRM_LOGIN, CONFIRM_LOGIN),
    (NEW_APPLICATION, NEW_APPLICATION),
    (NEW_MESSAGE, NEW_MESSAGE)
]