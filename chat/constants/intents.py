"""Intent keys"""

NO_INTENT = 'NO_INTENT' # User has no intent
CONFIRM_LOGIN = 'CONFIRM_LOGIN'
LOOK_UP = 'LOOK_UP'
MENU = 'MENU'
REGISTER = 'REGISTER'
SUPPORT = 'SUPPORT'
VERIFY_WHATSAPP = 'VERIFY_WHATSAPP'

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    (NO_INTENT, NO_INTENT),
    (CONFIRM_LOGIN, CONFIRM_LOGIN),
    (LOOK_UP, LOOK_UP),
    (MENU, MENU),
    (REGISTER, REGISTER),
    (SUPPORT, SUPPORT),
    (VERIFY_WHATSAPP, VERIFY_WHATSAPP)
]