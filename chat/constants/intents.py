"""Intent keys"""

NO_INTENT = 'NO_INTENT' # User has no intent
REGISTER = 'REGISTER'
LOGIN = 'LOGIN'
CONTACT_REQUEST = 'CONTACT_REQUEST'

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    (NO_INTENT, NO_INTENT),
    (REGISTER, REGISTER),
    (LOGIN, LOGIN),
    (CONTACT_REQUEST, CONTACT_REQUEST)
]